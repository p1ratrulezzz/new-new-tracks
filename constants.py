import yaml

__all__ = ["JSON_FILENAME", "NRJ_TRACKS_URL", 'FULL_PARSE_INTERVAL_S', "SPOTIFY"]

JSON_FILENAME = 'resources/tracks.json'
NRJ_TRACKS_URL = 'https://www.energyfm.ru/new-tracks__load/page'
FULL_PARSE_INTERVAL_S = 30 * 24 * 3600  # 30 Days

with open('spotify.yml', 'r') as token_fp:
    spotify_data = yaml.safe_load(token_fp)
    token_fp.close()

if not spotify_data:
    raise RuntimeError('Spotify.yml can\'t be read')

intersect = spotify_data.keys() & {'client_id', 'client_secret'}
if len(intersect) != 2:
    raise RuntimeError('There must be client_id and client_secret set for spotify')


class SPOTIFY:
    CLIENT_ID = spotify_data['client_id']
    CLIENT_SECRET = spotify_data['client_secret']
    ICON_URL = '<img src="/images/spotify_icon.svg?raw=true" alt="Listen on spotify">'
