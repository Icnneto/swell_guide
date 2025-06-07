from pathlib import Path

def insert_html_template(path:Path, doc:str) -> str:
    try:
        with path.open('r', encoding='utf-8') as tpl:
            template = tpl.read()
            return template.replace('{{content}}', doc)
    except FileNotFoundError:
        raise FileNotFoundError(f"Template HTML não encontrado no caminho: {path}")
    except Exception as e:
        raise RuntimeError(f"Erro ao inserir conteúdo no template: {e}")