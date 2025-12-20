from curl_cffi.requests import Session

payload = {
    "messages": ["Hello"],
    "character": "deepseek-r1"
}

try:
    with Session(impersonate="chrome124") as s:
        s.headers.update({
            "Origin": "https://chatsandbox.com",
            "Referer": "https://chatsandbox.com/chat/deepseek-r1",
        })
        print("POST api...")
        resp = s.post("https://chatsandbox.com/api/chat", json=payload, stream=True)
        print(f"Status: {resp.status_code}")
        for chunk in resp.iter_content():
             if chunk:
                 print(chunk.decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")
