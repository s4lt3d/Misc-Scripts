# Written to convert html blog posts to md format for jekyll.

import os
import re

def replace_html_with_markdown(directory):
    html_tags = {
        'h1': '#',
        'h2': '##',
        'h3': '###',
        'h4': '####',
        'h5': '#####',
        'h6': '######',
        'p': '',
        'a': '[{text}]({url})',
        'strong': '**{text}**',
        'em': '*{text}*',
        'ul': '- {text}',
        'ol': '1. {text}',
        'li': '- {text}',
        'code': '`{text}`',
        'pre': '```\n{text}\n```',
        'blockquote': '> {text}',
        'br': '\n',
        'span': '\n',
        'div': '\n'
    }

    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                content = file.read()

            for tag, markdown in html_tags.items():
                if tag == 'br':
                    pattern = r"<{0}.*?\/?>".format(tag)
                    content = re.sub(pattern, markdown, content)
                else:
                    pattern = r"<{0}.*?>(.*?)<\/{0}>".format(tag)
                    if tag == 'a':
                        content = re.sub(pattern, markdown.format(text=r"\1", url=r"\1"), content)
                    else:
                        content = re.sub(pattern, markdown.format(text=r"\1"), content)

            with open(file_path, 'w') as file:
                file.write(content)

            print(f"Converted HTML tags to Markdown in file: {filename}")

# Specify the directory where the files are located
directory_path = "./"

# Call the function to replace HTML tags with Markdown tags
replace_html_with_markdown(directory_path)
