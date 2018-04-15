#!/bin/bash

prog='python3 sha3-order.py'
args='--release'
round="p-c"

# All UNSAT == correct order
for w in 1 2 4 8 16 32 64; do
    $prog $args $w $round 24
done

# ALL SAT == wrong order
for w in 1 2 4 8 16 32 64; do
    for o in `seq 1 23`; do
        $prog $args $w $round $o
    done
done
