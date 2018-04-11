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
    print(sys.argv[0] + " [--run] [--release] [--args file] [w r i o]")
    print('---')
    print("Generates models for benchmarking. Runs if specified, otherwise only creates models.")
    print("--run - runs the resulting CNF file")
    print("--release - deletes the intermediate stages after creation")
    print("--args file - specify a file to load arguments from")
    print("w - sha3 w")
    print("r - sha3 rounds format")
    print("i - input error")
    print("o - output error")
    sys.exit(0)

def sha3_differences_args():
    r_args = sys.argv[1:]
    if run:
        r_args = r_args[1:]
    if release:
        r_args = r_args[1:]

    w = int(r_args[0])
    r = r_args[1].split('-')
    i = int(r_args[2])
    o = int(r_args[3])

    sha3_differences(w, r, i, o)

def sha3_differences_file():
    fname = sys.argv[-1]
    args = open(fname, 'r').read().split('\n')
    for s_arg in args:
        if len(s_arg) == 0:
            continue
        arg = s_arg.split(" ")
        w = int(arg[0])
        r = arg[1].split('-')
        i = int(arg[2])
        o = int(arg[3])

        sha3_differences(w, r, i, o)


def sha3_differences(w, r, i, o):
    algo = hf.algorithms.sha3(w=w, rounds=r)
    tag = "sha3-families-w" + str(w) + "-r" + '-'.join(r) + "-i" + str(i) + "-o" + str(o)

    m = hf.models()
    m.start(tag, recreate=True)

    hf.models.vars.write_header()
    hf.models.generate(algo, ['h1', 'h2'], rounds=r, bypass=True)
    hf.models.vars.write_assign(['cinput', 'coutput'])

    tail = '*'*25*w
    cinput = hf.models.vars.differential(tail, 'h1in', 0, 'h2in', 0)
    hf.models.vars.write_range_clause('cinput', i, i, cinput, '50-input.txt')

    tail = '*'*25*w
    coutput = hf.models.vars.differential(tail, 'h1out', 0, 'h2out', 0)
    hf.models.vars.write_range_clause('coutput', o, o, coutput, '50-output.txt')


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
    sha3_differences_file()
else:
    sha3_differences_args()
