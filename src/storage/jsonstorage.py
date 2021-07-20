from src.storage.storage import Storage
import os
import json
from datetime import datetime, timezone

class JsonStorage(Storage):
    _sandbox : dict = {}
    _last_exit_clean = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "filename" not in self._options:
            raise RuntimeError("Filename option must be set")

        self._last_exit_clean : bool = self.getSandboxData('last_exit_clean', True)
        self.setSandboxData('counter', 1)
        self.readTracks()

    def _getFilename(self):
        return self._options['filename']

    def readTracks(self):
        if os.path.exists(self._getFilename()):
            with open(self._getFilename(), 'r') as fp:
                data = json.load(fp)
                if data.get('tracks'):
                    self._tracks = data['tracks']
                if data.get('sandbox'):
                    self._sandbox = data['sandbox']

                fp.close()

    def delSandboxData(self, prop:str):
        self.setSandboxData(prop, None)

    def setSandboxData(self, prop:str, value):
        if value is None:
            self._sandbox.pop(prop)
        else:
            self._sandbox[prop] = value

    def getSandboxData(self, prop:str, default = None):
        return self._sandbox.get(prop) or default

    def mergeTrack(self, newinfo, trackInfo):
        counter = self.getSandboxData('counter', 1)
        newinfo['counter'] = counter
        counter += 1
        self.setSandboxData('counter', counter)
        return super(JsonStorage, self).mergeTrack(newinfo, trackInfo)

    def save(self):
        json_data = {
            'updated': datetime.now(timezone.utc).isoformat(timespec='seconds'),
            'tracks': self._tracks,
            'sandbox': self._sandbox
        }

        with open(self._getFilename(), 'w') as fp:
            fp.write(json.dumps(json_data, indent=True))
            fp.close()

