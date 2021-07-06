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
        self.data = None

    def store(self, data):
        """Stores the actual sample data for later use.

        The input data are signed 8-bit values.  We upscale to 16 bits and
        double the number of samples through simple linear interpolation.

        For convenience in mixing, the upconverted sample is stored as an
        array of ints rather than a bytearray.
        """
        self.data = []
        for i in range(len(data) - 1):
            a = 256 * (data[i] if data[i] < 128 else data[i] - 256)
            b = 256 * (data[i+1] if data[i+1] < 128 else data[i+1] - 256)
            self.data.append(a)
            self.data.append((a + b) // 2)

        if len(data):
            last = 256 * data[-1] if data[-1] < 128 else data[-1] - 256
            self.data.append(last)
            self.data.append(last)

    def __str__(self):
        """Provides a human-readable one-line summary."""
        return '"{}" [{} bytes, volume {}, finetune {}, repeat({}, {})]'.format(
            self.name, self.length, self.volume, self.finetune, self.repeat_offset, self.repeat_length)
