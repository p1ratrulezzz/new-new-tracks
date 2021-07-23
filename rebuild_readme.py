from src.parser.nrjtracksparser import NRJTracksParser
from src.storage.jsonstorage import JsonStorage
from constants import *
from src.tagger.spotifytagger import SpotifyTagger
from src.formatter.readmeformatter import ReadmeFormatter
from datetime import datetime, timezone
import dateutil.parser
from urllib3.exceptions import TimeoutError, HTTPError

storage = JsonStorage(filename = JSON_FILENAME)

is_full_parse = True
last_finished = storage.getSandboxData('finished')
if last_finished:
    last_finished = dateutil.parser.isoparse(last_finished)
    if (datetime.now(timezone.utc) - last_finished).seconds <= FULL_PARSE_INTERVAL_S:
        is_full_parse = False

page : int = 1 if not is_full_parse else storage.getSandboxData('page', 1)

finished = False
while (not finished):
    url = NRJ_TRACKS_URL + '/' + str(page)
    parser = NRJTracksParser(url)
    try:
        tracks = parser.parseTracks()
        if len(tracks) == 0:
            finished = True
            storage.delSandboxData('page')
            storage.setSandboxData('finished', datetime.now(timezone.utc).isoformat(timespec='seconds'))
        else:
            page += 1
            storage.mergeTracks(tracks)
            storage.setSandboxData('page', page)

    except (TimeoutError, HTTPError):
        storage.setSandboxData('last_exit_clean', False)
    finally:
        if not is_full_parse:
            finished = 1
            storage.setSandboxData('page', 1)
            storage.setSandboxData('partly_parsed', datetime.now(timezone.utc).isoformat(timespec='seconds'))

        storage.save()

# Set tags
tagger = SpotifyTagger(client_id=SPOTIFY.CLIENT_ID, client_secret=SPOTIFY.CLIENT_SECRET)
tagger.processTracks(storage.getTracks())
storage.save()

# Create a playlist
# if storage.getSandboxData('has_new_tracks', False) or is_full_parse:
#     playlist_id = storage.getSandboxData('spotify_playlist_id')
#     tracks_sorted = sorted(storage.getTracks(), key=itemgetter('sort_string'))
#     if not playlist_id:
#         playlist_id = tagger.createPlaylist()

# Build README.md
formatter = ReadmeFormatter(storage)
formatter.render('README.md')