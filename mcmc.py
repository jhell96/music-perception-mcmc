from keyboard import Keyboard
import numpy as np
from util import *
from tqdm import tqdm


class MCMC_MH():
    def __init__(self, max_iterations):
        self.max_iterations = max_iterations
        self.keyboard = Keyboard()
        self.history = []

    def estimate(self, audio, sensitivity=100.0):
        # ALG:
        #   initialize
        #   generate candidate from g(x' | x_t)
        #   calculate acceptance probability A(x', x_t) = min(1, ( p(x') / p(x) ) * ( g(x_t | x') / g(x' | x_t) ) )
        #   uniformly generate number [0, 1]
        #   if u <= A(x', x_t) accept and set x_{t+1} = x'
        #   otherwise reject the new state and copy the old state forward
        #   increment t
        ######################################################

        # init
        self.keyboard.state = [0]*len(self.keyboard.state)
        # self.keyboard.toggle_note(73)

        num_accepted = 0
        for t in tqdm(range(self.max_iterations)):
            states = self.keyboard.possible_next_states()

            state_dist = self.proposal_dist(states)
            proposal_idx = np.random.choice(len(states), 1, p=state_dist)[0]
            proposal_state = states[proposal_idx]

            current_score = self.keyboard.score(audio)
            proposal_score = self.keyboard.score(audio, state=proposal_state)

            # print(current_score, proposal_score)
            score_distribution = self.keyboard.softmax([current_score, proposal_score], scale=sensitivity)

            # print(score_distribution, self.keyboard.state, proposal_state)
            current_prob, proposal_prob = score_distribution

            acceptance_probability = min(1, (proposal_prob/(current_prob + 1e-5)))
            u = np.random.uniform(0, 1)

            if (u <= acceptance_probability):
                self.keyboard.state = proposal_state
                self.history.append(proposal_state)
                num_accepted += 1

    def proposal_dist(self, states):
        return [1/len(states) for i in states]

    def run_test(self, test_num):
        lookback = 1000

        audio_file = "piano/resources/tests/test{}.wav".format(test_num)
        audio = load_wav(audio_file)

        with open("piano/resources/tests/correct_notes.txt", 'r') as f:
            correct = f.read()

        print("Getting correct answer...")
        correct_state = [0]*self.keyboard.num_notes
        for t in [x.split(":") for x in correct.split('\n')]:
            if t[0] == 'test{}'.format(test_num):
                for p in t[1].split(','):
                    correct_state[int(p)-self.keyboard.starting_pitch] = 1


        print("Running MCMC...")
        self.estimate(audio)

        s = np.sum(np.array(self.history[-min(lookback, self.max_iterations):]), axis=0)

        pitches = np.arange(self.keyboard.starting_pitch, self.keyboard.starting_pitch+self.keyboard.num_notes)
        probabilities = s/np.sum(s)

        print("Pitch Probabilities from last {} iterations:".format(lookback))
        print("Pitch Prob")
        for pitch, prob in zip(pitches, probabilities):
            print("{}   {}".format(pitch, round(prob, 3)))

        print("")
        print("Top Note: " + str(np.argmax(s)+self.keyboard.starting_pitch))
        print("Final state:   " + str(self.keyboard.state))
        print("Correct State: " + str(correct_state))
        print("Pitches:       " + str(pitches))
        print("")
        print("Playing original audio...")
        print("")
        play_wav(audio_file)
        print("")
        print("Playing estimated audio...")
        print("")
        self.keyboard.play_current_state()


if __name__ == '__main__':
    num_iters = 10000
    mh = MCMC_MH(num_iters)
    mh.run_test(3)

