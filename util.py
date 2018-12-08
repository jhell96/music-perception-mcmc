import sys
import numpy as np
import wave
import pyaudio
import os
import os.path


class Distribution(dict):
    def __missing__(self, key):
        # if missing, return 0
        return 0

    def renormalize(self):
        normalization_constant = sum(self.values())
        assert normalization_constant > 0, "Sum of probabilities is 0"
        for key in self.keys():
            self[key] /= normalization_constant


def load_wav(filepath, t_start=0, t_end=sys.maxsize, only_22k=True):
    """Load a wave file, which must be 22050Hz and 16bit and must be either
    mono or stereo.
    Inputs:
        filepath: audio file
        t_start, t_end:  (optional) subrange of file to load (in seconds)
        only_22k: if True (default), assert if sample rate is different from 22050.
    Returns:
        a numpy floating-point array with a range of [-1, 1]
    """

    wf = wave.open(filepath)
    num_channels, sampwidth, fs, end, comptype, compname = wf.getparams()

    # for now, we will only accept 16 bit files at 22k
    assert(sampwidth == 2)
    # assert(fs == 22050)

    # start frame, end frame, and duration in frames
    f_start = int(t_start * fs) 
    f_end = min(int(t_end * fs), end)
    frames = f_end - f_start

    wf.setpos(f_start)
    raw_bytes = wf.readframes(frames)

    # convert raw data to numpy array, assuming int16 arrangement
    samples = np.fromstring(raw_bytes, dtype = np.int16)

    # convert from integer type to floating point, and scale to [-1, 1]
    samples = samples.astype(np.float)
    samples *= (1 / 32768.0)

    if num_channels == 1:
        return samples

    elif num_channels == 2:
        return 0.5 * (samples[0::2] + samples[1::2])

    else:
        raise('Can only handle mono or stereo wave files')


def play_wav(filepath):
    # define stream chunk
    chunk = 1024

    # open a wav format music
    f = wave.open(filepath, "rb")
    # instantiate PyAudio
    p = pyaudio.PyAudio()
    # open stream
    stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                    channels=f.getnchannels(),
                    rate=f.getframerate(),
                    output=True)
    # read data
    data = f.readframes(chunk)

    # play stream
    while data:
        stream.write(data)
        data = f.readframes(chunk)

    # stop stream
    stream.stop_stream()
    stream.close()

    # close PyAudio
    p.terminate()


def get_directory_files(dirpath, file_ext=None):
    '''Return all files in a directory
    Inputs:
        dirpath: directory name
        file_ext: (optional) only return files ending with that extension.
    '''
    files = sorted(os.listdir(dirpath))
    return [os.path.join(dirpath, f) for f in files if file_ext == None or f.endswith(file_ext)]


if __name__ == '__main__':
    # path = "/home/josh/Music/cant_sleep_love_pentatonix.wav"
    path = "/home/josh/Documents/school/senior/6.804/project/music-perception-mcmc/resources/keys_wav/60.wav"
    play_wav(path)
    