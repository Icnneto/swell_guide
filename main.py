import os
from src.services.llm_service import LLMService
from src.services.weather_service import WeatherService
from src.services.mailing_service import MailchimpService
from src.utils.markdown_to_html_service import markdown_to_html
from src.utils.html_to_template import insert_html_template
from dotenv import load_dotenv
from pathlib import Path
from premailer import transform

load_dotenv()

STORMGLASS_API_KEY = os.getenv('STORMGLASS_API_KEY')
if not STORMGLASS_API_KEY:
    raise ValueError('Stormglass API Key not found')

MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')
if not MAILCHIMP_API_KEY:
    raise ValueError('Mailchim API Key not found')

MAILCHIMP_PUBLIC_ID = os.getenv('MAILCHIMP_PUBLIC_ID')
if not MAILCHIMP_PUBLIC_ID:
    raise ValueError('Mailchim public id not found')

SERVER_PREFIX = 'us9'

PATH_TO_TEMPLATE = Path("templates") / "email_template.html"

surf_spot = "Florianópolis, SC - Brasil"
floripa_latitude = -27.593500
floripa_longitude = -48.558540

# weather_service retorna dict da API
weather_service = WeatherService(STORMGLASS_API_KEY)
print('Resgatando dados meteorológicos...')
weather_data = weather_service.fetch_weather_data(floripa_latitude, floripa_longitude)

# llm_service recebe dict e retorna markdown
llm_service = LLMService()
print('Chamando análise da LLM...')
llm_response = llm_service.call_ai_analysis(weather_data, surf_spot)

# transformar markdown em html
html_output = markdown_to_html(llm_response)

# inserir html no template de e-mail
embedded_html = insert_html_template(PATH_TO_TEMPLATE, html_output)

final_html = transform(embedded_html)

mailing_service = MailchimpService(MAILCHIMP_API_KEY, SERVER_PREFIX, MAILCHIMP_PUBLIC_ID)

send_campaign = mailing_service.create_and_send_campaign(final_html)
