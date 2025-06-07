from pathlib import Path
from typing import List, Dict

from src.services.llm_service import LLMService
from src.services.weather_service import WeatherService
from src.services.mailing_service import MailchimpService

from src.utils.helpers import ( get_env_variable, generate_forecast_report_for_spot, load_spots_from_json )


def main():
    try:
        # Carregar variáveis
        stormglass_key = get_env_variable('STORMGLASS_API_KEY')
        mailchimp_key = get_env_variable('MAILCHIMP_API_KEY')
        mailchimp_public_id = get_env_variable('MAILCHIMP_PUBLIC_ID')
        server_prefix = 'us9'  # poderá vir de env futuramente
        template_path = Path("templates/email_template.html")

        # Instanciar serviços
        weather_service = WeatherService(stormglass_key)
        llm_service = LLMService()
        mail_service = MailchimpService(mailchimp_key, server_prefix, mailchimp_public_id)

        # Lista de locais (fácil de expandir)
        database_path = Path("database/surf_spots.json")
        surf_spots = load_spots_from_json(database_path)

        for spot in surf_spots:
            final_html = generate_forecast_report_for_spot(
                spot_name=spot["name"],
                latitude=spot["lat"],
                longitude=spot["lon"],
                template_path=template_path,
                llm_service=llm_service,
                weather_service=weather_service
            )

            mail_service.create_and_send_campaign(final_html)

    except Exception as e:
        # Ideal: logar erro em arquivo ou sistema de monitoramento
        print(f"[ERROR] Unexpected failure: {e}")


if __name__ == "__main__":
    main()