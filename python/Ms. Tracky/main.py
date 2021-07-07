"""Ms. Tracky is a MOD player for Python.  It's not even close to done."""

import mod
import pyaudio


def main():
    m = mod.Mod('ELYSIUM.MOD')
    m.print_summary()

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=2, rate=44100, output=True)

    for samp in m.samples:
        print('Sample: {}'.format(samp))
        continue

        notes = [214, 170, 143]  # C4, E4, G4
        for n in notes:
            samps = samp.play(n, 0.5)
            data = bytearray()
            for s in samps:
                for chan in range(2):
                    data.append(s & 0xff)
                    data.append((s & 0xff00) >> 8)
            stream.write(bytes(data))

        s1 = samp.play(214, 0.5)
        s2 = samp.play(170, 0.5)
        s3 = samp.play(143, 0.5)
        data = bytearray()
        for i in range(len(s1)):
            s = int((s1[i] + s2[i] + s3[i]) / 3)
            for chan in range(2):
                data.append(s & 0xff)
                data.append((s & 0xff00) >> 8)
        stream.write(bytes(data))

    pat = m.patterns[9]
    last_samp = [0, 0, 0, 0]
    last_period = [0, 0, 0, 0]
    for rnum, row in enumerate(pat.rows):
        print('{:02d} > {}'.format(rnum, row))
        notes = []
        for nnum, note in enumerate(row.notes):
            snum = note.sample if note.sample else last_samp[nnum]
            period = note.period if note.period else last_period[nnum]
            last_samp[nnum] = snum
            last_period[nnum] = period
            notes.append(m.samples[snum].play(period, 0.5))
        data = bytearray()
        for i in range(len(notes[0])):
            left = int((notes[0][i] + notes[3][i]) / 2)
            right = int((notes[1][i] + notes[2][i]) / 2)
            data.append(left & 0xff)
            data.append((left & 0xff00) >> 8)
            data.append(right & 0xff)
            data.append((right & 0xff00) >> 8)
        stream.write(bytes(data))

    stream.stop_stream()
    stream.close()

    p.terminate()


if __name__ == '__main__':
    main()
