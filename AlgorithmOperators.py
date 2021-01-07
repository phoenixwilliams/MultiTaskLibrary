import random
from operator import attrgetter


def BinaryTournament(population, tournament_size):
    """
    Binary Tournament Selection
    :param population:
    :param tournament_size:
    :return:
    """
    tournament_1 = [population[random.randint(0, len(population) - 1)] for i in range(tournament_size)]
    tournament_2 = [population[random.randint(0, len(population) - 1)] for i in range(tournament_size)]

    parent1 = min(tournament_1, key=attrgetter('scalar_fitness'))
    parent2 = min(tournament_2, key=attrgetter('scalar_fitness'))

    return parent1, parent2


def mutGaussian(parent1geno, parent2geno, mean, sigma, pm, length):
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

        if bounds[0] > term:
            violation += abs(bounds[0] - term)
        if bounds[1] < term:
            violation += abs(bounds[1] - term)

        mb_geno[i] = term

    return mb_geno[:dimension], violation