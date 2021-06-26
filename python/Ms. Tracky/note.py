"""Definitions related to a single note in a MOD file."""


PERIOD_TABLE = {
    1712: "C 2", 1616: "C#2", 1525: "D 2", 1440: "D#2", 1357: "E 2", 1281: "F 2",
    1209: "F#2",
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
        return '{} [Period {}, Effect {}]'.format(self.sample, self.period, self.effect)
