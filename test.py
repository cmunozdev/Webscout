from webscout.client import Client

client = Client(print_provider_info=True)

test_models = [
    "auto",             # Should trigger fuzzy matching
]*100

for model in test_models:
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": "Say 'Test'"}
            ],
            stream=True
        )
        for chunk in resp:
            content = chunk.choices[0].delta.content
            if content is not None:
                print(content, end='', flush=True)
        print("\n" + "-"*30)
    except Exception as e:
        print(f"\nError testing {model}: {e}")
