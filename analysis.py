import numpy as np
import matplotlib.pyplot as plt
import piano.data.parse_results as pr
import mcmc
from util import *

PATH_TO_TRIALS = 'piano/data/raw/trials.txt'

# musical experience tier : (sim, proposal)
BEST_PARAMS = {0:(50.0, 100.0),  1:(10.0, 27.83), 2:(16.9, 215.4), 3:(10.0, 215.44)}

def plot_sim(data):
    loss = []
    sim = []
    prop = []

    for s in data:
        loss.append(s[0])
        sim.append(int(s[1]))
        prop.append(int(s[2]))

    plt.plot(sim, loss)
    plt.show()


def optimize_params(level):
    losses = []
    sim_params = np.logspace(1, 3, num=10)
    prop_params = np.logspace(1, 3, num=10)

    num_trials_each = 2

    for sim_sen in sim_params:
        for prop_sen in prop_params:
            loss = 0
            for test in range(1, 6):
                mean_q = []
                for n in range(num_trials_each):
                    # multiplying by 1.3 accounts for 30% burn in rate we use when calculating the 
                    # probabiltiy distribution.

                    num_iters = int(get_avg_num_trials(test, level) * 1.3)
                    mh = mcmc.MCMC_MH(num_iters, proposal_method='sim', proposal_sensitivity=int(prop_sen), similarity_sensitivity=int(sim_sen))
                    audio_file = "piano/resources/tests/test{}.wav".format(test)
                    audio = load_wav(audio_file)

                    # call the mcmc
                    mh.estimate(audio)
                    q = mh.get_dist()
                    mean_q.append(q)

                # get the average probabilities over several trials
                mean_q = np.array(mean_q)
                mean_q = np.mean(mean_q, axis=0)
                mean_q /= np.sum(mean_q)

                # p is true model (human)
                # q is estimated model (mcmc)
                p = get_trial_distribution(test, level)
                div = kl_div(p, mean_q)
                loss += div

            losses.append((loss, sim_sen, prop_sen))

    best = min(losses)
    best_loss, best_sim, best_prop = best

    # log trial
    with open('best_params.txt', 'a') as f:
        f.write('\n'+'#'*100+'\n')
        f.write('Level {} \n'.format(level))
        f.write('Sim_params: \n')
        f.write(str(list(sim_params)))
        f.write('\n')
        f.write('Prop_params: \n')
        f.write(str(list(prop_params)))
        f.write('\n')
        f.write('Losses: \n')
        f.write(str(losses))
        f.write('\n')
        f.write('Best Sim: {}, Best Prop: {}'.format(best_sim, best_prop))
        f.write('')

    return (best_loss, best_sim, best_prop)


def get_avg_num_trials(test, level):
    results = pr.parse_results(file=PATH_TO_TRIALS, web_refresh=True)
    res = filter(lambda trial: int(trial.skill_level) == int(level), results)
    return int(np.mean([len(t.tests[test-1]) for t in res]))


