from openai import OpenAI

def ai_analysis (api_key:str, forecast:object, spot:str) -> str:
    client = OpenAI(api_key=api_key)

    with open("prompt_instructions.txt", "r", encoding="utf-8") as f:
        instructions = f.read()

    try:
        response = client.responses.create(
            model="gpt-4.1",
            instructions=instructions,
            input=(
                f"A seguir está um arquivo com a previsão de vento e ondas obtida da API da Stormglass para a localidade: {spot}."
                f"Arquivo com a previsão: {forecast}"
                "Analise esses dados e produza um relatório em **Markdown** que será enviado como uma newsletter. "
                "Lembre-se que o público é composto por pessoas com níveis variados de familiaridade com o mar, "
                "então use uma linguagem acessível, respeitosa e objetiva, conforme as instruções anteriores."
            ),
        )   

        return response.output_text
    
    except Exception as e:
        return f"Error generating AI analysis: {str(e)}"