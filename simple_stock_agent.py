#!/usr/bin/env python3
"""
Simple Stock Recommendation Agent
A direct, working implementation that provides stock recommendations
"""

import os
import asyncio
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

def get_free_llm_model():
    """Get a free LLM model with fallback options"""
    
    # Try Anthropic Claude (free tier available)
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key:
        try:
            print("🆓 Using Anthropic Claude (free tier)")
            return init_chat_model(model="anthropic:claude-3-haiku-20240307", api_key=anthropic_key)
        except Exception as e:
            print(f"⚠️  Claude failed: {e}")
    
    # Try Ollama (completely free, runs locally)
    try:
        print("🆓 Using Ollama (local, completely free)")
        return init_chat_model(model="ollama:llama3.2")
    except Exception as e:
        print(f"⚠️  Ollama failed: {e}")
    
    # Last resort - try OpenAI if available
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            print("💰 Using OpenAI (paid)")
            return init_chat_model(model="openai:gpt-4o-mini", api_key=openai_key)
        except Exception as e:
            print(f"⚠️  OpenAI failed: {e}")
    
    raise Exception("No LLM provider available. Please set up Anthropic API key or install Ollama.")

async def get_stock_recommendations(query):
    """Get comprehensive stock recommendations"""
    
    try:
        model = get_free_llm_model()
        print("✅ LLM model initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize LLM: {e}")
        return None

    # Comprehensive stock analysis prompt
    prompt = f"""
You are an expert stock market analyst specializing in NYSE-listed stocks. 

The user has requested: "{query}"

Please provide a comprehensive stock recommendation analysis including:

**STOCK SELECTION (2-3 stocks):**
1. [TICKER] - [Company Name]
   - Current Price: $[price]
   - Market Cap: $[market cap]
   - Sector: [sector]
   - Why Promising: [brief explanation]

2. [TICKER] - [Company Name]
   - Current Price: $[price]
   - Market Cap: $[market cap]
   - Sector: [sector]
   - Why Promising: [brief explanation]

**MARKET ANALYSIS:**
For each selected stock, provide:
- Recent Performance: [7-day and 30-day trends]
- Volume Analysis: [trading volume insights]
- Technical Indicators: [RSI, moving averages, etc.]
- Key News/Events: [recent developments affecting the stock]

**TRADING RECOMMENDATIONS:**
For each stock:
- Action: [BUY/SELL/HOLD]
- Target Price: $[specific price]
- Stop Loss: $[stop loss price]
- Time Horizon: [Short-term/Medium-term]
- Risk Level: [Low/Medium/High]
- Reasoning: [detailed explanation]

**PORTFOLIO CONSIDERATIONS:**
- Diversification: [how these stocks complement each other]
- Risk Management: [overall portfolio risk assessment]
- Market Conditions: [current market environment impact]

Focus on well-known, liquid stocks with good trading volume. Provide actionable, specific recommendations with clear reasoning.
"""

    print(f"\n🚀 Analyzing stocks for: '{query}'")
    print("=" * 60)
    
    try:
        response = await model.ainvoke(prompt)
        print("\n📊 STOCK RECOMMENDATION ANALYSIS")
        print("=" * 60)
        print(response.content)
        print("\n✅ Analysis completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during analysis: {e}")
        return None

async def main():
    """Main function to run the stock recommendation agent"""
    print("🎯 Simple Stock Recommendation Agent")
    print("=" * 50)
    
    # Get user query
    query = "Give me good stock recommendation from NYSE"
    
    # Get recommendations
    await get_stock_recommendations(query)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
