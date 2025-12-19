"""Test a single AISEARCH provider"""
import sys

def main():
    print("Testing IAsk provider...")
    try:
        from webscout.Provider.AISEARCH import IAsk
        ai = IAsk()
        print("SUCCESS: IAsk imported successfully")
        
        response = ai.search("What is Python?", stream=False)
        print(f"SUCCESS: Response received: {str(response)[:100]}...")
        print(f"Full response length: {len(str(response))} characters")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()