import os
import json

from dotenv import load_dotenv
from typing import List, Dict
from pathlib import Path

from src.exceptions.custom_exceptions import MissingEnvVarError, ProcessingError
from src.utils.markdown_to_html_service import markdown_to_html
from src.utils.html_to_template import insert_html_template

from premailer import transform

load_dotenv()

def get_env_variable(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise MissingEnvVarError(f"Missing required environment variable: {key}")
    return value

def generate_forecast_report_for_spot(
    spot_name: str, 
    latitude: float, 
    longitude: float, 
    template_path: Path,
    llm_service, 
    weather_service
) -> str:
    try:
        weather_data = weather_service.fetch_weather_data(latitude, longitude)
        llm_response = llm_service.call_ai_analysis(weather_data, spot_name)

        markdown_html = markdown_to_html(llm_response)
        embedded_html = insert_html_template(template_path, markdown_html)
        return transform(embedded_html)
    except Exception as e:
        raise ProcessingError(f"Failed to process spot '{spot_name}': {str(e)}")


def load_spots_from_json(path: Path) -> List[Dict]:
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)
