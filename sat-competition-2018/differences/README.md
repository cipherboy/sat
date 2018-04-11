# SHA3 Difference Matrices

In this repository are arguments (in the `args` subfolder) and generators (`*.py`) used to generate
the attached instances. Note that the generators depend on `hash_framework` (available
[here](https://github.com/cipherboy/hash_framework)) and dependencies (namely `bc2cnf` from
[circuits](https://users.ics.aalto.fi/tjunttil/circuits)) being installed and configured properly.

At the core of Keccak/SHA-3 are five permutation functions: theta, rho, pi, chi, and iota. Theta and
chi are non-trivial bijective functions, rho and pi only change the location of bits and do not
change their values (and are thus a permutation of the order of the bits), and iota is an xor with a
fixed constant dependent upon the current round. Hence, for all a, b as inputs to rho or pi,

    #(1, a xor b) = #(1, rho(a) xor rho(b))
    #(1, a xor b) = #(1, pi(a) xor pi(b))

However, while rho runs quickly, pi takes a longer time to verify this; in particular, consider models
of the form:

    #(1, a xor b) = x
    #(1, pi(a) xor pi(b)) = y

for arguments x and y. That is, find a satisfying a and b which differ in x locations, and when mapped
under pi, differ in y locations. Since pi is a permutation of the order of bits, clearly this is only
SAT when x == y and UNSAT otherwise. However, certain choices of x and y result in longer than expected
runtimes, even for small w. These are represented in a collection of benchmarks in the `benchmarks-pi`
directory, with argument choices and estimated timings in `args-pi`.

A set of benchmarks are also given for the theta function (including SAT and UNSAT in this case) and
for the chi function (with only three SAT instances and the rest UNSAT), with a similar directory
layout. No benchmarks for rho have been provided as they are relatively quick to run.

For ease of use, please consider using some of the provided benchmarks. If desired, more complete timing
information can be provided and alternative parameters can be supplied.
