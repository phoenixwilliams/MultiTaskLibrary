import math

def sphere(x):
    return sum([xi**2 for xi in x])



def rosenbrock(x):

    sum1=0
    for i in range(len(x)-1):
        sum1 += (100 * (x[i]**2 - x[i+1])**2 + (x[i] - 1)**2)

    return sum1


def ackley(x):

    a = 0
    b = 0
    for xi in x:
        a += (xi ** 2)
        b += math.cos(2*math.pi*xi)


    a = -0.2 * math.sqrt(a / len(x))
    b = b / len(x)

    return -20 * math.exp(a) - math.exp(b) + 20 + math.exp(1)




def rastrigin(x):

    a = 0
    for xi in x:
        a += (xi**2 - 10*math.cos(2*math.pi*xi) + 10)

    return a


def griewank(x):

    a = 0
    b = 1

    for i in range(0, len(x)):
        a += x[i]**2
        b = b * math.cos(x[i]/math.sqrt(i+1))

    return 1 + (1/4000)*a - b


def wierestrass(x):

    a = 0.5
    b = 3
    kmax = 20
    term1 = 0
    for i in range(len(x)):
        term1 += sum([a**k * math.cos(2 * math.pi * b**k * (x[i] + 0.5)) for k in range(kmax)])

    term2 = len(x) * sum([a**k * math.cos(2*math.pi*0.5*b**k) for k in range(kmax)])
    return term1 - term2


def schwefel(x):

    term1 = 0
    for xi in x:
        term1 += xi * math.sin(abs(xi)**0.5)

    return 418.9829 * len(x) - term1
