#!/usr/bin/env python3

import hash_framework as hf
hf.config.model_dir = "/home/cipherboy/GitHub/sat/sat-competition-2018/models"

import time, sys, os, random

run = False
release = False
if '--run' in sys.argv:
    run = True
if '--release' in sys.argv:
    release = True
if '-h' in sys.argv or '--help' in sys.argv:
    print(sys.argv[0] + " [--run] [--release] [--args file] [w r e s]")
    print('---')
    print("Generates models for benchmarking. Runs if specified, otherwise only creates models.")
    print("--run - runs the resulting CNF file")
    print("--release - deletes the intermediate stages after creation")
    print("--args file - specify a file to load arguments from")
    print("w - sha3 w")
    print("r - sha3 rounds format (str only)")
    print("e - effective margin (128/256/.../512: as if w=1600)")
    print("s - steps to apply to base state (extract s*e*w/64 bits from the XOF)")
    sys.exit(0)

def sha3_xof_recreate_args():
    r_args = sys.argv[1:]
    if run:
        r_args = r_args[1:]
    if release:
        r_args = r_args[1:]

    w = int(r_args[0])
    r = int(r_args[1])
    e = int(r_args[2])
    s = int(r_args[3])

    sha3_xof_recreate(w, r, e, s)

def sha3_xof_recreate_file():
    fname = sys.argv[-1]
    args = open(fname, 'r').read().split('\n')
    for s_arg in args:
        if len(s_arg) == 0:
            continue
        arg = s_arg.split(" ")
        w = int(arg[0])
        r = int(arg[1])
        e = int(arg[2])
        s = int(arg[3])

        sha3_xof_recreate(w, r, e, s)

def sha3_perform(w, r, in_state):
    eval_table = hf.algorithms._sha3.perform_sha3({}, in_state, None, rounds=r, w=w)
    out_state = []
    for j in range(0, 25*w):
        out_state.append(eval_table['out' + str(j)])
    return ''.join(out_state)

def sha3_xof_recreate(w, r, e, s):
    margin = e*w//64

    algo = hf.algorithms.sha3(w=w, rounds=r)

    base_seed = []
    for j in range(0, 25*w):
        if random.randint(0, 1) == 0:
            base_seed.append('F')
        else:
            base_seed.append('T')
    base_seed = ''.join(base_seed)

    states = []
    cstate = sha3_perform(w, r, base_seed)
    for i in range(0, s):
        states.append(cstate)
        cstate = sha3_perform(w, r, cstate)

    tag = "sha3-xof_recreate-w" + str(w) + "-r" + str(r) + '-e' + str(e) + "-s" + str(s)

    prefixes = []
    for i in range(0, s):
        prefixes.append('h' + str(i))

    m = hf.models()
    m.start(tag, recreate=True)
    print(w, r, e, s, margin)
    print("base_seed: " + base_seed)
    for i in range(0, s):
        print("state " + str(i) + ": " + states[i])

    hf.models.vars.write_header()
    hf.models.generate(algo, prefixes, rounds=r, bypass=True)
    hf.models.vars.write_assign(['cchain', 'cknown'])

    if s > 1:
        cchain = ['and']
        for i in range(0, s-1):
            for j in range(0, 25*w):
                cchain.append(('equal', 'h' + str(i) + 'out' + str(j), 'h' + str(i+1) + 'in' + str(j)))
        cchain = tuple(cchain)
        hf.models.vars.write_clause('cchain', cchain, '10-chain.txt')

    cknown = ['and']
    for i in range(0, s):
        for j in range(0, margin):
            cknown.append(('equal', 'h' + str(i) + 'out' + str(j), states[i][j]))
    cknown = tuple(cknown)
    hf.models.vars.write_clause('cknown', cknown, '20-known.txt')

    m.collapse()
    m.build()

    if run:
        t1 = time.time()
        res = m.run(count=1)
        t2 = (time.time() - t1)
        print("Run time: " + str(t2))

        for result in m.load_results():
            o_s = ""
            for j in range(0, 25*w):
                o_s += result['h0in' + str(j)]
            print("predicted_seed: " + str(o_s))
    if release:
        os.system("rm -rf *.txt *.bc *.concat *.out")
    print("")

if '--args' in sys.argv:
    sha3_xof_recreate_file()
else:
    sha3_xof_recreate_args()
