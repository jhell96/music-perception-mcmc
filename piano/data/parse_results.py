import numpy as np


def note_string_to_array(note_string, num_notes=20):
    lst = note_string.split(",")
    return np.array([[int(x) for x in lst[i:i+num_notes]] for i in range(0, len(lst), num_notes)])


def play_string_to_array(play_string):
    return np.array([int(x) for x in play_string.split(",")])


def parse_results(file='raw/trials.txt'):
    results_string = None
    with open(file, 'r') as f:
        results_string = f.read()

    res = [trial_string.split('\n') for trial_string in results_string.split("-"*100)]

    results = []
    for i, trial in enumerate(res):
        if len(trial) == 12:
            skill_level, test1, test1_plays, test2, test2_plays, test3, test3_plays, test4, test4_plays, test5, test5_plays = trial[:-1]

            skill_level = int(skill_level)
            test1 = note_string_to_array(test1)
            test2 = note_string_to_array(test2)
            test3 = note_string_to_array(test3)
            test4 = note_string_to_array(test4)
            test5 = note_string_to_array(test5)

            test1_plays = play_string_to_array(test1_plays)
            test2_plays = play_string_to_array(test2_plays)
            test3_plays = play_string_to_array(test3_plays)
            test4_plays = play_string_to_array(test4_plays)
            test5_plays = play_string_to_array(test5_plays)

            t = Trial(skill_level)
            t.tests.append(test1)
            t.tests.append(test2)
            t.tests.append(test3)
            t.tests.append(test4)
            t.tests.append(test5)

            t.test_plays.append(test1_plays)
            t.test_plays.append(test2_plays)
            t.test_plays.append(test3_plays)
            t.test_plays.append(test4_plays)
            t.test_plays.append(test5_plays)

            results.append(t)

    return results


class Trial():
    def __init__(self, skill_level):
        self.tests = []
        self.test_plays = []

if __name__ == '__main__':
    trials = parse_results()

    person = 0
    test = 0
    example = trials[person].tests[test]
    print("Person: {}, Test: {} \n {}".format(person, test, example))