# Stock Recommendation Agent

A sophisticated multi-agent system that provides comprehensive stock recommendations using LangGraph, Model Context Protocol (MCP), and specialized AI agents. This system orchestrates four distinct agents through a supervisor pattern to deliver actionable trading insights.

## 🏗️ System Architecture

### High-Level Overview

```
User Query → Supervisor Agent → Sequential Agent Workflow → Comprehensive Recommendation
                ↓
    ┌─────────────────────────────────────────────────────────┐
    │                    Supervisor Agent                     │
    │  (Coordinates workflow and manages agent handoffs)      │
    └─────────────────────────────────────────────────────────┘
                ↓
    ┌─────────────┬─────────────┬─────────────┬─────────────┐
    │ Stock Finder│ Market Data │ News Analyst│Price Recom. │
    │   Agent     │   Agent     │   Agent     │   Agent     │
    └─────────────┴─────────────┴─────────────┴─────────────┘
                ↓
    ┌─────────────────────────────────────────────────────────┐
    │                 Bright Data MCP Server                  │
    │           (Real-time market data & news)               │
    └─────────────────────────────────────────────────────────┘
```

## 🤖 Multi-Agent Workflow

### 1. Supervisor Agent
**Role**: Workflow Orchestrator and Traffic Controller

The supervisor agent acts as the central coordinator, managing the sequential execution of specialized agents. It ensures that:
- Each agent receives the appropriate context from previous agents
- The workflow follows the correct sequence
- All agents complete their tasks before final recommendations
- Results are properly formatted and presented

**Key Responsibilities**:
- Parse user queries and determine workflow requirements
- Manage agent handoffs with proper context passing
- Aggregate results from all agents
- Present final comprehensive recommendations

### 2. Stock Finder Agent
**Role**: Initial Stock Selection and Screening

**Input**: User query (e.g., "Find technology stocks for short-term trading")
**Output**: 2-3 promising NYSE-listed stocks with reasoning

**Process**:
1. Analyzes user requirements and market conditions
2. Screens for liquid, actively traded stocks
3. Applies criteria (volume, recent performance, news buzz)
4. Provides stock tickers with brief reasoning

**Example Output**:
```
1. AAPL - Apple Inc.
   Reasoning: Strong technical momentum, high volume, recent product announcements

2. MSFT - Microsoft Corporation
   Reasoning: Cloud growth, AI integration news, stable price action
```

### 3. Market Data Agent
**Role**: Real-time Market Data Collection and Analysis

**Input**: Stock tickers from Stock Finder Agent
**Output**: Comprehensive market data for each stock

**Data Collected**:
- Current and previous closing prices
- Trading volume and trends
- Technical indicators (RSI, moving averages)
- Price momentum (7-day, 30-day trends)
- Volatility metrics

**MCP Integration**: Uses Bright Data MCP server to fetch real-time market data

### 4. News Analyst Agent
**Role**: News Sentiment Analysis and Impact Assessment

**Input**: Stock tickers and market context
**Output**: Recent news summary with sentiment classification

**Analysis Process**:
1. Searches for recent news (3-5 days)
2. Classifies sentiment (Positive/Negative/Neutral)
3. Assesses potential price impact
4. Identifies key catalysts and events

### 5. Price Recommender Agent
**Role**: Final Trading Recommendations and Strategy

**Input**: Combined data from all previous agents
**Output**: Actionable trading recommendations

**Recommendation Components**:
- Buy/Sell/Hold decision
- Target price with specific dollar amount
- Risk assessment (Low/Medium/High)
- Time horizon for the trade
- Detailed reasoning based on all collected data

## 🔌 Model Context Protocol (MCP) Integration

### What is MCP?

Model Context Protocol (MCP) is a standardized way for AI applications to interact with external data sources and tools. It provides a unified interface for accessing real-time market data, news, and other financial information.

### Bright Data MCP Server

This system integrates with Bright Data's MCP server to access:

**Real-time Market Data**:
- Live stock prices and quotes
- Historical price data
- Volume and trading metrics
- Technical indicators

**Financial News and Information**:
- Recent news articles
- Earnings announcements
- Market sentiment data
- Company filings and updates

### MCP Configuration

```python
client = MultiServerMCPClient({
    "bright_data": {
        "command": "npx",
        "args": ["@brightdata/mcp"],
        "env": {
            "API_TOKEN": os.getenv("BRIGHT_DATA_API_TOKEN")
        },
        "transport": "stdio",
    },
})
```

**Key Components**:
- **MultiServerMCPClient**: Manages connections to multiple MCP servers
- **Bright Data MCP**: Provides financial data and news
- **stdio transport**: Standard input/output communication
- **Environment variables**: Secure API token management

### MCP Tools Available

The Bright Data MCP server provides various tools that agents can use:

1. **Stock Data Tools**:
   - Real-time price quotes
   - Historical price data
   - Volume and trading metrics
   - Technical indicators

2. **News and Information Tools**:
   - Recent news articles
   - Company announcements
   - Market sentiment analysis
   - Earnings data

3. **Market Analysis Tools**:
   - Sector performance
   - Market trends
   - Volatility metrics
   - Correlation analysis

## 🔄 Agent Communication Flow

### Sequential Workflow

```
1. User Query
   ↓
2. Supervisor → Stock Finder Agent
   ↓
3. Stock Finder → Supervisor (with selected stocks)
   ↓
4. Supervisor → Market Data Agent (with stock list)
   ↓
5. Market Data → Supervisor (with market data)
   ↓
6. Supervisor → News Analyst Agent (with stocks + market context)
   ↓
7. News Analyst → Supervisor (with news analysis)
   ↓
8. Supervisor → Price Recommender Agent (with all collected data)
   ↓
9. Price Recommender → Supervisor (with final recommendations)
   ↓
10. Supervisor → User (comprehensive recommendation)
```

