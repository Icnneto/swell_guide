import os
from src.services.llm_service import LLMService
from src.services.weather_service import WeatherService
from src.utils.markdown_to_html_service import markdown_to_html
from dotenv import load_dotenv

load_dotenv()


STORMGLASS_API_KEY = os.getenv("STORMGLASS_API_KEY")
if not STORMGLASS_API_KEY:
    raise ValueError("Stormglass API Key not found")

surf_spot = "Florianópolis, SC - Brasil"
floripa_latitude = -27.593500
floripa_longitude = -48.558540

# def main():

#     # set configs
#     stormglass_auth = os.getenv("STORMGLASS_KEY")
#     if not stormglass_auth:
#         raise ValueError("Stormglass API Key not found")

#     openai_key = os.getenv("OPEN_AI")
#     if not openai_key:
#         raise ValueError("Open AI API Key not found")

#     surf_spot = "Florianópolis, SC - Brasil"
#     floripa_latitude = -27.593500
#     floripa_longitude = -48.558540


#     # 1. call wheater API function
#     print("Collecting forecast data...")
#     stormglass_response = fetch_weather_data(floripa_latitude, floripa_longitude, stormglass_auth)

#     # 2. call AI analysis over JSON response
#     print("AI analysis starting...")
#     ai_response = ai_analysis(openai_key, stormglass_response, surf_spot)

#     # 3. convert markdown to html
#     print("Converting AI output to HTML")
#     html = markdown.markdown(ai_response)
#     # with open('result.html', 'w', encoding="utf-8") as output_file:
#     #     output_file.write(html)

#     # 4. adicionar estilo ao HTML via template
#     print("Setting CSS to HTML")
#     with open("email_template.html", "r", encoding="utf-8") as tpl:
#         template = tpl.read()
#         final_html = template.replace("{{content}}", html)
    
#     # 5. Enviar campanha
#     main_campaign_function(final_html)

# if __name__ == "__main__":
#     main()


# weather_service retorna dict da API
weather_service = WeatherService(STORMGLASS_API_KEY)
print('Resgatando dados meteorológicos...')
weather_data = weather_service.fetch_weather_data(floripa_latitude, floripa_longitude)

# llm_service recebe dict e retorna markdown
llm_service = LLMService()
print('Chamando análise da LLM...')
llm_response = llm_service.call_ai_analysis(weather_data, surf_spot)
print('Gerando resposta da IA:')

# transformar markdown em html
html_output = markdown_to_html(llm_response)
