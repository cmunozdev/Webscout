"""Test script for all AISEARCH providers in webscout"""
import sys
import time
from typing import Dict, List, Tuple

# Fix encoding for Windows console
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, errors='replace')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, errors='replace')

def test_provider(name: str, provider_class, test_query: str = "What is Python?"):
    """Test a single provider and return (success, error_message)"""
    try:
        # Initialize the provider
        client = provider_class()
        
        print(f"  Testing with query: {test_query}")
        
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
                return (False, f"Generator error: {str(gen_error)[:100]}")
            response_text = full_response
        else:
            response_text = str(response)
            
        if response_text:
            if len(response_text.strip()) > 0:
                # Show first 200 characters of response
                preview = response_text[:200] + ("..." if len(response_text) > 200 else "")
                return (True, f"Success - got response ({len(response_text)} chars): {preview}")
            else:
                return (False, "Empty response")
        return (False, "No response object")
    except Exception as e:
        return (False, str(e)[:200])

def main():
    print("=" * 60)
    print("Testing AISEARCH Providers")
    print("=" * 60)
    
    # Import all providers
    try:
        from webscout.Provider.AISEARCH import (
            Genspark, IAsk, Monica, PERPLEXED, Perplexity, Stellar, webpilotai
        )
        
        print("✅ Successfully imported all providers")
    except Exception as e:
        print(f"❌ Failed to import providers: {e}")
        return
    
    # Define providers to test
    providers = [
        ("Genspark", Genspark),
        ("IAsk", IAsk),
        ("Monica", Monica),
        ("PERPLEXED", PERPLEXED),
        ("Perplexity", Perplexity),
        ("Stellar", Stellar),
        ("WebPilot", webpilotai),
    ]
    
    results: List[Tuple[str, bool, str]] = []  # (name, success, message)
    
    test_query = "What is artificial intelligence?"
    
    for name, provider_class in providers:
        print(f"\n{'=' * 40}")
        print(f"Testing: {name}")
        print(f"{'=' * 40}")
        
        success, message = test_provider(name, provider_class, test_query)
        
        if success:
            print(f"  ✅ WORKING: {message}")
            results.append((name, True, message))
        else:
            print(f"  ❌ FAILED: {message}")
            results.append((name, False, message))
        
        time.sleep(2)  # Small delay between tests
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    working = [(n, m) for n, s, m in results if s is True]
    failed = [(n, m) for n, s, m in results if s is False]
    
    print(f"\n✅ WORKING ({len(working)}):")
    for name, msg in working:
        print(f"  - {name}")
    
    print(f"\n❌ FAILED ({len(failed)}):")
    for name, msg in failed:
        print(f"  - {name}: {msg[:60]}...")
    
    print(f"\n📊 Total: {len(working)} working, {len(failed)} failed")

if __name__ == "__main__":
    main()