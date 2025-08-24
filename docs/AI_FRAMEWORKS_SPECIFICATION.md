# AI/ML Frameworks Specification - PulseQuill

## 🎯 **Purpose**
This document clarifies the specific roles and responsibilities of each AI/ML framework in PulseQuill to eliminate confusion and ensure proper implementation.

## 🏗️ **Framework Architecture Overview**

```
┌─────────────────────────────────────────────────────────────┐
│                    PulseQuill AI Stack                      │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   LangChain │  │   LangGraph │  │   CrewAI    │         │
│  │  (Core)     │  │  (Workflow) │  │ (Agents)    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│         │               │               │                  │
│         └───────────────┼───────────────┘                  │
│                         │                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  LlamaIndex │  │   AutoGen   │  │   pgvector  │         │
│  │   (RAG)     │  │ (Human-AI)  │  │ (Embedding) │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

## 📋 **Framework Specifications**

### **1. LangChain - Core Orchestration Engine**
**Purpose**: Primary framework for LLM interactions, prompt management, and basic AI operations

**Specific Use Cases**:
- **Model Selection**: Router logic for GPT-4 vs Claude selection
- **Prompt Templates**: Structured prompt skeletons for email generation
- **Output Parsing**: Parse AI responses into structured data
- **Memory Management**: Conversation context and user preferences
- **Basic Chains**: Simple email content generation workflows

**Implementation**:
```python
# Core LangChain usage
from langchain.chat_models import ChatOpenAI, ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser

# Model selection router
def choose_model(task: str, complexity: str) -> str:
    if task in ["subject", "cta", "short_variant"]:
        return "gpt-4"  # Punchy creativity
    elif complexity == "high" or task == "brand_alignment":
        return "claude"  # Nuanced style control
    else:
        return "gpt-4"  # Default choice
```

### **2. LangGraph - Complex Workflow Orchestration**
**Purpose**: Manage complex, multi-step AI workflows with state management

**Specific Use Cases**:
- **Quality Gates**: LLM draft → Style lint → Fact validator → Compliance → Human preview
- **A/B Testing Workflows**: Generate variants → Test → Analyze → Select winner
- **Campaign Lifecycle**: Draft → Review → Approve → Schedule → Send → Analyze
- **Error Recovery**: Handle failures and retry logic in AI workflows

**Implementation**:
```python
# LangGraph workflow for quality gates
from langgraph.graph import StateGraph, END

def create_quality_gate_workflow():
    workflow = StateGraph(StateType=CampaignState)
    
    workflow.add_node("llm_draft", generate_initial_draft)
    workflow.add_node("style_lint", check_brand_compliance)
    workflow.add_node("fact_validator", validate_facts_urls)
    workflow.add_node("compliance_check", add_gdpr_can_spam)
    workflow.add_node("human_preview", human_review_step)
    
    workflow.add_edge("llm_draft", "style_lint")
    workflow.add_edge("style_lint", "fact_validator")
    workflow.add_edge("fact_validator", "compliance_check")
    workflow.add_edge("compliance_check", "human_preview")
    workflow.add_edge("human_preview", END)
    
    return workflow.compile()
```

### **3. CrewAI - Multi-Agent Collaboration**
**Purpose**: Orchestrate specialized AI agents for complex email campaign creation

**Specific Use Cases**:
- **Campaign Strategy**: Strategist agent analyzes audience and goals
- **Content Creation**: Writer agent generates email content
- **Brand Specialist**: Ensures brand voice consistency
- **Compliance Officer**: Validates legal and regulatory requirements
- **Performance Analyst**: Optimizes for engagement metrics

**Implementation**:
```python
# CrewAI multi-agent system
from crewai import Agent, Task, Crew, Process

