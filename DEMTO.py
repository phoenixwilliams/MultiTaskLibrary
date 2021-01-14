import AlgorithmOperators
import random
from operator import attrgetter

class MTSolution:
    def __init__(self, genotype):

        self.genotype = genotype
        self.fitness = None

    def set_fitness(self, fitness):
        self.fitness = fitness

class Cluster:
    def __init__(self, population, task):
        self.population = population
        self.task = task
        self.center = None
        self.offspring_population = []

    def set_center(self, center):
        self.center = center


def initial_clusters(ntasks, dimension, size):

    population: Cluster = [None] * ntasks

    for t in range(ntasks):
        cluster_population: MTSolution = [None for _ in range(size)]
        for i in range(size):
            cluster_population[i] = MTSolution([random.random() for _ in range(dimension)])

        population[t] = Cluster(cluster_population, t)

    return population

def evaluate_solution(solution_geno, problem, bounds, dimension, penalty):
    raw_geno = AlgorithmOperators.map_back_and_clip(solution_geno, bounds, dimension)
    return problem(solution_geno)


def evaluate_population(population, problems, bounds, dimensions, penalty):

    for ci in population:
        for p in ci.population:
            if p.fitness is None:
                raw_geno = AlgorithmOperators.map_back_and_clip(p.genotype, bounds[ci.task], dimensions[ci.task])
                p.set_fitness(problems[ci.task](raw_geno))

        ci.set_center(min(ci.population, key=attrgetter('fitness')))

class DEMTO:

    def __init__(self, design):
        self.design = design



    def optimize(self, return_process):
        population = initial_clusters(self.design["K"], max(self.design["dimensions"]), self.design["N"])
        evaluate_population(population, self.design["problems"], self.design["bounds"],
                            self.design["dimensions"], self.design["penalty"])
        avg_task_fitness = [[] for _ in range(self.design["K"])]

        c_it = 0
        while c_it < self.design["function_evaluations"]-(self.design["N"]*self.design["K"]):
            for cj in population:
                mutant_vectors = [None] * self.design["N"]

                crs = [self.design["compute_cr"](**self.design["compute_cr_params"]) for _ in range(self.design["N"])]
                fs = [self.design["compute_f"](**self.design["compute_f_params"]) for _ in range(self.design["N"])]

                for tn in range(self.design["N"]):
                    # rand/1 mutant generator
                    x1, x2, x3 = random.choice(cj.population), random.choice(cj.population), random.choice(cj.population)
                    mutant_vectors[tn] = self.design["mutant_generator"](x1.genotype, x2.genotype, x3.genotype, fs[tn])

                if random.random() < self.design["rmp"]:
                    indices = random.sample(range(0, self.design["N"]), self.design["K"]-1)
                    tasks_left = [population[x] for x in range(0,self.design["K"]) if x != cj.task]

                    for i in range(len(indices)):
                        mutant_vectors[indices[i]] = tasks_left[i].center.genotype[:]

                for ti in range(self.design["N"]):
                    trial_vector = self.design["crossover"](cj.population[ti].genotype, mutant_vectors[ti],
                                                            crs[ti], self.design["bounds"][cj.task])
                    fitness = evaluate_solution(trial_vector, self.design["problems"][cj.task],
                                                self.design["bounds"][cj.task],
                                                self.design["dimensions"][cj.task], self.design["penalty"])

                    if fitness <= cj.population[ti].fitness:
                        cj.population[ti] = MTSolution(trial_vector)
                        cj.population[ti].set_fitness(fitness)

                cj.set_center(min(cj.population, key=attrgetter('fitness')))
                avg_task_fitness[cj.task].append(sum(x.fitness for x in cj.population)/self.design["N"])

                c_it += self.design["N"]

        if return_process:
            return population, avg_task_fitness
        else:
            return population