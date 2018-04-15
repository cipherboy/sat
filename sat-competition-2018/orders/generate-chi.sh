#!/bin/bash

prog='python3 sha3-order.py'
args='--release --run'

# All UNSAT == correct order
$prog $args 1 c 4
$prog $args 2 c 4
$prog $args 4 c 4
$prog $args 8 c 4
$prog $args 16 c 4
$prog $args 32 c 4
$prog $args 64 c 4

# ALL SAT == wrong order
$prog $args 1 c  1
$prog $args 2 c  1
$prog $args 4 c  1
$prog $args 8 c  1
$prog $args 16 c 1
$prog $args 32 c 1
$prog $args 64 c 1
$prog $args 1 c  2
$prog $args 2 c  2
$prog $args 4 c  2
$prog $args 8 c  2
$prog $args 16 c 2
$prog $args 32 c 2
$prog $args 64 c 2
$prog $args 1 c  3
$prog $args 2 c  3
$prog $args 4 c  3
$prog $args 8 c  3
$prog $args 16 c 3
$prog $args 32 c 3
$prog $args 64 c 3
