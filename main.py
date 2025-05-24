import os
import markdown
from call_weather import fetch_weather_data
from call_ai_analysis import ai_analysis
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
    print(ai_response)

    # 3. convert markdown to html
    print("Converting AI output to HTML")
    html = markdown.markdown(ai_response)
    with open('result.html', 'w', encoding="utf-8") as output_file:
        output_file.write(html)

if __name__ == "__main__":
    main()
