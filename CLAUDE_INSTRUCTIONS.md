# 🤖 Claude Instructions - AI Email Campaign Writer

## 🎯 **Project Overview**

This is an AI-powered email campaign writer that uses multiple AI frameworks to create engaging, personalized email campaigns. The system integrates various AI technologies to provide different levels of sophistication based on user needs.

## 🏗️ **AI Framework Architecture**

### **1. Core AI Frameworks**

#### **LangChain** (Primary Orchestration)
```python
# Purpose: Core AI workflow orchestration and prompt management
# Version: 0.0.350
# Key Features:
- Prompt templates and chaining
- Memory systems for conversation context
- Output parsing and validation
- Tool integration
- Model abstraction layer

# Implementation Location: backend/app/services/ai_service.py
# Usage: Simple email generation, prompt management, conversation memory
```

#### **CrewAI** (Multi-Agent Collaboration)
```python
# Purpose: Multi-agent system for complex email campaign creation
# Version: 0.11.0
# Key Features:
- Role-based AI agents with specific expertise
- Sequential and parallel task execution
- Agent delegation and collaboration
- Quality assurance through agent review

# Agent Roles:
1. Email Campaign Strategist - Analyzes audience and creates strategy
2. Email Content Writer - Writes compelling email content
3. Subject Line Specialist - Creates high-performing subject lines
4. Brand Manager - Ensures brand voice consistency

# Implementation: Used for complex campaign generation
```

#### **LangGraph** (Advanced Workflow Management)
```python
# Purpose: Complex workflow orchestration with state management
# Version: 0.0.20
# Key Features:
- Stateful workflow execution
- Conditional logic and branching
- Multi-step process management
- Error handling and recovery

# Workflow Steps:
1. Strategy Analysis → 2. Content Creation → 3. Subject Line Generation → 4. Brand Review → 5. Analytics

# Implementation: Used for advanced campaign generation with complex logic
```

#### **AutoGen** (Human-in-the-Loop)
```python
# Purpose: Interactive AI agents with human collaboration
# Version: 0.2.0
# Key Features:
- Human-in-the-loop workflows
- Interactive content refinement
- Real-time feedback integration
- Collaborative editing

# Implementation: Used for interactive campaign refinement and human review
```

#### **LlamaIndex** (Knowledge Management)
```python
# Purpose: Knowledge base and document processing
# Version: 0.9.0
# Key Features:
- Brand guidelines indexing
- Historical campaign analysis
- Customer data retrieval
- Content recommendation engine

# Implementation: Used for brand knowledge base and historical data analysis
```

### **2. AI Models Integration**

#### **OpenAI GPT-4** (Primary Content Generation)
```python
# Model: gpt-4 (configurable via settings.AI_MODEL)
# Use Cases:
- General email content generation
- Subject line creation
- Campaign strategy development
- A/B testing variations

# Configuration:
- Temperature: 0.7 (configurable)
- Max Tokens: 2000 (configurable)
- API Key: settings.OPENAI_API_KEY
```

#### **Anthropic Claude** (Brand Voice & Consistency)
```python
# Model: claude-3-sonnet-20240229
# Use Cases:
- Brand voice consistency
- Tone analysis and adjustment
- Complex personalization
- Content optimization

# Configuration:
- Temperature: 0.7
- Max Tokens: 2000
- API Key: settings.ANTHROPIC_API_KEY
```

### **3. Specialized AI Tools**

#### **Sentence Transformers** (Content Analysis)
```python
# Purpose: Semantic similarity and content analysis
# Version: 2.2.2
# Use Cases:
- Content similarity detection
- Brand voice analysis
- Audience segmentation
- Content clustering
```

#### **Transformers & PyTorch** (Custom Models)
```python
# Purpose: Custom model development and fine-tuning
# Versions: transformers==4.35.2, torch==2.1.1
# Use Cases:
- Custom email classification models
- Sentiment analysis
- Engagement prediction
- Content optimization
```

## 🔄 **AI Workflow Patterns**

### **Pattern 1: Simple Generation (LangChain Only)**
```python
# Use Case: Basic email campaigns, quick generation
# Complexity: Low
# Framework: LangChain
# Flow: Single prompt → Single model → Structured output

async def _simple_generation(request, user):
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", user_prompt)
    ])
    chain = prompt | openai_client
    response = await chain.ainvoke(request_data)
    return parse_response(response)
```

