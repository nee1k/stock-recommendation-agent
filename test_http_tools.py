#!/usr/bin/env python3
"""
Test script to verify HTTP-based tools work with the Patra server
"""

import httpx
import os

def test_patra_server_connection():
    """Test basic connection to Patra server"""
    patra_server_url = os.getenv('PATRA_SERVER_URL', 'http://patra-server:5002')
    
    print(f"Testing connection to Patra server at: {patra_server_url}")
    
    try:
        # Test basic connectivity
        response = httpx.get(f"{patra_server_url}/modelcards")
        print(f"✅ GET /modelcards: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test model IDs endpoint
        response = httpx.get(f"{patra_server_url}/modelcards/ids")
        print(f"✅ GET /modelcards/ids: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test tools endpoint
        response = httpx.get(f"{patra_server_url}/tools")
        print(f"✅ GET /tools: {response.status_code}")
        tools_data = response.json()
        print(f"   Found {len(tools_data.get('tools', []))} tools")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_http_tools():
    """Test the HTTP-based tools"""
    patra_server_url = os.getenv('PATRA_SERVER_URL', 'http://patra-server:5002')
    
    print("\n🧪 Testing HTTP-based tools...")
    
    # Test list_all_model_cards
    try:
        response = httpx.get(f"{patra_server_url}/modelcards")
        response.raise_for_status()
        print(f"✅ list_all_model_cards: {response.json()}")
    except Exception as e:
        print(f"❌ list_all_model_cards failed: {e}")
    
    # Test list_model_ids
    try:
        response = httpx.get(f"{patra_server_url}/modelcards/ids")
        response.raise_for_status()
        print(f"✅ list_model_ids: {response.json()}")
    except Exception as e:
        print(f"❌ list_model_ids failed: {e}")
    
    # Test search_model_cards
    try:
        response = httpx.get(f"{patra_server_url}/modelcards/search", params={"q": "test"})
        response.raise_for_status()
        print(f"✅ search_model_cards: {response.json()}")
    except Exception as e:
        print(f"❌ search_model_cards failed: {e}")

if __name__ == "__main__":
    print("🚀 Testing Patra Server HTTP Tools")
    print("=" * 50)
    
    if test_patra_server_connection():
        test_http_tools()
        print("\n✅ All tests completed!")
    else:
        print("\n❌ Basic connection failed, skipping tool tests")
