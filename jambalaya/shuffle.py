import random

def shuffle_duration(min, max, songs):
    new_song_ids = []
    total_duration = 0
    while total_duration < min:
        chosen_song = random.choice(songs)
        if chosen_song['id'] in new_song_ids:
            continue
        total_duration += chosen_song['duration_ms'] / 1000
        if total_duration > max:
            total_duration = 0
            new_song_ids = []
        new_song_ids.append(chosen_song['id'])
    return new_song_ids