def create_campaign_crew():
    # Define specialized agents
    strategist = Agent(
        role="Email Campaign Strategist",
        goal="Analyze audience and create winning campaign strategy",
        backstory="Expert in email marketing with 10+ years experience"
    )
    
    writer = Agent(
        role="Email Copywriter",
        goal="Create compelling email content that drives action",
        backstory="Award-winning copywriter specializing in conversion"
    )
    
    brand_specialist = Agent(
        role="Brand Voice Specialist",
        goal="Ensure all content matches brand guidelines",
        backstory="Brand strategist with deep understanding of voice consistency"
    )
    
    # Define tasks
    strategy_task = Task(
        description="Analyze audience data and create campaign strategy",
        agent=strategist
    )
    
    writing_task = Task(
        description="Write email content based on strategy",
        agent=writer
    )
    
    brand_task = Task(
        description="Review and adjust content for brand consistency",
        agent=brand_specialist
    )
    
    # Create crew
    crew = Crew(
        agents=[strategist, writer, brand_specialist],
        tasks=[strategy_task, writing_task, brand_task],
        process=Process.sequential
    )
    
    return crew
```

### **4. LlamaIndex - RAG (Retrieval-Augmented Generation)**
**Purpose**: Provide context-aware AI responses using brand guidelines and historical data

**Specific Use Cases**:
- **Brand Guidelines**: Retrieve relevant brand voice examples
- **Historical Performance**: Access past successful campaigns
- **Industry Best Practices**: Reference email marketing best practices
- **Compliance Rules**: Retrieve relevant legal and compliance information
- **Personalization Data**: Access user preferences and behavior patterns

**Implementation**:
```python
# LlamaIndex RAG system
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext

def setup_rag_system():
    # Load brand guidelines
    brand_docs = SimpleDirectoryReader('data/brand_guidelines').load_data()
    
    # Load historical campaigns
    campaign_docs = SimpleDirectoryReader('data/historical_campaigns').load_data()
    
    # Load compliance rules
    compliance_docs = SimpleDirectoryReader('data/compliance').load_data()
    
    # Create vector index
    service_context = ServiceContext.from_defaults(llm=openai_client)
    index = VectorStoreIndex.from_documents(
        brand_docs + campaign_docs + compliance_docs,
        service_context=service_context
    )
    
    return index

def query_brand_context(query: str, index: VectorStoreIndex):
    """Query brand guidelines and historical data"""
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    return response
```

### **5. AutoGen - Human-in-the-Loop Interactions**
**Purpose**: Enable human oversight and intervention in AI workflows

**Specific Use Cases**:
- **Content Approval**: Human review of AI-generated content
- **Strategy Refinement**: Human input on campaign strategy
- **Brand Adjustments**: Human guidance on brand voice
- **Compliance Review**: Human verification of legal compliance
- **Performance Optimization**: Human insights for campaign improvement

**Implementation**:
```python
# AutoGen human-in-the-loop
import autogen

def setup_human_ai_workflow():
    # Configure AI assistant
    assistant = autogen.AssistantAgent(
        name="Email Assistant",
        llm_config={"config_list": [{"model": "gpt-4"}]}
    )
    
    # Configure human user
    user_proxy = autogen.UserProxyAgent(
        name="Human Reviewer",
        human_input_mode="ALWAYS",
        max_consecutive_auto_reply=0
    )
    
    return assistant, user_proxy

def human_review_workflow(content: str, assistant, user_proxy):
    """Workflow for human review of AI content"""
    user_proxy.initiate_chat(
        assistant,
        message=f"Please review this email content for brand consistency: {content}"
    )
```

### **6. pgvector - Vector Embeddings & Similarity Search**
**Purpose**: Store and search brand voice examples and content embeddings

**Specific Use Cases**:
- **Brand Voice Matching**: Find similar brand voice examples
- **Content Similarity**: Identify similar successful campaigns
- **Personalization**: Match content to user preferences
- **A/B Testing**: Compare variant performance
- **Performance Prediction**: Predict engagement based on similar content

**Implementation**:
```python
# pgvector for brand voice embeddings
from sqlalchemy.dialects.postgresql import VECTOR
import openai

