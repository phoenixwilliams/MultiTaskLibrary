import random
from operator import attrgetter
import AlgorithmOperators

class MTsolution:

    def __init__(self, genotype, skill_factor, divergent_offspring):
        self.genotype = genotype
        self.skill_factor = skill_factor
        self.scalar_fitness = None
        self.fitness = None
        self.divergent_offspring = divergent_offspring

    def set_fitness(self, sf):
        self.fitness = sf

    def set_scalar_fitness(self, sf):
        self.scalar_fitness = sf

    def set_divergent_offspring(self, do):
        self.divergent_offspring = do

def initial_poplation_genotypes(dimension, size):
    """
    Generated initial population in unified search space using random keys
    :param dimension: problem dimension
    :param size: size of population
    :return: population of genotypes
    """
    population: list = [None] * size
    for i in range(size):
        population[i] = [random.random() for _ in range(dimension)]

    return population


def initial_solution_population(dimension, size, K):
    """
    :param dimension: dimension of the problem
    :param size: Size of the population
    :param K: number of tasks
    :return:
    """

    genotype_population = initial_poplation_genotypes(dimension, size)
    mtsolution_popualtion: MTsolution = [None] * size

    # assign skill factor
    for j in range(size):
        tj = (j % K)

        mtsolution_popualtion[j] = MTsolution(genotype_population[j], tj, False)

    return mtsolution_popualtion


def evaluate_population(population, problems, bounds, dimensions, penalty_constant):
    """
    Function evaluations a population for each task
    :param population: Population of Solutions
    :param problems: Arrays of problems
    :param bounds: Array of problem bounds
    :param dimensions: Array of problem dimensions
    :param penalty_constant: Penalty multiplied to the combined violation of a solution
    :return: Null
    """


    task_population = [[] for _ in range(len(problems))]

    for p in population:
        if p.fitness == None:
            raw_geno = AlgorithmOperators.map_back_and_clip(p.genotype, bounds[p.skill_factor], dimensions[p.skill_factor])
            fitness = problems[p.skill_factor](raw_geno)
            p.set_fitness(fitness)


        task_population[p.skill_factor].append(p)

    for subpop in task_population:
        # rank sub-population
        ordered_subpop = sorted(subpop, key=attrgetter('fitness'))

        for rank in range(1, len(subpop)+1):
            ordered_subpop[rank-1].set_scalar_fitness(1/rank)




def generate_child(parent1, parent2, crossover, crossover_params, mutation, mutation_params, rmp, divergents):

    p1geno, p2geno, tj1, tj2 = parent1.genotype, parent2.genotype, parent1.skill_factor, parent2.skill_factor


    if tj1==tj2:
        child1geno, child2geno = crossover(p1geno,p2geno, **crossover_params)
        child1geno, child2geno = mutation(child1geno, child2geno, **mutation_params)

        return MTsolution(child1geno, random.choice([tj1, tj2]), False), \
               MTsolution(child2geno, random.choice([tj1, tj2]), False)

    elif random.random() < rmp:
        divergents += 1
        child1geno, child2geno = crossover(p1geno, p2geno, **crossover_params)
        child1geno, child2geno = mutation(child1geno, child2geno, **mutation_params)

        return MTsolution(child1geno, random.choice([tj1, tj2]), True),\
               MTsolution(child2geno, random.choice([tj1, tj2]), True)


    else:
        child1geno, child2geno = mutation(p1geno[:], p2geno[:], **mutation_params)
        return MTsolution(child1geno, tj1, False), MTsolution(child2geno, tj2, False)



class MFEARR:
    def __init__(self, design):
        self.design = design


    def optimize(self, return_process):
        """
        Minimizes problems
        :return: final population and avergage iteration fitntess of each task
        """

        avg_task_fitness = [[] for _ in range(self.design["K"])]

        # ASRD values
        asrds: float = []

        # initial population
        population = initial_solution_population(max(self.design["dimensions"]), self.design["size"], self.design["K"])
        evaluate_population(population, self.design["problems"], self.design["bounds"],
                            self.design["dimensions"], self.design["penalty_constant"])

        offspring_pop_size = self.design["offspring_pop_size"]
        offsprings: MTsolution = [None] * offspring_pop_size
        c_it = self.design["size"]
        generation = 0
        while c_it < self.design["function_evaluations"]:
            # number of divergents created
            num_divergents = 0

            # divergents survived
            divergents_survived = 0

            # store task average fitness
            temp_tasks_fitness = [0 for _ in range(self.design["K"])]
            num_solutions = [0 for _ in range(self.design["K"])]

            for p in population:
                temp_tasks_fitness[p.skill_factor] += p.fitness
                num_solutions[p.skill_factor] += 1

            for t in range(len(num_solutions)):
                avg_task_fitness[t].append(temp_tasks_fitness[t] / num_solutions[t])


            parents = [[self.design["selection"](population, **self.design["selection_params"]),self.design["selection"](population, **self.design["selection_params"])] for _ in range(offspring_pop_size)]

            for j in range(0, offspring_pop_size, 2):
                offsprings[j], offsprings[j+1] = generate_child(parents[j][0], parents[j][1], self.design["crossover"],
                                                                self.design["crossover_params"], self.design["mutation"],
                                                                self.design["mutation_params"], self.design["rmp"],
                                                                num_divergents)


            population = population + offsprings
            evaluate_population(population, self.design["problems"], self.design["bounds"],self.design["dimensions"],
                                self.design["penalty_constant"])
            population = sorted(population, key=attrgetter('scalar_fitness'), reverse=True)[0:self.design["size"]]

            # store task average fitness
            temp_tasks_fitness = [0 for _ in range(self.design["K"])]
            num_solutions = [0 for _ in range(self.design["K"])]

            for p in population:
                temp_tasks_fitness[p.skill_factor] += p.fitness
                num_solutions[p.skill_factor] += 1
                if p.divergent_offspring:
                    p.set_divergent_offspring(False)
                    divergents_survived += 1

            for t in range(len(num_solutions)):
                avg_task_fitness[t].append(temp_tasks_fitness[t] / num_solutions[t])

            if num_divergents > 0:
                asrds.append(divergents_survived / num_divergents)

                if generation > self.design["t"]:
                    asrd = sum(asrds[generation-t:])

                    if asrd < self.design["e"]:
                        self.design["rmp"] = 0

            c_it += self.design["offspring_pop_size"]
            generation += 1

        if return_process:
            return population, avg_task_fitness

        else:
            return population