### **Pattern 2: Advanced Generation (LangGraph)**
```python
# Use Case: Complex campaigns with multiple steps
# Complexity: Medium
# Framework: LangGraph
# Flow: Strategy → Content → Subject Lines → Analytics

def create_langgraph_workflow():
    workflow = StateGraph(dict)
    workflow.add_node("strategist", strategist_agent)
    workflow.add_node("writer", content_writer_agent)
    workflow.add_node("analytics", analytics_agent)
    workflow.add_edge("strategist", "writer")
    workflow.add_edge("writer", "analytics")
    return workflow.compile()
```

### **Pattern 3: Complex Generation (CrewAI)**
```python
# Use Case: Enterprise campaigns with multiple specialists
# Complexity: High
# Framework: CrewAI
# Flow: Multiple agents collaborating sequentially

def create_crewai_agents():
    strategist = Agent(role='Email Campaign Strategist', ...)
    writer = Agent(role='Email Content Writer', ...)
    subject_specialist = Agent(role='Subject Line Specialist', ...)
    brand_manager = Agent(role='Brand Manager', ...)
    
    crew = Crew(
        agents=[strategist, writer, subject_specialist, brand_manager],
        tasks=[strategy_task, content_task, subject_task, review_task],
        process=Process.sequential
    )
    return crew
```

## 🎨 **Prompt Engineering Guidelines**

### **System Prompt Structure**
```python
def _get_system_prompt(user: User) -> str:
    return f"""
    You are an expert email marketing AI assistant for {user.company_name}.
    
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
```

### **Content Generation Prompts**
```python
# Email Content Generation
EMAIL_CONTENT_PROMPT = """
Generate an email campaign with the following details:
- Audience: {audience_description}
- Objective: {objective}
- Brand Voice: {brand_voice}
- Call to Action: {call_to_action}

Please provide:
1. Subject line (under 60 characters)
2. Email body (HTML and text versions)
3. Preview text (under 150 characters)
4. Call-to-action button text
"""

# Subject Line Generation
SUBJECT_LINE_PROMPT = """
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
```

## 📊 **AI Analytics & Optimization**

### **Content Optimization Types**
```python
OPTIMIZATION_TYPES = {
    "engagement": "Optimize this email for maximum engagement and opens",
    "conversion": "Optimize this email for conversion and click-through rates",
    "clarity": "Make this email clearer and more concise",
    "tone": "Adjust the tone to be more professional and brand-appropriate"
}
```

### **Performance Prediction**
```python
# AI-driven performance prediction
async def predict_campaign_performance(content: str) -> dict:
    prompt = f"""
    Analyze this email content and predict performance:
    {content}
    
    Provide predictions for:
    - Open rate (percentage)
    - Click-through rate (percentage)
    - Conversion rate (percentage)
    - Engagement score (1-10)
    - Risk factors and suggestions
    """
    
    response = await ai_client.ainvoke([HumanMessage(content=prompt)])
    return parse_performance_prediction(response.content)
```

## 🔧 **Configuration & Settings**

### **AI Configuration (app/core/config.py)**
```python
# AI Model Settings
AI_MODEL: str = "gpt-4"
AI_MAX_TOKENS: int = 2000
AI_TEMPERATURE: float = 0.7

# API Keys
OPENAI_API_KEY: Optional[str] = None
ANTHROPIC_API_KEY: Optional[str] = None

# Feature Flags
ENABLE_AI_GENERATION: bool = True
ENABLE_A_B_TESTING: bool = True
ENABLE_ADVANCED_ANALYTICS: bool = True

# Usage Limits
MAX_AI_GENERATIONS_PER_DAY: int = 1000
```

### **Environment Variables**
```bash
# Required AI Environment Variables
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Optional AI Configuration
AI_MODEL=gpt-4
AI_MAX_TOKENS=2000
AI_TEMPERATURE=0.7
```

## 🚀 **Implementation Guidelines**

### **When to Use Each Framework**

#### **Use LangChain When:**
- Simple email generation
- Basic prompt management
- Single-step workflows
- Quick prototyping

