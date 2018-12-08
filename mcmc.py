class MCMC_MH():
    def __init__(self, max_iterations):
        pass

    def run():
        # ALG:
        # initialize
        # generate candidate from g(x' | x_t)
        # calculate acceptance probability A(x', x_t) = min(1, ( p(x') / p(x) ) * ( g(x_t | x') / g(x' | x_t) ) )
        # uniformly generate number [0, 1]
        # if u <= A(x', x_t) accept and set x_{t+1} = x'
        # otherwise reject the new state and copy the old state forward
        # increment t
        pass


if __name__ == '__main__':
    pass