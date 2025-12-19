from typing import Generator, Optional, Union, Any, Dict
import json
import time
from curl_cffi import CurlError
from curl_cffi.requests import Session

from webscout.AIutel import Optimizers
from webscout.AIutel import Conversation
from webscout.AIutel import AwesomePrompts
from webscout.AIbase import Provider
from webscout import exceptions
from webscout.litagent import LitAgent
from webscout.sanitize import sanitize_stream


class EssentialAI(Provider):
    """
    A class to interact with the EssentialAI rnj-1-instruct Space Gradio API.

    This provider integrates the RNJ-1-Instruct model into the Webscout framework.
    """
    required_auth = False
    AVAILABLE_MODELS = ["rnj-1-instruct"]

    def __init__(
        self,
        is_conversation: bool = True,
        max_tokens: int = 512,
        timeout: int = 60,
        intro: str = None,
        filepath: str = None,
        update_file: bool = True,
        proxies: dict = {},
        history_offset: int = 10250,
        act: str = None,
        system_prompt: str = "You are a helpful AI assistant.",
        model: str = "rnj-1-instruct",
        temperature: float = 0.2,
        top_p: float = 0.95,
    ):
        """
        Initializes the EssentialAI API with given parameters.

        Args:
            is_conversation (bool): Whether the provider is in conversation mode.
            max_tokens (int): Maximum number of tokens to sample.
            timeout (int): Timeout for API requests.
            intro (str): Introduction message for the conversation.
            filepath (str): Filepath for storing conversation history.
            update_file (bool): Whether to update the conversation history file.
            proxies (dict): Proxies for the API requests.
            history_offset (int): Offset for conversation history.
            act (str): Act for the conversation.
            system_prompt (str): The system prompt to define the assistant's role.
            model (str): Model to use.
            temperature (float): Sampling temperature.
            top_p (float): Nucleus sampling threshold.
        """
        self.session = Session()
        self.is_conversation = is_conversation
        self.max_tokens_to_sample = max_tokens
        self.api_endpoint = "https://essentialai-rnj-1-instruct-space.hf.space"
        self.timeout = timeout
        self.last_response = {}
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.top_p = top_p

        # Initialize LitAgent for user agent generation
        self.agent = LitAgent()

        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": self.agent.random(),
            "Accept": "text/event-stream",
        }

        self.__available_optimizers = (
            method
            for method in dir(Optimizers)
            if callable(getattr(Optimizers, method)) and not method.startswith("__")
        )
        self.session.headers.update(self.headers)
        self.session.proxies = proxies

        Conversation.intro = (
            AwesomePrompts().get_act(
                act, raise_not_found=True, default=None, case_insensitive=True
            )
            if act
            else intro or Conversation.intro
        )
        self.conversation = Conversation(
            is_conversation, self.max_tokens_to_sample, filepath, update_file
        )
        self.conversation.history_offset = history_offset

    def _get_session_hash(self) -> str:
        """Generate a session hash for the Gradio API."""
        import random
        import string
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=11))

    @staticmethod
    def _essentialai_extractor(chunk: Union[str, Dict[str, Any]]) -> Optional[str]:
        """Extracts content from EssentialAI Gradio stream JSON objects."""
        if isinstance(chunk, dict):
            msg = chunk.get("msg")
            if msg == "process_generating":
                output = chunk.get("output", {})
                data = output.get("data")
                if data and isinstance(data, list) and len(data) > 0:
                    # Gradio 4 ChatInterface usually returns the full response in data[0]
                    # or an array of operations.
                    val = data[0]
                    if isinstance(val, str):
                        return val
                    elif isinstance(val, list):
                        # Some versions return a list of operations
                        for op in val:
                            if isinstance(op, list) and len(op) > 2 and op[0] == "append":
                                return op[2]
            elif msg == "process_completed":
                output = chunk.get("output", {})
                data = output.get("data")
                if data and isinstance(data, list) and len(data) > 0:
                    val = data[0]
                    if isinstance(val, str):
                        return val
        return None

    def ask(
        self,
        prompt: str,
        stream: bool = False,
        raw: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
    ) -> Union[Dict[str, Any], Generator]:
        """
        Sends a prompt to the EssentialAI Gradio API and returns the response.

        Args:
            prompt (str): The prompt to send to the API.
            stream (bool): Whether to stream the response.
            raw (bool): Whether to return the raw response.
            optimizer (str): Optimizer to use for the prompt.
            conversationally (bool): Whether to generate the prompt conversationally.

        Returns:
            Dict[str, Any]: The API response.
        """
        conversation_prompt = self.conversation.gen_complete_prompt(prompt)
        if optimizer:
            if optimizer in self.__available_optimizers:
                conversation_prompt = getattr(Optimizers, optimizer)(
                    conversation_prompt if conversationally else prompt
                )
            else:
                raise Exception(
                    f"Optimizer is not one of {self.__available_optimizers}"
                )

        session_hash = self._get_session_hash()
        
        # Payload for the named endpoint /chat
        # Parameters: [message, system_message, max_tokens, temperature, top_p]
        payload = {
            "data": [
                conversation_prompt,
                self.system_prompt,
                self.max_tokens_to_sample,
                self.temperature,
                self.top_p
            ],
            "event_data": None,
            "fn_index": None,
            "api_name": "/chat",
            "session_hash": session_hash,
        }

        def for_stream():
            streaming_text = ""
            try:
                # Join the queue
                join_url = f"{self.api_endpoint}/gradio_api/queue/join"
                join_response = self.session.post(join_url, json=payload, timeout=self.timeout)
                join_response.raise_for_status()

                # Stream the data
                url = f"{self.api_endpoint}/gradio_api/queue/data?session_hash={session_hash}"
                response = self.session.get(
                    url,
                    stream=True,
                    timeout=self.timeout,
                    impersonate="chrome110"
                )
                if not response.ok:
                    raise exceptions.FailedToGenerateResponseError(
                        f"Failed to generate response - ({response.status_code}, {response.reason}) - {response.text}"
                    )

                # Use sanitize_stream
                processed_stream = sanitize_stream(
                    data=response.iter_content(chunk_size=None),
                    intro_value="data:",
                    to_json=True,
                    content_extractor=self._essentialai_extractor,
                    yield_raw_on_error=False,
                    raw=raw
                )

                last_full_text = ""
                for current_full_text in processed_stream:
                    if current_full_text and isinstance(current_full_text, str):
                        # Gradio often returns the full text accumulated so far.
                        # We calculate the delta.
                        if current_full_text.startswith(last_full_text):
                            delta = current_full_text[len(last_full_text):]
                        else:
                            delta = current_full_text
                        
                        last_full_text = current_full_text
                        
                        if delta:
                            if raw:
                                yield delta
                            else:
                                streaming_text += delta
                                resp = dict(text=delta)
                                yield resp

            except CurlError as e:
                raise exceptions.FailedToGenerateResponseError(f"Request failed (CurlError): {e}")
            except Exception as e:
                raise exceptions.FailedToGenerateResponseError(f"An unexpected error occurred ({type(e).__name__}): {e}")
            finally:
                if streaming_text:
                    self.last_response = {"text": streaming_text}
                    self.conversation.update_chat_history(prompt, streaming_text)

        def for_non_stream():
            for _ in for_stream():
                pass
            return self.last_response if not raw else self.last_response.get("text", "")

        return for_stream() if stream else for_non_stream()

    def chat(
        self,
        prompt: str,
        stream: bool = False,
        optimizer: str = None,
        conversationally: bool = False,
        raw: bool = False,
    ) -> Union[str, Generator[str, None, None]]:
        """
        Generates a response from the EssentialAI API.

        Args:
            prompt (str): The prompt to send to the API.
            stream (bool): Whether to stream the response.
            optimizer (str): Optimizer to use for the prompt.
            conversationally (bool): Whether to generate the prompt conversationally.
            raw (bool): Whether to return raw response chunks.

        Returns:
            str: The API response.
        """

        def for_stream():
            for response in self.ask(
                prompt, True, raw=raw, optimizer=optimizer, conversationally=conversationally
            ):
                if raw:
                    yield response
                else:
                    yield self.get_message(response)

        def for_non_stream():
            result = self.ask(
                prompt,
                False,
                raw=raw,
                optimizer=optimizer,
                conversationally=conversationally,
            )
            if raw:
                return result
            else:
                return self.get_message(result)

        return for_stream() if stream else for_non_stream()

    def get_message(self, response: dict) -> str:
        """
        Extracts the message from the API response.

        Args:
            response (dict): The API response.

        Returns:
            str: The message content.
        """
        assert isinstance(response, dict), "Response should be of dict data-type only"
        return response.get("text", "")


if __name__ == "__main__":
    from rich import print
    ai = EssentialAI(timeout=120)
    response = ai.chat("write a poem about AI", stream=True, raw=False)
    for chunk in response:
        print(chunk, end="", flush=True)
