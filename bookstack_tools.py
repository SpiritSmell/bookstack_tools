# -*- coding: utf-8 -*-
import requests

API_ID = 'gXVA7jkJurfSOZrkTO3XFZT7FKbou301'
API_SECRET = 'GwN4OpxuDrURdCPQnHExzEHdVK211s47'
ADDRESS = 'https://wiki.eurasia.kz'


class bookstack_tools:
    api_id = ''
    api_secret = ''
    address = ''
    pages_data = None
    chapters_data = None
    books_data = None

    def __init__(self, api_id, api_secret, address):
        self.api_id = api_id
        self.api_secret = api_secret
        self.address = address

    def refresh_pages(self):

        headers = {
            'Authorization': f'Token {self.api_id}:{self.api_secret}'
        }
        url = f"{self.address}/api/pages"

        # if pages were read previously

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            results = response.json()['data']
            # print("Pages list:")
            # for result in results:
            #     print(result)
            return results
        else:
            print(f"Error getting pages: {response.status_code}")
            print("                   Error description:", response.text.encode().decode('unicode_escape'))
            print(response.json())
            return None

    @property
    def pages(self):
        # if data is already present, return it
        if self.pages_data:
            return self.pages_data
        # otherwise request and then return
        self.pages_data = self.refresh_pages()
        return self.pages_data

    def find_page(self, name):
        for page in self.pages:
            if page['name'] == name:
                return page
        return None

    def move_page(self, page, chapter=None, book=None):

        if not chapter and not book:
            print(f"Nor chapter neither book is defined")
            return None

        print(f"Moving page {page['id']} {page['name']} ")

        headers = {
            'Authorization': f'Token {self.api_id}:{self.api_secret}'
        }
        url = f"{self.address}/api/pages/{page['id']}"

        body = {}

        if chapter:
            body["chapter_id"] = chapter['id']
            print(f"to chapter {chapter['id']} {chapter['name']}")

        if book:
            body["book_id"] = book['id']
            print(f"to book {book['id']} {book['name']}")

        response = requests.put(url, headers=headers, json=body)

        if response.status_code == 200:
            updated_page = response.json()
            print(
                f'Page {updated_page["id"]} moved sucessfully to book {updated_page["book_id"]}, chapter {updated_page["chapter_id"]}:')
        else:
            print("Error moving page. Error code:", response.status_code)
            print("                   Error description:", response.text.encode().decode('unicode_escape'))

    def refresh_chapters(self):

        headers = {
            'Authorization': f'Token {self.api_id}:{self.api_secret}'
        }
        url = f"{self.address}/api/chapters"

        # if chapters were read previously

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            results = response.json()['data']
            # print("Chapters list:")
            # for result in results:
            # print(result)
            return results

        else:
            print(f"Error getting chapters: {response.status_code}")
            print("                   Error description:", response.text.encode().decode('unicode_escape'))
            print(response.json())
            return None

    @property
    def chapters(self):
        # if data is already present, return it
        if self.chapters_data:
            return self.chapters_data
        # otherwise request and then return
        self.chapters_data = self.refresh_chapters()
        return self.chapters_data

    def find_chapter(self, name):
        for chapter in self.chapters:
            if chapter['name'] == name:
                return chapter
        return None

    def create_chapter(self, book, chapter_name, chapter_description=None, chapter_tags=None):

        print(f"Creating chapter {chapter_name} in a book {book['id']} ")

        headers = {
            'Authorization': f'Token {self.api_id}:{self.api_secret}'
        }
        url = f"{self.address}/api/chapters"

        body = {}

        body["book_id"] = book['id']
        body["name"] = chapter_name
        if chapter_description:
            body["description"] = chapter_description
        if chapter_tags:
            body["description"] = chapter_tags

        response = requests.post(url, headers=headers, json=body)

        if response.status_code == 200:
            updated_chapter = response.json()
            print(f'chapter {updated_chapter["id"]} created')
            return updated_chapter
        else:
            print("Error creating chapter. Error code:", response.status_code)
            print("                   Error description:", response.text.encode().decode('unicode_escape'))
            return None

    def delete_chapter(self, chapter):

        print(f"Deleting chapter {chapter['name']} ")

        headers = {
            'Authorization': f'Token {self.api_id}:{self.api_secret}'
        }
        url = f"{self.address}/api/chapters/{chapter['id']}"

        response = requests.delete(url, headers=headers)

        if response.status_code == 204:
            print(f'chapter {chapter["id"]} {chapter["name"]} deleted')
            return chapter
        else:
            print("Error deleting chapter. Error code:", response.status_code)
            print("                   Error description:", response.text.encode().decode('unicode_escape'))
            return None

    def move_chapter(self, book, chapter):

        print(f"Moving chapter {chapter['id']} {chapter['name']} ")
        # create new chapter
        new_chapter = self.create_chapter(book,chapter['name'])

        if not new_chapter:
            return None

        source_chapter_details = self.get_chapter_details(chapter)
        # move all pages to the new chapter
        for item in source_chapter_details['pages']:
            self.move_page(item, chapter=new_chapter, book=book)

        # delete old chapter
        self.delete_chapter(chapter)


    def get_chapter_details(self, chapter):

        headers = {
            'Authorization': f'Token {self.api_id}:{self.api_secret}'
        }
        url = f"{self.address}/api/chapters/{chapter['id']}"

        # if chapters were read previously

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            results = response.json()
            # print("chapters list:")
            # for result in results:
            #    print(result)
            return results

        else:
            print(f"Error getting chapter details: {response.status_code}")
            print("                   Error description:", response.text.encode().decode('unicode_escape'))
            print(response.json())
            return None

    def refresh_books(self):

        headers = {
            'Authorization': f'Token {self.api_id}:{self.api_secret}'
        }
        url = f"{self.address}/api/books"

        # if books were read previously

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            results = response.json()['data']
            # print("Books list:")
            # for result in results:
            #    print(result)
            return results

        else:
            print(f"Error getting books: {response.status_code}")
            print("                   Error description:", response.text.encode().decode('unicode_escape'))
            print(response.json())
            return None

    @property
    def books(self):
        # if data is already present, return it
        if self.books_data:
            return self.books_data
        # otherwise request and then return
        self.books_data = self.refresh_books()
        return self.books_data

    def find_book(self, name):
        for book in self.books:
            if book['name'] == name:
                return book
        return None

    def get_book_details(self, book):

        headers = {
            'Authorization': f'Token {self.api_id}:{self.api_secret}'
        }
        url = f"{self.address}/api/books/{book['id']}"

        # if books were read previously

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            results = response.json()
            # print("Books list:")
            # for result in results:
            #    print(result)
            return results

        else:
            print(f"Error getting book details: {response.status_code}")
            print("                   Error description:", response.text.encode().decode('unicode_escape'))
            print(response.json())
            return None

    def move_from_book_to_chapter(self, book_name, chapter_name):
        book = self.find_book(book_name)
        # if chapter is not found
        if book is None:
            print(f"Book {book_name} is not found")
            return None

        chapter = self.find_chapter(chapter_name)
        # if chapter is not found
        if chapter is None:
            print(f"Chapter {chapter_name} is not found")
            return None

        book_details = self.get_book_details(book)
        # if book details is not found
        if book_details is None:
            print(f"Book {book_name} details is not found")
            return None

        # find and move all pages within a book
        for item in book_details['contents']:
            if item['type'] == 'page':
                self.move_page(item, chapter)
            if item['type'] == 'chapter':
                for page in item['pages']:
                    self.move_page(page, chapter)

    def move_pages(self, source_book_name=None, source_chapter_name=None, destination_book_name=None,
                   destination_chapter_name=None):

        # if sources are not provided
        if not source_chapter_name and not source_book_name:
            print(f"Book or chapter name is not provided")
            return None

        if source_chapter_name and source_book_name:
            print(f"Both book and chapter name is provided (pick one)")
            return None

        # if destinations are not provided
        if not source_chapter_name and not source_book_name:
            print(f"Book or chapter name is not provided")
            return None

        # get sources
        if source_book_name:
            source = self.find_book(source_book_name)
            # if source book is provided, but not found
            if source is None:
                print(f"Book {source_book_name} is not found")
                return None

            source_details = self.get_book_details(source)
            # if book details is not found
            if source_details is None:
                print(f"Book {source_book_name} details is not found")
                return None
        else:
            source = self.find_chapter(source_chapter_name)
            # if source chapter is provided, but not found
            if source is None:
                print(f"chapter {source_chapter_name} is not found")
                return None
            source_details = self.get_chapter_details(source_chapter_name)
            # if chapter details is not found
            if source_details is None:
                print(f"chapter {source_chapter_name} details is not found")
                return None

        # get destinations
        if destination_book_name:
            destination_book = self.find_book(destination_book_name)
            # if destination book is provided, but not found
            if destination_book is None:
                print(f"Book {destination_book_name} is not found")
                return None
        else:
            destination_book = None

        if destination_chapter_name:
            destination_chapter = self.find_chapter(destination_chapter_name)
            # if destination chapter is provided, but not found
            if destination_chapter is None:
                print(f"chapter {destination_chapter_name} is not found")
                return None
        else:
            destination_chapter = None

        # find and move all pages from a book/chapter
        for item in source_details['contents']:
            if item['type'] == 'page':
                self.move_page(item, chapter=destination_chapter, book=destination_book)
            if item['type'] == 'chapter':
                # if moving chapter to a chapter, then just move pages
                if destination_chapter:
                    for page in item['pages']:
                        self.move_page(page, chapter=destination_chapter, book=destination_book)
                # if moving chapter from book to another book
                else:
                    self.move_chapter(destination_book, item)


