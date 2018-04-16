# SHA3 Bijectivity

In this repository are arguments (in the `args` subfolder) and generators (`*.py`) used to generate
the attached instances. Note that the generators depend on `hash_framework` (available
[here](https://github.com/cipherboy/hash_framework)) and dependencies (namely `bc2cnf` from
[circuits](https://users.ics.aalto.fi/tjunttil/circuits)) being installed and configured properly.

At the core of Keccak/SHA-3 are five permutation functions: theta, rho, pi, chi, and iota. Theta and
chi are non-trivial bijective functions, rho and pi only change the location of bits and do not
change their values (and are thus a permutation of the order of the bits), and iota is an xor with a
fixed constant dependent upon the current round. We seek to prove, with SAT, that each of these
functions are bijective, verifying the authors' claims. In general, these are all easy benchmarks
for solvers; however, as w->64, the time for `theta` increases.

As these are simple benchmarks, there are no parameters besides those already presented as part of
the benchmarks.
