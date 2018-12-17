from keyboard import Keyboard
import numpy as np
from util import *
from tqdm import tqdm
import matplotlib.pyplot as plt


class MCMC_MH():
    def __init__(self, max_iterations, proposal_method='uniform', proposal_sensitivity=1000.0, similarity_sensitivity=100.0):
        self.max_iterations = max_iterations
        self.keyboard = Keyboard()
        self.history = []
        self.proposal_method = proposal_method
        self.proposal_sensitivity = proposal_sensitivity
        self.similarity_sensitivity = similarity_sensitivity

    def estimate(self, audio):
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
            score_distribution = self.keyboard.softmax([current_score, proposal_score], scale=self.similarity_sensitivity)

            # print(score_distribution, self.keyboard.state, proposal_state)
            current_prob, proposal_prob = score_distribution

            acceptance_probability = min(1, (proposal_prob/(current_prob + 1e-5)))
            u = np.random.uniform(0, 1)

            if (u <= acceptance_probability):
                self.keyboard.state = proposal_state
                self.history.append(proposal_state)
                num_accepted += 1
            else:
                self.history.append(self.keyboard.state)

    def proposal_dist(self, states):
        if self.proposal_method == 'uniform':
            # Uniform dist:
            return [1/len(states) for i in states]

        if self.proposal_method == 'sim':
            # Similarity dist

            current_state = self.keyboard.state
            curr_energy = self.keyboard.get_state_chroma_energy()
            sim = []
            for s in states:
                energy = self.keyboard.get_state_chroma_energy(state=s)
                sim.append(np.dot(curr_energy, energy))

            dist = np.array(sim)/(sum(sim) + 1e-5)
            dist = self.keyboard.softmax(dist, scale=self.proposal_sensitivity)
            return dist

    def plot_history(self, correct_state=None):
        if correct_state:
            correct_state = list(map(lambda x: x*2, correct_state))
            out = self.history[:]
            for i in range(int(max(1, 0.05*len(out)))):
                out.append(correct_state)
        else:
            out = self.history

        h = np.array(out)
        plt.title("prop method: {}, prop_sen: {}, sim_sen: {}".format(self.proposal_method, self.proposal_sensitivity, self.similarity_sensitivity))
        plt.imshow(h.T, origin='lower', aspect='auto')
        plt.xlabel("Iteration")
        plt.ylabel("Note")
        plt.show()

    def get_dist(self):
        burn_in = 100
        cut = int(min(burn_in, 0.3 * self.max_iterations)) 
        s = np.sum(np.array(self.history[cut:]), axis=0)
        probabilities = s/np.sum(s)
        return np.array(probabilities)

    def run_test(self, test_num):
        burn_in = 1000

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

        cut = int(min(burn_in, 0.3 * self.max_iterations)) 
        s = np.sum(np.array(self.history[cut:]), axis=0)

        pitches = np.arange(self.keyboard.starting_pitch, self.keyboard.starting_pitch+self.keyboard.num_notes)
        probabilities = s/np.sum(s)

        print("Pitch Probabilities")
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
        self.plot_history(correct_state)



if __name__ == '__main__':

    # number of iterations to run (normal values: 10 - 10,000)
    num_iters = 10000

    # proposal distribution method (normal values: 'uniform' or 'sim' for simliarity proposal)
    # method = 'uniform'
    method = 'sim'

    # sets the sensitivity of how simliar we think any state is to a piece of audio
    # normal values: 50 - 500
    sim_sen = 120

    # sets the sensitivity of how simliar we think our proposed state is to the current state
    # normal values: 10 - 1,000
    # ONLY ACTUALLY USED WHEN USING 'sim' METHOD
    prop_sen = 50

    # initialize mcmc
    mh = MCMC_MH(num_iters, proposal_method=method, proposal_sensitivity=prop_sen, similarity_sensitivity=sim_sen)

    # run test number 5
    # will play audio and will generate a plot
    # this uses
    mh.run_test(4)

