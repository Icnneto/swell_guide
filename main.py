import json
from langchain_openai import ChatOpenAI

# Importações refatoradas
from src.config import settings
from src.llm.llm_service import LLMService
from src.llm.prompt_manager import PromptManager
from src.services.weather_service import WeatherService
from src.services.mailing_service import MailchimpService
from src.use_cases.report_generator import ReportGenerator
from templates.prompt_template import template_str # Importa a string diretamente

def main():
    try:
        # 1. Construção das Dependências (usando o módulo de config)
        llm_client = ChatOpenAI(
            model=settings.llm_model_name,
            temperature=settings.llm_temperature
        )
        prompt_manager = PromptManager(template_string=template_str)
        
        weather_service = WeatherService(api_key=settings.stormglass_api_key)
        llm_service = LLMService(client=llm_client, prompt_manager=prompt_manager)
        
        report_generator = ReportGenerator(
            weather_service=weather_service,
            llm_service=llm_service,
            email_template_path=settings.email_template_path
        )
        
        mail_service = MailchimpService(
            api_key=settings.mailchimp_api_key,
            server_prefix=settings.mailchimp_server_prefix,
            public_id=settings.mailchimp_public_id
        )

        # 2. Execução da Lógica Principal
        with settings.surf_spots_path.open('r', encoding='utf-8') as f:
            surf_spots = json.load(f)

        print(f"Iniciando processo para {len(surf_spots)} pico(s) de surf...")
        for spot in surf_spots:
            print(f"-> Gerando relatório para {spot['name']}...")
            final_html_content = report_generator.generate_for_spot(
                spot_name=spot["name"],
                latitude=spot["lat"],
                longitude=spot["lon"]
            )
            
            print(f"-> Enviando campanha por e-mail para {spot['name']}...")
            mail_service.create_and_send_campaign(final_html_content)
            print(f"✅ Campanha para {spot['name']} enviada com sucesso!")

    except Exception as e:
        # Idealmente, usar um sistema de logging mais robusto
        print(f"[ERRO FATAL] A aplicação falhou: {e}")

if __name__ == "__main__":
    main()