#!/bin/bash

prog='python3 sha3-order.py'
args='--release --run'
round="r"

# All UNSAT == correct order
for w in 1 2 4 8 16 32 64; do
    $prog $args $w $round $w
done

# ALL SAT == wrong order
#for w in 1 2 4 8 16 32 64; do
#    for o in `seq 1 $((3*w - 1))`; do
#        $prog $args $w $round $o
#    done
#done