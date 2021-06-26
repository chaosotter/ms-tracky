"""Definitions related to a sample stored in a MOD file."""


class Sample:
    """Encapsulates an individual sample from a MOD file."""

    def __init__(self, name, length, finetune, volume, repeat_offset, repeat_length):
        """Initializes a new sample.

        Note that the actual sample data are stored later, using store_samples().
        """
        self.name = name
        self.length = length
        self.finetune = finetune
        self.volume = volume
        self.repeat_offset = repeat_offset
        self.repeat_length = repeat_length

    def __str__(self):
        """Provides a human-readable one-line summary."""
        return '"{}" [{} bytes, volume {}, finetune {}, repeat({}, {})]'.format(
            self.name, self.length, self.volume, self.finetune, self.repeat_offset, self.repeat_length)
