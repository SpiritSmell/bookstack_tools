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
    book_name = ''
    chapter_name = ''

    # Определение опций и аргументов командной строки
    short_options = "hs:d:i:k:a:"
    long_options = ["help", "source=", "destination=", "id=", "key=", "address="]

    # Получение параметров командной строки
    arguments, values = getopt.getopt(sys.argv[1:], short_options, long_options)

    if len(arguments) < 5:
        print("Usage: move_pages.py -h|--help -s|--source <source book> -d|--destination <destination chapter> -i|--id <id token> -k|--key -a|--address <wiki address>")
        print(" -i|--id <API id> -k|--key <API key> -a|--address <wiki address>")
        sys.exit(2)
    # Обработка полученных параметров
    for current_argument, current_value in arguments:
        if current_argument in ("-h", "--help"):
            print("Usage: move_pages.py -h|--help -s|--source <source book> -d|--destination <destination chapter>")
            print(" -i|--id <API id> -k|--key <API key> -a|--address <wiki address>")
        elif current_argument in ("-s", "--source"):
            book_name = current_value
            print("Source book name:", book_name)
        elif current_argument in ("-d", "--destination"):
            chapter_name = current_value
            print("Destination chapter name:", chapter_name)
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
    bt.move_from_book_to_chapter(book_name, chapter_name)
