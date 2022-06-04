#!/usr/bin/python3

import cmsh
from collections import defaultdict
import json
import sys

SHA256LENGTH = (256//8 * 2)

def space(m):
    return m.vec(4)

def hashVec(m):
    return list(map(lambda x: space(m), range(0, SHA256LENGTH)))

def vecToHash(vec):
    return "".join(list(map(lambda x: hexToVec(x), vec)))

def charToVec(m, char):
    return m.to_vec(int(char, 16), 4)

def hexToVec(vec):
    return hex(int(vec))[len("0x"):]

def addPositiveConstraint(m, vec, index, char):
    m.add_assert(vec[index] == charToVec(m, char))

def addNegativeConstraint(m, vec, index, char):
    m.add_assert(vec[index] != charToVec(m, char))

def recordCountConstraints(guess):
    counts = defaultdict(lambda: 0)
    finished = set()

    exactcounts = dict()
    lowerbounds = dict()

    for index, details in enumerate(guess):
        character, state = details
        if state == 'correct' or state == 'present':
            counts[character] += 1
        else:
            finished.add(character)

    for character in counts:
        if character in finished:
            exactcounts[character] = counts[character]
        elif counts[character] > 0:
            lowerbounds[character] = counts[character]

    return exactcounts, lowerbounds, finished

def addCountConstraints(m, vec, all_exactcounts, all_lowerbounds, all_finished):
    exactcounts = dict()
    lowerbounds = defaultdict(lambda: 0)
    all_chars = set()
    for exact in all_exactcounts:
        for char, value in exact.items():
            exactcounts[char] = value
            all_chars.add(char)
    for lower in all_lowerbounds:
        for char, value in lower.items():
            if char not in exactcounts:
                lowerbounds[char] = max(lowerbounds[char], value)
                all_chars.add(char)

    missing = set()
    for finished in all_finished:
        for char in finished:
            if char not in all_chars:
                missing.add(char)

    print(exactcounts, lowerbounds, missing)

    constraints = []

    for character in all_chars:
        char = character
        value = charToVec(m, character)
        vec_places_with_value = m.to_vec(list(map(lambda x: x == value, vec)))
        actual_number_of = vec_places_with_value.bit_sum()

        if char in exactcounts:
            repr_should = m.to_vec(exactcounts[char], len(actual_number_of))
            constraint = actual_number_of == repr_should
            constraints.append((constraint, f"number of char {char} should be exactly {exactcounts[char]}"))
            m.add_assert(constraint)
            assert char not in lowerbounds
            assert char not in missing
        elif char in lowerbounds:
            repr_should = m.to_vec(lowerbounds[char], len(actual_number_of))
            constraint = actual_number_of >= repr_should
            constraints.append((constraint, f"number of char {char} should be greater than or equal to {lowerbounds[char]}"))
            m.add_assert(constraint)
            assert char not in exactcounts
            assert char not in missing
        elif char in missing:
            for index in range(0, len(vec)):
                addNegativeConstraint(m, vec, index, char)
            assert char not in exactcounts
            assert char not in lowerbounds

    return constraints

def avoidHash(m, vec):
    flattened = []
    for subvec in vec:
        for var in subvec:
            flattened.append(var)
    m.add_assert(m.negate_solution(flattened))

def findAllHashesForGuesses(guesses):
    with cmsh.Model() as m:
        vec = hashVec(m)

        all_exact = []
        all_lower = []
        all_finished = []

        for guess in guesses:
            for index, details in enumerate(guess):
                character, state = details
                if state == 'correct':
                    addPositiveConstraint(m, vec, index, character)
                else:
                    addNegativeConstraint(m, vec, index, character)

            exact, lower, finished = recordCountConstraints(guess)
            all_exact.append(exact)
            all_lower.append(lower)
            all_finished.append(finished)

        addCountConstraints(m, vec, all_exact, all_lower, all_finished)

        result = m.solve()
        assert result, "invalid puzzle: no solutions for model"

        count = 1
        print_cutoff = 10
        cutoff = 1000
        while result and count < cutoff:
            if count < print_cutoff:
                print(vecToHash(vec))
            avoidHash(m, vec)
            result = m.solve()
            count += 1

        if count >= cutoff:
            print(f"too many solutions: over {count}")

def main():
    if len(sys.argv) != 2:
        print("Usage: main.py /path/to/guesses.json")
        sys.exit(1)

    document = sys.argv[1]
    guesses = json.load(open(document, 'r'))

    findAllHashesForGuesses(guesses)

if __name__ == "__main__":
    main()
