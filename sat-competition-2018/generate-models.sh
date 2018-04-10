#!/bin/bash

rm -rf models
mkdir -p models

python3 sha3-chi-order.py
python3 sha3-theta-order.py

# See md4-families.args for possible argument values which produce SAT/UNSAT
# with estimated timings.

# Else for a large series of benchmarks, run something like the following:
# (has many easy SAT/UNSAT mixed in with harder instances)

# python3 md4-families.py 28 4
