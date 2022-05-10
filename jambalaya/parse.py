import random
from datetime import datetime, timedelta

import yaml

import jambalaya as jb


def load_spec(fname):
    with open(fname) as file:
        return yaml.safe_load(file)

def parse_song(client, song):
    if len(song) == 1:
        song_item = client.get_song(uid=song[0])
    else:
        artist = song[0]
        title = song[1]
        song_item = client.get_song(artist=artist, title=title)
    return song_item

def parse_songs(client, songs):
    song_items = []
    for song in songs:
        song_items.append(parse_song(client, song))
    return song_items

def parse_playlist(client, playlist):
    return client.get_playlist_songs(name=playlist)

def get_song_ids(client, spec):
    pl_song_ids = []

    for block in spec['blocks']:
        if 'songs' in block:
            new_song_items = parse_songs(client, block['songs'])
        elif 'playlist' in block:
            new_song_items = parse_playlist(client, block['playlist'])

        if block['type'] == 'fixed':
            new_song_ids = [song['id'] for song in new_song_items]
        elif block['type'] == 'shuffle-all':
            new_song_ids = [song['id'] for song in new_song_items]
            random.shuffle(new_song_ids)
        elif block['type'] == 'shuffle-duration':
            shuffled_songs = jb.shuffle_duration(block['min'], block['max'], new_song_items)
            new_song_ids = [song['id'] for song in shuffled_songs]

        pl_song_ids.extend(new_song_ids)

    return pl_song_ids
