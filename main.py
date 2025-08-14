import os
import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from utils import pretty_print_messages, load_prompt_from_file, get_large_language_model
load_dotenv()


async def run_agent(query):

    client = MultiServerMCPClient(
        {
            "bright_data": {
                "command": "npx",
                "args": ["@brightdata/mcp"],
                "env": {
                    "API_TOKEN": os.getenv("BRIGHT_DATA_API_TOKEN")
                },
                "transport": "stdio",
            },
        }
    )
    tools = await client.get_tools()    
    model = get_large_language_model()

    # Create agents with loaded prompts
    stock_finder_agent = create_react_agent(model=model, 
                                            tools=tools, 
                                            prompt=load_prompt_from_file("stock_finder_prompt.txt"), 
                                            name = "stock_finder_agent")

    market_data_agent = create_react_agent(model=model, 
                                           tools=tools, 
                                           prompt=load_prompt_from_file("market_data_prompt.txt"), 
                                           name = "market_data_agent")

    news_analyst_agent = create_react_agent(model=model, 
                                            tools=tools, 
                                            prompt=load_prompt_from_file("news_analyst_prompt.txt"), 
                                            name = "news_analyst_agent")

    price_recommender_agent = create_react_agent(model=model, 
                                                 tools=tools, 
                                                 prompt=load_prompt_from_file("price_recommender_prompt.txt"), 
                                                 name = "price_recommender_agent")

    supervisor = create_supervisor(
        model=model,
        agents=[stock_finder_agent, market_data_agent, news_analyst_agent, price_recommender_agent],
        prompt=load_prompt_from_file("supervisor_prompt.txt")        ,
        add_handoff_back_messages=True,
        output_mode="full_history",
    ).compile()

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


if __name__ == "__main__":
    user_query = input("Enter your query: ")
    asyncio.run(run_agent(user_query))