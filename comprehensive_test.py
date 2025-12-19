"""Comprehensive test script for all AISEARCH providers in webscout"""
import sys
import time
from typing import Dict, List, Tuple

# Fix encoding for Windows console
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, errors='replace')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, errors='replace')

def test_provider(name: str, provider_class, test_query: str = "What is Python?"):
    """Test a single provider and return (success, error_message, response_preview)"""
    try:
        print(f"  Testing with query: {test_query}")
        
        # Initialize the provider
        client = provider_class()
        
        # Try a basic search
        response = client.search(
            prompt=test_query,
            stream=False,
            raw=False
        )
        
        # Handle generators that some providers incorrectly return for non-streaming
        if hasattr(response, '__iter__') and not isinstance(response, (str, bytes)):
            # This is a generator, collect all chunks
            full_response = ""
            try:
                for chunk in response:
                    if hasattr(chunk, 'text'):
                        full_response += chunk.text
                    else:
                        full_response += str(chunk)
            except Exception as gen_error:
                return (False, f"Generator error: {str(gen_error)[:100]}", "")
            response_text = full_response
        else:
            response_text = str(response)
            
        if response_text:
            if len(response_text.strip()) > 0:
                # Show first 200 characters of response
                preview = response_text[:200] + ("..." if len(response_text) > 200 else "")
                return (True, "Success", preview)
            else:
                return (False, "Empty response", "")
        return (False, "No response object", "")
    except Exception as e:
        return (False, str(e)[:200], "")

def main():
    print("=" * 60)
    print("Testing AISEARCH Providers")
    print("=" * 60)
    
    # Define providers to test with lazy imports
    provider_configs = [
        ("Genspark", "webscout.Provider.AISEARCH.genspark_search", "Genspark"),
        ("IAsk", "webscout.Provider.AISEARCH.iask_search", "IAsk"),
        ("Monica", "webscout.Provider.AISEARCH.monica_search", "Monica"),
        ("PERPLEXED", "webscout.Provider.AISEARCH.PERPLEXED_search", "PERPLEXED"),
        ("Perplexity", "webscout.Provider.AISEARCH.Perplexity", "Perplexity"),
        ("Stellar", "webscout.Provider.AISEARCH.stellar_search", "Stellar"),
        ("WebPilot", "webscout.Provider.AISEARCH.webpilotai_search", "webpilotai"),
    ]
    
    results: List[Tuple[str, bool, str, str]] = []  # (name, success, message, preview)
    
    test_query = "What is artificial intelligence?"
    
    for name, module_path, class_name in provider_configs:
        print(f"\n{'=' * 40}")
        print(f"Testing: {name}")
        print(f"{'=' * 40}")
        
        try:
            # Lazy import
            module = __import__(module_path, fromlist=[class_name])
            provider_class = getattr(module, class_name)
            print(f"✅ Successfully imported {name}")
        except Exception as e:
            error_msg = f"Import failed: {str(e)[:100]}"
            print(f"❌ {error_msg}")
            results.append((name, False, error_msg, ""))
            continue
        
        success, message, preview = test_provider(name, provider_class, test_query)
        
        if success:
            print(f"  ✅ WORKING: {message}")
            results.append((name, True, message, preview))
        else:
            print(f"  ❌ FAILED: {message}")
            results.append((name, False, message, preview))
        
        time.sleep(1)  # Small delay between tests
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    working = [(n, m, p) for n, s, m, p in results if s is True]
    failed = [(n, m, p) for n, s, m, p in results if s is False]
    
    print(f"\n✅ WORKING ({len(working)}):")
    for name, msg, preview in working:
        print(f"  - {name}")
    
    print(f"\n❌ FAILED ({len(failed)}):")
    for name, msg, preview in failed:
        print(f"  - {name}: {msg}")
    
    print(f"\n📊 Total: {len(working)} working, {len(failed)} failed")

if __name__ == "__main__":
    main()