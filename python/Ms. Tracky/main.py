"""Ms. Tracky is a MOD player for Python.  It's not even close to done."""

import mod
import pyaudio


def main():
    m = mod.Mod('ELYSIUM.MOD')
    m.print_summary()

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt8, channels=1, rate=44100, output=True)

    samp = m.samples[0]
    print('Sample: {}'.format(samp))
    stream.write(samp.data)

    notes = [214, 170, 143]  # C4, E4, G4
    for n in notes:
        scale = 44100.0 / 8287.14  # extend samples this many units for middle C
        extend = scale * (n / 214.0)  # extend samples this many units for this note
        print(scale, extend)

        data = bytearray()
        rem = 0.0
        for s in samp.data:
            rem += extend
            while rem > 1:
                data.append(s)
                rem -= 1

        for x in range(10):
            stream.write(bytes(data))

    stream.stop_stream()
    stream.close()

    p.terminate()


if __name__ == '__main__':
    main()