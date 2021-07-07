"""Definitions related to a sample stored in a MOD file."""


class Sample:
    """Encapsulates an individual sample from a MOD file."""

    SCALE = 44100.0 / (2 * 8287.14)  # extend samples this many units for middle C

    def __init__(self, name, length, finetune, volume, repeat_offset, repeat_length):
        """Initializes a new sample.

        Note that the actual sample data are stored later, using store_samples().
        """
        self.name = name
        self.length = length
        self.finetune = finetune
        self.volume = volume
        self.repeat_offset = repeat_offset * 2  # because of upsampling
        self.repeat_length = repeat_length * 2  # because of upsampling
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

    def play(self, period=214, duration=1, volume=None):
        """Play the sample with the given period, duration, and volume.

        Args:
          period (int): Expressed using the "period" values stored in the MOD
              file format, where 214 is middle C, 170 is E above middle C, etc.
          duration (float): The number of seconds to play the sample.
          volume (int): Expressed using the range [0, 64], with 64 being the
              loudest.  If None, then use the "native" volume of the sample.

        If the sample isn't long enough to last for the full duration, we try
        to apply the repetition settings.  Otherwise, the end of the return
        array is zero-padded to provide the expected number of sample values.

        We assume a 44100-Hz output channel.
        """
        # number of output samples per internal sample
        extend = self.SCALE * (period / 214.0)
        volume = (volume if volume else self.volume) / 64

        data = []
        count = int(44100 * duration)
        offset = 0
        repeating = False
        empty = len(self.data) == 0

        hold = extend
        while count:
            # Move to the next sample if it's time.
            if hold < 1:
                hold += extend
                offset += 1
                if repeating:
                    if offset > (self.repeat_offset + self.repeat_length):
                        offset = self.repeat_offset
                elif offset >= len(self.data):
                    if self.repeat_length > 4:  # *2 for words->bytes, *2 for upsampling
                        repeating = True
                        offset = self.repeat_offset
                    else:
                        empty = True

            if empty:
                data.append(0)
            else:
                data.append(self.data[offset] * volume)

            hold -= 1
            count -= 1

        return data

    def __str__(self):
        """Provides a human-readable one-line summary."""
        print("len = {}, repeat = {}, rlen = {}".format(len(self.data), self.repeat_offset, self.repeat_length))
        return '"{}" [{} bytes, volume {}, finetune {}, repeat({}, {})]'.format(
            self.name, self.length, self.volume, self.finetune, self.repeat_offset, self.repeat_length)
