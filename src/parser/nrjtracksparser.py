from src.parser.parser import Parser
from bs4 import BeautifulSoup, element, ResultSet
import urllib3

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

        divEls: ResultSet = bs.select('.list.pr .new-track-next-name')
        divEl: element.Tag
        for divEl in divEls:
            track_data = {}
            track_data['href'] = self._baseurl + '/' + divEl.parent['href'].lstrip('/')
            track_label = divEl.get_text(separator = '\n', strip=True)
            labels = track_label.split('\n')
            track_data['artist'] = self.clearTrackName(labels[0])
            track_data['title'] = self.clearTrackName(labels[-1])
            images = divEl.find_previous_siblings('img')
            if len(images) > 0:
                track_data['image'] = images[0]['src']

            tracks.append(track_data)

        return tracks
