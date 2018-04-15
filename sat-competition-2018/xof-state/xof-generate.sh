#!/bin/bash

prog='python3 sha3-xof.py'
args='--release'

for w in 1 2 4 8; do
    for r in `seq 1 24 3`; do
        for em in 256 512; do
            for s in 1 4 7 24; do
                $prog $args $w $r $em $s
            done
        done
    done
done
