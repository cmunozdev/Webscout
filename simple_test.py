"""Simple test for one AISEARCH provider"""
import sys

# Fix encoding for Windows console
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, errors='replace')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, errors='replace')

def test_provider(provider_name, provider_class, test_query="What is artificial intelligence?"):
    """Test a single provider"""
    print(f"Testing {provider_name}...")
    try:
        # Initialize the provider
        client = provider_class()
        print(f"  Initialized {provider_name}")
        
        # Try a basic search
        print(f"  Sending query: {test_query}")
        response = client.search(
            prompt=test_query,
            stream=False,
            raw=False
        )
        print(f"  Got response type: {type(response)}")
        print(f"  Response: {str(response)[:200]}...")
        print(f"  SUCCESS!")
    except Exception as e:
        print(f"  ERROR: {e}")

if __name__ == "__main__":
    # Test just one provider
    try:
        from webscout.Provider.AISEARCH import IAsk
        test_provider("IAsk", IAsk)
    except Exception as e:
        print(f"Failed to import or test provider: {e}")