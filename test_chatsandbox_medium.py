from curl_cffi.requests import Session

payload = {
    "messages": ["This is a test message to see if length matters for the API. Please respond with 'Ok' if you received this correctly."],
    "character": "openai-gpt-4o"
}

try:
    with Session(impersonate="chrome124") as s:
        s.headers.update({
            "Origin": "https://chatsandbox.com",
            "Referer": "https://chatsandbox.com/chat/openai-gpt-4o",
        })
        print("POST api...")
        resp = s.post("https://chatsandbox.com/api/chat", json=payload, stream=True)
        print(f"Status: {resp.status_code}")
        for chunk in resp.iter_content():
             if chunk:
                 print(chunk.decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
