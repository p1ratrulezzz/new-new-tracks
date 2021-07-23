from mako.template import Template
from src.formatter.readmeformatter import ReadmeFormatter
import calendar
import base64
import hashlib
from datetime import datetime
import secrets
from operator import itemgetter

class HtmlFormatter(ReadmeFormatter):
    def _embedSpotify(self, trackInfo):
        if not hasattr(self, '_spotifyEmbedTpl'):
            self._spotifyEmbedTpl = Template(filename='docs/templates/spotify_embed.html.tpl', input_encoding='utf-8')

        track = {}
        track['id'] = trackInfo['spotify']['track'][len('spotify:track:'):]
        html = self._spotifyEmbedTpl.render(track = track)

        return base64.b64encode(html.encode('ascii')).decode()


    def render(self, filepath:str):
        tpl = Template(filename="docs/templates/index.html.tpl", input_encoding='utf-8')
        tracks = {}
        i = 0
        for trackInfo in self._storage.getTracks().values():
            # if i > 30:
            #     break

            i += 1
            trackInfo['date_formatted'] = None
            trackInfo['spotify_track'] = None

            if trackInfo.get('spotify') and trackInfo['spotify'].get('track'):
                trackInfo['spotify_track'] = self._embedSpotify(trackInfo)

            year = 'unknown'
            if trackInfo.get('date'):
                year = str(trackInfo['date']['year'])
                month_name = (', ' + calendar.month_name[trackInfo['date']['month']]) if isinstance(trackInfo['date']['month'], int) else ''
                trackInfo['date_formatted'] = year + month_name

            if not tracks.get(year):
                tracks[year] = {
                    'tracks': [],
                    'year': year,
                    'sort_weight': str(10000) if year == 'unknown' else year
                }

            tracks[year]['tracks'].append(trackInfo)

        buildhash = hashlib.pbkdf2_hmac('sha256', bytes(datetime.now().timestamp().hex(), 'ascii'), secrets.token_bytes(64), 1).hex()
        html = tpl.render(tracks=sorted(tracks.values(), key=itemgetter('sort_weight'), reverse=True), page={'title': 'NRJ Tracks'}, buildhash = buildhash)

        with open(filepath, "w") as output:
            output.write(html)
            output.close()