#!/usr/bin/python3

import cmsh
import sys
import math

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <modulus>", file=sys.stderr)
    sys.exit(1)

modulus = int(sys.argv[1])
bits = 4 * math.ceil(math.log(modulus, 2)) + 2

print(f"Underlying minimum width: {bits}")

def lcg(model, x, a, c, m):
    q, r = divmod(a*x + c, m)
    if model:
        model.add_assert(q < 2**(bits//2))
    return q, r

with cmsh.Model() as model:
    print("Building model...", end="", flush=True)
    multiplier = model.vec(bits)
    increment = model.vec(bits)

    values = [0]
    quotients = []

    for i in range(1, modulus):
        q, x = lcg(model, values[-1], multiplier, increment, modulus)
        for j in range(0, i):
            model.add_assert(x != values[j])
        quotients.append(q)
        values.append(x)

    _, x = lcg(model, values[-1], multiplier, increment, modulus)
    model.add_assert(x == values[0])
    values.append(x)

    model.add_assert(multiplier < modulus)
    model.add_assert(multiplier > 0)
    model.add_assert(increment < modulus)

    print(" Done", flush=True)

    assert model.solve()

    print(f"multiplier: {int(multiplier)} / increment: {int(increment)}")
    cycle = list(map(int, values))
    print(f"cycle: {cycle}")
    for prevIndex, expected in enumerate(cycle[1:]):
        prev = cycle[prevIndex]
        _, actual = lcg(None, prev, int(multiplier), int(increment), modulus)
        assert expected == actual, f"value at index {prevIndex} doesn't compute {prevIndex+1}: {expected} != lcg({prev}, {int(multiplier)}, {int(increment)}, {modulus}) = {actual}"

