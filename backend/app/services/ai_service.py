"""
AI Service for Email Campaign Generation
Integrates LangChain, CrewAI, LangGraph, and AutoGen for comprehensive email creation
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

# Core AI Frameworks
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.memory import ConversationBufferMemory

# Advanced Frameworks
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import autogen
from crewai import Agent, Task, Crew, Process
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext

# Local imports
from app.core.config import settings
from app.models.user import User
from app.models.campaign import Campaign
from app.schemas.ai import (
    AIGenerationRequest,
    AIGenerationResponse,
    EmailContent,
    SubjectLineVariation,
    CampaignStrategy
)

class AIService:
    """Main AI service orchestrating all AI frameworks for email campaign generation"""
    
    def __init__(self):
        self.openai_client = ChatOpenAI(
            model=settings.AI_MODEL,
            temperature=settings.AI_TEMPERATURE,
            max_tokens=settings.AI_MAX_TOKENS,
            api_key=settings.OPENAI_API_KEY
        )
        
        self.claude_client = ChatAnthropic(
            model="claude-3-sonnet-20240229",
            temperature=0.7,
            max_tokens=2000,
            api_key=settings.ANTHROPIC_API_KEY
        )
        
        # Initialize memory for conversation context
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Initialize knowledge base
        self.knowledge_base = self._initialize_knowledge_base()
        
    def _initialize_knowledge_base(self) -> VectorStoreIndex:
        """Initialize LlamaIndex knowledge base for brand guidelines and historical data"""
        try:
            # Load brand guidelines and historical campaigns
            documents = SimpleDirectoryReader('data/brand_guidelines').load_data()
            service_context = ServiceContext.from_defaults(
                llm=self.openai_client
            )
            return VectorStoreIndex.from_documents(
                documents, 
                service_context=service_context
            )
        except Exception as e:
            print(f"Warning: Could not initialize knowledge base: {e}")
            return None

    async def generate_campaign_content(
        self, 
        request: AIGenerationRequest,
        user: User
    ) -> AIGenerationResponse:
        """
        Generate complete email campaign using multi-agent system
        """
        
        # Choose workflow based on complexity
        if request.complexity == "simple":
            return await self._simple_generation(request, user)
        elif request.complexity == "advanced":
            return await self._advanced_generation(request, user)
        else:
            return await self._crewai_generation(request, user)

    async def _simple_generation(
        self, 
        request: AIGenerationRequest,
        user: User
    ) -> AIGenerationResponse:
        """Simple generation using LangChain only"""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", self._get_system_prompt(user)),
            ("human", """
            Generate an email campaign with the following details:
            - Audience: {audience_description}
            - Objective: {objective}
            - Brand Voice: {brand_voice}
            - Call to Action: {call_to_action}
            
            Please provide:
            1. Subject line
            2. Email body (HTML and text versions)
            3. Preview text
            """)
        ])
        
        chain = prompt | self.openai_client
        
        response = await chain.ainvoke({
            "audience_description": request.audience_description,
            "objective": request.objective,
            "brand_voice": request.brand_voice,
            "call_to_action": request.call_to_action
        })
        
        return self._parse_simple_response(response.content)

    async def _advanced_generation(
        self, 
        request: AIGenerationRequest,
        user: User
    ) -> AIGenerationResponse:
        """Advanced generation using LangGraph workflow"""
        
        # Define state for the workflow
        class CampaignState:
            def __init__(self):
                self.strategy = None
                self.content = None
                self.subject_lines = None
                self.final_campaign = None
                self.analytics = None
        
        # Create workflow
        workflow = self._create_langgraph_workflow()
        
        # Initialize state
        initial_state = CampaignState()
        initial_state.strategy = {
            "audience": request.audience_description,
            "objective": request.objective,
            "brand_voice": request.brand_voice
        }
        
        # Execute workflow
        result = await workflow.ainvoke(initial_state)
        
        return self._parse_advanced_response(result)

    async def _crewai_generation(
        self, 
        request: AIGenerationRequest,
        user: User
    ) -> AIGenerationResponse:
        """Complex generation using CrewAI multi-agent system"""
        
        # Define agents
        strategist = Agent(
            role='Email Campaign Strategist',
            goal='Analyze audience and create effective campaign strategy',
            backstory="""You are an expert email marketing strategist with 10+ years 
            of experience in creating high-converting email campaigns.""",
            verbose=True,
            allow_delegation=False,
            llm=self.openai_client
        )
        
        writer = Agent(
            role='Email Content Writer',
            goal='Write compelling email content that drives engagement',
            backstory="""You are a skilled copywriter specializing in email marketing 
            with expertise in persuasive writing and conversion optimization.""",
            verbose=True,
            allow_delegation=False,
            llm=self.claude_client
        )
        
        subject_specialist = Agent(
            role='Subject Line Specialist',
            goal='Create high-performing subject lines that maximize open rates',
            backstory="""You are a subject line optimization expert who understands 
            what drives email opens and engagement.""",
            verbose=True,
            allow_delegation=False,
            llm=self.openai_client
        )
        
        brand_manager = Agent(
            role='Brand Manager',
            goal='Ensure content aligns with brand voice and guidelines',
            backstory="""You are a brand manager responsible for maintaining 
            consistent brand voice and messaging across all communications.""",
            verbose=True,
            allow_delegation=False,
            llm=self.claude_client
        )
        
        # Define tasks
        strategy_task = Task(
            description=f"""
            Analyze the audience: {request.audience_description}
            Campaign objective: {request.objective}
            Brand voice: {request.brand_voice}
            
            Create a comprehensive campaign strategy including:
            - Target audience analysis
            - Key messaging points
            - Tone and style recommendations
            - Call-to-action strategy
            """,
            agent=strategist
        )
        
        content_task = Task(
            description="""
            Based on the strategy, write compelling email content including:
            - Engaging opening
            - Clear value proposition
            - Persuasive body content
            - Strong call-to-action
            - Both HTML and text versions
            """,
            agent=writer
        )
        
        subject_task = Task(
            description="""
            Create 5 subject line variations that:
            - Are compelling and click-worthy
            - Align with the campaign strategy
            - Optimize for open rates
            - Include personalization elements
            """,
            agent=subject_specialist
        )
        
        review_task = Task(
            description="""
            Review the campaign content and ensure:
            - Brand voice consistency
            - Message alignment
            - Tone appropriateness
            - Overall quality and effectiveness
            """,
            agent=brand_manager
        )
        
        # Create crew
        crew = Crew(
            agents=[strategist, writer, subject_specialist, brand_manager],
            tasks=[strategy_task, content_task, subject_task, review_task],
            verbose=True,
            process=Process.sequential
        )
        
        # Execute
        result = await crew.kickoff()
        
        return self._parse_crewai_response(result)

    def _create_langgraph_workflow(self) -> StateGraph:
        """Create LangGraph workflow for advanced campaign generation"""
        
        def strategist_agent(state):
            """Campaign strategy agent"""
            prompt = f"""
            Analyze the campaign requirements and create a strategy:
            Audience: {state['strategy']['audience']}
            Objective: {state['strategy']['objective']}
            Brand Voice: {state['strategy']['brand_voice']}
            
            Provide a detailed strategy including:
            - Target audience insights
            - Key messaging framework
            - Content structure
            - Call-to-action approach
            """
            
            response = self.openai_client.invoke([HumanMessage(content=prompt)])
            state['strategy']['detailed_plan'] = response.content
            return state
        
        def content_writer_agent(state):
            """Content writing agent"""
            strategy = state['strategy']['detailed_plan']
            
            prompt = f"""
            Based on this strategy: {strategy}
            
            Write compelling email content including:
            - Subject line
            - Email body (HTML and text)
            - Preview text
            - Call-to-action
            """
            
            response = self.claude_client.invoke([HumanMessage(content=prompt)])
            state['content'] = response.content
            return state
        
        def analytics_agent(state):
            """Analytics and optimization agent"""
            content = state['content']
            
            prompt = f"""
            Analyze this email content for performance optimization:
            {content}
            
            Provide:
            - Engagement predictions
            - Optimization suggestions
            - A/B testing recommendations
            - Performance metrics to track
            """
            
            response = self.openai_client.invoke([HumanMessage(content=prompt)])
            state['analytics'] = response.content
            return state
        
        # Create workflow
        workflow = StateGraph(dict)
        
        # Add nodes
        workflow.add_node("strategist", strategist_agent)
        workflow.add_node("writer", content_writer_agent)
        workflow.add_node("analytics", analytics_agent)
        
        # Add edges
        workflow.add_edge("strategist", "writer")
        workflow.add_edge("writer", "analytics")
        workflow.add_edge("analytics", END)
        
        return workflow.compile()

    async def generate_subject_lines(
        self, 
        campaign_content: str,
        count: int = 5
    ) -> List[SubjectLineVariation]:
        """Generate multiple subject line variations using AI"""
        
        prompt = f"""
        Based on this email content, generate {count} compelling subject lines:
        
        Content: {campaign_content}
        
        Requirements:
        - Each subject line should be under 60 characters
        - Include personalization elements
        - Create urgency or curiosity
        - Optimize for open rates
        - Vary the approach (question, statement, benefit-focused)
        
        Return as JSON array with 'subject_line' and 'reasoning' fields.
        """
        
        response = await self.openai_client.ainvoke([HumanMessage(content=prompt)])
        
        try:
            variations = json.loads(response.content)
            return [SubjectLineVariation(**var) for var in variations]
        except:
            # Fallback parsing
            return self._parse_subject_lines_fallback(response.content)

    async def optimize_content(
        self, 
        content: str,
        optimization_type: str = "engagement"
    ) -> str:
        """Optimize email content for specific goals"""
        
        optimization_prompts = {
            "engagement": "Optimize this email for maximum engagement and opens",
            "conversion": "Optimize this email for conversion and click-through rates",
            "clarity": "Make this email clearer and more concise",
            "tone": "Adjust the tone to be more professional and brand-appropriate"
        }
        
        prompt = f"""
        {optimization_prompts.get(optimization_type, optimization_prompts['engagement'])}
        
        Original content: {content}
        
        Provide the optimized version with explanations of changes made.
        """
        
        response = await self.claude_client.ainvoke([HumanMessage(content=prompt)])
        return response.content

    def _get_system_prompt(self, user: User) -> str:
        """Generate system prompt based on user's brand and preferences"""
        return f"""
        You are an expert email marketing AI assistant for {user.company_name or 'a business'}.
        
        Brand Guidelines:
        - Company: {user.company_name}
        - Industry: {user.industry}
        - Brand Voice: Professional yet approachable
        
        User Preferences:
        - Subscription Plan: {user.subscription_plan}
        - Email Limit: {user.get_email_limit()}
        - AI Generation Limit: {user.get_ai_generation_limit()}
        
        Always create content that:
        1. Aligns with the brand voice
        2. Drives engagement and conversions
        3. Follows email marketing best practices
        4. Is personalized and relevant
        5. Includes clear calls-to-action
        """

    def _parse_simple_response(self, content: str) -> AIGenerationResponse:
        """Parse simple AI response into structured format"""
        # Implementation for parsing simple responses
        return AIGenerationResponse(
            subject_line="Generated Subject Line",
            html_content=content,
            text_content=content,
            preview_text="Generated preview text",
            generated_at=datetime.utcnow()
        )

    def _parse_advanced_response(self, result: Dict) -> AIGenerationResponse:
        """Parse advanced workflow result into structured format"""
        # Implementation for parsing advanced responses
        return AIGenerationResponse(
            subject_line="Advanced Generated Subject Line",
            html_content=result.get('content', ''),
            text_content=result.get('content', ''),
            preview_text="Advanced preview text",
            generated_at=datetime.utcnow()
        )

    def _parse_crewai_response(self, result: str) -> AIGenerationResponse:
        """Parse CrewAI result into structured format"""
        # Implementation for parsing CrewAI responses
        return AIGenerationResponse(
            subject_line="CrewAI Generated Subject Line",
            html_content=result,
            text_content=result,
            preview_text="CrewAI preview text",
            generated_at=datetime.utcnow()
        )

    def _parse_subject_lines_fallback(self, content: str) -> List[SubjectLineVariation]:
        """Fallback parsing for subject lines"""
        lines = content.split('\n')
        variations = []
        
        for line in lines[:5]:  # Take first 5 lines
            if line.strip():
                variations.append(SubjectLineVariation(
                    subject_line=line.strip(),
                    reasoning="AI-generated variation"
                ))
        
        return variations