def get_trial_distribution(test, level):
    results = pr.parse_results(file=PATH_TO_TRIALS, web_refresh=True)
    res = filter(lambda trial: int(trial.skill_level) == int(level), results)

    trials = []
    for t in res:
        trials.extend(t.tests[test-1])
    trials = np.sum(np.array(trials), axis=0)
    return trials/np.sum(trials)

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
def evaluation1(results, exp_level, test):
	count = 0
	plt.figure(1)

	for i in range(len(results)):
		test_subject = results[i]

		if test_subject.skill_level == exp_level:
			count += 1
			human_trials = test_subject.tests[test]
			x_model = []
			y_model = []
			x_human = []
			y_human = []

			num_iters = int(len(human_trials)*(1.3))
			mh = mcmc.MCMC_MH(num_iters, proposal_method='sim', proposal_sensitivity=BEST_PARAMS[test][1], similarity_sensitivity=BEST_PARAMS[test][0])
			audio_file = "piano/resources/tests/test{}.wav".format(test+1)
			audio = load_wav(audio_file)

			mh.estimate(audio)
			model_trials = mh.history[(num_iters-len(human_trials)):]

			for trial in range(len(human_trials)):
				human_keys = np.where(human_trials[trial]==1)[0]
				for key in human_keys:
					x_human.append(trial)
					y_human.append(key)

				model_keys = np.where(np.array(model_trials[trial])==1)[0]

				for key in model_keys:
					x_model.append(trial)
					y_model.append(key)

			plt.subplot(4, 2, count)
			plt.xlabel("Trials")
			plt.ylabel("Notes")
			plt.plot(x_human, y_human, 'ro')
			plt.plot(x_model, y_model, 'g^')
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
    # results = pr.parse_results(file=PATH_TO_TRIALS, web_refresh=True)
    # print(results)

    # res = get_trial_distribution(1, 4)
    # print(res)

    # for level in range(1, 5):
    #     params = optimize_params(level)
    #     print(params)
    # sim = [(6.534918296223005, 10.0, 10.0), (5.2816352584450454, 10.0, 16.68100537200059), (6.232476345186236, 10.0, 27.825594022071243), (5.657731689816818, 10.0, 46.41588833612777), (5.880941015139102, 10.0, 77.4263682681127), (6.854989949518111, 10.0, 129.1549665014884), (5.414083924612736, 10.0, 215.44346900318823), (5.420603289669291, 10.0, 359.38136638046257), (5.0500863444453445, 10.0, 599.4842503189409), (4.694948364528973, 10.0, 1000.0), (8.093793012371002, 16.68100537200059, 10.0), (5.718552511152068, 16.68100537200059, 16.68100537200059), (7.836685344228659, 16.68100537200059, 27.825594022071243), (8.13024182397358, 16.68100537200059, 46.41588833612777), (7.976866082357776, 16.68100537200059, 77.4263682681127), (10.14287556398001, 16.68100537200059, 129.1549665014884), (5.3495121573248525, 16.68100537200059, 215.44346900318823), (5.172336702239255, 16.68100537200059, 359.38136638046257), (6.909755098484978, 16.68100537200059, 599.4842503189409), (8.745685254759763, 16.68100537200059, 1000.0), (11.812265796033003, 27.825594022071243, 10.0), (8.697343584786095, 27.825594022071243, 16.68100537200059), (13.475464896633953, 27.825594022071243, 27.825594022071243), (11.063935873447079, 27.825594022071243, 46.41588833612777), (12.73214974943682, 27.825594022071243, 77.4263682681127), (11.488283719454346, 27.825594022071243, 129.1549665014884), (12.20911156174264, 27.825594022071243, 215.44346900318823), (9.24808550848027, 27.825594022071243, 359.38136638046257), (10.413535759932284, 27.825594022071243, 599.4842503189409), (14.03184392103674, 27.825594022071243, 1000.0), (14.580396566561138, 46.41588833612777, 10.0), (17.120964531560833, 46.41588833612777, 16.68100537200059), (16.232889000756195, 46.41588833612777, 27.825594022071243), (14.076814522427451, 46.41588833612777, 46.41588833612777), (15.452400814049513, 46.41588833612777, 77.4263682681127), (16.382892345572852, 46.41588833612777, 129.1549665014884), (12.00359841916583, 46.41588833612777, 215.44346900318823), (15.339498022820502, 46.41588833612777, 359.38136638046257), (20.233008553367448, 46.41588833612777, 599.4842503189409), (18.22999432160807, 46.41588833612777, 1000.0), (20.454755064049394, 77.4263682681127, 10.0), (20.095270404598708, 77.4263682681127, 16.68100537200059), (22.1585194209129, 77.4263682681127, 27.825594022071243), (19.31101543676676, 77.4263682681127, 46.41588833612777), (20.285001452562142, 77.4263682681127, 77.4263682681127), (21.57429940024425, 77.4263682681127, 129.1549665014884), (22.032868571893168, 77.4263682681127, 215.44346900318823), (18.798750704411745, 77.4263682681127, 359.38136638046257), (16.027560001159923, 77.4263682681127, 599.4842503189409), (22.911778833936527, 77.4263682681127, 1000.0), (20.639441464084094, 129.1549665014884, 10.0), (20.69809918180237, 129.1549665014884, 16.68100537200059), (19.983168623777953, 129.1549665014884, 27.825594022071243), (22.31063551407069, 129.1549665014884, 46.41588833612777), (19.72356279538463, 129.1549665014884, 77.4263682681127), (21.04587220791518, 129.1549665014884, 129.1549665014884), (20.94838677807219, 129.1549665014884, 215.44346900318823), (20.266450568787427, 129.1549665014884, 359.38136638046257), (21.090023796012137, 129.1549665014884, 599.4842503189409), (23.413235580593955, 129.1549665014884, 1000.0), (21.71466370558637, 215.44346900318823, 10.0), (22.99054631034873, 215.44346900318823, 16.68100537200059), (24.89590708786448, 215.44346900318823, 27.825594022071243), (24.969845759990367, 215.44346900318823, 46.41588833612777), (26.279438480527332, 215.44346900318823, 77.4263682681127), (22.689707603232446, 215.44346900318823, 129.1549665014884), (26.077970827012972, 215.44346900318823, 215.44346900318823), (30.603320234513916, 215.44346900318823, 359.38136638046257), (26.004300491002752, 215.44346900318823, 599.4842503189409), (26.74417409432339, 215.44346900318823, 1000.0), (25.669620553863844, 359.38136638046257, 10.0), (25.39745776225257, 359.38136638046257, 16.68100537200059), (25.391416031255776, 359.38136638046257, 27.825594022071243), (25.892716263908376, 359.38136638046257, 46.41588833612777), (28.105467998309692, 359.38136638046257, 77.4263682681127), (24.424839103427246, 359.38136638046257, 129.1549665014884), (26.301887547451706, 359.38136638046257, 215.44346900318823), (26.022326220494612, 359.38136638046257, 359.38136638046257), (30.06476074135746, 359.38136638046257, 599.4842503189409), (28.57590954059821, 359.38136638046257, 1000.0), (24.60669988188203, 599.4842503189409, 10.0), (22.7456960852497, 599.4842503189409, 16.68100537200059), (22.263604880138455, 599.4842503189409, 27.825594022071243), (28.310667474175734, 599.4842503189409, 46.41588833612777), (22.88091486587483, 599.4842503189409, 77.4263682681127), (22.98255468440633, 599.4842503189409, 129.1549665014884), (27.232071634507502, 599.4842503189409, 215.44346900318823), (23.900615807473784, 599.4842503189409, 359.38136638046257), (25.95528008473711, 599.4842503189409, 599.4842503189409), (30.51457221275634, 599.4842503189409, 1000.0), (9.191097843081433, 1000.0, 10.0), (7.927788333525728, 1000.0, 16.68100537200059), (8.131486244112363, 1000.0, 27.825594022071243), (7.580429650715698, 1000.0, 46.41588833612777), (7.679205257714016, 1000.0, 77.4263682681127), (7.6919181206970135, 1000.0, 129.1549665014884), (7.8867153918512, 1000.0, 215.44346900318823), (11.270052657927346, 1000.0, 359.38136638046257), (18.27585352978322, 1000.0, 599.4842503189409), (14.425740204382212, 1000.0, 1000.0)]
    # plot_sim(sim)
    
    # results = pr.parse_results(file=PATH_TO_TRIALS, web_refresh=True)
    # evaluation1(results, 1, 3)
    results = pr.parse_results(file=PATH_TO_TRIALS, web_refresh=True)
    evaluation1(results, 1, 1) #results, exp_level, test)
    # evaluation2(results, 2)

    level_1 = [round(x, 2) for x in get_trial_distribution(4, 1)]
    level_4 = [round(x, 2) for x in get_trial_distribution(4, 4)]
    mcmc = [round(x,2) for x in [0.196,0.001,0.0,0.0,0.118,0.127,0.0,0.001,0.0,0.0,0.196,0.076,0.196,0.009,0.0,0.0,0.079,0.001,0.0, 0.001]]
    pitches = [x for x in range(60, 80)]
    plt.plot(pitches, level_1, label="beginner (level 1)")
    plt.plot(pitches, level_4, label="expert (level 4)")
    plt.plot(pitches, mcmc, label="expert tuned MCMC")
    plt.title("Test 4 True notes: {}".format([x + 60 for x in [4, 10, 12]]))
    plt.xlabel("Pitches")
    plt.xticks(pitches)
    plt.ylabel("Probabilities")
    plt.legend(loc='upper left')
    plt.show()
