#!/usr/bin/env python3
"""
Simple test script to verify the containerized application works
"""

import os
import sys

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import python-dotenv: {e}")
        return False
    
    try:
        import langchain
        print("✅ langchain imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import langchain: {e}")
        return False
    
    try:
        import langchain_core
        print("✅ langchain_core imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import langchain_core: {e}")
        return False
    
    try:
        import langgraph
        print("✅ langgraph imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import langgraph: {e}")
        return False
    
    return True

def test_application_files():
    """Test that application files exist and are readable"""
    files_to_check = [
        "main.py",
        "utils.py", 
        "prompts/agent_1.txt",
        "prompts/agent_2.txt",
        "prompts/agent_3.txt",
        "prompts/orchestrator.txt"
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    return True

def test_environment():
    """Test environment variables"""
    required_vars = ["PATRA_SERVER_URL"]
    optional_vars = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "OLLAMA_HOST"]
    
    print("\n🔧 Environment Variables:")
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var} = {value}")
        else:
            print(f"⚠️  {var} not set (using default)")
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"✅ {var} = {'*' * len(value)}")  # Hide API key
        else:
            print(f"ℹ️  {var} not set (optional)")

def main():
    """Run all tests"""
    print("🧪 Testing Model Recommendation Agent Container")
    print("=" * 50)
    
    # Test imports
    print("\n📦 Testing Python Imports:")
    if not test_imports():
        print("❌ Import tests failed")
        sys.exit(1)
    
    # Test application files
    print("\n📁 Testing Application Files:")
    if not test_application_files():
        print("❌ File tests failed")
        sys.exit(1)
    
    # Test environment
    test_environment()
    
    print("\n✅ All tests passed! Container is ready.")
    print("\n🚀 To run the application:")
    print("   python main.py")

if __name__ == "__main__":
    main()
