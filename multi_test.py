"""Test multiple AISEARCH providers"""
import sys
import time

def test_provider(name, provider_class, query="What is artificial intelligence?"):
    print(f"\n--- Testing {name} ---")
    try:
        client = provider_class()
        print(f"SUCCESS: {name} imported successfully")
        
        response = client.search(query, stream=False)
        response_text = str(response)
        print(f"SUCCESS: Response received ({len(response_text)} chars)")
        print(f"Preview: {response_text[:150]}...")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    print("Testing Multiple AISEARCH Providers")
    print("=" * 50)
    
    # Test providers one by one
    providers_to_test = [
        ("IAsk", "webscout.Provider.AISEARCH.iask_search", "IAsk"),
        ("Genspark", "webscout.Provider.AISEARCH.genspark_search", "Genspark"),
        ("Monica", "webscout.Provider.AISEARCH.monica_search", "Monica"),
        ("PERPLEXED", "webscout.Provider.AISEARCH.PERPLEXED_search", "PERPLEXED"),
        ("WebPilot", "webscout.Provider.AISEARCH.webpilotai_search", "webpilotai"),
    ]
    
    results = []
    
    for name, module_path, class_name in providers_to_test:
        try:
            # Import the provider
            module = __import__(module_path, fromlist=[class_name])
            provider_class = getattr(module, class_name)
            
            # Test the provider
            success = test_provider(name, provider_class)
            results.append((name, success))
            
        except Exception as e:
            print(f"\n--- Testing {name} ---")
            print(f"IMPORT ERROR: {e}")
            results.append((name, False))
        
        time.sleep(1)  # Brief pause between tests
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    working = [name for name, success in results if success]
    failed = [name for name, success in results if not success]
    
    print(f"Working providers ({len(working)}): {', '.join(working)}")
    print(f"Failed providers ({len(failed)}): {', '.join(failed)}")

if __name__ == "__main__":
    main()