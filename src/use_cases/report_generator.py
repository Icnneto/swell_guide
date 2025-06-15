import markdown
from premailer import transform
from pathlib import Path
from src.services.weather_service import WeatherService
from src.llm.llm_service import LLMService
from src.exceptions.custom_exceptions import ProcessingError, FileNotFoundError

class ReportGenerator:

    def __init__(self, weather_service: WeatherService, llm_service: LLMService, email_template_path: Path):
        self.weather_service = weather_service
        self.llm_service = llm_service
        self.email_template_path = email_template_path
        self._html_template_cache = self._load_template()

    def _load_template(self) -> str:
        try:
            with self.email_template_path.open('r', encoding='utf-8') as tpl:
                return tpl.read()
        except IOError as e:
            raise FileNotFoundError(f"Template de email não encontrado em {self.email_template_path}: {e}")

    def _markdown_to_html(self, doc: str) -> str:
        return markdown.markdown(doc)

    def _insert_content_in_template(self, content_html: str) -> str:
        return self._html_template_cache.replace('{{content}}', content_html)

    def generate_for_spot(self, spot_name: str, latitude: float, longitude: float) -> str:
        try:
            weather_data = self.weather_service.fetch_weather_data(latitude, longitude)
            llm_response = self.llm_service.generate_analysis(weather_data, spot_name)

            content_html = self._markdown_to_html(llm_response)
            email_body_html = self._insert_content_in_template(content_html)
            
            # Transforma CSS em inline para compatibilidade com clientes de e-mail
            return transform(email_body_html)
        except Exception as e:
            raise ProcessingError(f"Falha ao gerar relatório para '{spot_name}': {e}") from e