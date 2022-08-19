#!/usr/bin/env python3

import requests
import re
import os
from pathlib import Path

def get_torrents(query):
    response = requests.get(f"https://nyaa.si/?q=${query}&s=seeders&o=desc")
    if not response.ok:
        print('error: couldn\'t download torrent list - aborting')
        exit(1)

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

        torrents.append(torrent)

    return torrents

def download_torrent(nid):
    response = requests.get(f"https://nyaa.si/download/{nid}.torrent")
    if not response.ok:
        print('error: couldn\'t download torrent file - aborting')
        exit(1)

    # return raw bytes
    return response.content

def run():
    query = input('query: ')

    # you probably want the one with the most seeders
    torrents = get_torrents(query)

    i = 0
    selections = []
    while True:
        for j in range(i, min(i + 10, len(torrents))):
            print(f"{j}: {torrents[j]['name']}")

        c = input('[numbers] / (c)ontinue / (f)inish: ')

        if c == 'c':
            i += 10
            if i >= len(torrents):
                print('error: no selection made - aborting')
                exit(1)
        elif c == 'f':
            break
        else:
            try:
                selections += ([int(x) for x in c.split(' ')])
                print(f"selection updated (have {selections})")
            except:
                print('warning: number list wrong - try again')

    for selection in selections:
        print(f"processing {torrents[selection]['name']}...")
        nid = torrents[selection]['nid']
        torrent_url = f"https://nyaa.si/view/{nid}"
        torrent = download_torrent(torrents[selection]['nid'])
        with open(f"{nid}.torrent", 'wb') as file:
            file.write(torrent)

        d = Path(__file__).resolve().parent.joinpath('downloads')
        Path(d).mkdir(exist_ok=True)
        # we are good people and seed
        os.system(f"transmission-remote -a {nid}.torrent -gsr 5 -w {d}")
        print('torrent launched')
        os.system(f"rm {nid}.torrent")

    print("finished!")


if __name__ == '__main__':
    run()
