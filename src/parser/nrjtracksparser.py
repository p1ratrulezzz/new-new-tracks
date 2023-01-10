from src.parser.parser import Parser
from bs4 import BeautifulSoup, element, ResultSet, Tag
import urllib3
import re

class NRJTracksParser(Parser):
    def __init__(self, url):
        self._url = url
        self._http = urllib3.PoolManager(
            retries = False
        )

        parsed_url = urllib3.util.parse_url(self._url)
        self._baseurl = parsed_url.scheme + '://' + parsed_url.hostname

    """:rtype list"""
    def parseTracks(self):
        tracks = []
        r: urllib3.response.HTTPResponse = self._http.request('GET', self._url)

        # Error on server side. Can't get data.
        if r.status != 200:
            raise urllib3.exceptions.HTTPError()

        # No more data
        if (len(r.data) == 0):
            return tracks

        bs = BeautifulSoup(r.data, 'html.parser')

        divEls: ResultSet = bs.select('.track-list__item>.track')
        divEl: element.Tag
        re_compiled = re.compile('\/files\/([0-9]{4})([0-9]{2})\/', flags=re.IGNORECASE)
        for divEl in divEls:
            trackEl = divEl.select('.track__inner>.track__title>a')[0]
            artistEl = divEl.select('.track__artist>a.track__link')[0]
            track_data = {}
            track_data['href'] = self._baseurl + '/' + trackEl['href'].lstrip('/')
            track_data['href_artist'] = self._baseurl + '/' + artistEl['href'].lstrip('/')
            track_data['artist'] = self.clearTrackName(artistEl.get_text(strip=True))
            track_data['title'] = self.clearTrackName(trackEl.get_text(strip=True))
            images = divEl.find_all('img')
            if len(images) > 0:
                img: Tag = images[0]
                if img.has_attr('src'):
                    imgsrc = img['src']
                elif img.has_attr('data-src'):
                    imgsrc = img['data-src']

                if imgsrc is None:
                    continue

                track_data['image'] = imgsrc
                matches = re_compiled.findall(imgsrc)
                if len(matches) > 0:
                    track_data['date'] = {
                        'year': int(matches[0][0]),
                        'month': int(matches[0][1])
                    }

            tracks.append(track_data)

        return tracks