### Context Passing

Each agent receives context from previous agents:

- **Stock Finder**: Receives user query
- **Market Data**: Receives selected stocks + user context
- **News Analyst**: Receives stocks + market data + user context
- **Price Recommender**: Receives stocks + market data + news analysis + user context

## 🧠 LLM Integration and Fallback Strategy

### Primary LLM: Ollama (Local)

**Advantages**:
- 100% free and runs locally
- No API rate limits
- Complete privacy
- No internet dependency after setup

**Setup**:
```bash
# Install Ollama
brew install ollama

# Start service
brew services start ollama

# Pull model
ollama pull llama3.2
```

### Fallback LLM: OpenAI

**When Used**:
- Ollama not available
- Local model performance issues
- Need for specific model capabilities

**Configuration**:
```python
def get_large_language_model():
    # Try Ollama first
    try:
        return init_chat_model(model="ollama:llama3.2")
    except Exception:
        # Fallback to OpenAI
        return init_chat_model(model="openai:gpt-4o-mini")
```

## 📁 Project Structure Deep Dive

```
stock-recommendation-agent/
├── main.py                    # Application entry point and agent orchestration
├── utils.py                   # LLM setup, prompt loading, and utility functions
├── prompts/                   # Agent behavior definitions
│   ├── supervisor_prompt.txt  # Workflow coordination instructions
│   ├── stock_finder_prompt.txt    # Stock selection criteria
│   ├── market_data_prompt.txt     # Market data collection format
│   ├── news_analyst_prompt.txt    # News analysis guidelines
│   └── price_recommender_prompt.txt # Recommendation format
├── requirements.txt           # Python dependencies
└── README.md                 # This documentation
```

### Key Files Explained

**main.py**:
- Initializes MCP client with Bright Data
- Creates four specialized agents with custom prompts
- Sets up LangGraph supervisor for workflow management
- Handles streaming responses and message formatting

**utils.py**:
- `get_large_language_model()`: LLM provider selection with fallbacks
- `load_prompt_from_file()`: Dynamic prompt loading from files
- `pretty_print_messages()`: Formatted output display

**prompts/**: Each file defines the behavior and output format for a specific agent

## 🚀 Running the System

### Basic Usage

```bash
# Start the system
python main.py

# Enter your query when prompted
# Example: "Find technology stocks for short-term trading"
```

### Programmatic Usage

```python
from main import run_agent
import asyncio

# Run a stock recommendation query
result = asyncio.run(run_agent("Find dividend-paying stocks on NYSE"))
```

### Example Workflow Output

```
Update from node supervisor:
Enter your query: Find technology stocks for short-term trading

Update from subgraph stock_finder_agent:
1. AAPL - Apple Inc.
   Reasoning: Strong technical momentum, high volume, recent product announcements

2. MSFT - Microsoft Corporation
   Reasoning: Cloud growth, AI integration news, stable price action

Update from subgraph market_data_agent:
Stock: AAPL
- Current Price: $175.43
- Previous Close: $174.79
- Volume: 52.3M
- 7-day Trend: up 2.1%
- 30-day Trend: up 8.7%
- Technical Indicators: RSI 65, above 50-day MA
- Notable Events: High volume spike yesterday

Update from subgraph news_analyst_agent:
Stock: AAPL
Recent News:
• New iPhone announcement - Positive - Likely price increase
• Supply chain improvements - Positive - Cost reduction benefits

Update from subgraph price_recommender_agent:
Stock: AAPL
- Recommendation: BUY
- Target Price: $182.00
- Reasoning: Strong technical momentum, positive news flow, above key moving averages
- Risk Level: Medium
- Time Horizon: Short-term (1-2 weeks)
```

## 🔧 Configuration and Customization

### Environment Variables

```bash
# Required for market data
BRIGHT_DATA_API_TOKEN=your_bright_data_token_here

# Optional: OpenAI fallback
OPENAI_API_KEY=your_openai_key_here
```

### Customizing Agent Behavior

Modify the prompt files in `prompts/` to change agent behavior:

- **stock_finder_prompt.txt**: Adjust stock selection criteria
- **market_data_prompt.txt**: Change data collection format
- **news_analyst_prompt.txt**: Modify news analysis approach
- **price_recommender_prompt.txt**: Update recommendation format

### Adding New Agents

1. Create a new prompt file in `prompts/`
2. Add agent creation in `main.py`
3. Update supervisor prompt to include new agent
4. Modify workflow sequence as needed

## 🛠️ Technical Dependencies

### Core Libraries

- **LangChain**: LLM integration and tool management
- **LangGraph**: Multi-agent workflow orchestration
- **LangGraph Supervisor**: Agent coordination and supervision
- **LangChain MCP Adapters**: MCP server integration

### External Services

- **Bright Data**: Real-time market data and news
- **Ollama**: Local LLM inference
- **OpenAI**: Cloud LLM fallback

## 🔍 Troubleshooting

### Common Issues

1. **MCP Connection Failed**:
   - Verify Bright Data API token
   - Check internet connection
   - Ensure MCP server is running

2. **LLM Not Available**:
   - Install Ollama: `brew install ollama`
   - Start Ollama service: `brew services start ollama`
   - Pull model: `ollama pull llama3.2`

3. **Agent Workflow Issues**:
   - Check prompt files for syntax errors
   - Verify agent names match supervisor prompt
   - Ensure proper context passing

### Debug Mode

Add debug logging to see detailed agent interactions:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Test with different LLM providers
4. Update documentation
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.
