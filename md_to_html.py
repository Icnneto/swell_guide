import markdown

with open('./test_ai_output/ai_output3.md', 'r', encoding="utf-8") as input_file:
    text = input_file.read()
    html = markdown.markdown(text)

with open('result.html', 'w', encoding="utf-8") as output_file:
    output_file.write(html)