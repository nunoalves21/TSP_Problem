# Travel Salesman Problem

Travel Salesman Problem solved using Evolutionary Algorithms.



The program was developed for Intelligent Systems for Bioinformatics class of Bioinformatics Masters in University of Minho.



## Authors

Nuno Alves

Raquel Cardoso

Tiago Oliveira



## Requirements

The program requires:

1. tqdm

   ```
   pip install tqdm
   ```

   

2. numpy

```
pip install numpy
```





## Usage

```
usage: tsp.py [-h] [-f FILE] [-i ITER] [-p POP_SIZE]
              [-m {mutation,crossover,mixed}] [-e {True,False}]

Travel Salesman problem with Evolutionary Algorithms

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  .tsp file
  -i ITER, --iter ITER  number of iterations
  -p POP_SIZE, --pop_size POP_SIZE
                        Population size
  -m {mutation,crossover,mixed}, --method {mutation,crossover,mixed}
                        Method of evolutionary algorithm
  -e {True,False}, --elitistm {True,False}
                        Run with elitism
```



## Example

Default run with elitism

```
python tsp.py -e True
```

