
class Problem:

    def __init__(self, function, function_params):
        self.function = function
        self.function_params = function_params

    def __call__(self, x):

        return self.function(x, **self.function_params)