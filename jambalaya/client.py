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
        playlists = self._sp.current_user_playlists()  # TODO handle >50 playlists
        for pl in playlists['items']:
            if pl['name'] == name:
                return pl

    def set_playlist(self, pl_id, t_ids):
        self._sp.playlist_replace_items(pl_id, t_ids)
