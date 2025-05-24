import os
import markdown
from call_weather import fetch_weather_data
from call_ai_analysis import ai_analysis
from call_mailchimp import main_campaign_function
from dotenv import load_dotenv

load_dotenv()

def main():

    # set configs
    stormglass_auth = os.getenv("STORMGLASS_KEY")
    if not stormglass_auth:
        raise ValueError("Stormglass API Key not found")

    openai_key = os.getenv("OPEN_AI")
    if not openai_key:
        raise ValueError("Open AI API Key not found")

    surf_spot = "Florianópolis, SC - Brasil"
    floripa_latitude = -27.593500
    floripa_longitude = -48.558540


    # 1. call wheater API function
    print("Collecting forecast data...")
    stormglass_response = fetch_weather_data(floripa_latitude, floripa_longitude, stormglass_auth)

    # 2. call AI analysis over JSON response
    print("AI analysis starting...")
    ai_response = ai_analysis(openai_key, stormglass_response, surf_spot)

    # 3. convert markdown to html
    print("Converting AI output to HTML")
    html = markdown.markdown(ai_response)
    # with open('result.html', 'w', encoding="utf-8") as output_file:
    #     output_file.write(html)

    # 4. adicionar estilo ao HTML via template
    print("Setting CSS to HTML")
    with open("template.html", "r", encoding="utf-8") as tpl:
        template = tpl.read()
        final_html = template.replace("{{content}}", html)
    
    # 5. Enviar campanha
    main_campaign_function(final_html)

if __name__ == "__main__":
    main()
