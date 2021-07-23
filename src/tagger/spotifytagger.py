import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from src.parser.parser import Parser

class SpotifyTagger():
    def __init__(self, client_id, client_secret):
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self._sp = spotipy.Spotify(auth_manager=auth_manager)
    def processTracks(self, tracks:dict):
        for trackInfo in tracks.values():
            if not trackInfo.get('spotify'):
                trackInfo['spotify'] = {}

            # Do not process if there is already a spotify info
            if trackInfo['spotify'].get('track') is not None:
                continue

            artist = ''
            if trackInfo.get('artist'):
                artist = Parser.clearArtistName(str(trackInfo['artist'])) + ' '

            for tries in range(0, 2):
                q = artist
                q += trackInfo['title']

                try:
                    results = self._sp.search(q, limit=3, market='RU')
                except Exception:
                    continue

                if results.get('tracks') and results['tracks'].get('items'):
                    trackItem = results['tracks']['items'][0]
                    trackInfo['spotify']['track'] = trackItem['uri']
                    trackInfo['spotify']['album'] = trackItem['album']['uri']
                    trackInfo['spotify']['image'] = trackItem['album']['images'][0]['url']
                    if not trackInfo.get('date') and trackItem['album'].get('release_date'):
                        trackInfo['date'] = {}
                        release_date = trackItem['album']['release_date'].split('-')
                        trackInfo['date']['year'] = release_date[0]
                        trackInfo['date']['month'] = release_date[1] if release_date[1] else 1
                    break
                elif trackInfo.get('artist'):
                    for char in [',', ' ']:
                        artist = str(trackInfo['artist'])
                        lastSpacePos = artist.rfind(char)
                        if lastSpacePos != -1:
                            artist = artist[lastSpacePos + 1:] + ' '
                            break

    def createPlaylist(self, tracks:dict):
        for trackInfo in tracks:
            pass

    def rebuildPlaylist(self, tracks:dict):
        pass