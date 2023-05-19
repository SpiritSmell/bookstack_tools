# -*- coding: utf-8 -*-
import requests

API_ID = 'gXVA7jkJurfSOZrkTO3XFZT7FKbou301'
API_SECRET = 'GwN4OpxuDrURdCPQnHExzEHdVK211s47'
ADDRESS = 'https://wiki.eurasia.kz'


class bookstack_tools:
    api_id = ''
    api_secret = ''
    address = ''
    chapters_data = None
    books_data = None

    def __init__(self, api_id, api_secret, address):
        self.api_id = api_id
        self.api_secret = api_secret
        self.address = address

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

    def get_book_details(self,book):

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
            print(f"Error getting books: {response.status_code}")
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


    def move_page(self, page, chapter):
        print(f"Move page {page['id']} {page['name']} to chapter {chapter['id']} {chapter['name']}")

if __name__ == '__main__':
    book_name = 'Move pages source'
    chapter_name = 'Move page destination chapter'

    bt = bookstack_tools(API_ID, API_SECRET, ADDRESS)
    assert (bt)
    chapters = bt.chapters
    assert (bt.chapters)
    print(f"Chapters{chapters}")
    books = bt.books
    assert (bt.books)
    print(f"Books{books}")

    chapter = bt.find_chapter(chapter_name)
    assert (chapter)
    print(f"Search for a chapter {chapter}")

    book = bt.find_book(book_name)
    assert (book)
    print(f"Search for a book {book}")

    bt.get_book_details(book)

    bt.move_from_book_to_chapter(book_name, chapter_name)
