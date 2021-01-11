import DEMTO
import AlgorithmOperators
import BenchmarkProblems
import time
import matplotlib.pyplot as plt

if __name__ == "__main__":
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
        "problems": [BenchmarkProblems.rastrigin, BenchmarkProblems.schwefel],
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
