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
            raise MailchimpAPIError(f"Mailchimp API request failed: {str(e)}")

    def create_campaign(self) -> str:
        url = f"{self.base_url}/campaigns"
        payload = {
            "type": "regular",
            "recipients": {
                "list_id": self.public_id
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
