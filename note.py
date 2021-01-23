
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

    _OCTAVE_NOTES = 12  # semitones in an octave

    # region reference note
    _PITCH_REFERENCE = 440  # Hz
    _NOTE_REFERENCE = 5 * 12 + 9  # Note 9 (A) in octave 5 (Midi Note Number)
    _OCTAVE_OFFSET = 1  # Offset of naming convention to numeric notation

    @classmethod
    def _freq_note_0(cls):
        rel = cls._get_relation(cls._NOTE_REFERENCE)
        freq = cls._PITCH_REFERENCE / rel
        return freq

    # endregion

    def __init__(self, freq):
        self.freq = freq  # frequency in Hz
        self.num = self._get_note(freq)  # numerical note as Midi Note Number

    def __repr__(self):
        note_error = self.num - round(self.num)
        error_cent = int(round(note_error * 100))
        err_str = ""
        if error_cent:
            err_str = " %+d cent" % error_cent
        res = (self.name
               + err_str
               + " %.3f Hz" % self.freq
        )
        return res

    # alternative constructor
    @classmethod
    def create(cls, note, octave=None):
        """create object from musical representation"""
        octave = octave or 0
        note_num = note + cls._OCTAVE_NOTES * octave
        freq = cls._get_freq(note_num)
        return cls(freq)

    # region properties

    @property
    def octave(self) -> float:
        """returns octave in numerical form"""
        return self.num / 12

    @property
    def name(self):
        """return name of note"""
        octave, note = divmod(self.num, self._OCTAVE_NOTES)
        octave -= self._OCTAVE_OFFSET
        note_enum = NoteName(round(note))
        note_str = str(note_enum).split('.')[-1]  # remove 'NoteName'
        note_name = note_str + str(int(octave))
        return note_name

    # endregion

    # region internal calculations
    @classmethod
    def _get_note(cls, frequency):
        # get numerical note from frequency
        freq_base = cls._freq_note_0()
        rel = frequency / freq_base
        note_interval = cls._get_interval(rel)
        return note_interval

    @classmethod
    def _get_freq(cls, note):
        # get frequency from numerical note
        rel = cls._get_relation(note)
        root = cls._freq_note_0()
        freq = root * rel
        return freq


    @staticmethod
    def _get_interval(relation):
        rel_log = np.log2(relation)
        interval = rel_log * 12
        return interval

    @staticmethod
    def _get_relation(interval):
        octaves = interval / 12
        rel = 2**octaves
        return rel

    # endregion


if __name__ == "__main__":
    pass
