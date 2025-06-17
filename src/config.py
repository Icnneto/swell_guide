import os
from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path
from src.exceptions.custom_exceptions import MissingEnvVarError

load_dotenv()

def get_env(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise MissingEnvVarError(f"Variável de ambiente obrigatória não encontrada: {key}")
    return value

@dataclass(frozen=True)
class Settings:
    """
    Agrupa todas as configurações da aplicação de forma imutável.
    """
    # API Keys
    stormglass_api_key: str = get_env('STORMGLASS_API_KEY')
    mailchimp_api_key: str = get_env('MAILCHIMP_API_KEY')
    openai_api_key: str = get_env('OPENAI_API_KEY') # Embora o Langchain pegue automaticamente, é bom ter explícito

    # Mailchimp
    mailchimp_public_id: str = get_env('MAILCHIMP_PUBLIC_ID')
    mailchimp_server_prefix: str = "us10" # Pode ser movido para .env

    # LLM
    llm_model_name: str = 'gpt-4'
    llm_temperature: float = 0.3

    # Paths
    templates_dir: Path = Path("templates")
    database_dir: Path = Path("database")

    @property
    def email_template_path(self) -> Path:
        return self.templates_dir / "email_template.html"

    @property
    def surf_spots_path(self) -> Path:
        return self.database_dir / "surf_spots.json"

# Instância única para ser importada em outros lugares
settings = Settings()