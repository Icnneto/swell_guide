import arrow
import requests

def fetch_weather_data (lat:int, lng:int, auth: str):
    
  timezone = 'America/Sao_Paulo'
  # Data de amanhã
  tomorrow = arrow.now(timezone).shift(days=+1).floor('day')

  # Definir o horário de início e fim no horário de Brasília
  # Como estamos -3h do UTC, defino o horário compensando a diferença para receber os dados de 05 às 19h do horário de Brasília
  start_time_brasilia = tomorrow.replace(hour=5, minute=0, second=0)
  end_time_brasilia = tomorrow.replace(hour=16, minute=0, second=0)

  response = requests.get(
      'https://api.stormglass.io/v2/weather/point',
      params={
          'lat':lat,
          'lng':lng,
          'params': ','.join(['waveHeight', 'windSpeed', 'swellDirection', 'swellHeight', 'swellPeriod']),
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


