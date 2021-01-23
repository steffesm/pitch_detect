
from enum import IntEnum, unique
from collections import namedtuple

import numpy as np
from matplotlib import pyplot as plt

from wave_unify import WaveUnifyData


# region enums

@unique
class NoteName(IntEnum):
    C = 0
    Db = 1
    D = 2
    Eb = 3
    E = 4
    F = 5
    Gb = 6
    G = 7
    Ab = 8
    A = 9
    Bb = 10
    B = 11


@unique
class Interval(IntEnum):
    UNISON = 0
    MINOR_SECOND = 1
    MAJOR_SECOND = 2
    MINOR_THIRD = 3
    MAJOR_THIRD = 4
    FOURTH = 5
    TRITONE = 6
    FIFTH = 7
    MINOR_SIXTH = 8
    MAJOR_SIXTH = 9
    MINOR_SEVENTH = 10
    MAJOR_SEVENTH = 11
    OCTAVE = 12

# endregion


class Note:
    """musical representation of frequency"""

    # region reference note
    _PITCH_REFERENCE = 440  # Hz
    _NOTE_REFERENCE = 4 * 12 + 9  # Note 9 (A) in octave 4

    def __init__(self, freq):
        self.freq = freq


    def __repr__(self):
        octave, note = np.divmod(self.note, 12)  # integer octave and note
        note_int, error = np.divmod(note, 1)  # integer note-name and error
        add = error > 0.5
        note_int = note_int + 1 * add
        error = error - 1 * add

        note_name = NoteName(note_int)
        note_str = str(note_name).split('.')[-1]  # remove 'NoteName'

        error_cent = int(round(error * 100))
        err_str = ""
        if error_cent:
            err_str = " %+d cent" % error_cent
        res = (note_str
               + str(int(octave))
               + err_str
               + " %f3 Hz" % self.freq
        )
        return res

    @classmethod
    def _freq_note_0(cls):
        rel = cls._get_relation(cls._NOTE_REFERENCE)
        freq = cls._PITCH_REFERENCE / rel
        return freq

    # endregion

    # alternative constructor
    @classmethod
    def create(cls, note, octave=None):
        """create object from musical representation"""
        octave = 0 if octave is None else octave
        octave = 0 if note > 12 else octave
        note += 12 * octave  # apply octave
        rel = cls._get_relation(note)
        freq = cls._freq_note_0() / rel
        return cls()

    # region properties

    @property
    def note(self):
        """returns note in numerical form"""
        freq_base = self._freq_note_0()
        rel = self.freq / freq_base
        note = self._get_interval(rel)
        return note + 12  # include octave -1 in positive range

    @property
    def name(self):
        """return name of note"""
        octave, note = divmod(self.note, 12)
        name = NoteName(note)
        return name


    # endregion

    # region internal calculations

    @staticmethod
    def _get_interval(relation):
        rel_log = np.log2(relation)
        interval = rel_log * 12
        return interval

    @staticmethod
    def _get_relation(interval):
        octaves = interval / 12
        rel = 2 ** octaves
        return rel

    # endregion

    # @property
    # def error


    # def _get_note_num(self, freq_sig):
    #     rel = freq_sig / self.freq_note_0
    #     note = self._get_freq_interval(rel)
    #     return note

    # def get_note_error(self, freq_sig):
    #     """return note for a frequency and difference in cent"""
    #     note_float = self._get_note_num(freq_sig)
    #     note_int = round(note_float)
    #     note_name = self.Note(note_int)
    #     note_err_log = note_float - note_int
    #     note_err_cent = note_err_log * 12
    #
    #     # octaves = int(rel_log)
    #     # return note_name, error
    #
    # def _get_freq_interval(self, freq_note, freq_root):
    #     rel = freq_note / freq_root
    #     rel_log = np.log2(rel)
    #     interval = rel_log * 12 + 1
    #     return interval
    #
    # def _get_interval_relation(self, interval):
    #     octaves = interval / 12
    #     rel = 2**octaves
    #     return rel


if __name__ == "__main__":
    print(Note(440))
    print(Note(8.175799 + 0.01))
    print(Note(200))
    print(Note(27.2))

    # freqs = np.array((
    #     440,
    #     8.175799 + 0.01,
    #     200,
    #     27.2,
    # ))
    # print(Note(freqs))
