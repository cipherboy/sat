#!/usr/bin/env python3

import hash_framework as hf
hf.config.model_dir = "/home/cipherboy/GitHub/sat/sat-competition-2018/models"

import time
import sys

run = False
if len(sys.argv) == 2 and sys.argv[1] == '--run':
    run = True
elif len(sys.argv) == 2 and (sys.argv[1] == '--help' or sys.argv[1] == '-h'):
    print(sys.argv[0] + " [--run]")
    print('---')
    print("Generates models for benchmarking. Runs if specified, otherwise just creates models.")
    sys.exit(0)

# Shows that chi^4 is the identity function
def prove_identity_chi4():
    for w in [1, 2, 4, 8, 16, 32, 64]:
        count = 4
        rounds = ['c']*count

        algo = hf.algorithms.sha3(w=w, rounds=rounds)
        tag = "sha3-chi-identity-w" + str(w)

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


prove_identity_chi4()
