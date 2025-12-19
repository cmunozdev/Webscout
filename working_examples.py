"""
Working AISEARCH Providers Example
=================================

This script demonstrates how to use the working AISEARCH providers in webscout.
"""

def test_working_providers():
    """Test the working providers with proper error handling"""
    
    # Test IAsk (fully working)
    print("=== Testing IAsk ===")
    try:
        from webscout.Provider.AISEARCH import IAsk
        ai = IAsk()
        response = ai.search("Explain quantum computing in simple terms", stream=False)
        print(f"Response length: {len(str(response))} characters")
        print(f"Preview: {str(response)[:200]}...")
        print()
    except Exception as e:
        print(f"IAsk failed: {e}\n")
    
    # Test PERPLEXED (fully working)
    print("=== Testing PERPLEXED ===")
    try:
        from webscout.Provider.AISEARCH import PERPLEXED
        ai = PERPLEXED()
        response = ai.search("Explain quantum computing in simple terms", stream=False)
        print(f"Response length: {len(str(response))} characters")
        print(f"Preview: {str(response)[:200]}...")
        print()
    except Exception as e:
        print(f"PERPLEXED failed: {e}\n")
    
    # Test Monica with streaming (partial working)
    print("=== Testing Monica (Streaming) ===")
    try:
        from webscout.Provider.AISEARCH import Monica
        ai = Monica()
        response_stream = ai.search("Explain quantum computing in simple terms", stream=True)
        full_response = ""
        for chunk in response_stream:
            full_response += str(chunk)
        print(f"Response length: {len(full_response)} characters")
        print(f"Preview: {full_response[:200]}...")
        print()
    except Exception as e:
        print(f"Monica failed: {e}\n")
    
    # Test WebPilot with streaming (partial working)
    print("=== Testing WebPilot (Streaming) ===")
    try:
        from webscout.Provider.AISEARCH import webpilotai
        ai = webpilotai()
        response_stream = ai.search("Explain quantum computing in simple terms", stream=True)
        full_response = ""
        for chunk in response_stream:
            full_response += str(chunk)
        print(f"Response length: {len(full_response)} characters")
        print(f"Preview: {full_response[:200]}...")
        print()
    except Exception as e:
        print(f"WebPilot failed: {e}\n")

if __name__ == "__main__":
    test_working_providers()