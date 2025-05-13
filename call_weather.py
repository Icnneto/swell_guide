import arrow
import requests

def fetch_weather_data (lat:int, lng:int, auth: str):
    
  timezone = 'America/Sao_Paulo'
  tomorrow = arrow.now(timezone).shift(days=+1).floor('day')

  # Set start and end date in Brasília time zone
  # As Brasília is -3h from UTC, set the date compensating the difference to receive data from 06 till 19h (Brasília timezone)
  start_time_brasilia = tomorrow.replace(hour=3, minute=0, second=0)
  end_time_brasilia = tomorrow.replace(hour=16, minute=0, second=0)

  try:
    response = requests.get(
        'https://api.stormglass.io/v2/weather/point',
        params={
            'lat':lat,
            'lng':lng,
            'params': ','.join(['windDirection', 'windSpeed', 'swellDirection', 'swellHeight', 'swellPeriod']),
            'start': start_time_brasilia.to('UTC').timestamp(),
            'end': end_time_brasilia.to('UTC').timestamp()
        },
        headers={
        'Authorization': auth
      }
    )

    if response.status_code != 200:
      raise Exception(f"Erro na requisição: {response.status_code} - {response.text}")
    
    return response.json()
  
  except Exception as e:
    return f"Error calling Stormglass API: {e}"


