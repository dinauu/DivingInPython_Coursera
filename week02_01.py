import argparse
import json
import os
import tempfile

STORAGE_PATH = os.path.join(tempfile.gettempdir(), 'storage.data')
if not os.path.isfile(STORAGE_PATH):
    with open(STORAGE_PATH, 'w') as f:
        pass


def save_to_json(key, value, file_name=STORAGE_PATH):
    with open(file_name, encoding='utf-8') as file:
        try:
            data = json.load(file)
        except ValueError:
            data = []
    data.append({key: value})
    with open(file_name, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2)


def find_in_json(key, file_name=STORAGE_PATH):
    with open(file_name, encoding='utf-8') as file:
        try:
            data = json.load(file)
        except ValueError:
            data = []
    items_list = list()
    for items in data:
        if key in items.keys():
            items_list.append(items.get(key, None))
    print(*items_list, sep=', ')


parser = argparse.ArgumentParser()
parser.add_argument('--key', help='get values of key or add key and value in storage')
parser.add_argument('--value', help='add key and value in storage')
args = parser.parse_args()
if args.key or args.key == '':
    key = args.key
    if args.value or args.value == '':
        value = args.value
        save_to_json(key, value)
    else:
        find_in_json(key)
