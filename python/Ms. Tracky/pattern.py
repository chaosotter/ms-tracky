"""Definitions related to a single pattern in a MOD file."""


class Pattern:
    """Represents a pattern, which consists of 64 rows."""

    def __init__(self, rows):
        """Initializes a new Pattern."""
        self.rows = rows

    def __str__(self):
        """Creates a human-readable representation of the pattern."""
        ret = []
        for i in range(len(self.rows)):
            ret.append('{:02d}: {}'.format(i, self.rows[i]))
        return '\n'.join(ret)
