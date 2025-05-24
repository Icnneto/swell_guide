import os
import requests
from dotenv import load_dotenv
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError

load_dotenv()

API_KEY = os.getenv("MAILCHIMP_KEY")
if not API_KEY:
    raise ValueError("Mailchimp API Key not found")

SERVER_PREFIX = 'us9'
PUBLIC_ID = os.getenv("MAILCHIMP_PUBLIC_ID")
if not PUBLIC_ID:
    raise ValueError("Public Id not found")

TEMPLATE_ID = os.getenv("TEMPLATE_ID")
if not TEMPLATE_ID:
   raise ValueError("Template Id not found")

BASE_URL = f"https://{SERVER_PREFIX}.api.mailchimp.com/3.0"

def create_campaign():
    url = f"{BASE_URL}/campaigns"
    payload = {
        "type": "regular",
        "recipients": {
            "list_id": PUBLIC_ID
        },
        "settings": {
            "subject_line": "🌊 Seu guia de surf chegou!",
            "title": "Swell Guide - Boletim Diário",
            "from_name": "Swell Guide",
            "reply_to": "israelnetonunes@gmail.com",
        }
    }

    response = requests.post(url, auth=("anystring", API_KEY), json=payload)
    response.raise_for_status()
    return response.json()["id"]

def set_campaign_content(campaign_id, html_content):
    url = f"{BASE_URL}/campaigns/{campaign_id}/content"
    payload = {
        "html": html_content
    }

    response = requests.put(url, auth=("anystring", API_KEY), json=payload)
    response.raise_for_status()

def send_campaign(campaign_id):
    url = f"{BASE_URL}/campaigns/{campaign_id}/actions/send"
    response = requests.post(url, auth=("anystring", API_KEY))
    if response.status_code != 204:  # 204 = sucesso sem conteúdo
        print("Erro ao enviar campanha:", response.status_code, response.text)
    response.raise_for_status()

def main_campaign_function(emailContent):

    print("Criando campanha...")
    campaign_id = create_campaign()

    print("Adicionando conteúdo...")
    set_campaign_content(campaign_id, emailContent)

    print("Enviando campanha...")
    send_campaign(campaign_id)

    print("Campanha enviada com sucesso!")
