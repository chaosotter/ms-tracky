import note
import pattern
import row
import sample


class Mod:
    """Class for working with a Soundtracker ("MOD") file."""

    def __init__(self, path):
        """Reads in the MOD file at the given location.

        Args:
            path (str): Path to the file.
        Raises:
            IOError: If the file cannot be read.
            IndexError: If the file is internally inconsitent or truncated.
        """
        self.path = path
        with open(path, 'rb') as file:
            self.data = file.read()

        self.offset = 0
        self.name = self._consume_string(20)

        self.samples = []
        for i in range(self.sample_count()):
            self.samples.append(self._consume_sample_header())

        self.position_count = self._consume_byte()
        self.restart_position = self._consume_byte()

        self.positions = []
        for i in range(128):
            pat = self._consume_byte()
            if i < self.position_count:
                self.positions.append(pat)

        self.tag = self._consume_string(4)

        self.pattern_count = max(self.positions) + 1
        self.patterns = []
        for i in range(self.pattern_count):
            self.patterns.append(self._consume_pattern())

    def _consume_byte(self):
        """Consumes a single byte."""
        code = self.data[self.offset]
        self.offset += 1
        return code

    def _consume_finetune(self):
        code = self._consume_byte()
        if code & 0x08:  # sign bit
            return -((~code & 0x07) + 1)
        else:
            return code & 0x07

    def _consume_note(self):
        data = self.data[self.offset:self.offset+4]
        sample = (data[0] & 0xf0) | ((data[2] & 0xf0) >> 4)
        period = ((data[0] & 0x0f) << 8) | data[1]
        effect = ((data[2] & 0x0f) << 8) | data[3]
        self.offset += 4
        return note.Note(sample, period, effect)

    def _consume_pattern(self):
        rows = []
        for i in range(64):
            rows.append(self._consume_row())
        return pattern.Pattern(rows)

    def _consume_row(self):
        notes = []
        for i in range(4):  # assume 4 channels
            notes.append(self._consume_note())
        return row.Row(notes)

    def _consume_sample_header(self):
        name = self._consume_string(22)
        length = self._consume_word() * 2  # words -> bytes
        finetune = self._consume_finetune()
        volume = self._consume_byte()
        repeat_offset = self._consume_word() * 2  # words -> bytes
        repeat_length = self._consume_word() * 2  # words -> bytes
        return sample.Sample(name, length, finetune, volume, repeat_offset, repeat_length)

    def _consume_string(self, count):
        """Consumes a NUL-terminated string field of |count| bytes."""
        ret = ''
        for i in range(count):
            code = self._consume_byte()
            if code:
                ret += chr(code)
        return ret

    def _consume_word(self):
        """Consumes a single 2-byte word, MSB first."""
        ret = self.data[self.offset] * 256 + self.data[self.offset + 1]
        self.offset += 2
        return ret

    def print_summary(self):
        """Prints out a basic summary of the file."""
        print('File: {} ({} bytes total)'.format(self.path, self.size))
        print('Name: "{}"'.format(self.name))
        print('Tag:  "{}"'.format(self.tag))

        print('\nSamples:')
        for i in range(len(self.samples)):
            print('  {:02d}: {}'.format(i+1, self.samples[i]))

        print('\nPositions:')
        for i in range(len(self.positions)):
            if i % 8 == 0:
                if i:
                    print()
                print('  ', end='')
            print('{:3d}'.format(self.positions[i]), end='')
        print()

        for i in range(len(self.patterns)):
            print('\nPATTERN {}'.format(i))
            print(self.patterns[i])

    def sample_count(self):
        """Determines if this is a 15-sample or 31-sample MOD file."""
        if self.data[1080:1084] in {b'M.K.', b'M!K!', b'4CHN', b'6CHN', b'8CHN', b'FLT4', b'FLT8'}:
            return 31
        else:
            return 15

    @property
    def size(self):
        """Returns the size of the MOD file in bytes."""
        return len(self.data)
