import random
import numpy as np

from scipy import signal
from scipy.io import wavfile as wav
from matplotlib import pyplot as pp


fs = 48000
channel_count = 128
cell_count = 64
duration = 1


def Synthesize(onset_prob=0.4):
    output = np.zeros((fs * duration), dtype=int)
    block_size = int(fs / cell_count)
    for i in range(0, cell_count * duration):
        onset = int(random.random() * block_size)
        output[i * block_size + onset] = 1 if (random.random() < onset_prob) else 0

    return output


# =============================================================================
# Test function for sound
# =============================================================================

def main():
    rate, sample = wav.read("breathing00.wav")
    signal.resample(sample, 48000)
    sample = np.interp(sample, (sample.min(), sample.max()), (-1, 1))
    print(rate)

    pattern = Synthesize(onset_prob=0.75)
    wav.write("test_pattern.wav", fs, pattern.astype(np.int32))

    pp.figure
    pp.plot(pattern)
    pp.show()


if __name__ == "__main__":
    main()