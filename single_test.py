"""Test a single AISEARCH provider"""
import sys

def main():
    print("Testing Perplexity provider...")
    try:
        from webscout.Provider.AISEARCH import Perplexity
        ai = Perplexity()
        print("SUCCESS: Perplexity imported successfully")
        
        response = ai.search("What is Python?", stream=False)
        print(f"SUCCESS: Response received: {str(response)[:100]}...")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()