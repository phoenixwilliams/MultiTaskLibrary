import math

def cauchy_distribution(x, t, s):

    return 1 / (math.pi * s * (1 + ((x-t)/s)**2))




def gradient_vector_approximate(x, problem, step_size):
    gradient_vector: float = [None] * len(x)

    for i in range(len(x)):
        temp_x = x[:]
        temp_x[i] += step_size
        gradient_vector[i] = (problem(temp_x) - problem(x)) / step_size

    return gradient_vector


def print_matrix(Title, M):
    print(Title)
    for row in M:
        print([round(x,3)+0 for x in row])


def print_matricies(Action, Title1, M1, Title2, M2):
    print(Action)
    print(Title1, '\t'*int(len(M1/2) + "\t"*len(M1), Title2))
    for i in range(len(M1)):
        row1 = ['{0:+7.3f}'.format(x) for x in M1[i]]
        row2 = ['{0:+7.3f}'.format(x) for x in M2[i]]
        print(row1, '\t', row2)


def zeros_matrix(rows, cols):
    a: float = [[None for _ in range(rows)] for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            a[i][j] = 0.0
    return a


def copy_matrix(M):
    a: float = [None] * len(M)
    for i in range(len(M)):
        a[i] = M[i][:]

    return a


def matrix_multiply(A, B):

    rowsa, colsa, rowsb, colsb = len(A), len(A[0]), len(B), len(B[0])

    assert colsa == colsb, f"{colsa} != {colsb}"
    c = zeros_matrix(rowsa, colsb)

    for i in range(rowsa):
        for j in range(colsb):
            total = 0
            for ii in range(colsa):
                total += A[i][ii] * B[ii][j]
            c[i][j] = total

    return c


def inverse_matrix(M):
    mc = copy_matrix(M)
    im = zeros_matrix(len(M), len(M[0]))

    for i in range(len(im)):
        im[i][i] = 1.0

    n = len(mc)
    indices = list(range(n))
    for fd in range(0, n):
        fdScaler = 1.0 / mc[fd][fd]

        for j in range(n):
            mc[fd][j] *= fdScaler
            im[fd][j] *= fdScaler


        # operate on all rows but fd row
        for i in indices[:fd] + indices[fd+1:]:
            crScaler = mc[i][fd]
            for j in range(n):
                mc[i][j] = mc[i][j] - crScaler * mc[fd][j]
                im[i][j] = im[i][j] - crScaler * im[fd][j]
    return im


def identity_matrix(size):
    a = zeros_matrix(size, size)

    for i in range(size):
        a[i][i] = 1.0

    return a







