from abc import ABC, abstractmethod
import json
import zlib
from datetime import datetime, timezone

class Storage(ABC):
    _tracks = {}
    _options = {}
    _sandbox = {}

    def __init__(self, **kwargs):
        for k in kwargs.keys():
            self._options[k] = kwargs[k]

        self.delSandboxData('has_new_tracks')

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
                self.setSandboxData('has_new_tracks', True)
                newinfo['added'] = datetime.now(timezone.utc).isoformat(timespec='seconds')

            newinfo = self.mergeTrack(newinfo, trackInfo)

            self._tracks[hash] = newinfo

    def delSandboxData(self, prop:str):
        self.setSandboxData(prop, None)

    def setSandboxData(self, prop:str, value):
        if value is None:
            self._sandbox.pop(prop, None)
        else:
            self._sandbox[prop] = value

    def getSandboxData(self, prop:str, default = None):
        return self._sandbox.get(prop) or default

    @abstractmethod
    def save(self):
        pass

    @staticmethod
    def hashTrack(trackInfo:dict):
        data = []
        if trackInfo.get("artist"):
            data.append(trackInfo['artist'].lower())
        data.append(trackInfo["title"].lower())

        hash = zlib.adler32(json.dumps(data).encode('utf8'))
        return hex(hash).lstrip("0x").rstrip("L")