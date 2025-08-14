# Stock Recommendation Agent

A multi-agent system that provides stock recommendations for NYSE-listed stocks using **free LLM providers** and AI agents for research, market data analysis, news analysis, and trading recommendations.

## Features

- **Stock Finder Agent**: Identifies promising NYSE stocks for short-term trading
- **Market Data Agent**: Gathers current market data, trends, and technical indicators
- **News Analyst Agent**: Analyzes recent news and sentiment for selected stocks
- **Price Recommender Agent**: Provides buy/sell recommendations with target prices
- **Free LLM Support**: Works with multiple free AI providers
- **Graceful Fallbacks**: Automatically switches between available providers

## Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd stock-recommendation-agent
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Choose your free LLM provider**:

   **Option A: Anthropic Claude (Free Tier)**
   ```bash
   # Get free API key from: https://console.anthropic.com/
   # Add to .env file:
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

   **Option B: Ollama (Local, 100% Free)**
   ```bash
   # Install Ollama
   brew install ollama  # macOS
   # or visit: https://ollama.ai/
   
   # Start Ollama service
   brew services start ollama
   
   # Pull a model
   ollama pull llama3.2
   ```

3. **Run the troubleshooting script**:
   ```bash
   python troubleshoot.py
   ```

4. **Run the agent**:
   ```bash
   python multi_agent_demo.py
   ```

## LLM Setup Guide

### Anthropic Claude (Free Tier)
1. Visit [Anthropic Console](https://console.anthropic.com/)
2. Sign up for a free account
3. Create an API key
4. Add to `.env`: `ANTHROPIC_API_KEY=sk-ant-your-key-here`

### Ollama
1. Install Ollama:
   ```bash
   # macOS
   brew install ollama
   
   # Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Windows: Use WSL2 or visit https://ollama.ai/
   ```

2. Start Ollama service:
   ```bash
   brew services start ollama  # macOS
   # or: ollama serve
   ```

3. Pull a model:
   ```bash
   ollama pull llama3.2
   ```

## Usage Examples

### Basic Stock Recommendation
```python
from multi_agent_demo import run_agent
import asyncio

# Get stock recommendations using free LLM
asyncio.run(run_agent("Give me good stock recommendation from NYSE"))
```

### Custom Query
```python
# Ask for specific type of stocks
asyncio.run(run_agent("Find technology stocks with high volume on NYSE"))
```

## Architecture

The system uses a supervisor pattern with four specialized agents:

1. **Stock Finder Agent**: Identifies promising stocks
2. **Market Data Agent**: Gathers technical and market data
3. **News Analyst Agent**: Analyzes news sentiment
4. **Price Recommender Agent**: Provides trading recommendations

The supervisor coordinates these agents sequentially using **free LLM providers**.