import librosa


class NoteDetector:
    @staticmethod
    def get_onset(song):
        # TODO: Change return to a numpy array instead of a regular list
        """ Takes a list of waveforms, or a single wave, as numpy arrays and returns the onsets for each waveform
        and returns them in a list"""
        if not isinstance(song, list):
            song = [song]
        if len(song) == 1:
            return [song[0]+1]
        return [librosa.onset.onset_detect(song[0])] + self.get_onset(song[1:])

    @staticmethod
    def segment_notes():
        pass


