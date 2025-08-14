import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain.chat_models import init_chat_model
from langgraph_supervisor import create_supervisor

load_dotenv()

from langchain_core.messages import convert_to_messages


def pretty_print_message(message, indent=False):
    pretty_message = message.pretty_repr(html=True)
    if not indent:
        print(pretty_message)
        return

    indented = "\n".join("\t" + c for c in pretty_message.split("\n"))
    print(indented)


def pretty_print_messages(update, last_message=False):
    is_subgraph = False
    if isinstance(update, tuple):
        ns, update = update
        # skip parent graph updates in the printouts
        if len(ns) == 0:
            return

        graph_id = ns[-1].split(":")[0]
        print(f"Update from subgraph {graph_id}:")
        print("\n")
        is_subgraph = True

    for node_name, node_update in update.items():
        update_label = f"Update from node {node_name}:"
        if is_subgraph:
            update_label = "\t" + update_label

        print(update_label)
        print("\n")

        messages = convert_to_messages(node_update["messages"])
        if last_message:
            messages = messages[-1:]

        for m in messages:
            pretty_print_message(m, indent=is_subgraph)
        print("\n")

def get_free_llm_model():
    """
    Get a free LLM model with fallback options
    Priority: Claude (Anthropic) > Ollama > Local models
    """
    
    # Try Anthropic Claude (free tier available)
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key:
        try:
            print("Using Anthropic Claude")
            return init_chat_model(model="anthropic:claude-3-haiku-20240307", api_key=anthropic_key)
        except Exception as e:
            print(f"⚠️  Claude failed: {e}")
    
    # Try Ollama (completely free, runs locally)
    try:
        print("Using Ollama")
        return init_chat_model(model="ollama:llama3.2")
    except Exception as e:
        print(f"⚠️  Ollama failed: {e}")
    
    # Last resort - try OpenAI if available
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            print("Using OpenAI")
            return init_chat_model(model="openai:gpt-4o-mini", api_key=openai_key)
        except Exception as e:
            print(f"⚠️  OpenAI failed: {e}")
    
    raise Exception("No LLM provider available. Please set up Anthropic API key or install Ollama.")

async def run_agent(query):
    # Initialize MCP client for Bright Data
    try:
        client = MultiServerMCPClient(
            {
                "bright_data": {
                    "command": "npx",
                    "args": ["@brightdata/mcp"],
                    "env": {
                        "API_TOKEN": os.getenv("BRIGHT_DATA_API_TOKEN"),
                        "WEB_UNLOCKER_ZONE": os.getenv("WEB_UNLOCKER_ZONE", "unblocker"),
                        "BROWSER_ZONE": os.getenv("BROWSER_ZONE", "scraping_browser")
                    },
                    "transport": "stdio",
                },
            }
        )
        tools = await client.get_tools()
        print("✅ Bright Data MCP client initialized")
    except Exception as e:
        print(f"⚠️  Bright Data failed: {e}")
        print("   Continuing without web scraping tools...")
        tools = []

    # Get free LLM model
    try:
        model = get_free_llm_model()
        print("✅ LLM model initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize LLM: {e}")
        print("\n💡 Setup options:")
        print("   1. Get free Anthropic API key: https://console.anthropic.com/")
        print("   2. Install Ollama: https://ollama.ai/")
        print("   3. Use OpenAI (paid): https://platform.openai.com/")
        return

    stock_finder_agent = create_react_agent(model, tools, prompt=""" You are a stock research analyst specializing in the US Stock Market (NYSE). Your task is to select 2 promising, actively traded NYSE-listed stocks for short term trading (buy/sell) based on recent performance, news buzz, volume or technical strength.
    Avoid penny stocks and illiquid companies.
    Output should include stock names, tickers, and brief reasoning for each choice.
    Respond in structured plain text format.""", name = "stock_finder_agent")

    market_data_agent = create_react_agent(model, tools, prompt="""You are a market data analyst for US stocks listed on NYSE. Given a list of stock tickers (eg RELIANCE, INFY), your task is to gather recent market information for each stock, including:
    - Current price
    - Previous closing price
    - Today's volume
    - 7-day and 30-day price trend
    - Basic Technical indicators (RSI, 50/200-day moving averages)
    - Any notable spikes in volume or volatility
    
    Return your findings in a structured and readable format for each stock, suitable for further analysis by a recommendation engine. Use USD as the currency. Be concise but complete.""", name = "market_data_agent")

    news_analyst_agent = create_react_agent(model, tools, prompt="""You are a financial news analyst. Given the names or the tickers of US NYSE listed stocks, your job is to-
    - Search for the most recent news articles (past 3-5 days)
    - Summarize key updates, announcements, and events for each stock
    - Classify each piece of news as positive, negative or neutral
    - Highlight how the news might affect short term stock price
                                            
    Present your response in a clear, structured format - one section per stock.

    Use bullet points where necessary. Keep it short, factual and analysis-oriented""", name = "news_analyst_agent")

    price_recommender_agent = create_react_agent(model, tools, prompt="""You are a trading strategy advisor for the US Stock Market. You are given -
    - Recent market data (current price, volume, trend, indicators)
    - News summaries and sentiment for each stock
        
    Based on this info, for each stock-
    1. Recommend an action : Buy, Sell or Hold
    2. Suggest a specific target price for entry or exit (USD)
    3. Briefly explain the reason behind your recommendation.
        
    Your goal is to provide practical, near-term trading advice for the next trading day.
        
    Keep the response concise and clearly structured.""", name = "price_recommender_agent")

    # Create supervisor with the same free model
    supervisor_model = get_free_llm_model()
    supervisor = create_supervisor(
        model=supervisor_model,
        agents=[stock_finder_agent, market_data_agent, news_analyst_agent, price_recommender_agent],
        prompt=(
            "You are a supervisor managing four agents:\n"
            "- a stock_finder_agent. Assign research-related tasks to this agent and pick 2 promising NYSE stocks\n"
            "- a market_data_agent. Assign tasks to fetch current market data (price, volume, trends)\n"
            "- a news_analyst_agent. Assign task to search and summarize recent news\n"
            "- a price_recommender_agent. Assign task to give buy/sell decision with target price."
            "Assign work to one agent at a time, do not call agents in parallel.\n"
            "Do not do any work yourself."
            "Make sure you complete till end and do not ask for proceed in between the task."
        ),
        add_handoff_back_messages=True,
        output_mode="full_history",
    ).compile()

    print(f"\n🚀 Starting stock recommendation process for: '{query}'")
    print("=" * 60)

    try:
        for chunk in supervisor.stream(
        {
                "messages": [
                    {
                        "role": "user",
                        "content": query,
                    }
                ]
            },
        ):
            pretty_print_messages(chunk, last_message=True)

        final_message_history = chunk["supervisor"]["messages"]
        print("\n✅ Stock recommendation process completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during agent execution: {e}")
        print("\n💡 Troubleshooting:")
        print("   1. Check your API keys in .env file")
        print("   2. Ensure Ollama is running if using local models")
        print("   3. Check internet connection for cloud models")

if __name__ == "__main__":
    try:
        asyncio.run(run_agent("Give me good stock recommendation from NYSE"))
    except KeyboardInterrupt:
        print("\n\n⏹️  Process interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")