if __name__ == '__main__':
    source_book_name = 'Move pages source'
    destination_book_name = 'Move pages destination'
    # chapter_name = 'Move page destination chapter'
    chapter_name = 'Test chapter 2'
    source_page_name = 'Test page 2.1'

    bt = bookstack_tools(API_ID, API_SECRET, ADDRESS)
    assert bt

    pages = bt.pages
    assert bt.pages
    print(f"Pages {pages}")

    chapters = bt.chapters
    assert bt.chapters
    print(f"Chapters {chapters}")

    books = bt.books
    assert bt.books
    print(f"Books {books}")

    page = bt.find_page(source_page_name)
    assert page
    print(f"Search for a page {page}")

    chapter = bt.find_chapter(chapter_name)
    assert chapter
    print(f"Search for a chapter {chapter}")

    chapter_details = bt.get_chapter_details(chapter)
    assert chapter_details
    print(f"Get chapter details {chapter_details}")

    book = bt.find_book(destination_book_name)
    assert book
    print(f"Search for a book {book}")

    book_details = bt.get_book_details(book)

    # bt.move_from_book_to_chapter(book_name, chapter_name)
    # bt.move_page(page, chapter=chapter)
    # bt.create_chapter(book_details, chapter_name)
    # bt.move_chapter(book_details, chapter_details)
    # bt.delete_chapter(chapter_details)

    bt.move_pages(source_book_name=source_book_name, destination_book_name=destination_book_name)
