from curl_cffi.requests import Session

url_chat = "https://chatsandbox.com/chat/openai"
url_api = "https://chatsandbox.com/api/chat"

# Headers matching Chrome 124 (approximately)
headers = {
    'authority': 'chatsandbox.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://chatsandbox.com',
    'referer': 'https://chatsandbox.com/chat/openai',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
}

payload = {
    "messages": ["Hello, this is a test."],
    "character": "openai"
}

try:
    with Session(impersonate="chrome124") as s:
        print("Visiting chat page...")
        s.get(url_chat, headers=headers)
        print("Cookies:", s.cookies)
        
        print("Sending message...")
        response = s.post(
            url_api,
            headers=headers,
            json=payload,
            stream=True
        )
        print(f"Status: {response.status_code}")
        for chunk in response.iter_content():
            if chunk:
                print(chunk.decode('utf-8'))
except Exception as e:
    print(f"Error: {e}")