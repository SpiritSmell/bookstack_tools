# -*- coding: utf-8 -*-
import getopt
import sys
from sys import argv

from bookstack_tools import bookstack_tools

API_ID = 'gXVA7jkJurfSOZrkTO3XFZT7FKbou301'
API_SECRET = 'GwN4OpxuDrURdCPQnHExzEHdVK211s47'
ADDRESS = 'https://wiki.eurasia.kz'

if __name__ == '__main__':
    # read command line
    source_book_name = None
    source_chapter_name = None
    destination_book_name = None
    destination_chapter_name = None

    # options definition
    short_options = "hsc:sb:dc:db:i:k:a:"
    long_options = ["help", "source_chapter=", "source_book=", "destination_chapter=", "destination_book=", "id=", "key=", "address="]

    # get command line arguments
    arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)

    if len(arguments) < 5:
        print("Usage: move_pages.py -h|--help -sc|--source_chapter <source chapter> -sb|--source_book <source book>")
        print(" -dc|--destination_chapter <destination chapter>  -db|--destination_book <destination book> ")
        print(" -i|--id <API id> -k|--key <API key> -a|--address <wiki address>")
        sys.exit(2)
    # Обработка полученных параметров
    for current_argument, current_value in arguments:
        if current_argument in ("-h", "--help"):
            print("Usage: move_pages.py -h|--help -sc|--source_chapter <source chapter> -sb|--source_book <source book>")
            print(" -dc|--destination_chapter <destination chapter>  -db|--destination_book <destination book> ")
            print(" -i|--id <API id> -k|--key <API key> -a|--address <wiki address>")
        elif current_argument in ("-sc", "--source_chapter"):
            source_chapter_name = current_value
            print("Source chapter name:", source_chapter_name)
        elif current_argument in ("-sb", "--source_book"):
            source_book_name = current_value
            print("Source book name:", source_book_name)
        elif current_argument in ("-dc", "--destination_chapter"):
            destination_chapter_name = current_value
            print("Destination chapter name:", destination_chapter_name)
        elif current_argument in ("-dc", "--destination_book"):
            destination_book_name = current_value
            print("Destination book name:", destination_book_name)
        elif current_argument in ("-i", "--id"):
            API_ID = current_value
            print("ID:", API_ID)
        elif current_argument in ("-k", "--key"):
            API_SECRET = current_value
            print("Key:", API_SECRET)
        elif current_argument in ("-a", "--address"):
            ADDRESS = current_value
            print("Address:", ADDRESS)

    # Обработка оставшихся аргументов
    for value in values:
        print("Extra arguments:", value)

    bt = bookstack_tools(API_ID, API_SECRET, ADDRESS)
    bt.move_pages(source_book_name=source_book_name, source_chapter_name=source_chapter_name,
                  destination_book_name=destination_book_name, destination_chapter_name=destination_chapter_name)
