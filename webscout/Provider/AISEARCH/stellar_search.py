import requests
import re
import random
import string
from typing import Dict, Optional, Generator, Union, Any
from webscout.AIbase import AISearch, SearchResponse
from webscout import exceptions
from webscout.litagent import LitAgent
from webscout.sanitize import sanitize_stream

class Stellar(AISearch):
    """AI Search provider for stellar.byastra.ai"""
    def __init__(self, timeout: int = 30, proxies: Optional[dict] = None):
        self.api_endpoint_base = "https://stellar.byastra.ai/search/"
        self.timeout = timeout
        self.proxies = proxies
        self.session = requests.Session()
        self.agent = LitAgent()
        self.headers = {
            "accept": "text/x-component",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
            "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryBk4qteEWiLFjxatO",
            "dnt": "1",
            "next-action": "efc2643ed9bafe182a010b58ebea17f068ad3985",
            "next-router-state-tree": "%5B%22%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%2C%22%2F%22%2C%22refresh%22%5D%7D%2Cnull%2Cnull%2Ctrue%5D",
            "origin": "https://stellar.byastra.ai",
            "priority": "u=1, i",
            "referer": "https://stellar.byastra.ai/",
            "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": self.agent.random()
        }
        self.session.headers.update(self.headers)
        if proxies:
            self.session.proxies = proxies

    def _generate_id(self, length: int = 7) -> str:
        """Generate a random alphanumeric ID for the search thread."""
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

    def _make_payload(self, prompt: str, search_id: str) -> bytes:
        boundary = "----WebKitFormBoundaryBk4qteEWiLFjxatO"
        parts = [
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"1\"\r\n\r\n{{\"id\":\"71bb616ba5b7cbcac2308fe0c249a9f2d51825b7\",\"bound\":null}}\r\n",
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"2\"\r\n\r\n{{\"id\":\"8bcca1d0cb933b14fefde88dacb2865be3d1d525\",\"bound\":null}}\r\n",
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"3_input\"\r\n\r\n{prompt}\r\n",
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"3_id\"\r\n\r\n{search_id}\r\n",
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"3_userId\"\r\n\r\nnull\r\n",
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"0\"\r\n\r\n[{{\"action\":\"$F1\",\"options\":{{\"onSetAIState\":\"$F2\"}}}},{{\"messages\":[],\"chatId\":\"\"}},\"$K3\"]\r\n",
            f"--{boundary}--\r\n"
        ]
        return "".join(parts).encode("utf-8")

    @staticmethod
    def _stellar_extractor(chunk: Union[str, bytes, Dict[str, Any]]) -> Optional[str]:
        """
        Extracts content from the Stellar stream format (Next.js RSC).
        
        Matches patterns like: 16:{"diff":[0,"AI"]} or 16:{"text":"..."}
        """
        if isinstance(chunk, bytes):
            try:
                chunk = chunk.decode('utf-8', errors='replace')
            except Exception:
                return None
        if not isinstance(chunk, str):
            return None
        
        # Pattern for diff updates
        primary_pattern = r'\{"diff":\[0,\"([^\"]*?)\"\}"'
        primary_matches = re.findall(primary_pattern, chunk)
        
        if primary_matches:
            extracted_text = ''.join(primary_matches)
            # Handle escape sequences
            extracted_text = extracted_text.encode().decode('unicode_escape')
            return extracted_text if extracted_text.strip() else None
        
        # Fallback for direct text field in JSON-like RSC segments
        text_pattern = r'"text":"([^\"]*?)"'
        text_matches = re.findall(text_pattern, chunk)
        if text_matches:
            extracted_text = ''.join(text_matches)
            try:
                extracted_text = extracted_text.encode().decode('unicode_escape')
            except:
                pass
            return extracted_text if extracted_text.strip() else None

        return None

    def search(self, prompt: str, stream: bool = False, raw: bool = False) -> Union[SearchResponse, Generator[Union[Dict[str, str], SearchResponse, str], None, None]]:
        search_id = self._generate_id()
        payload = self._make_payload(prompt, search_id)
        endpoint = f"{self.api_endpoint_base}{search_id}"
        
        try:
            response = self.session.post(
                endpoint,
                data=payload,
                timeout=self.timeout,
                proxies=self.proxies,
                stream=stream,
            )
            if not response.ok:
                if response.status_code == 404:
                    raise exceptions.APIConnectionError(f"Stellar API endpoint not found (404). The service may have changed its URL structure again.")
                raise exceptions.APIConnectionError(f"Failed to get response: {response.status_code} {response.text}")

            def _yield_stream():
                processed_stream = sanitize_stream(
                    data=response.iter_lines(decode_unicode=True),
                    intro_value=None,
                    to_json=False,
                    content_extractor=self._stellar_extractor
                )
                full_response = ""
                for content in processed_stream:
                    if content and isinstance(content, str):
                        full_response += content
                        if raw:
                            yield {"text": content}
                        else:
                            yield content

            if stream:
                return _yield_stream()
            else:
                full_response = ""
                for content in _yield_stream():
                    full_response += str(content)
                
                if not full_response:
                    # Check for quota exceeded error in the full text
                    if "exceeded your current quota" in response.text:
                        raise exceptions.FailedToGenerateResponseError("Stellar API quota exceeded.")
                    
                if raw:
                    return {"text": full_response}
                else:
                    return SearchResponse(full_response)
        except requests.RequestException as e:
            raise exceptions.APIConnectionError(f"Request failed: {e}")

if __name__ == "__main__":
    ai = Stellar()
    user_query = "What is the capital of France?"
    print(f"Searching for: {user_query}")
    try:
        response = ai.search(user_query, stream=True, raw=False)
        for chunk in response:
            print(chunk, end="", flush=True)
    except Exception as e:
        print(f"\nError: {e}")