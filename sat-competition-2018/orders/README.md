# SHA3 Difference Matrices

In this repository are arguments (in the `args` subfolder) and generators (`*.py`) used to generate
the attached instances. Note that the generators depend on `hash_framework` (available
[here](https://github.com/cipherboy/hash_framework)) and dependencies (namely `bc2cnf` from
[circuits](https://users.ics.aalto.fi/tjunttil/circuits)) being installed and configured properly.

At the core of Keccak/SHA-3 are five permutation functions: theta, rho, pi, chi, and iota. Theta and
chi are non-trivial bijective functions, rho and pi only change the location of bits and do not
change their values (and are thus a permutation of the order of the bits), and iota is an xor with a
fixed constant dependent upon the current round. We seek to prove, with SAT, the order of the
permutation described by these functions. This is accomplished by showing that there exists no witness
that x != f^{k}(x), where f is the particular set of round functions and f^{k} is f composed with
itself k times. If there is such a witness, then k cannot be the order of f. See the below table of
orders for expected orders of round functions:

func        | order
-------------------
theta       | 3w
rho         | w
pi          | 24
chi         | 4
theta ; rho | 3w

These are all largely easy problems: when k is the order of f, then f similifies to the identity,
leaving the model as x != x, a trivial UNSAT. Benchmarks are given for the above functions at
various orders and w values, where known. However, as some orders are large, this tests the
ability of the SAT solver to handle large, easy problems. When theta >= 4, these problems
become hard for CMS.

For ease of use, please consider using some of the provided benchmarks. If desired, more complete timing
information can be provided and alternative parameters can be supplied.
