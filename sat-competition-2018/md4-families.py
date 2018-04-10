#!/usr/bin/env python3

import hash_framework as hf
hf.config.model_dir = "/home/cipherboy/GitHub/sat/sat-competition-2018/models"

import time, itertools
import sys

run = False
if len(sys.argv) >= 2 and sys.argv[1] == '--run':
    run = True
elif len(sys.argv) >= 2 and (sys.argv[1] == '--help' or sys.argv[1] == '-h'):
    print(sys.argv[0] + " [--run] r p [places]")
    print('---')
    print("Generates models for benchmarking. Runs if specified, otherwise just creates models.")
    print("r - number of rounds (multiple of 4, between 8 and 48 inclusive)")
    print("p - number of places (0 to r inclusive)")
    print("places - specific place (dash separated list)")
    sys.exit(0)

def md4_families():
    r_args = sys.argv[1:]
    if run:
        r_args = r_args[1:]

    r = int(r_args[0])
    p = int(r_args[1])

    if len(r_args) == 2:
        for places in itertools.combinations(list(range(0, r)), p):
            md4_family(r, p, places)
    else:
        places = tuple(map(int, r_args[2].split('-')))
        if p != len(places):
            print("p and places do not match: " + str(p) + " " + str(len(places)))
            sys.exit(1)
        md4_family(r, p, places)

def md4_family(r, p, places):
    algo = hf.algorithms.md4()
    algo.rounds = r
    tag = "md4-families-r" + str(r) + "-c" + str(p) + "-p" + str('-'.join(map(str, places)))

    m = hf.models()
    m.start(tag, recreate=True)

    hf.models.vars.write_header()
    hf.models.generate(algo, ['h1', 'h2'], rounds=r, bypass=True)
    hf.attacks.collision.write_constraints(algo)
    hf.attacks.collision.write_optional_differential(algo)
    hf.attacks.collision.write_same_state(algo)
    hf.models.vars.write_assign(['ccollision', 'cblocks', 'cstate', 'cdifferentials', 'cnegated', 'cspecific'])
    hf.attacks.collision.reduced.specified_difference(algo, places, "07-differential.txt")

    m.collapse()
    m.build()

    if run:
        t1 = time.time()
        res = m.run(count=1)
        t2 = (time.time() - t1)
        if res:
            result = m.results(algo)
            print(result[0])
        print("Run time: " + str(t2))
    print("")


md4_families()
