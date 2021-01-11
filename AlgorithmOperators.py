import random
from operator import attrgetter
import NumericalFunctions


def BinaryTournament(population, tournament_size, fitness_name):
    """
    Binary Tournament Selection
    :param population:
    :param tournament_size:
    :return:
    """
    tournament_1 = [random.choice(population) for i in range(tournament_size)]
    tournament_2 = [random.choice(population) for i in range(tournament_size)]

    parent1 = min(tournament_1, key=attrgetter(fitness_name))
    parent2 = min(tournament_2, key=attrgetter(fitness_name))

    return parent1, parent2

def Single_BinaryTournament(population, tournament_size, fitness_name):
    """
    Binary Tournament Selection that returns a single solution
    :param population:
    :param tournament_size:
    :return:
    """
    tournament_1 = [random.choice(population) for _ in range(tournament_size)]
    parent1 = min(tournament_1, key=attrgetter(fitness_name))

    return parent1

def mutGaussian(parent1geno, parent2geno, sigma, pm, length):
    """
    :param parent1geno:
    :param parent2geno:
    :param sigma:
    :param pm:
    :return:
    """
    rs = [random.random() for _ in range(length)]
    child1geno = parent1geno[:]
    child2geno = parent2geno[:]

    for c in range(length):
        if rs[c] < pm:
            child1geno[c] += random.normalvariate(0,sigma)
            child2geno[c] += random.normalvariate(0, sigma)

    return child1geno, child2geno

def mutpoly(parent1geno, parent2geno, pm, nm, diffmut, length):
    """
    Polynomial Mutation
    :param parent1geno:
    :param parent2geno:
    :param pm:
    :param nm:
    :param diffmut:
    :param length:
    :return:
    """

    rs = [random.random() for _ in range(length)]
    ris = [random.random() for _ in range(length)]
    child1geno = parent1geno[:]
    child2geno = parent2geno[:]

    for c in range(length):
        if rs[c] < pm:
            deltai = (2 * ris[c]) ** (1 / (nm + 1)) - 1 if ris[c] < 0.5 else 1 - (2 * (1 - ris[c])) ** (1 / (nm + 1))
            child1geno[c] = parent1geno[c] + diffmut * deltai
            child2geno[c] = parent2geno[c] + diffmut * deltai

    return child1geno, child2geno


def sbx(parent1geno, parent2geno, pc, nc, length):
    """
    SBX crossover operator
    :param parent1geno:
    :param parent2geno:
    :param pc:
    :param nc:
    :param length:
    :return:
    """
    rs = [random.random() for _ in range(length)]
    uis = [random.random() for _ in range(length)]
    child1geno = parent1geno[:]
    child2geno = parent1geno[:]
    for g1, g2, c in zip(parent1geno, parent2geno, range(length)):
        if rs[c] < pc:
            bqi = (2 * uis[c]) ** (1 / (nc + 1)) if uis[c] < 0.5 else (1 / (2 * (1 - uis[c]))) ** (1 / (nc + 1))

            child1geno[c] = 0.5 * ((1 + bqi) * g1 + (1 - bqi) * g2)
            child2geno[c] = 0.5 * ((1 - bqi) * g1 + (1 + bqi) * g2)

    return child1geno, child2geno



def map_back(genotype, bounds, dimension):

    """
    Function maps solution to original search space
    :param genotype: solution decision variables
    :param bounds: problem bounds
    :param dimension: problem dimensions
    :return: mapped back genotype
    """

    mb_geno:float = [None]*dimension
    violation = 0
    for x, i in zip(genotype[:dimension], range(dimension)):
        term = x * (bounds[1] - bounds[0]) + bounds[0]


        #if bounds[0] > term:
        #    violation += abs(bounds[0] - term)
        #if bounds[1] < term:
        #    violation += abs(bounds[1] - term)

        mb_geno[i] = term

    return mb_geno[:dimension], violation

def de_rand_1(population, F, bounds):
    """
    This function is a DE function that returns a mutant vector genotype using
    v = x1 + F * (x2 - x3) for x1, x2 and x3 to be randomly selected solution genotypes
    :param population: Population of MTSolutions, we can acces the genotype using a.genotype
    with a being an MTSolution object.
    :return: Mutant vector genotype, not MTSolution because different algorithms have
    different MTSolution objects, but all have a genotype property.
    """

    x1, x2 , x3 = random.choice(population).genotype, random.choice(population).genotype,random.choice(population).genotype

    mutant_genotype: float = [None] * len(x1)
    for i in range(len(mutant_genotype)):
        mutant_genotype[i] = x1[i] + F * (x2[i] - x3[i])
        if mutant_genotype[i] < bounds[0]:
            mutant_genotype[i] = (bounds[0] + mutant_genotype[i]) / 2

        if mutant_genotype[i] > bounds[1]:
            mutant_genotype[i] = (bounds[1] + mutant_genotype[i]) / 2

    return mutant_genotype


def de_best_1(population, F, bounds):
    """
    This function is a DE function that returns a mutant vector genotype using
    v = x1 + F * (x2 - x3) for x1, x2 and x3 to be randomly selected solution genotypes
    :param population: Population of MTSolutions, we can acces the genotype using a.genotype
    with a being an MTSolution object.
    :return: Mutant vector genotype, not MTSolution because different algorithms have
    different MTSolution objects, but all have a genotype property.
    """
    x1, x2 , x3 = min(population, key=attrgetter('fitness')).genotype, random.choice(population).genotype,random.choice(population).genotype

    mutant_genotype:float = [None] * len(x1)
    for i in range(len(mutant_genotype)):
        mutant_genotype[i] = x1[i] + F * (x2[i] - x3[i])
        if mutant_genotype[i] < bounds[0]:
            mutant_genotype[i] = (bounds[0] + mutant_genotype[i]) / 2

        if mutant_genotype[i] > bounds[1]:
            mutant_genotype[i] = (bounds[1] + mutant_genotype[i]) / 2

    return mutant_genotype


def de_binomial_crossover(parent1geno, mutantgeno, CR, bounds):
    offspring_genotype = parent1geno[:]
    randj = random.randint(0, len(parent1geno)-1)
    rands = [random.random() for _ in range(len(parent1geno))]

    for i in range(len(parent1geno)):

        if rands[i] < CR or i == randj:
            offspring_genotype[i] = mutantgeno[i]

        if offspring_genotype[i] < bounds[0]:
            offspring_genotype[i] = bounds[0]
        if offspring_genotype[i] > bounds[1]:
            offspring_genotype[i] = bounds[1]

    return offspring_genotype


def compute_cr(mean, sigma):
    return random.normalvariate(mean, sigma)


def compute_f(t, s):
    f = NumericalFunctions.cauchy_distribution(random.uniform(0, 1), t, s)
    return f


def get_f(f):
    return f





