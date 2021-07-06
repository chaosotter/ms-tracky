"""Ms. Tracky is a MOD player for Python.  It's not even close to done."""

import mod
import pyaudio


def main():
    m = mod.Mod('ELYSIUM.MOD')
    m.print_summary()

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)

    for samp in m.samples:
        print('Sample: {}'.format(samp))

        notes = [214, 170, 143]  # C4, E4, G4
        for n in notes:
            samps = samp.play(n, 0.5)
            data = bytearray()
            for s in samps:
                data.append(s & 0xff)
                data.append((s & 0xff00) >> 8)
            stream.write(bytes(data))

        s1 = samp.play(214, 0.5)
        s2 = samp.play(170, 0.5)
        s3 = samp.play(143, 0.5)
        data = bytearray()
        for i in range(len(s1)):
            s = int((s1[i] + s2[i] + s3[i]) / 3)
            data.append(s & 0xff)
            data.append((s & 0xff00) >> 8)
        stream.write(bytes(data))

    stream.stop_stream()
    stream.close()

    p.terminate()


if __name__ == '__main__':
    main()
