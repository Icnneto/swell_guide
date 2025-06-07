import markdown

def markdown_to_html(doc: str) -> str:
    return markdown.markdown(doc)
        