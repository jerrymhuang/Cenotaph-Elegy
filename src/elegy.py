import os
import random
import numpy as np

from cenotaph import generate
from matplotlib import pyplot as pplot
from scipy.io.wavfile import read, write
from scipy import signal


chunk_size = 8


def load_all_audio(folder_path):
    all_fs = []
    all_audio = []

    file_names = os.listdir(folder_path)
    for item in file_names:
        fs, audio = read(folder_path + item)
        all_fs.append(fs)
        all_audio.append(audio)

    return file_names, all_fs, all_audio


def get_audio_patterns(fs=48000, duration=1):
    visual_pattern = 1 - generate()
    print(visual_pattern[:,0:8])
    chunk_count         = int(visual_pattern.shape[1] / chunk_size)
    audio_pattern_size  = visual_pattern.shape[0] * chunk_size
    audio_pattern_seeds = np.zeros(
        (audio_pattern_size, chunk_count), 
        dtype=np.float32
        )
    audio_chunk_size    = int(fs / audio_pattern_size)
    print(audio_chunk_size)

    for i in range(0, chunk_count):
        audio_pattern_seeds[:,i] = np.reshape(
            visual_pattern[:,i*chunk_size:(i+1)*chunk_size],
            (chunk_size * chunk_size,)
        )        

    audio_patterns = np.zeros((fs*duration, chunk_count), dtype=np.float32)
    for i in range(0, chunk_count):
        for j in range(0, audio_pattern_size):
            tick = j*audio_chunk_size + random.randint(0, audio_chunk_size-1)
            audio_patterns[tick, i] = audio_pattern_seeds[j, i]

    return audio_patterns


def get_audio_segment(samples, pattern):
    max_sample_count = len(samples)
    
    segment = np.zeros(
        (pattern.shape[0] + max_sample_count, ), 
        dtype=np.float32
        )
    
    for i in range(0, len(pattern)):
        if pattern[i] == 1:
            segment[i:i+len(samples)] += samples[:,0]

    return segment


def save_all_audio(segments, fs, dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    for i in range(len(segments)):
        write("ch_{}.wav".format(i), fs, segments[i])


def main():
    file_names, all_fs, all_audio = load_all_audio("./Assets/Audio/Input/")
    print(file_names)
    print(all_fs)

    patterns = get_audio_patterns()

    # segment = get_audio_segment(all_audio[12], patterns[:,0])
    # segment = segment / max(segment)
    # write("test.wav", all_fs[0], segment)
    # pplot.figure
    # pplot.plot(segment)
    # pplot.show()


if __name__ == "__main__":
    main()