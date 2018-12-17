import numpy as np
import matplotlib.pyplot as plt
import piano.data.parse_results as pr

PATH_TO_TRIALS = 'piano/data/raw/trials.txt'


'''
Evaluation 1: MCMC vs. single person over time (for individual test, at particular experience level)
x-axis: trials
y-axis: keys 60-78
Looking at the MCMC and humans actual attempts and seeing if they converge, or for any particular
clustering of notes in their attempts

results array: parsed results 
exp_level int: experience level (1-4)
test int: test number (0-4)
MCMC: MCMC with the appropriate params corresponding to the exp_level
'''
def evaluation1(results, exp_level, test, MCMC):
	count = 0
	plt.figure(1)

	for test_subject in results:
		if test_subject.skill_level == exp_level:
			count += 1
			trials = test_subject.tests[test]
			x = []
			y = []
			for trial in range(len(trials)):
				pressed_keys = np.where(trials[trial]==1)[0]
				for key in pressed_keys:
					x.append(trial)
					y.append(key)
			plt.subplot(4, 2, count)
			# plt.title("Subject " + str(count))
			plt.plot(x, y, 'ro')
	plt.show()


'''
Evaluation 2: MCMC vs. humans (at particular skill level) # of steps to converge
x-axis: test1, test2, ..., test5
y-axis: # of iterations
Looking at the MCMC and avg. humans (at particular skill level) # of steps needed to converge

results array: parsed results
exp_level int: experience level (1-4)
MCMC: MCMC with the appropriate params corresponding to the exp_level
'''
def evaluation2(results, exp_level):
	# answers
	answers = {0: [13], 1:[5,8], 2:[0, 4, 7], 3:[4, 10, 12], 4:[3, 10, 14]}
	tests_convergence = {0:[], 1:[], 2:[], 3:[], 4:[]}

	plt.figure(2)

	for test_subject in results:
		# filter out by experience level
		if test_subject.skill_level == exp_level:

			# iterate through valid test_subject's test
			for test in range(5):
				trials = test_subject.tests[test]

				# iterate through test subject's test's trials
				pressed = [] # trials list of indices == 1
				for trial in trials:
					pressed.append((np.where(trial==1)[0]).tolist())

				try: 
					tests_convergence[test].append(pressed.index(answers[test]))
				except ValueError:
					pass 

	iterations_to_converge = [] # y-values for humans
	for i in tests_convergence.values():
		iterations_to_converge.append(int(np.average(i)))

	
	x = np.arange(5)
	y = iterations_to_converge

	plt.title("Iterations to Converge, Level: "+str(exp_level))
	plt.bar(x, y)
	plt.xticks(x, ('test1', 'test2', 'test3', 'test4', 'test5'))
	plt.show()




if __name__ == '__main__':
    # example of fetching results from the web, and storing in trials.txt
    results = pr.parse_results(file=PATH_TO_TRIALS, web_refresh=True)
    # evaluation1(results, 1, 3)
    # evaluation2(results, 2)
