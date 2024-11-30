# Benchmark

## Setup
First step is to setup an `.env` file with the following Tokens set:
```
LUNA_ENCRYPTION_KEY="<YOUR ENCRYPTION KEY>"
LUNA_API_TOKEN="<YOUR API TOKEN>"
D_WAVE_TOKEN="<YOUR WAVE TOKEN>"
```

`lunaSolve.py` is a single benchmark run script.


## What to benchmark
### Solvers
Quantum:
- QA

Hybrid:
- QAGA+ (general non optimized solver)

Classic:
- SAGA+

### Versions
- glb file
- 1
- 2
- 3

### Columns
- 3
- 5
- 10
- 20

## Parameters
- `p_size`: This is the population size, which affects how many solutions are considered in each step of the algorithm.
- `mut_rate`: The mutation rate determines the chance of changes occurring in each solution per iteration.
- `rec_rate`: The recommendation rate decides how many pairings are made for creating new solutions.
