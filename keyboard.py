from os import listdir
from os.path import isfile, join

class Keyboard():
    def __init__(self, num_octaves=2, starting_pitch=40):
        self.starting_pitch = starting_pitch
        self.num_notes = 12*num_octaves
        self.state = [0]*self.num_notes
        self.audio = dict()

    def possible_next_states(self):
        new_states = []
        for i, note in enumerate(self.state):
            possible = self.state[:]
            possible[i] = 1 if possible[i] == 0 else 0
            new_states.append(possible)
        return new_states

    def toggle_note(pitch):
        if self.on_keyboard(pitch):
            idx = pitch - self.starting_pitch
            self.state[idx] = 1 if self.state[idx] == 0 else 0

    def on_keyboard(pitch):
        above = (pitch >= starting_pitch)
        below = (pitch < self.starting_pitch + self.num_notes)
        return above and below

    def load_audio_files(path):
        files = [f for f in listdir(path) if isfile(join(path, f))]

        for f in files:
            self.audio[]


        

    def state_to_sound():
        pass

if __name__ == '__main__':
    k = Keyboard()
    states = k.possible_next_states()
    print(states)
