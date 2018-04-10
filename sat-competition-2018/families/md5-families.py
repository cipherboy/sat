#!/usr/bin/env python3

import hash_framework as hf
hf.config.model_dir = "/home/cipherboy/GitHub/sat/sat-competition-2018/models"

import time, itertools
import sys, os

run = False
release = False
if '--run' in sys.argv:
    run = True
elif '--release' in sys.argv:
    release = True
elif '-h' in sys.argv or '--help' in sys.argv:
    print(sys.argv[0] + " [--run] [--release] [--args file] [r p [places]]")
    print('---')
    print("Generates models for benchmarking. Runs if specified, otherwise only creates models.")
    print("--run - runs the resulting CNF file")
    print("--release - deletes the intermediate stages after creation")
    print("--args file - specify a file to load arguments from")
    print("r - number of rounds (multiple of 4, between 8 and 48 inclusive)")
    print("p - number of places (0 to r inclusive)")
    print("places - specific place (dash separated list)")
    sys.exit(0)

def md5_families_args():
    r_args = sys.argv[1:]
    if run:
        r_args = r_args[1:]

    r = int(r_args[0])
    p = int(r_args[1])

    if len(r_args) == 2:
        for places in itertools.combinations(list(range(0, r)), p):
            md5_family(r, p, places)
    else:
        places = tuple(map(int, r_args[2].split('-')))
        if p != len(places):
            print("p and places do not match: " + str(p) + " " + str(len(places)))
            sys.exit(1)
        md5_family(r, p, places)

def md5_families_file():
    fname = sys.argv[-1]
    args = open(fname, 'r').read().split('\n')
    for s_arg in args:
        if len(s_arg) == 0:
            continue
        arg = s_arg.split(" ")
        r = int(arg[0])
        p = int(arg[1])
        if len(arg) == 2:
            for places in itertools.combinations(list(range(0, r)), p):
                md5_family(r, p, places)
        else:
            places = tuple(map(int, arg[2].split('-')))
            md5_family(r, len(places), places)


def md5_family(r, p, places):
    algo = hf.algorithms.md5()
    algo.rounds = r
    tag = "md5-families-r" + str(r) + "-c" + str(p) + "-p" + str('-'.join(map(str, places)))

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
    if release:
        os.system("rm -rf *.txt *.bc *.concat *.out")
    print("")

if '--args' in sys.argv:
    md5_families_file()
else:
    md5_families_args()
