from keyboard import Keyboard
import numpy as np
from util import *
from tqdm import tqdm


class MCMC_MH():
    def __init__(self, max_iterations):
        self.max_iterations = max_iterations
        self.keyboard = Keyboard()
        self.history = []

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
        self.keyboard.state = [1]*len(self.keyboard.state)

        num_accepted = 0
        for t in tqdm(range(self.max_iterations)):
            states = self.keyboard.possible_next_states()
            new_idx = np.random.randint(len(states))
            proposal_state = states[new_idx]

            current_score = self.keyboard.score(audio)
            proposal_score = self.keyboard.score(audio, state=proposal_state)

            current_prob = current_score
            proposal_prob = proposal_score

            acceptance_probability = min(1, (proposal_prob/current_prob))
            u = np.random.uniform(0, 1)

            if (u <= acceptance_probability):
                self.keyboard.state = proposal_state
                self.history.append(proposal_state)
                num_accepted += 1


if __name__ == '__main__':
    mh = MCMC_MH(100000)
    audio = load_wav("resources/keys_wav/60.wav")
    mh.estimate(audio)
    print("Final state: " + str(mh.keyboard.state))
    mh.keyboard.play_current_state()
    s = np.sum(np.array(mh.history[-10:]), axis=0)
    print(s)