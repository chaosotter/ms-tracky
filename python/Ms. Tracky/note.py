"""Definitions related to a single note in a MOD file."""


# Note that the octave numbers we use here reflect conventional music octave
# numbers (in which middle C is "C4"), as opposed to MOD convention (in which
# middle C is "C2").
PERIOD_TABLE = {
    1712: "C 2", 1616: "C#2", 1525: "D 2", 1440: "D#2", 1357: "E 2", 1281: "F 2",
    1209: "F#2", 1141: "G 2", 1077: "G#2", 1017: "A 2",  961: "A#2",  907: "B 2",
     856: "C 3",  808: "C#3",  762: "D 3",  720: "D#3",  678: "E 3",  640: "F 3",
     604: "F#3",  570: "G 3",  538: "G#3",  508: "A 3",  480: "A#3",  453: "B 3",
     428: "C 4",  404: "C#4",  381: "D 4",  360: "D#4",  339: "E 4",  320: "F 4",
     302: "F#4",  285: "G 4",  269: "G#4",  254: "A 4",  240: "A#4",  226: "B 4",
     214: "C 5",  202: "C#5",  190: "D 5",  180: "D#5",  170: "E 5",  160: "F 5",
     151: "F#5",  143: "G 5",  135: "G#5",  127: "A 5",  120: "A#5",  113: "B 5",
     107: "C 6",  101: "C#6",   95: "D 6",   90: "D#6",   85: "E 6",   80: "F 6",
      76: "F#6",   71: "G 6",   67: "G#6",   64: "A 6",   60: "A#6",   57: "B 6",
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
            str(self.sample) if self.sample else '**',
            PERIOD_TABLE.get(self.period, str(self.period)) if self.period else '***',
            self.effect)
