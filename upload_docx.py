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

def main():
    # Check provided arguments
    if len(sys.argv) < 3:
        print('Both <docx_file> and <book_slug> arguments need to be provided')
        sys.exit()

    # Get arguments passed via command
    _, docx_file, book_slug = sys.argv[:3]

    # Check if the docx file exists
    if not os.path.exists(docx_file):
        print(f'Provided docx file "{docx_file}" could not be found')
        sys.exit()

    # Create a session for our API requests
    session = requests.Session()
    session.headers = {
        'Authorization': f'Token {bookStackConfig["token_id"]}:{bookStackConfig["token_secret"]}'
    }

    # Fetch the related book to ensure it exists
    book_search = session.get(f'{bookStackConfig["base_url"]}/api/books', params={'filter[slug]': book_slug})
    book_data = book_search.json()['data']
    if not book_data:
        print(f'Book with a slug of "{book_slug}" could not be found')
        sys.exit()
    book = book_data[0]

    # Convert the document to HTML
    with open(docx_file, 'rb') as file:
        result = mammoth.convert_to_html(file)
    html = result.value
    messages = result.messages

    # Create a name from the document file name
    name = os.path.splitext(os.path.basename(docx_file))[0]
    name = name.replace('-', ' ').replace('_', ' ')

    # Upload the page
    page_data = {
        'book_id': book['id'],
        'name': name,
        'html': html
    }
    response = session.post(f'{bookStackConfig["base_url"]}/api/pages', json=page_data, timeout=300000)

    if not (response.status_code == 200):
        print(f"Error getting books: {response.status_code}")
        print("                   Error description:", response.text.encode().decode('unicode_escape'))
        print(response.json())
        return None

    # Output the results
    page = response.json()

    print('File converted and created as a page.')
    print(f' - Page ID: {page["id"]}')
    print(f' - Page Name: {page["name"]}')
    print('====================================')
    print(f'Conversion occurred with {len(messages)} message(s):')
    for message in messages:
        print(f'[{message["type"]}] {message["message"]}')

if __name__ == '__main__':
    main()