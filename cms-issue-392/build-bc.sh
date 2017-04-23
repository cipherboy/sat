#!/bin/bash

cat *.txt > problem.bc
#../tools/BCpackage-0.40/bc2cnf -nots -nocoi -nosimplify ./problem.bc problem.cnf
../tools/BCpackage-0.40/bc2cnf ./problem.bc problem.cnf
head -n 10 ./problem.cnf
grep 'p cnf' ./problem.cnf
notify-send "Done building CNF" || true
