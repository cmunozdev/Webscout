from webscout.client import Client

client = Client(print_provider_info=True)
resp = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a joke about cats."}
    ],
    stream=True
)
for chunk in resp:
    content = chunk.choices[0].delta.content
    if content is not None:
        print(content, end='', flush=True)