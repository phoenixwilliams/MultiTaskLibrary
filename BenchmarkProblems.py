import math

def sphere(x):
    return sum([xi**2 for xi in x])



def rosenbrock(x):

    sum1=0
    for i in range(len(x)-1):
        sum1 += 100*((x[i+1] - (x[i]**2))**2 + (x[i] - 1)**2)

    return sum1


def ackley(x):

    a = 0
    b = 0
    for xi in x:
        a += xi**2
        b += math.cos(2*math.pi*xi)

    a = -0.2 * math.sqrt(a / len(x))
    b = b / len(x)

    return -20 * math.exp(a) - math.exp(b) + 20 + math.exp(1)




def rastrigin(x):

    a = 10*len(x)
    for xi in x:
        a += (xi**2 - 10*math.cos(2.0*math.pi*xi))

    return a


def griewank(x):
    a = 0
    b = 1
    for i in range(len(x)):
        xi = x[i]
        a += xi**2
        b = b * math.cos(xi/math.sqrt(i+1))

    return 1 + (1/4000)*a - b


def wierestrass(x):

    a = 0.5
    b = 3
    kmax = 20
    term1 = 0
    for xi in x:
        term1 += sum([a**k * math.cos(2 * math.pi * (b**k) * (xi + 0.5)) for k in range(kmax)])

    term1 = term1 - len(x) * sum([a**k * math.cos(2*math.pi*0.5*(b**k)) for k in range(kmax)])
    return term1


def schwefel(x):

    term1 = 0
    for xi in x:
        term1 += xi * math.sin(math.sqrt(math.fabs(xi)))

    return (418.9829 * len(x)) - term1
