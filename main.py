#!/usr/bin/env python3

import requests
import sys
import re

def parse_args():
    options = {}
    for arg in sys.argv:
        if arg.startswith('--'):
            arg = arg[2:].split('=')
            options[arg[0]] = arg[1]
    return options

def parse_nyaa_response(response):
    torrents = []

    text    = response.text.replace('\n', '').replace('\t', '')
    regex   = re.compile(r"<a href=\"/view/\d{7}\" title=\".*?\">.*?</a>")

    matches = regex.findall(text)
    for m in matches:
        torrent = {}

        i = m.find('/view/')
        torrent['nid'] = m[i+6 : i+13]

        i = m.find('title="', i)
        torrent['name'] = m[i+7 : m.find('"', i+7)]

        print(m[i:i+10])
        i = m.find('<td class="', i)
        i = m.find('<td class="', i)
        i = m.find('>', i)

        torrents.append(torrent)

    return torrents

def interactive():
    # query = input('query: ')
    query = 'jujutsu kaisen'
    # you probably want the one with the most seeders
    response = requests.get(f"https://nyaa.si/?q=${query}&s=seeders&o=desc")
    torrents = parse_nyaa_response(response)
    # for torrent in torrents:
        # print(f"{torrent['nid']}: {torrent['name']}")

def run():
    options = parse_args()
    interactive()

if __name__ == '__main__':
    run()
