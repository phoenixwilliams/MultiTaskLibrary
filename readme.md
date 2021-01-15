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

    - The algorithm returns population and if stated the average fitness of each task throughout the optimization process.

    - Each iteration calls the objective function 'offspring_popu_size' times
    


### BSMTO-I: A Novel Multi-Task Optimization Algorithm Based on the Brainstorming Process. <br>
#### Cheo Lyu, Yuhui Shi and Lijun Sun

    - This algorithm is implemented within the BSMTO.py file, an example of how to use the package can be seen in the BSMTO.py file.

    - This algorithm requires no external libraries

    - The implemented algorithm does not consist of the BFGS optimization algorithm (as included in the published paper). <br>
        Reason for this exclusion is that it would require an increased number function calls beyond what is detailed in the algorithm definition, this can be misleading.

    - Each iteration calls the objective function 'nk' times


### DEMOTO: Differential Evolutionary Multi-task Optimization. <br>
#### Xiaolong Zheng, Yu Lei, A. K. Qin, Deyun Zhou, Jiao Shi and Maoguo Gong

    - This algorithm is implemented within the DEMOTO.py file, an example of how to use the package for this algorithm <br>
        can be seen in DEMOTOexample.py.

    - This algorithm requires no external libraries

    - The algorithm maintains ntasks amount of populations, and evolves each population using a standard DE method with a <br>
        probability of rmp of selecting the best performing solution from other task populations at mutant vectors within <br>
        each task population. 

    - Current implementation defines the F and CR values using a distribution, a standard value for both can be generated <br>  
        by simply defining a function that returns its value, e.g. AlgorithmOperators.get_f.

### MFEARR: Parting Ways and Reallocating Resources in Evolutionary Multitasking. <br>
#### Yu-Wei Wen and Chuan-Kang Ting

    -This algorithm is implemented within the MFEARR.py file, an exmaple of how to use the package for this algorithm <br>
        can be seen in MFEARRexample.py

    - This algroithm requires no external libraries

    - This algorithm follows the exact procecudre as MFEA apart from a single feature. MFEARR keeps track of the number <br>
        of inter-task offsprings that successfully make it to the next generation. If the average number of sucessful <br>
        inter-task offsprings drop below a given value e then the rmp value is set to 0.