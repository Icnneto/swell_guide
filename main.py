import os
from call_weather import fetch_weather_data
from dotenv import load_dotenv

load_dotenv()

# set configs
stormglass_auth = os.getenv("STORMGLASS_KEY")

if not stormglass_auth:
    raise ValueError("Chave de API STORMGLASS_KEY não encontrada no .env")

floripa_latitude = -27.5954
floripa_longitude = -48.5480

# 1. call wheater API function
stormglass_response = fetch_weather_data(floripa_latitude, floripa_longitude, stormglass_auth)
print(stormglass_response)

