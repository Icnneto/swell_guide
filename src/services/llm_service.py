from typing import Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.exceptions.custom_exceptions import LLMAPIError, LLMServiceError

class LLMService:

    def __init__ (self, 
                  model: str = 'gpt-4', 
                  temperature: float = 0.2
                ):
        
        """
        Note:
            API key is automatically retrieved by the env variable: OPENAI_API_KEY (langchain automation)
        """

        self.model = model
        self.temperature = temperature
        self._client: Optional[ChatOpenAI] = None
        self._prompt_template: Optional[ChatPromptTemplate] = None
    
    def _init_connection(self) -> ChatOpenAI:

        if self._client is None:
            try:
                self._client = ChatOpenAI(
                    model = self.model,
                    temperature = self.temperature
                )
            except Exception as e:
                raise LLMServiceError(f"Unexpected error LLM connection: {str(e)}")

        return self._client
    
    def _load_prompt_template(self) -> ChatPromptTemplate:
        if self._prompt_template is None:
            try:
                from templates.prompt_template import template_str
                self._prompt_template = ChatPromptTemplate.from_template(template_str)
            except Exception as e:
                raise LLMServiceError(f"Unexpected error at retrieving prompt template: {str(e)}")
            
        return self._prompt_template    
    
    def call_ai_analysis(self, forecast: Dict[str, Any], spot: str):

        try:
            model = self._init_connection()

            prompt_template = self._load_prompt_template()

            formatted_messages = prompt_template.format_messages(
                local=spot,
                forecast_json=forecast
            )

            response = model.invoke(formatted_messages)
            markdown_response = response.content

            return markdown_response
        except Exception as e:
            raise LLMAPIError(f"Unexpected error on LLM communication: {str(e)}")
    