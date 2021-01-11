import math
import numpy as np

def sphere(x, opt):
    return sum([(x[i]-opt[i])**2 for i in range(len(x))])


def rosenbrock(x):

    sum1=0
    for i in range(len(x)-1):
        sum1 += (100 * (x[i+1] - (x[i]**2))**2 + (x[i] - 1)**2)

    return sum1


def ackley(x, M, opt):

    a = 0
    b = 0
    x = np.dot(x, M)
    for i in range(len(x)):
        xi = x[i] - opt[i]
        a += xi**2
        b += math.cos(2*math.pi*xi)

    a = -0.2 * math.sqrt(a / len(x))
    b = b / len(x)

    return -20 * math.exp(a) - math.exp(b) + 20 + math.exp(1)


def rastrigin(x, M, opt):

    a = 0
    x = np.dot(x, M)
    for i in range(len(x)):
        xi = x[i]-opt[i]
        a += (xi**2 - 10*math.cos(2*math.pi*xi) + 10)

    return a


def griewank(x, M, opt):
    a = 0
    b = 1
    x = np.dot(x, M)
    for i in range(0, len(x)):
        xi = x[i]-opt[i]
        a += xi**2
        b = b * math.cos(xi/math.sqrt(i+1))

    return 1 + (1/4000)*a - b


def wierestrass(x, M, opt):

    a = 0.5
    b = 3
    kmax = 20
    term1 = 0
    x = np.dot(x,M)
    for i in range(len(x)):
        xi = x[i]-opt[i]
        term1 += sum([a**k * math.cos(2 * math.pi * (b**k) * (xi + 0.5)) for k in range(kmax)])

    term1 = term1 - len(x) * sum([a**k * math.cos(2*math.pi*0.5*(b**k)) for k in range(kmax)])
    return term1


def schwefel(x, a):
    # a = 418.9829

    term1 = 0
    for xi in x:
        term1 += (xi * math.sin(abs(xi)**0.5))

    return a * len(x) - term1
