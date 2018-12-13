from os import listdir
from os.path import isfile, join
from util import *
import numpy as np
import matplotlib.pyplot as plt
import fmp


class Keyboard():
    def __init__(self, num_notes=20, starting_pitch=60, audio_dirpath=None, max_sound_length_sec=4, sample_rate=22050):
        self.starting_pitch = starting_pitch
        self.num_notes = num_notes
        self.state = [0]*self.num_notes
        self.audio = dict()
        self.max_sound_length_sec = max_sound_length_sec
        self.sample_rate = sample_rate

        if audio_dirpath:
            self.load_audio_files(audio_dirpath)
        else:
            self.load_audio_files()

        self.pitch_to_chroma_energy = {}
        self.compute_chroma_energies()

    def possible_next_states(self):
        new_states = []
        for i, active in enumerate(self.state):
            possible = self.state[:]
            possible[i] = 1 if possible[i] == 0 else 0
            new_states.append(possible)
        return new_states

    def toggle_note(self, pitch):
        if self.in_key_range(pitch):
            idx = pitch - self.starting_pitch
            self.state[idx] = 1 if self.state[idx] == 0 else 0

    def in_key_range(self, pitch):
        above = (pitch >= self.starting_pitch)
        below = (pitch < self.starting_pitch + self.num_notes)
        return above and below

    def load_audio_files(self, path="piano/resources/keys_wav"):
        max_num_samples = self.max_sound_length_sec * self.sample_rate

        files = set(get_directory_files(path, file_ext="wav"))
        for pitch in range(self.starting_pitch, self.starting_pitch+self.num_notes):
            file = join(path, str(pitch)+".wav")
            if file in files:
                wav_data = load_wav(file)
                sound_start_idx = int(np.min(np.where(wav_data>0.01)[0]))
                trimmed_sound = wav_data[sound_start_idx:]
                if max_num_samples > trimmed_sound.shape[0]:
                    self.audio[pitch] = np.concatenate([trimmed_sound, np.zeros(max_num_samples - trimmed_sound.shape[0])])
                else:
                    self.audio[pitch] = trimmed_sound[:max_num_samples]

    def play_current_state(self):
        sound = self.get_state_audio()
        play_wav_data(sound)

    def play_pitch(self, pitch):
        if self.in_key_range(pitch):
            play_wav_data(self.audio[pitch])
        else:
            print("Pitch {} not in range".format(pitch))

    def get_state_audio(self, state=None):
        if state is None:
            state = self.state

        data_len = len(list(self.audio.values())[0])
        sound = np.zeros(data_len)
        for i, active in enumerate(state):
            if active:
                sound += self.audio[self.starting_pitch+i]

        return sound

    def get_state_chroma(self, state=None):
        if state is None:
            state = self.state
        sound = self.get_state_audio(state)
        return self.get_audio_chroma(sound)

    def get_state_chroma_energy_norm(self, state=None, efficient=True):
        if state is None:
            state = self.state


        # the efficient method is less "accurate" to what actually synthesizing
        # the notes would produce, but is pretty close. Differences are numerical
        # computing errors and a few other specific things to how chromagrams are created
        # but these two methods are theoretically the same: 
        # F(x + y) = F(x) + F(y) for fourier transform F and signals x and y

        # accumulate the pre-computed energies for each note
        if efficient:
            # 12 musical notes in a chromagram
            num_chroma_bins = 12
            energy = np.zeros(num_chroma_bins)
            for i, active in enumerate(state):
                if active:
                    energy += self.pitch_to_chroma_energy[i + self.starting_pitch]

        # synthesize the audio, get the chromagram, and then compute the energies
        else:
            energy = np.sum(self.get_state_chroma(state), axis=1)

        energy /= np.linalg.norm(energy)
        return energy

    def get_audio_chroma(self, sound):
        window_length = 4096
        hop_size = window_length//2
        log_comp = 1
        normalize = True
        return fmp.make_chromagram(sound, 
                                    self.sample_rate, 
                                    window_length, 
                                    hop_size, 
                                    gamma=log_comp, 
                                    normalize=normalize)

    def plot_state_chroma(self, state=None):
        if state is None:
            state = self.state
        plt.title("Pitches: {}".format([x+self.starting_pitch for x in np.where(np.array(self.state) == 1)[0]]))
        plt.imshow(self.get_state_chroma(state), origin='lower', aspect='auto')
        plt.xlabel("Time (downsampled)")
        plt.ylabel("Musical Pitch")
        plt.show()

    def plot_pitch(self, pitch):
        if self.in_key_range(pitch):
            data = self.audio[pitch]
            plt.title("pitch: {}".format(str(pitch)))
            plt.plot(np.arange(len(data)), data)
            plt.show()
        else:
            print("Pitch {} not in range".format(pitch))

    def score(self, song_audio, state=None):
        if state is None:
            state = self.state

        state_vec = self.get_state_chroma_energy_norm(state)
        song_vec = np.sum(self.get_audio_chroma(song_audio), axis=1)
        song_vec /= np.linalg.norm(song_vec)
        return np.dot(state_vec, song_vec)

    def compute_chroma_energies(self):
        for i in range(self.num_notes):
            pitch = i + self.starting_pitch
            state = [0] * self.num_notes
            state[i] = 1
            energy = np.sum(self.get_state_chroma(state), axis=1)
            energy /= np.linalg.norm(energy)
            self.pitch_to_chroma_energy[pitch] = energy


if __name__ == '__main__':
    k = Keyboard()
    # k.toggle_note(60)
    # k.toggle_note(64)
    # k.toggle_note(67)
    # audio = load_wav("resources/keys_wav/60.wav")
    # s = k.score(audio)
    # print(s)
    # print(np.exp(s))
    # k.play_current_state()

    # audio = load_wav("piano/resources/tests/test1.wav")
    audio = load_wav("piano/resources/keys_wav/73.wav")

    k.toggle_note(60)
    for t in range(k.starting_pitch+1, k.starting_pitch + k.num_notes):

        res = k.score(audio)
        print(res, t)

        k.toggle_note(t-1)
        k.toggle_note(t)
