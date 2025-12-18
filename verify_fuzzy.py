from webscout.client import Client, OPENAI_PROVIDERS
import difflib

def verify_fuzzy():
    # Initialize real client
    client = Client(print_provider_info=True)
    
    print("--- Real Data Fuzzy Matching Test ---")
    
    # We'll test with a few misspelled models that exist in the real providers
    test_cases = [
        "grok-4.1-fst",          # Should match grok-4.1-fast (Toolbaz)
        "gemini-2.0-flsh",       # Should match google/gemini-2.0-flash-001 or similar
        "llama-3.3-70b-vrsatile" # Should match llama-3.3-70b-versatile (Groq)
    ]
    
    for misspelled in test_cases:
        print(f"\nTesting misspelled model: '{misspelled}'")
        try:
            # We call the resolution logic directly to see what it picks
            # without making an actual network request.
            provider_cls, resolved_model = client.chat.completions._resolve_provider_and_model(misspelled, None)
            print(f"✅ Resolved to Provider: {provider_cls.__name__}")
            print(f"✅ Resolved to Model:    {resolved_model}")
        except Exception as e:
            print(f"❌ Failed to resolve '{misspelled}': {e}")

    print("\n--- Testing actual logic via .create() (Resolution phase) ---")
    print("Note: This will likely fail the actual network call if no API keys are set,")
    print("but it will show the 'Fuzzy match' print from the resolution logic.\n")
    
    try:
        # Using a model name that is clearly misspelled but close to a real one
        client.chat.completions.create(
            model="gpt-4o-mni", # Misspelling of gpt-4o-mini
            messages=[{"role": "user", "content": "Hi"}]
        )
    except Exception as e:
        # We expect a failure if network/keys are missing, but the fuzzy print 
        # (if print_provider_info=True) should have appeared in stdout.
        print(f"\nRequest phase ended: {e}")

if __name__ == "__main__":
    verify_fuzzy()
