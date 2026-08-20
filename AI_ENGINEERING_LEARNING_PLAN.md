# AI Engineering Learning Plan & Portfolio

## Phase 1: Foundations (Week 1-2)

### Learn
- [ ] LLM basics (prompting, tokens, models)
- [ ] Tool calling / Function calling concepts
- [ ] API calls to an LLM provider (Anthropic recommended)
- [ ] Python async/await (for production code)

### Do
- [ ] Set up Anthropic API key
- [ ] Make your first API call (Hello World)
- [ ] Build a simple chain: input → LLM → output
- [ ] Experiment with different prompts

### Portfolio
- Create `01_hello_llm/` with basic API call examples

---

## Phase 2: Core Frameworks (Week 3-4)

### Learn
- [ ] LangChain fundamentals (chains, tools, agents)
- [ ] How agents decide which tool to call
- [ ] Message formatting
- [ ] Response parsing

### Do
- [ ] Refactor your current `agent_api.py` to use LangChain
- [ ] Build a simple agent with 2-3 tools
- [ ] Test with real user queries

### Portfolio
- Create `02_basic_agent/` with:
  - Simple calculator agent
  - Weather lookup agent
  - File reader agent

---

## Phase 3: Advanced Patterns (Week 5-6)

### Learn
- [ ] LangGraph (stateful workflows)
- [ ] RAG concepts (Retrieval Augmented Generation)
- [ ] Vector databases basics
- [ ] Evaluation & testing agents

### Do
- [ ] Build a multi-step workflow (LangGraph)
- [ ] Implement a simple RAG system (document Q&A)
- [ ] Write eval tests for your agent

### Portfolio
- Create `03_stateful_agent/` with LangGraph workflow
- Create `04_rag_chatbot/` with document QA

---

## Phase 4: Real Projects (Week 7+)

### Project Ideas (pick 2-3)

**Project 1: Research Assistant**
- Takes a query
- Searches the internet (or uses documents)
- Summarizes findings
- Provides sources
- Stack: LangChain + LangGraph + RAG

**Project 2: Code Analysis Agent**
- Takes a GitHub repo URL or code
- Analyzes code quality
- Suggests improvements
- Explains architecture
- Stack: LangChain + File tools + Claude

**Project 3: Personal Knowledge Base**
- Upload your notes/documents
- Chat with your knowledge base
- Get personalized recommendations
- Stack: LangChain + RAG + Vector DB

**Project 4: Task Automation Agent**
- Takes complex tasks
- Breaks them into subtasks
- Executes with different tools
- Tracks progress
- Stack: LangGraph + LangChain

---

## Skills Checklist

### By End of Phase 1
- [ ] Can call an LLM API
- [ ] Understand how prompts work
- [ ] Know what tool calling is

### By End of Phase 2
- [ ] Can build a working agent
- [ ] Understand LangChain architecture
- [ ] Can create custom tools

### By End of Phase 3
- [ ] Can build multi-step workflows
- [ ] Understand RAG concepts
- [ ] Can evaluate agent performance

### By End of Phase 4
- [ ] 2-3 working projects in portfolio
- [ ] Can architect solutions for problems
- [ ] Can optimize agent performance

---

## Tech Stack (Recommended)

```
Core
├── Python 3.10+
├── Anthropic SDK or LangChain
└── LangGraph

Optional (add as needed)
├── LlamaIndex (for RAG)
├── Pinecone/Supabase (vector DB)
├── FastAPI (for APIs)
└── LangSmith (for evaluation)
```

---

## Portfolio Structure

```
ai-engineering-portfolio/
├── 01_hello_llm/
│   ├── simple_api_call.py
│   ├── prompt_engineering.py
│   └── README.md
├── 02_basic_agent/
│   ├── calculator_agent.py
│   ├── weather_agent.py
│   └── README.md
├── 03_stateful_agent/
│   ├── workflow.py
│   └── README.md
├── 04_rag_chatbot/
│   ├── knowledge_base.py
│   ├── query_handler.py
│   └── README.md
└── README.md (overview)
```

---

## Real-World Example: Predictive Maintenance with LLM Agents

### Problem: Injection Molding Machine Maintenance

**Traditional ML approach:**
- Collect 5 years of sensor data
- Train model on historical failures
- Predict "failure in X days"
- Issues: Needs massive datasets, new machine = new model, hard to explain

**LLM Agent approach:**

```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_anthropic import ChatAnthropic

# Define tools the agent can use
def get_sensor_data(machine_id):
    return {
        "temperature": 285,
        "pressure": 1200,
        "cycle_time": 45.2,
        "cycles_count": 125000,
        "last_maintenance": "2024-06-15"
    }

def get_maintenance_history(machine_id):
    return [
        {"date": "2024-06-15", "action": "Seal replacement", "reason": "Pressure leak"},
        {"date": "2024-03-20", "action": "Oil change", "reason": "Scheduled"},
    ]

def get_machine_manual(machine_id):
    return "Seal replacement recommended every 150k cycles. Max temp: 300C"

# Create agent
tools = [
    Tool(name="get_sensor_data", func=get_sensor_data),
    Tool(name="get_maintenance_history", func=get_maintenance_history),
    Tool(name="get_machine_manual", func=get_machine_manual),
]

llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
agent = create_tool_calling_agent(llm, tools)
executor = AgentExecutor(agent=agent, tools=tools)

# Ask the agent
result = executor.invoke({
    "input": """
    Machine M-401:
    - Temperature: 285C
    - Pressure: 1200 PSI (rising)
    - 125k cycles completed
    - Last maintenance: 3 months ago
    
    Is this machine at risk? What should we do?
    """
})

# Output: "Replace seal in next 2-3 days. Pressure rising indicates seal wear. 
#          At 125k cycles you're near the 150k replacement threshold. 
#          Recommend maintenance before next production run."
```

**Why LLM Agents Win Here:**

| Aspect | Traditional ML | LLM Agent |
|---|---|---|
| Works on Day 1 | ❌ Needs training | ✅ Yes |
| New machine type | ❌ Retrain model | ✅ Same agent |
| Explains decisions | ❌ Black box | ✅ Clear reasoning |
| Adapts to context | ❌ Fixed rules | ✅ Dynamic |
| Requires data scientist | ✅ Yes | ❌ Just engineering |

**Key insight:** You're not *predicting* with statistics—you're *reasoning* with data and knowledge. The agent:
- Gathers current sensor data
- Checks historical patterns
- References machine specs
- Reasons through similar past cases
- Makes intelligent recommendations

This is the **LLM Agent advantage** over traditional ML.

---

## What NOT to Do

- ❌ Don't learn TensorFlow/PyTorch (not needed for engineering)
- ❌ Don't master every LLM provider (pick 1)
- ❌ Don't get stuck on theory (build early)
- ❌ Don't wait for "the perfect project" (ship early)

---

## Success Metrics

- [ ] Build 2-3 working projects
- [ ] Can explain how agents work
- [ ] Can debug LLM responses
- [ ] Can evaluate agent quality
- [ ] Portfolio on GitHub with clear READMEs
