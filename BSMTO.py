import random
from operator import attrgetter
import AlgorithmOperators


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
        cluster_population: MTSolution = [None] * size
        for i in range(size):
            cluster_population[i] = MTSolution([random.random() for _ in range(dimension)])

        population[t] = Cluster(cluster_population, t)

    return population


def evaluate_population(population, problems, bounds, dimensions, penalty):

    for ci in population:
        if len(ci.offspring_population) > 0:
            ci.population.extend(ci.offspring_population)
            ci.offspring_population = []

        for p in ci.population:
            if p.fitness is None:
                raw_geno = AlgorithmOperators.map_back_and_clip(p.genotype, bounds[ci.task], dimensions[ci.task])
                p.set_fitness(problems[ci.task](raw_geno))

        ci.set_center(min(ci.population, key=attrgetter('fitness')))



def IBS(population, p3, crossover, crossover_params, mutations, mutations_params):
    spi = random.choice(population)
    mut_choice = random.randint(0, len(mutations)-1)

    if random.random() < p3:
        p1geno = random.choice(spi.population).genotype

        child1geno, child2geno = crossover(p1geno, spi.center.genotype, **crossover_params)
        child1geno, child2geno = mutations[mut_choice](child1geno, child2geno, **mutations_params[mut_choice])

        spi.offspring_population.extend([MTSolution(child1geno), MTSolution(child2geno)])


    else:
        p1geno, p2geno = random.choice(spi.population).genotype, random.choice(spi.population).genotype

        child1geno, child2geno = crossover(p1geno, p2geno, **crossover_params)
        child1geno, child2geno = mutations[mut_choice](child1geno, child2geno, **mutations_params[mut_choice])

        spi.offspring_population.extend([MTSolution(child1geno), MTSolution(child2geno)])


def CBS(population, crossover,  crossover_params, mutations, mutations_params):
    mut_choice = random.randint(0, len(mutations)-1)
    sp1, sp2 = random.choice(population), random.choice(population)
    #p1geno, p2geno = random.choice(sp1.population).genotype, random.choice(sp2.population).genotype
    p1geno, p2geno = random.choice(sp1.population).genotype, random.choice(sp2.population).genotype

    child1geno, child2geno = crossover(p1geno, p2geno, **crossover_params)
    child1geno, child2geno = mutations[mut_choice](child1geno, child2geno, **mutations_params[mut_choice])

    random.choice([sp1, sp2]).offspring_population.append(MTSolution(child1geno))
    random.choice([sp1, sp2]).offspring_population.append(MTSolution(child2geno))


class BSMTO:

    def __init__(self, design):
        self.design = design


    def optimize(self, return_process):

        avg_task_fitness = [[] for _ in range(self.design["K"])]

        population = initial_clusters(self.design["K"], max(self.design["dimensions"]), self.design["N"])
        evaluate_population(population, self.design["problems"], self.design["bounds"],
                            self.design["dimensions"], self.design["penalty"])

        c_it = 0
        while c_it < self.design["function_evaluations"]:
            for nki in range(0, self.design["nk"], 2):

                if random.random() < self.design["p2"]:
                    IBS(population, self.design["p3"], self.design["crossover"], self.design["crossover_params"],
                            self.design["mutations"], self.design["mutations_params"])

                else:
                    CBS(population, self.design["crossover"], self.design["crossover_params"],
                            self.design["mutations"], self.design["mutations_params"])

            c_it += self.design["nk"]
            evaluate_population(population, self.design["problems"], self.design["bounds"],
                                self.design["dimensions"], self.design["penalty"])

            for c in population:
                c.population = sorted(c.population, key=attrgetter('fitness'))[:self.design["N"]]
                avg_task_fitness[c.task].append(sum(i.fitness for i in c.population) / len(c.population))

        if return_process:
            return population, avg_task_fitness

        else:
            return population


