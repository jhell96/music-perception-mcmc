from os import listdir
from os.path import isfile, join
from util import *
import numpy as np
import matplotlib.pyplot as plt
import fmp


class Keyboard():
    def __init__(self, num_notes=20, starting_pitch=60, audio_dirpath=None):
        self.starting_pitch = starting_pitch
        self.num_notes = num_notes
        self.state = [0]*self.num_notes
        self.audio = dict()
        if audio_dirpath:
            self.load_audio_files(audio_dirpath)
        else:
            self.load_audio_files()

    def possible_next_states(self):
        new_states = []
        for i, note in enumerate(self.state):
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

    def load_audio_files(self, path="resources/keys_wav"):
        files = set(get_directory_files(path, file_ext="wav"))
        for pitch in range(self.starting_pitch, self.starting_pitch+self.num_notes+1):
            file = join(path, str(pitch)+".wav")
            if file in files:
                wav_data = load_wav(file)
                sound_start_idx = int(np.min(np.where(wav_data>0.01)[0]))
                self.audio[pitch] = np.concatenate([wav_data[sound_start_idx:], np.zeros(sound_start_idx)])

    def play_current_state(self):
        sound = self.get_current_state_audio()
        play_wav_data(sound)

    def play_pitch(self, pitch):
        if self.in_key_range(pitch):
            play_wav_data(self.audio[pitch])
        else:
            print("Pitch {} not in range".format(pitch))

    def get_current_state_audio(self):
        data_len = len(list(self.audio.values())[0])
        sound = np.zeros(data_len)
        for i, s in enumerate(self.state):
            if s == 1:
                sound += self.audio[self.starting_pitch+i]

        return sound

    def plot_state_chroma(self):
        sound = self.get_current_state_audio()
        plt.title("Pitches: {}".format([x+self.starting_pitch for x in np.where(np.array(self.state) == 1)[0]]))
        plt.imshow(fmp.make_chromagram(sound, 22050, 4096, 4096//2, gamma=1.0), origin='lower', aspect='auto')
        plt.show()

    def plot_pitch(self, pitch):
        if self.in_key_range(pitch):
            data = self.audio[pitch]
            plt.title("pitch: {}".format(str(pitch)))
            plt.plot(np.arange(len(data)), data)
            plt.show()
        else:
            print("Pitch {} not in range".format(pitch))

if __name__ == '__main__':
    k = Keyboard()
    k.toggle_note(60)
    k.toggle_note(64)
    k.toggle_note(67)
    k.play_current_state()
