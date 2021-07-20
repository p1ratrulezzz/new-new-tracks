from abc import ABC, abstractmethod
import json
import zlib
from datetime import datetime, timezone

class Storage(ABC):
    _tracks = {}
    _options = {}
    def __init__(self, **kwargs):
        for k in kwargs.keys():
            self._options[k] = kwargs[k]

    @abstractmethod
    def readTracks(self):
        pass

    def getTracks(self):
        return self._tracks

    def mergeTrack(self, newinfo, trackInfo):
        return {**newinfo, **trackInfo}

    def mergeTracks(self, newtracks):
        for trackInfo in newtracks:
            hash = self.hashTrack(trackInfo)
            newinfo = {}
            if self._tracks.get(hash):
                newinfo = self._tracks[hash]
            else:
                newinfo['added'] = datetime.now(timezone.utc).isoformat(timespec='seconds')

            newinfo = self.mergeTrack(newinfo, trackInfo)

            self._tracks[hash] = newinfo

    @abstractmethod
    def save(self):
        pass

    def hashTrack(self, trackInfo:dict):
        data = []
        if trackInfo.get("artist"):
            data.append(trackInfo['artist'].lower())
        data.append(trackInfo["title"].lower())

        hash = zlib.adler32(json.dumps(data).encode('utf8'))
        return hex(hash).lstrip("0x").rstrip("L")