"""Definitions related to a single note in a MOD file."""


# Note that the octave numbers we use here reflect conventional music octave
# numbers (in which middle C is "C4"), as opposed to MOD convention (in which
# middle C is "C3").
#
# TODO: Analyze the entire pattern to guess the key and use that to select
#       between sharps and flats for display.
PERIOD_TABLE = {
    1712: "C 1", 1616: "C#1", 1525: "D 1", 1440: "D#1", 1357: "E 1", 1281: "F 1",
    1209: "F#1", 1141: "G 1", 1077: "G#1", 1017: "A 1",  961: "A#1",  907: "B 1",
     856: "C 2",  808: "C#2",  762: "D 2",  720: "D#2",  678: "E 2",  640: "F 2",
     604: "F#2",  570: "G 2",  538: "G#2",  508: "A 2",  480: "A#2",  453: "B 2",
     428: "C 3",  404: "C#3",  381: "D 3",  360: "D#3",  339: "E 3",  320: "F 3",
     302: "F#3",  285: "G 3",  269: "G#3",  254: "A 3",  240: "A#3",  226: "B 3",
     214: "C 4",  202: "C#4",  190: "D 4",  180: "D#4",  170: "E 4",  160: "F 4",
     151: "F#4",  143: "G 4",  135: "G#4",  127: "A 4",  120: "A#4",  113: "B 4",
     107: "C 5",  101: "C#5",   95: "D 5",   90: "D#5",   85: "E 5",   80: "F 5",
      76: "F#5",   71: "G 5",   67: "G#5",   64: "A 5",   60: "A#5",   57: "B 5",
}


class Note:
    """Represents a single note played in some channel."""

    def __init__(self, sample, period, effect):
        """Initializes a new Note."""
        self.sample = sample
        self.period = period
        self.effect = effect

    def __str__(self):
        """Creates a human-readable representation of the note."""
        return '{:2s} [{:3s}] {{{:3X}}}'.format(
            str(self.sample) if self.sample else '..',
            PERIOD_TABLE.get(self.period, str(self.period)) if self.period else '...',
            self.effect)
