from webscout.Provider.AISEARCH import (
    PERPLEXED,
    Perplexity,
    Genspark,
    IAsk,
    Monica,
    Stellar,
    webpilotai
)
import sys

def test_provider(name, provider_class, **kwargs):
    print(f"Testing {name}...")
    try:
        provider = provider_class(**kwargs)
        response = provider.search("What is the capital of France?", stream=False)
        print(f"  Result: {str(response)[:100]}...")
        return True
    except Exception as e:
        print(f"  Error: {type(e).__name__}: {e}")
        return False

providers = [
    ("PERPLEXED", PERPLEXED),
    ("Perplexity", Perplexity),
    ("Genspark", Genspark),
    ("IAsk", IAsk),
    ("Monica", Monica),
    ("Stellar", Stellar),
    ("webpilotai", webpilotai),
]

results = {}
for name, cls in providers:
    results[name] = test_provider(name, cls)

print("\nSummary:")
for name, success in results.items():
    status = "OK" if success else "FAILED"
    print(f"{name}: {status}")
