# Multi-Task Library

<br>
Author: Phoenix Williams, Univeristy of Exeter <br>
Email: pw384@exeter.ac.uk
<br>
<br>

## Library Outline:

### This repository is built and maintained as part of my PhD for educational purposes. The aim of this library is to implement algorithms that can be used easily by those without a high level of knowledge in this area and simply want to optimize functions. 

<br>

I designed this package to be as flexible as possible, that is the implementation should work with any operators/functions you implement within the algorithm. Each algorithm is built to fully designed using an input dictionary.

<br>

### <b>If this package is used in research or applied to publishable problems please reference. This package should not be used within any framework that earns financial gain.</b>


### MFEA: Evolutionary Multitasking for Single-objective Continuous Optimization: Benchmark Problems, Performance Metric, and Baseline Results. <br>
##### Bingshui Da, Yew-Soon Ong, Liang Feng, A.K. Qin, Abhishek Gupta,Zexuan Zhu, Chuan-Kang Ting, Ke Tang and Xin Yao

    - This algorithm is implemented within the YSOMultiTaskEA.py file, an example of how to use the package can be seen in the YSOMultiTaskEAexample.py file.

    - This algorithm requires no external libraries.

    - The algorithm takes 0.5 seconds for carry out 100 iterations of a 50-dimensinoal problem with a population of 100.

    - The algorithm returns population and if stated the average fitness of each task throughout the optimization process.

    - Each iteration calls the objective function 'offspring_popu_size' times
    


### BSMTO-I: A Novel Multi-Task Optimization Algorithm Based on the Brainstorming Process. <br>
#### Cheo Lyu, Yuhui Shi and Lijun Sun

    - This algorithm is implemented within the BSMTO.py file, an example of how to use the package can be seen in the BSMTO.py file.

    - This algorithm requires no external libraries

    - The algorithm takes 0.2 seconds to carry out 100 iterations of a 50-dimensional problem with a population of 100 and 50 offspring created at each iteration.

    - The implemented algorithm does not consist of the BFGS optimization algorithm (as included in the published paper). <br>
        Reason for this exclusion is that it would require an increased number function calls beyond what is detailed in the algorithm definition, this can be misleading.

    - Each iteration calls the objective function 'nk' times