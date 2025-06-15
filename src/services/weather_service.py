"""
WeatherService - Service responsible for communicating with StormGlass API.

"""
import arrow
import requests
from typing import Dict, Any, Optional
from src.exceptions.custom_exceptions import WeatherAPIError

class WeatherService:

    def __init__(self, api_key: str, base_url: str = 'https://api.stormglass.io/v2/weather/point'):

        self.api_key = api_key
        self.base_url = base_url
        self.timezone = 'America/Sao_Paulo'

    def fetch_weather_data(self, lat: float, lng: float) -> Dict[str, Any]:

        try:
            # config dates to Brasilia timezone
            start_time, end_time = self._get_brasilia_time_range()

            # config request params
            params = self._build_request_params(lat, lng, start_time, end_time)

            # config request headers
            headers = self._build_headers()

            # Start API request
            response = requests.get(
                self.base_url,
                params=params,
                headers=headers
            )

            self._validate_response(response)

            return response.json()
        
        except requests.RequestException as e:
            raise WeatherAPIError(f'Error on API request: {str(e)}')
        except Exception as e:
            raise WeatherAPIError(f"Unexpected error on meteorological data search: {str(e)}")
    
    def _get_brasilia_time_range(self) -> tuple:

        tomorrow = tomorrow = arrow.now(self.timezone).shift(days=+1).floor('day')

        # Brasília is -3h from UTC, adjust date to receive infos from 06h to 19h
        start_time_brasilia = tomorrow.replace(hour=3, minute=0, second=0)
        end_time_brasilia = tomorrow.replace(hour=16, minute=0, second=0)
        
        return (
            start_time_brasilia.to('UTC').timestamp(),
            end_time_brasilia.to('UTC').timestamp()
        )

    def _build_request_params(self, lat: float, lng: float, start_time: float, end_time: float) -> Dict[str, Any]:

        return {
            'lat': lat,
            'lng': lng,
            'params': ','.join([
                'windDirection', 
                'windSpeed', 
                'swellDirection', 
                'swellHeight',
                'swellPeriod'
            ]),
            'start': start_time,
            'end': end_time
    }
    
    def _build_headers(self) -> Dict[str, str]:

        return {
            'Authorization': self.api_key
        }
    
    def _validate_response(self, response: requests.Response) -> None:

        if response.status_code != 200:
            error_message = f"Error on request: {response.status_code} - {response.text}"
            raise WeatherAPIError(error_message)





        