import requests
from typing import List, Dict, Optional, Any
from abc import ABC, abstractmethod

from src.core.config import config
from src.core.exceptions import LLMError


class BaseLLMService(ABC):
    """Abstract base class for LLM services"""
    
    @abstractmethod
    def chat(self, prompt: str, context: str, conversation_history: List[Dict[str, str]]) -> tuple[str, List[Dict[str, str]]]:
        """Generate response given prompt, context, and conversation history"""
        pass


class LocalLLMService(BaseLLMService):
    """Service for interacting with local LLM via API"""
    
    def __init__(self, base_url: Optional[str] = None, model: Optional[str] = None):
        self.config = config
        self.base_url = base_url or self.config.llm_base_url or "http://localhost:8080"
        self.model = model or self.config.llm_model or "local-model"
        
    def chat(self, prompt: str, context: str, conversation_history: List[Dict[str, str]]) -> tuple[str, List[Dict[str, str]]]:
        """
        Generate response using local LLM
        
        Args:
            prompt: User's question
            context: Video transcript context
            conversation_history: Previous conversation messages
            
        Returns:
            Tuple of (response, updated_conversation_history)
            
        Raises:
            LLMError: If API call fails
        """
        try:
            # Build system message with context
            system_message = f"""You are a helpful assistant that answers questions about a YouTube video based on its transcript.

Video transcript:
{context}

Please answer questions based solely on the information provided in the transcript. If the answer is not in the transcript, say so."""

            # Build messages for the API
            messages = [{"role": "system", "content": system_message}]
            messages.extend(conversation_history)
            messages.append({"role": "user", "content": prompt})
            
            # Make API call
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7,
                    "max_tokens": 1000
                },
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Extract response
            assistant_response = data["choices"][0]["message"]["content"]
            
            # Update conversation history
            updated_history = conversation_history.copy()
            updated_history.append({"role": "user", "content": prompt})
            updated_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response, updated_history
            
        except requests.RequestException as e:
            raise LLMError(f"API request failed: {str(e)}")
        except KeyError as e:
            raise LLMError(f"Invalid API response format: {str(e)}")
        except Exception as e:
            raise LLMError(f"LLM processing failed: {str(e)}")


class OpenAILLMService(BaseLLMService):
    """Service for interacting with OpenAI API"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        self.config = config
        self.api_key = api_key or self.config.llm_api_key
        self.model = model
        self.client = None
        
        if not self.api_key:
            raise LLMError("OpenAI API key not provided")
        
        # Initialize OpenAI client
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise LLMError("OpenAI package not installed. Please install with: pip install openai")
    
    def chat(self, prompt: str, context: str, conversation_history: List[Dict[str, str]]) -> tuple[str, List[Dict[str, str]]]:
        """
        Generate response using OpenAI API
        
        Args:
            prompt: User's question
            context: Video transcript context
            conversation_history: Previous conversation messages
            
        Returns:
            Tuple of (response, updated_conversation_history)
        """
        
        try:
            # Build system message with context
            system_message = f"""You are a helpful assistant that answers questions about a YouTube video based on its transcript.

Video transcript:
{context}

Please answer questions based solely on the information provided in the transcript. If the answer is not in the transcript, say so."""

            # Build messages
            messages = [{"role": "system", "content": system_message}]
            messages.extend(conversation_history)
            messages.append({"role": "user", "content": prompt})
            
            # Make API call using new client format
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract response
            assistant_response = response.choices[0].message.content
            
            # Update conversation history
            updated_history = conversation_history.copy()
            updated_history.append({"role": "user", "content": prompt})
            updated_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response, updated_history
            
        except Exception as e:
            raise LLMError(f"OpenAI API call failed: {str(e)}")


def create_llm_service(service_type: str = "local", **kwargs) -> BaseLLMService:
    """
    Factory function to create LLM service
    
    Args:
        service_type: Type of service ("local" or "openai")
        **kwargs: Additional arguments for the service
        
    Returns:
        LLM service instance
    """
    if service_type.lower() == "local":
        return LocalLLMService(**kwargs)
    elif service_type.lower() == "openai":
        return OpenAILLMService(**kwargs)
    else:
        raise ValueError(f"Unsupported LLM service type: {service_type}")