#### **Use LangGraph When:**
- Multi-step workflows
- State management needed
- Conditional logic required
- Complex branching

#### **Use CrewAI When:**
- Multiple specialized agents needed
- Sequential collaboration required
- Quality assurance important
- Enterprise-level campaigns

#### **Use AutoGen When:**
- Human-in-the-loop needed
- Interactive refinement required
- Real-time feedback integration
- Collaborative editing

#### **Use LlamaIndex When:**
- Knowledge base queries
- Document processing
- Historical data analysis
- Content recommendations

### **Best Practices**

1. **Model Selection:**
   - Use GPT-4 for general content generation
   - Use Claude for brand voice and consistency
   - Use specialized models for specific tasks

2. **Prompt Engineering:**
   - Always include brand context
   - Use structured prompts with clear sections
   - Include user preferences and limits
   - Validate outputs with parsers

3. **Error Handling:**
   - Implement fallback mechanisms
   - Handle API rate limits gracefully
   - Provide meaningful error messages
   - Log AI interactions for debugging

4. **Performance Optimization:**
   - Cache frequently used prompts
   - Implement token usage tracking
   - Use async operations for better performance
   - Monitor AI generation costs

5. **Security & Privacy:**
   - Never log sensitive user data
   - Implement content filtering
   - Validate AI outputs before storage
   - Follow GDPR compliance guidelines

## 📝 **Development Workflow**

### **Adding New AI Features**

1. **Define the Requirement:**
   - What AI capability is needed?
   - Which framework is most appropriate?
   - What are the input/output requirements?

2. **Choose the Framework:**
   - Simple task → LangChain
   - Complex workflow → LangGraph
   - Multi-agent → CrewAI
   - Interactive → AutoGen
   - Knowledge base → LlamaIndex

3. **Implement the Feature:**
   - Create the service method
   - Add proper error handling
   - Include logging and monitoring
   - Add tests

4. **Integrate with API:**
   - Add endpoint to API router
   - Create Pydantic schemas
   - Add authentication/authorization
   - Document the API

### **Testing AI Features**

```python
# Example test for AI service
async def test_simple_generation():
    ai_service = AIService()
    request = AIGenerationRequest(
        audience_description="Tech professionals",
        objective="Product launch",
        brand_voice="Professional and innovative"
    )
    
    response = await ai_service.generate_campaign_content(request, user)
    
    assert response.subject_line is not None
    assert response.html_content is not None
    assert response.text_content is not None
    assert response.generated_at is not None
```

## 🔮 **Future Enhancements**

### **Planned AI Features**

1. **Advanced Personalization:**
   - Behavioral analysis
   - Purchase history integration
   - Real-time personalization
   - Dynamic content generation

2. **Predictive Analytics:**
   - Campaign performance prediction
   - Optimal send time prediction
   - Audience engagement scoring
   - Churn prediction

3. **Multi-Modal AI:**
   - Image generation for email graphics
   - Voice-to-text for content creation
   - Video thumbnail generation
   - Interactive email elements

4. **Advanced Automation:**
   - Automated A/B testing
   - Dynamic content optimization
   - Intelligent segmentation
   - Automated campaign scheduling

### **AI Model Improvements**

1. **Fine-tuned Models:**
   - Domain-specific email models
   - Industry-specific optimization
   - Brand voice fine-tuning
   - Performance prediction models

2. **Ensemble Methods:**
   - Multiple model voting
   - Confidence scoring
   - Fallback mechanisms
   - Quality assurance

3. **Real-time Learning:**
   - Campaign performance feedback
   - User preference learning
   - Continuous model improvement
   - Adaptive personalization

---

## 📚 **Additional Resources**

- **LangChain Documentation:** https://python.langchain.com/
- **CrewAI Documentation:** https://docs.crewai.com/
- **LangGraph Documentation:** https://langchain-ai.github.io/langgraph/
- **AutoGen Documentation:** https://microsoft.github.io/autogen/
- **LlamaIndex Documentation:** https://docs.llamaindex.ai/

---

**Note:** This document serves as the primary reference for AI implementation in the Email Campaign Writer. Always refer to this document when making changes to AI functionality or adding new AI features.
