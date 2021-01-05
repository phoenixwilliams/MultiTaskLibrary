import YSOMultiTaskEA
import BenchmarkProblems
import AlgorithmOperators
import time


if __name__ == "__main__":
    dimensions = [50, 50]
    rmp = 0.3
    problems = [BenchmarkProblems.rastrigin, BenchmarkProblems.schwefel]
    bounds = [[-50, 50], [-500, 500]]


    selection_params = {
        "tournament_size":1
    }


    crossover_params = {
        "pc": 1.0,
        "nc": 15.0,
        "length": max(dimensions)
    }

    mutation_params = {
        "nm": 20.0,
        "pm": 1 / (max(dimensions)),
        "length": max(dimensions),
        "diffmut": 1
    }

    design = {
        "dimensions": dimensions,
        "size": 100,
        "K": 2,
        "problems": problems,
        "bounds": bounds,
        "offspring_pop_size": 100,
        "iterations": 100,
        "crossover": AlgorithmOperators.sbx,
        "crossover_params": crossover_params,
        "mutation": AlgorithmOperators.mutpoly,
        "mutation_params": mutation_params,
        "rmp": rmp,
        "penalty_constant":10e+100,
        "selection":AlgorithmOperators.BinaryTournament,
        "selection_params":selection_params
    }

    mtea = YSOMultiTaskEA.MTEA(design)
    start = time.time()
    final_population, process = mtea.optimize(True)
    print("time:", time.time() - start)

