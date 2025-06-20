import requests
from typing import Optional
from src.exceptions.custom_exceptions import (
    MailchimpServiceError,
    MailchimpAPIError
)

class MailchimpService:

    def __init__(self, api_key: str, server_prefix: str, public_id: str, template_id: Optional[str] = None):
        self.api_key = api_key
        self.public_id = public_id
        self.template_id = template_id
        self.base_url = f"https://{server_prefix}.api.mailchimp.com/3.0"

    def _auth(self):
        return ("anystring", self.api_key)

    def _handle_request(self, method: str, url: str, json: Optional[dict] = None):
        try:
            response = requests.request(method, url, auth=self._auth(), json=json)
            response.raise_for_status()
            return response
        
        except requests.RequestException as e:
            error_message = f"Mailchimp API request failed: {e}"
            if e.response is not None:
                try:
                    error_data = e.response.json()
                    
                    detail = error_data.get("detail", "")
                    
                    field_errors = error_data.get("errors", [])
                    
                    error_message += f" | Detail: {detail}"
                    
                    # Se houver erros de campo específicos, formata e adiciona à mensagem
                    if field_errors:
                        error_list = [f"Campo '{err.get('field')}': {err.get('message')}" for err in field_errors]
                        error_message += " | Field-Specific Errors: [" + ", ".join(error_list) + "]"
                except ValueError: # Se a resposta de erro não for JSON
                    error_message += f" | Response Body: {e.response.text}"
            raise MailchimpAPIError(error_message) from e
        
    def get_tags_id(self):
        url = f"{self.base_url}/lists/{self.public_id}/segments?type=static"
        response = self._handle_request("GET", url)

        # criar dicionário da resposta para mapear as tags e seus ids
        segments_list = response.json().get("segments")
        tags_map = {segment["name"]: segment["id"] for segment in segments_list}

        tag_id_florianopolis = tags_map["Florianópolis"]
        tag_id_cadastrado = tags_map["Cadastrado"]

        return [tag_id_florianopolis, tag_id_cadastrado]
       
    def create_campaign(self) -> str:
        # Campanha que envia apenas para quem está com as tags "Florianópolis" e "Cadastrado"
        tags = self.get_tags_id()
        tag_id_florianopolis = tags[0]
        tag_id_cadastrado = tags[1]

        url = f"{self.base_url}/campaigns"
        payload = {
            "type": "regular",
            "recipients": {
                "list_id": self.public_id,
                "segment_opts": {
                    "match": "all",
                    "conditions": [
                            {
                                "condition_type": "StaticSegment",
                                "field": "static_segment",
                                "op": "static_is",
                                "value": tag_id_florianopolis,   
                            },
                            {
                                "condition_type": "StaticSegment",
                                "field": "static_segment",
                                "op": "static_is",
                                "value": tag_id_cadastrado,   
                            }
                        ]
                }
            },
            "settings": {
                "subject_line": "🌊 Seu guia de surf chegou!",
                "title": "Swell Guide - Boletim Diário",
                "from_name": "Swell Guide",
                "reply_to": "swellguide@swellguide.com.br",
            }
        }
        response = self._handle_request("POST", url, json=payload)
        return response.json().get("id")

    def set_campaign_content(self, campaign_id: str, html_content: str):
        url = f"{self.base_url}/campaigns/{campaign_id}/content"
        payload = {"html": html_content}
        self._handle_request("PUT", url, json=payload)

    def send_campaign(self, campaign_id: str):
        url = f"{self.base_url}/campaigns/{campaign_id}/actions/send"
        response = self._handle_request("POST", url)
        if response.status_code != 204:
            raise MailchimpServiceError(f"Unexpected status code on send: {response.status_code} - {response.text}")

    def create_and_send_campaign(self, html_content: str):
        try:
            campaign_id = self.create_campaign()
            self.set_campaign_content(campaign_id, html_content)
            self.send_campaign(campaign_id)
        except Exception as e:
            raise MailchimpServiceError(f"Failed to create and send campaign: {str(e)}")
