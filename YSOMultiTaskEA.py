import random
from operator import attrgetter
import AlgorithmOperators

class MTsolution:

    def __init__(self, genotype, skill_factor):
        self.genotype = genotype
        self.skill_factor = skill_factor
        self.scalar_fitness = None
        self.fitness = None

    def set_fitness(self, sf):
        self.fitness = sf

    def set_scalar_fitness(self, sf):
        self.scalar_fitness = sf


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

        mtsolution_popualtion[j] = MTsolution(genotype_population[j], tj)

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
            raw_geno, violation = AlgorithmOperators.map_back(p.genotype, bounds[p.skill_factor], dimensions[p.skill_factor])
            fitness = problems[p.skill_factor](raw_geno) + violation*penalty_constant
            p.set_fitness(fitness)


        task_population[p.skill_factor].append(p)

    for subpop in task_population:
        # rank sub-population
        ordered_subpop = sorted(subpop, key=attrgetter('fitness'))

        for rank in range(1, len(subpop)+1):
            ordered_subpop[rank-1].set_scalar_fitness(1/rank)




def generate_child(parent1, parent2, crossover, crossover_params, mutation, mutation_params, rmp):

    p1geno, p2geno, tj1, tj2 = parent1.genotype, parent2.genotype, parent1.skill_factor, parent2.skill_factor


    if tj1==tj2 or random.random() < rmp:
        child1geno, child2geno = crossover(p1geno,p2geno, **crossover_params)
        child1geno,child2geno = mutation(child1geno, child2geno, **mutation_params)

        return MTsolution(child1geno, random.choice([tj1, tj2])), MTsolution(child2geno, random.choice([tj1, tj2]))

    else:
        child1geno, child2geno = mutation(p1geno[:], p2geno[:], **mutation_params)
        return MTsolution(child1geno, tj1), MTsolution(child2geno, tj2)



class MTEA:
    def __init__(self, design):
        self.design = design


    def optimize(self, return_process):
        """
        Minimizes problems
        :return: final population and avergage iteration fitntess of each task
        """

        avg_task_fitness = [[] for _ in range(self.design["K"])]

        # initial population
        population = initial_solution_population(max(self.design["dimensions"]), self.design["size"], self.design["K"])
        evaluate_population(population, self.design["problems"], self.design["bounds"],
                            self.design["dimensions"], self.design["penalty_constant"])

        offspring_pop_size = self.design["offspring_pop_size"]
        offsprings: MTsolution = [None] * offspring_pop_size
        for i in range(self.design["iterations"]):

            # store task average fitness
            temp_tasks_fitness = [0 for _ in range(self.design["K"])]
            num_solutions = [0 for _ in range(self.design["K"])]

            for p in population:
                temp_tasks_fitness[p.skill_factor] += p.fitness
                num_solutions[p.skill_factor] += 1

            for t in range(len(num_solutions)):
                avg_task_fitness[t].append(temp_tasks_fitness[t] / num_solutions[t])


            parents = [[self.design["selection"](population, **self.design["selection_params"]),self.design["selection"](population, **self.design["selection_params"])]
                       for _ in range(offspring_pop_size)]

            for j in range(0, offspring_pop_size, 2):
                offsprings[j], offsprings[j+1] = generate_child(parents[j][0], parents[j][1], self.design["crossover"],
                                                                self.design["crossover_params"], self.design["mutation"],
                                                                self.design["mutation_params"], self.design["rmp"])


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

        for t in range(len(num_solutions)):
            avg_task_fitness[t].append(temp_tasks_fitness[t] / num_solutions[t])

        if return_process:
            return population, avg_task_fitness

        else:
            return population