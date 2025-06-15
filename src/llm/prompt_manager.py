from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import BaseMessage
from typing import Any, List

class PromptManager:
    def __init__(self, template_string: str):
        self.template = ChatPromptTemplate.from_template(template_string)

    def format(self, **kwargs: Any) -> List[BaseMessage]:
        return self.template.format_messages(**kwargs)