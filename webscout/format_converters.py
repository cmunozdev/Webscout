"""
format_converters.py

This module provides utilities for converting between legacy and OpenAI message formats.
It enables backward compatibility while supporting the modern OpenAI-compatible interface.

Functions:
    legacy_to_openai_messages: Convert legacy prompt to OpenAI message format
    openai_to_legacy_response: Convert OpenAI response to legacy format
    legacy_prompt_to_messages: Convert a legacy string prompt to OpenAI messages
    messages_to_legacy_prompt: Convert OpenAI messages to legacy string prompt
"""

from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import json


def legacy_to_openai_messages(
    prompt: str,
    conversationally: bool = False,
    conversation_history: Optional[List[Dict[str, Any]]] = None,
    intro: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Convert a legacy prompt to OpenAI message format.
    
    Args:
        prompt: The user's prompt text
        conversationally: Whether to include conversation history
        conversation_history: List of previous messages in OpenAI format
        intro: System introduction/instruction
        
    Returns:
        List of message dictionaries in OpenAI format
    """
    messages = []
    
    # Add system message if intro is provided
    if intro:
        messages.append({
            "role": "system",
            "content": intro
        })
    
    # Add conversation history if conversational mode is enabled
    if conversationally and conversation_history:
        messages.extend(conversation_history)
    
    # Add the current user prompt
    messages.append({
        "role": "user",
        "content": prompt
    })
    
    return messages


def openai_to_legacy_response(
    completion: Dict[str, Any],
    include_metadata: bool = False
) -> Dict[str, Union[str, bool, None]]:
    """
    Convert an OpenAI ChatCompletion response to legacy format.
    
    Args:
        completion: OpenAI ChatCompletion object (as dict)
        include_metadata: Whether to include additional metadata
        
    Returns:
        Dictionary in legacy response format with 'text' key
    """
    # Extract the message content from the first choice
    message_content = ""
    sources = []
    media = []
    
    if "choices" in completion and len(completion["choices"]) > 0:
        choice = completion["choices"][0]
        message = choice.get("message", {})
        message_content = message.get("content", "")
        
        # Check for tool calls (these might be in metadata)
        if "tool_calls" in message:
            # Tool calls are handled separately in the unified interface
            pass
    
    legacy_response = {
        "text": message_content,
        "sources": sources,
        "media": media
    }
    
    if include_metadata:
        legacy_response["metadata"] = {
            "model": completion.get("model"),
            "created": completion.get("created"),
            "finish_reason": completion["choices"][0].get("finish_reason") if "choices" in completion else None
        }
    
    return legacy_response


def legacy_prompt_to_messages(
    prompt: str,
    intro: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Convert a simple legacy string prompt to OpenAI message format.
    
    Args:
        prompt: The prompt text
        intro: Optional system message
        
    Returns:
        List of message dictionaries
    """
    messages = []
    
    if intro:
        messages.append({
            "role": "system",
            "content": intro
        })
    
    messages.append({
        "role": "user",
        "content": prompt
    })
    
    return messages


def messages_to_legacy_prompt(
    messages: List[Dict[str, Any]],
    include_system: bool = True
) -> str:
    """
    Convert OpenAI messages to a legacy string prompt format.
    
    Args:
        messages: List of message dictionaries in OpenAI format
        include_system: Whether to include system messages in output
        
    Returns:
        Formatted string prompt
    """
    prompt_parts = []
    
    for message in messages:
        role = message.get("role", "")
        content = message.get("content", "")
        
        if role == "system" and include_system:
            prompt_parts.append(f"System: {content}")
        elif role == "user":
            prompt_parts.append(f"User: {content}")
        elif role == "assistant":
            prompt_parts.append(f"Assistant: {content}")
        elif role == "tool":
            # Tool messages are formatted specially
            tool_call_id = message.get("tool_call_id", "unknown")
            prompt_parts.append(f"Tool ({tool_call_id}): {content}")
    
    return "\n".join(prompt_parts)


def validate_openai_message(message: Dict[str, Any]) -> bool:
    """
    Validate that a message conforms to OpenAI format.
    
    Args:
        message: Message dictionary to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(message, dict):
        return False
    
    # Must have role and content
    if "role" not in message:
        return False
    
    # Valid roles
    valid_roles = {"system", "user", "assistant", "tool"}
    if message["role"] not in valid_roles:
        return False
    
    # Content is required for most roles (assistant can have empty content during streaming)
    if message["role"] != "assistant" and "content" not in message:
        return False
    
    # Tool messages must have tool_call_id
    if message["role"] == "tool" and "tool_call_id" not in message:
        return False
    
    return True


def extract_message_content(response: Union[Dict, str]) -> str:
    """
    Extract message content from various response formats.
    
    Args:
        response: Response in various formats (OpenAI completion, legacy response, or string)
        
    Returns:
        Extracted message content as string
    """
    if isinstance(response, str):
        return response
    
    if isinstance(response, dict):
        # Try OpenAI format first
        if "choices" in response:
            return response["choices"][0]["message"]["content"]
        
        # Try legacy format
        if "text" in response:
            return response["text"]
        
        # Try direct message format
        if "message" in response:
            return response["message"]
        
        # Try content field
        if "content" in response:
            return response["content"]
    
    return str(response)


def normalize_role(role: str) -> str:
    """
    Normalize role names to lowercase for consistency.
    
    Args:
        role: Role name (may be mixed case)
        
    Returns:
        Normalized role name in lowercase
    """
    return role.lower().strip()