def create_brand_embedding(content: str) -> List[float]:
    """Create embedding for brand voice content"""
    response = openai.Embedding.create(
        input=content,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

def find_similar_brand_examples(
    query_content: str,
    db_session,
    limit: int = 5
) -> List[CopyCorpus]:
    """Find similar brand voice examples using vector similarity"""
    query_embedding = create_brand_embedding(query_content)
    
    # Vector similarity search
    similar_examples = db_session.query(CopyCorpus).order_by(
        CopyCorpus.embedding.cosine_distance(query_embedding)
    ).limit(limit).all()
    
    return similar_examples
```

## 🔄 **Workflow Integration**

### **Simple Email Generation** (LangChain Only)
```python
async def simple_generation(request: AIGenerationRequest) -> AIGenerationResponse:
    """Simple email generation using only LangChain"""
    # 1. Model selection
    model = choose_model(request.task, request.complexity)
    
    # 2. Prompt template
    prompt = ChatPromptTemplate.from_template(
        "Generate {task} for {audience} with {tone} tone"
    )
    
    # 3. Generate content
    chain = prompt | model | PydanticOutputParser(pydantic_object=EmailContent)
    result = await chain.ainvoke({
        "task": request.task,
        "audience": request.audience,
        "tone": request.tone
    })
    
    return AIGenerationResponse(content=result)
```

### **Advanced Campaign Creation** (Multi-Framework)
```python
async def advanced_campaign_creation(request: AIGenerationRequest) -> AIGenerationResponse:
    """Advanced campaign creation using multiple frameworks"""
    
    # 1. RAG Context (LlamaIndex)
    brand_context = query_brand_context(request.brand_guidelines, knowledge_base)
    
    # 2. Multi-Agent Strategy (CrewAI)
    crew = create_campaign_crew()
    strategy_result = await crew.kickoff({
        "audience": request.audience,
        "goals": request.goals,
        "brand_context": brand_context
    })
    
    # 3. Quality Gate Workflow (LangGraph)
    workflow = create_quality_gate_workflow()
    final_content = await workflow.ainvoke({
        "initial_draft": strategy_result.content,
        "brand_guidelines": brand_context
    })
    
    # 4. Human Review (AutoGen)
    if request.requires_human_review:
        assistant, user_proxy = setup_human_ai_workflow()
        approved_content = await human_review_workflow(
            final_content, assistant, user_proxy
        )
        final_content = approved_content
    
    return AIGenerationResponse(content=final_content)
```

## 📊 **Framework Selection Matrix**

| Use Case | Primary Framework | Supporting Frameworks | Complexity |
|----------|------------------|---------------------|------------|
| Simple email generation | LangChain | - | Low |
| Brand voice matching | pgvector + LlamaIndex | LangChain | Medium |
| Multi-step quality gates | LangGraph | LangChain | Medium |
| Complex campaign strategy | CrewAI | LangChain, LlamaIndex | High |
| Human-in-the-loop review | AutoGen | LangChain | Medium |
| Historical performance analysis | pgvector | LlamaIndex | Low |

## 🎯 **Implementation Guidelines**

### **When to Use Each Framework**:

1. **Start with LangChain**: Always use LangChain for basic LLM interactions
2. **Add LangGraph for workflows**: Use when you need multi-step processes with state
3. **Use CrewAI for complex tasks**: When you need specialized agents working together
4. **Implement RAG with LlamaIndex**: When you need context from documents/data
5. **Add AutoGen for human oversight**: When human review is required
6. **Use pgvector for similarity**: When you need to find similar content/examples

### **Performance Considerations**:
- **LangChain**: Fastest for simple operations
- **LangGraph**: Moderate overhead for workflow management
- **CrewAI**: Higher overhead due to multi-agent coordination
- **LlamaIndex**: Overhead for document processing and retrieval
- **AutoGen**: Human interaction time is the bottleneck
- **pgvector**: Fast similarity search with proper indexing

This specification ensures clear understanding of each framework's role and eliminates confusion in implementation.
