from curl_cffi.requests import Session

payload = {
    "messages": ["Hello"],
    "character": "openai-o1-mini"
}

try:
    with Session(impersonate="chrome124") as s:
        s.headers.update({
            "Origin": "https://chatsandbox.com",
            "Referer": "https://chatsandbox.com/chat/openai-o1-mini",
        })
        print("GET chat page...")
        s.get("https://chatsandbox.com/chat/openai-o1-mini")
        
        print("POST api...")
        resp = s.post("https://chatsandbox.com/api/chat", json=payload, stream=True)
        print(f"Status: {resp.status_code}")
        for chunk in resp.iter_content():
             if chunk:
                 print(chunk.decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
