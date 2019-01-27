import dejavu.fingerprint as fingerprint
import dejavu.hash_reader as hreader
import numpy as np
import pyaudio
import time


class HBaseRecognizer(object):

    def __init__(self, dejavu):
        self.dejavu = dejavu
        self.Fs = fingerprint.DEFAULT_FS

    def _recognize(self, hashes):
        matches = []
        matches = self.dejavu.find_matches_hashes(hashes)
        return self.dejavu.align_matches(matches)

    def recognize(self):
        pass  # base class does nothing


class HFileRecognizer(HBaseRecognizer):
    def __init__(self, dejavu):
        super(HFileRecognizer, self).__init__(dejavu)

    def recognize_file(self, filename):
        hashes =  hreader.read(filename)

        t = time.time()
        match = self._recognize(hashes)
        t = time.time() - t

        if match:
            match['match_time'] = t

        return match

    def recognize(self, filename):
        return self.recognize_file(filename)

class NoRecordingError(Exception):
    pass
