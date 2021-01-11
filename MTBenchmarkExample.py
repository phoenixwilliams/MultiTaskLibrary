import YSOBenchmarkSuite
import DEMTO
import Problem
import scipy.io
import AlgorithmOperators
import time
import matplotlib.pyplot as plt


"""
This script is to show how to set up an MT benchmark problem an algorithm to optimize the MT problems. 
These benchmark problems comes from the paper:
Evolutionary Multitasking for Single-objective Continuous Optimization: Benchmark Problems, 
Performance Metric, and Baseline Results by Bingshui Da, Yew-Soon Ong, Liang Feng,
A.K. Qin, Abhishek Gupta, Zexuan Zhu, Chuan-Kang Ting, Ke Tang, and Xin Yao

To load the rotation matricies and/or displacement vectors for a given Benchmark problem, this requires the scipy 
package. Matplotlib is used to plot the process in graph form.

This Specific example uses the DEMOTO optimization algorithm, the important aspect of this example is the Problem 
set-up, once set up correctly it can be used within any optimization in this package as normal. The use of the Problems
object also allows the construction of custom complex problems that involve constraints or values in addition to the 
input. These can be constructed by simply defining a design dictionary as been done throughout this package.
"""


if __name__ == "__main__":

    # CI+HS MT problem
    NI_M = scipy.io.loadmat("YSO_MTBenchmarks/NI_M.mat")


    problem1_params = {
        "M": NI_M["Rotation_Task1"],
        "opt": [0 for _ in range(50)]
    }

    rastrigin = Problem.Problem(YSOBenchmarkSuite.rastrigin, problem1_params)

    problem2_params = {
        "a": 418.9829
    }

    schwefel = Problem.Problem(YSOBenchmarkSuite.schwefel, problem2_params)

    dimensions = [50, 50]

    compute_cr_params = {
        "mean": 0.4,
        "sigma": 0.1
    }

    compute_f_params = {
        "t": 0.3,
        "s": 0.1
    }

    design = {
        "K": 2,
        "dimensions": dimensions,
        "N": 50,
        "problems": [rastrigin, schwefel],
        "bounds": [[-50, 50], [-500, 500]],
        "penalty": 0,
        "function_evaluations": 100000,
        "rmp": 0.5,
        "mutant_generator": AlgorithmOperators.de_rand_1,
        "crossover": AlgorithmOperators.de_binomial_crossover,
        "compute_cr": AlgorithmOperators.compute_cr,
        "compute_cr_params": compute_cr_params,
        "compute_f": AlgorithmOperators.compute_f,
        "compute_f_params": compute_f_params
    }

    demoto = DEMTO.DEMTO(design)
    start = time.time()
    final_population, process = demoto.optimize(True)
    print(time.time() - start)

    avgs = [0, 0]
    for c in range(len(final_population)):
        avg = 0
        for p in final_population[c].population:
            avg += p.fitness
        avg = avg / len(final_population[c].population)
        avgs[c] = avg

    print(avgs)
    print(final_population[0].center.fitness, final_population[1].center.fitness)
    print(final_population[1].center.genotype)

    plt.plot(process[0])
    plt.show()
    plt.plot(process[1])
    plt.show()

