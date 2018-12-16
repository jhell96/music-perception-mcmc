import numpy as np
import matplotlib.pyplot as plt
import piano.data.parse_results as pr

PATH_TO_TRIALS = 'piano/data/raw/trials.txt'

if __name__ == '__main__':
    # example of fetching results from the web, and storing in trials.txt
    results = pr.parse_results(file=PATH_TO_TRIALS, web_refresh=True)
    print(results)

