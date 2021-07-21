from abc import ABC, abstractmethod
import re

class Parser(ABC):
    @abstractmethod
    def parseTracks(self):
        pass

    @staticmethod
    def clearTrackName(trackName:str):
        trackName.strip("\r\n\t ")
        trackName = re.sub("[\u2013\u2014\u2015\u2012\u2E3B\u2E3A]+", "-", trackName, flags=re.IGNORECASE|re.UNICODE)
        trackName = re.sub("[\s\r\n\t]{2,}", " ", trackName, flags=re.IGNORECASE|re.UNICODE)
        return trackName

    @staticmethod
    def clearArtistName(artistName:str):
        artistName = Parser.clearTrackName(artistName)
        artists = []
        for artist in artistName.split('&'):
            artists.append(artist.strip('\r\n\t '))

        return ','.join(artists)

    def parseTrackName(self, trackName:str):
        info = {"title": trackName}
        dashPos = trackName.rfind("-")
        if dashPos != -1:
            info["artist_cleaned"] = self.clearArtistName(trackName[:dashPos])
            info["artist"] = trackName[:dashPos].strip('\r\n\t ')
            info["title"] = trackName[dashPos+1:].strip("\r\n\t ")
        return info