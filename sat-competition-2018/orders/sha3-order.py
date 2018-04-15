#!/usr/bin/env python3

import hash_framework as hf
hf.config.model_dir = "/home/cipherboy/GitHub/sat/sat-competition-2018/models"

import time, sys, os

run = False
release = False
if '--run' in sys.argv:
    run = True
if '--release' in sys.argv:
    release = True
if '-h' in sys.argv or '--help' in sys.argv:
    print(sys.argv[0] + " [--run] [--release] [--args file] [w r o]")
    print('---')
    print("Generates models for benchmarking. Runs if specified, otherwise only creates models.")
    print("--run - runs the resulting CNF file")
    print("--release - deletes the intermediate stages after creation")
    print("--args file - specify a file to load arguments from")
    print("w - sha3 w")
    print("r - sha3 rounds format (str only)")
    print("o - expected order")
    sys.exit(0)

def sha3_prove_identity_args():
    r_args = sys.argv[1:]
    if run:
        r_args = r_args[1:]
    if release:
        r_args = r_args[1:]

    w = int(r_args[0])
    r = r_args[1].split('-')
    o = int(r_args[2])

    sha3_prove_identity(w, r, o)

def sha3_prove_identity_file():
    fname = sys.argv[-1]
    args = open(fname, 'r').read().split('\n')
    for s_arg in args:
        if len(s_arg) == 0:
            continue
        arg = s_arg.split(" ")
        w = int(arg[0])
        r = arg[1].split('-')
        o = int(arg[2])

        sha3_prove_identity(w, r, o)


def sha3_prove_identity(w, r, o):
    rounds = [r]*o

    algo = hf.algorithms.sha3(w=w, rounds=rounds)
    tag = "sha3-chi-identity-w" + str(w) + "-r" + ''.join(r) + '-o' + str(o)

    m = hf.models()
    m.start(tag, recreate=True)
    hf.models.vars.write_header()
    hf.models.generate(algo, ['h1'], rounds=rounds, bypass=True)
    hf.models.vars.write_assign(['cidentity'])

    cidentity = ['and']
    for i in range(0, 25*w):
        cidentity.append(('equal', 'h1in' + str(i), 'h1out' + str(i)))
    cidentity = ('not', tuple(cidentity))
    hf.models.vars.write_clause('cidentity', cidentity, '01-problem.txt')

    m.collapse()
    m.build()

    if run:
        t1 = time.time()
        res = m.run(count=1)
        t2 = (time.time() - t1)
        print("Run time: " + str(t2))
    if release:
        os.system("rm -rf *.txt *.bc *.concat *.out")
    print("")

if '--args' in sys.argv:
    sha3_prove_identity_file()
else:
    sha3_prove_identity_args()
