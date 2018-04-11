#!/usr/bin/env python3

import hash_framework as hf
hf.config.model_dir = "/home/cipherboy/GitHub/sat/sat-competition-2018/models"

import time
import sys

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

def sha3_bijection_args():
    r_args = sys.argv[1:]
    if run:
        r_args = r_args[1:]
    if release:
        r_args = r_args[1:]

    w = int(r_args[0])
    r = r_args[1].split('-')
    sha3_bijection(w, r)

def sha3_bijection_file():
    pass

# Shows that chi^4 is the identity function
def sha3_bijection(w, r):
    algo = hf.algorithms.sha3(w=w, rounds=r)
    tag = "sha3-bijection-w" + str(w) + "-r" + "-".join(r)

    m = hf.models()
    m.start(tag, recreate=True)
    hf.models.vars.write_header()
    hf.models.generate(algo, ['h1', 'h2'], rounds=r, bypass=True)
    hf.models.vars.write_assign(['cbijection'])

    cinin = ['and']
    for i in range(0, 25*w):
        cinin.append(('equal', 'h1in' + str(i), 'h2in' + str(i)))
    cinin = ('not', tuple(cinin))
    hf.models.vars.write_clause('cinin', cinin, '02-inin.txt')
    cinout = ['and']
    for i in range(0, 25*w):
        cinout.append(('equal', 'h1out' + str(i), 'h2out' + str(i)))
    cinout = tuple(cinout)
    hf.models.vars.write_clause('cinout', cinout, '02-inout.txt')

    csurin = ['and']
    for i in range(0, 25*w):
        csurin.append(('equal', 'h1in' + str(i), 'h2in' + str(i)))
    csurin = tuple(csurin)
    hf.models.vars.write_clause('csurin', csurin, '02-surin.txt')
    csurout = ['and']
    for i in range(0, 25*w):
        csurout.append(('equal', 'h1out' + str(i), 'h2out' + str(i)))
    csurout = ('not', tuple(csurout))
    hf.models.vars.write_clause('csurout', csurout, '02-surout.txt')

    cinjection = ('and', 'cinin', 'cinout')
    csurjection = ('and', 'csurin', 'csurout')
    cbijection = ('or', cinjection, csurjection)
    hf.models.vars.write_clause('cbijection', cbijection, '98-problem.txt')

    m.collapse()
    m.build()

    if run:
        t1 = time.time()
        res = m.run(count=1)
        if res:
            print(m.results(algo))
        t2 = (time.time() - t1)
        print("Run time: " + str(t2))



if '--args' in sys.argv:
    sha3_bijection_file()
else:
    sha3_bijection_args()
