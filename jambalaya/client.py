import math

import spotipy
from spotipy.oauth2 import SpotifyOAuth


class Client:
    def __init__(self):
        scope = "user-library-read, \
                playlist-modify-private, \
                playlist-modify-public"

        self._sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        self._user = self._sp.me()

    def get_song(self, artist=None, title=None, uid=None):
        if artist is not None and title is not None:
            title = title.replace("'", '')  # Spotify doesn't like apostrophes in query strings
            artist = artist.replace("'", '')
            query = f'track:{title} artist:{artist}'
            resp = self._sp.search(query, limit=10, type='track')
            tracks = resp['tracks']['items']
            return tracks[0]  # TODO perform better matching
        elif uid is not None:
            return self._sp.track(uid)

    def get_playlist(self, name):
        limit = 50
        offset = 0
        remaining = limit

        while remaining > 0:
            playlists = self._sp.current_user_playlists(limit=limit, offset=offset)
            for pl in playlists['items']:
                if pl['name'] == name:
                    return pl
            remaining = playlists['total'] - (offset + limit)
            offset += limit

    def get_playlist_songs(self, name=None, uid=None):
        if name is not None:
            uid = self.get_playlist(name=name)['uri']

        tracks = []

        limit = 100
        offset = 0
        remaining = limit

        while remaining > 0:
            resp = self._sp.playlist_tracks(uid, limit=limit, offset=offset)
            tracks.extend([track['track'] for track in resp['items']])
            remaining = resp['total'] - (offset + limit)
            offset += limit

        return tracks

    def set_playlist(self, pl_id, t_ids):
        self._sp.playlist_replace_items(pl_id, [])  # Clear the playlist

        limit = 50

        for i in range(math.ceil(len(t_ids) / limit)):
            start_idx = i * limit
            end_idx = min(start_idx + limit, len(t_ids))
            self._sp.playlist_add_items(pl_id, t_ids[start_idx:end_idx])
