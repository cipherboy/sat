#!/usr/bin/python3

import cmsh
import math
import re
import sys

ALPHABET="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
REGEX = re.compile(r'^[' + ALPHABET.lower() + r']*$')
WORDLIST="words.txt"

def build_grid(model, width, height):
    return [
        [
            model.vector(math.ceil(math.log2(len(ALPHABET))))
            for j in range(0, width)
        ] for i in range(0, height)
    ]
    pass

def print_grid(grid):
    for line in grid:
        for letter_index in line:
            l_index = int(letter_index)
            assert l_index < len(ALPHABET)
            print(ALPHABET[l_index], end='')
        print()

def parse_wordlist():
    wordlist = set()

    for line in open(WORDLIST, 'r').readlines():
        word = line.strip()
        if REGEX.match(word):
            wordlist.add(tuple(map(lambda x: ALPHABET.index(x.upper()), word)))

    return wordlist

def gen_word_constraint(model, letters, word):
    con = True
    for index, letter in enumerate(letters):
        con = con & (letter == word[index])
    return con

def word_constraints_down(model, wordlist, grid):
    height = len(grid)
    filtered = list(filter(lambda x: len(x) == height, wordlist))
    print(f"Number of words of length {height}: {len(filtered)}")

    for j in range(0, len(grid[0])):
        con = False
        for word in filtered:
            letters = [ grid[i][j] for i in range(0, height) ]
            con = con | gen_word_constraint(model, letters, word)
        model.add_assert(con)

def diagonal_symmetry(model, grid):
    assert len(grid) == len(grid[0])
    con = True
    for i in range(0, len(grid)):
        for j in range(i+1, len(grid)):
            con = con & (grid[i][j] == grid[j][i])
    model.add_assert(con)

def reverse_filter(wordlist):
    filtered = set()
    for word in wordlist:
        t_reversed = tuple(reversed(word))
        if t_reversed in wordlist:
            filtered.add(word)
            filtered.add(t_reversed)
    return filtered

def new_grid(model, grid):
    con = True
    for row in grid:
        for square in row:
            con = con & (square == int(square))

    model.add_assert(-con)

def main():
    width = 7
    height = width
    symmetry = True

    # Enable for Sator
    both_directions = False

    wordlist = parse_wordlist()
    print(f"Length of wordlist: {len(wordlist)}")
    if both_directions:
        wordlist = reverse_filter(wordlist)
        print(f"Length of filtered wordlist: {len(wordlist)}")

    with cmsh.Model() as model:
        grid = build_grid(model, width, height)
        if symmetry:
            word_constraints_down(model, wordlist, grid)
            diagonal_symmetry(model, grid)

        print("Solving...")
        while model.solve():
            print(model.solver.num_constraint_vars(), model.solver.num_constraints())
            print_grid(grid)
            new_grid(model, grid)

if __name__ == "__main__":
    main()
