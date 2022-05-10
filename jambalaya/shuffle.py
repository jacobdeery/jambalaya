import random


def shuffle_duration(min, max, songs):
    new_song_items = []
    total_duration = 0
    while total_duration < min:
        chosen_song = random.choice(songs)
        if chosen_song in new_song_items:
            continue
        total_duration += chosen_song['duration_ms'] / 1000
        if total_duration > max:
            total_duration = 0
            new_song_items = []
        new_song_items.append(chosen_song)
    return new_song_items
