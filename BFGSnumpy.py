import numpy as np
import NumericalFunctions


class BFGS:
    """
    This class implements the BFGS algorithm making use of numpy library for matrix processing.
    """

    def __init__(self, design):
        self.design = design

    def optimize(self, initial_solution, problem):

        x = np.array(initial_solution)
        #initial steps
        b = np.eye(len(initial_solution))
        g = np.array(self.design["gradient_computer"](list(x), problem, **self.design["gradient_computer_params"])).T

        for i in range(self.design["iterations"]):

            s = -1.0 * np.dot(np.linalg.inv(b), g)

            xnew = x + self.design["alpha"] * s
            gnew = np.array(self.design["gradient_computer"](list(xnew), problem, **self.design["gradient_computer_params"])).T

            sigma = xnew - x

            if (all(sig < self.design["tolerence"] for sig in sigma)):
                return xnew

            y = gnew - g
            gradb = ((np.outer(y.T, y) / np.dot(sigma, y.T))) - (np.dot(b,np.dot(np.outer(sigma.T,sigma), b)) / np.dot(sigma,(np.dot(b, sigma.T))))

            b = b + gradb

            x = xnew


        s = -1.0 * np.dot(np.linalg.inv(b), g)
        xnew = x + self.design["alpha"] * s

        return xnew


















