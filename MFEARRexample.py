import MFEARR
import BenchmarkProblems
import AlgorithmOperators
import time


if __name__ == "__main__":
    dimensions = [50, 50]
    rmp = 0.3
    problems = [BenchmarkProblems.griewank, BenchmarkProblems.schwefel]
    bounds = [[-50, 50], [-50, 50]]


    selection_params = {
        "tournament_size":1,
        "fitness_name": "scalar_fitness"
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
        "function_evaluations": 100000,
        "crossover": AlgorithmOperators.sbx,
        "crossover_params": crossover_params,
        "mutation": AlgorithmOperators.mutpoly,
        "mutation_params": mutation_params,
        "rmp": rmp,
        "penalty_constant":10e+100,
        "selection":AlgorithmOperators.Single_BinaryTournament,
        "selection_params": selection_params,
        "t": 10,
        "e": 0.1
    }

    mtea = MFEARR.MFEARR(design)
    start = time.time()
    final_population, process = mtea.optimize(True)
    print("time:", time.time() - start)

    avg = [0, 0]
    num = [0, 0]
    for i in final_population:
        avg[i.skill_factor] += i.fitness
        num[i.skill_factor] += 1

    avg[0] = avg[0]/num[0]
    avg[1] = avg[1]/num[1]


    print(avg)




