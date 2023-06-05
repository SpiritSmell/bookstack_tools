import os
import sys
import requests
import mammoth

# BookStack API variables
bookStackConfig = {
    'base_url': 'https://wiki.eurasia.kz',
    'token_id': 'gXVA7jkJurfSOZrkTO3XFZT7FKbou301',
    'token_secret': 'GwN4OpxuDrURdCPQnHExzEHdVK211s47'
}

docx_file = '_CS Инструкция пользователя v2-1.docx'

# Convert the document to HTML
with open(docx_file, 'rb') as file:
    result = mammoth.convert_to_html(file)
html = result.value
messages = result.messages