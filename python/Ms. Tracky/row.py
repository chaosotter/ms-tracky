"""Definitions related to a single row in a pattern in a MOD file."""


class Row:
    """Represents a row in a pattern, which contains one note for each channel."""

    def __init__(self, notes):
        """Initializes a new Row."""
        self.notes = notes

    def __str__(self):
        """Creates a human-readable representation of the row."""
        return '  |  '.join([str(x) for x in self.notes])
