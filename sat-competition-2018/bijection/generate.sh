#!/bin/bash

prog="python3 ./sha3-bijection.py"
args="--release --run"

for w in 1 2 4 8 16 32 64; do
    for rs in t r p c; do
        $prog $args $w $rs
    done
done
