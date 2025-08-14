#!/usr/bin/env python3
"""
Troubleshooting script for stock recommendation agent
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def check_free_llm_providers():
    """Check available free LLM providers"""
    print("🔍 Checking Free LLM Providers...")
    
    providers_available = []
    
    # Check Anthropic Claude (free tier)
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key:
        print("✅ Anthropic Claude API key found (free tier available)")
        print("   Get your key from: https://console.anthropic.com/")
        providers_available.append("anthropic")
    else:
        print("❌ ANTHROPIC_API_KEY not found")
        print("   Get free API key from: https://console.anthropic.com/")
    
    # Check Ollama (completely free, local)
    try:
        import subprocess
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama installed: {result.stdout.strip()}")
            providers_available.append("ollama")
        else:
            print("❌ Ollama not working properly")
    except FileNotFoundError:
        print("❌ Ollama not installed")
        print("   Install from: https://ollama.ai/")
    
    # Check OpenAI (paid, fallback)
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print("✅ OpenAI API key found (paid)")
        providers_available.append("openai")
    else:
        print("⚠️  OPENAI_API_KEY not found (optional, paid)")
    
    return providers_available

def check_bright_data_api():
    """Check Bright Data API configuration"""
    print("\n🔍 Checking Bright Data API...")
    
    api_token = os.getenv("BRIGHT_DATA_API_TOKEN")
    if not api_token:
        print("❌ BRIGHT_DATA_API_TOKEN not found")
        print("   Add it to your .env file: BRIGHT_DATA_API_TOKEN=your-token-here")
        print("   Get your token from: https://brightdata.com/cp/setting/users")
        return False
    
    print("✅ Bright Data API token found")
    print("💡 If you get permission errors:")
    print("   1. Visit: https://brightdata.com/cp/setting/users")
    print("   2. Ensure your token has 'Zone Management' permissions")
    print("   3. Or use existing zones instead of creating new ones")
    return True

def check_node_npm():
    """Check if Node.js and npm are available"""
    print("\n🔍 Checking Node.js and npm...")
    
    try:
        import subprocess
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js version: {result.stdout.strip()}")
        else:
            print("❌ Node.js not found or not working")
            return False
    except FileNotFoundError:
        print("❌ Node.js not installed")
        print("   Install from: https://nodejs.org/")
        return False
    
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm version: {result.stdout.strip()}")
        else:
            print("❌ npm not found or not working")
            return False
    except FileNotFoundError:
        print("❌ npm not installed")
        return False
    
    return True

def check_python_dependencies():
    """Check if required Python packages are installed"""
    print("\n🔍 Checking Python dependencies...")
    
    required_packages = [
        "langchain",
        "langgraph", 
        "langchain-mcp-adapters",
        "langchain-anthropic",
        "langchain-ollama",
        "langchain-community",
        "langgraph_supervisor",
        "python-dotenv"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "python-dotenv":
                __import__("dotenv")
            else:
                __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n💡 Install missing packages:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    return True

def create_env_template():
    """Create a template .env file"""
    print("\n📝 Creating .env template...")
    
    template = """# Free LLM Providers (choose one or more)

# Anthropic Claude (free tier available)
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# OpenAI (paid, fallback option)
OPENAI_API_KEY=sk-your-openai-api-key-here

# Bright Data API Configuration (optional but recommended)
BRIGHT_DATA_API_TOKEN=your-bright-data-token-here
WEB_UNLOCKER_ZONE=unblocker
BROWSER_ZONE=scraping_browser

# Instructions:
# 1. Get free Anthropic API key: https://console.anthropic.com/
# 2. Install Ollama for local models: https://ollama.ai/
# 3. Get Bright Data token: https://brightdata.com/cp/setting/users
# 4. OpenAI is optional (paid)
"""
    
    with open(".env.template", "w") as f:
        f.write(template)
    
    print("✅ Created .env.template file")
    print("   Copy it to .env and fill in your API keys")

def main():
    print("🔧 Stock Recommendation Agent Troubleshooter")
    print("=" * 50)
    
    # Check all components
    llm_providers = check_free_llm_providers()
    bright_data_ok = check_bright_data_api()
    node_ok = check_node_npm()
    deps_ok = check_python_dependencies()
    
    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"   Free LLM Providers: {'✅' if llm_providers else '❌'}")
    print(f"   Bright Data API: {'✅' if bright_data_ok else '❌'}")
    print(f"   Node.js/npm: {'✅' if node_ok else '❌'}")
    print(f"   Python dependencies: {'✅' if deps_ok else '❌'}")
    
    if not llm_providers:
        print("\n❌ No LLM providers available")
        print("   Set up at least one of:")
        print("   - Anthropic Claude (free): https://console.anthropic.com/")
        print("   - Ollama (local, free): https://ollama.ai/")
        return False
    
    if not all([node_ok, deps_ok]):
        print("\n❌ Some critical components are missing")
        print("   Fix the issues above before running the agent")
        return False
    
    if not bright_data_ok:
        print("\n⚠️  Bright Data API not configured")
        print("   The agent will work with limited functionality")
    
    print(f"\n✅ Ready to use with: {', '.join(llm_providers)}")
    print("   You can now run: python multi_agent_demo.py")
    
    # Create .env template if it doesn't exist
    if not os.path.exists(".env"):
        create_env_template()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
