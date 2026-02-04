from langchain_core.messages import convert_to_messages
from langchain.chat_models import init_chat_model
import os

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

def load_prompt_from_file(filename):
    """Load prompt from a text file"""
    try:
        with open(f"prompts/{filename}", 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"⚠️  Prompt file {filename} not found, using default prompt")
        return "You are an AI agent. Please help the user with their request."

def get_large_language_model():
    """
    Get a LLM model with fallback options
    Priority: Claude (Anthropic) > Ollama > Local models
    """    
    # Try Ollama (completely free, runs locally)
    try:
        print("Initializing Ollama 3.2 model")
        return init_chat_model(model="ollama:llama3.2")
    except Exception as e:
        print(f"⚠️  Ollama failed: {e}")
    
    # Last resort - try OpenAI if available
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            print("Initializing OpenAI GPT-4o-mini model")
            return init_chat_model(model="openai:gpt-4o-mini", api_key=openai_key)
        except Exception as e:
            print(f"⚠️  OpenAI failed: {e}")
    
    raise Exception("No LLM provider available. Please set up Anthropic API key or install Ollama.")

def load_prompt_from_file(filename):
    """Load prompt from a text file"""
    try:
        with open(f"prompts/{filename}", 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"⚠️  Prompt file {filename} not found, using default prompt")
        return "You are an AI agent. Please help the user with their request."