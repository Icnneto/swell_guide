from langchain_openai import ChatOpenAI
from typing import Dict, Any
from .prompt_manager import PromptManager
from src.exceptions.custom_exceptions import LLMAPIError

class LLMService:

    def __init__(self, client: ChatOpenAI, prompt_manager: PromptManager):
        self.client = client
        self.prompt_manager = prompt_manager

    def generate_analysis(self, forecast: Dict[str, Any], spot: str) -> str:
        try:
            formatted_messages = self.prompt_manager.format(
                local=spot,
                forecast_json=str(forecast)
            )
            response = self.client.invoke(formatted_messages)
            
            content = response.content
            if not isinstance(content, str):
                raise LLMAPIError(f"Formato de resposta inesperado: {type(content)}")
            
            return content
        except Exception as e:
            raise LLMAPIError(f"Falha ao gerar análise da IA: {e}") from e