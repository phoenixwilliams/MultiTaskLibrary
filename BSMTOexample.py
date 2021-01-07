import BSMTO
import BenchmarkProblems
import time
import AlgorithmOperators
import matplotlib.pyplot as plt


if __name__ == "__main__":

    dimensions = [50, 50]
    crossover_params = {
        "pc": 1.0,
        "nc": 20,
        "length": max(dimensions)
    }

    gaussmutation_params = {
        "mean":0,
        "sigma":1,
        "pm": 1/max(dimensions),
        "length": max(dimensions)

    }

    polymutation_params = {
        "nm": 5,
        "pm": 1/max(dimensions),
        "length": max(dimensions),
        "diffmut": 1
    }

    selection_params = {
        "tournament_size": 1,
        "fitness_name": "fitness"
    }

    design = {
        "problems": [BenchmarkProblems.griewank, BenchmarkProblems.rastrigin],
        "K": 2,
        "dimensions": dimensions,
        "N": 100,
        "crossover": AlgorithmOperators.sbx,
        "crossover_params": crossover_params,
        "mutations": [AlgorithmOperators.mutpoly],
        "mutations_params": [polymutation_params],
        "p3": 0.85,
        "bounds": [[-100, 100], [-50, 50]],
        "penalty": 0,
        "iterations": 10000,
        "nk": 50,
        "p2":0.8,
        "selection": AlgorithmOperators.Single_BinaryTournament,
        "selection_params": selection_params
    }


    bsmto = BSMTO.BSMTO(design)
    start = time.time()
    final_population, process = bsmto.optimize(True)
    print(time.time()-start)

    avgs = [0,0]
    for c in range(len(final_population)):
        avg = 0
        for p in final_population[c].population:
            avg += p.fitness

        avg = avg/len(final_population[c].population)
        avgs[c] = avg

    print(avgs)

    plt.plot(process[0])
    plt.show()
    plt.plot(process[1])
    plt.show()