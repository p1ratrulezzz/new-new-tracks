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

        self.readTracks()

        self._last_exit_clean : bool = self.getSandboxData('last_exit_clean', True)
        if self._last_exit_clean:
            self.setSandboxData('counter', 1)

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

    def mergeTrack(self, newinfo, trackInfo):
        counter = self.getSandboxData('counter', 1)
        sort_string = counter
        date_info = newinfo['date'] if newinfo.get('date') else None
        date_info = trackInfo['date'] if not date_info and trackInfo.get('date') else date_info
        if date_info:
            sort_string = str(date_info['year']) + str(date_info['month']).rjust(2, '0') + '_' + str(counter)
        newinfo['counter'] = counter
        newinfo['sort_string'] = sort_string
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

