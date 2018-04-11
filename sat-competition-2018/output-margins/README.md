# SHA3 Input Difference -> Output Margin Matrices

In this repository are arguments (in the `args` subfolder) and generators (`*.py`) used to generate
the attached instances. Note that the generators depend on `hash_framework` (available
[here](https://github.com/cipherboy/hash_framework)) and dependencies (namely `bc2cnf` from
[circuits](https://users.ics.aalto.fi/tjunttil/circuits)) being installed and configured properly.

At the core of Keccak/SHA-3 are five permutation functions: theta, rho, pi, chi, and iota. Theta and
chi are non-trivial bijective functions, rho and pi only change the location of bits and do not
change their values (and are thus a permutation of the order of the bits), and iota is an xor with a
fixed constant dependent upon the current round. This benchmark deals with the interaction of these
functions with the sponge construction. Since the round functions are bijective, any non-zero
difference in state results in a non-zero output difference after applying the Keccak-f permutations.
The sponge function controls the security margin of the hash function. For a given width w, a power
of two (with b = 25*w), a security margin of k bits fixes a block size of b - k, and allows at most
k bits to be extracted at a time (before Keccak-f is reapplied). For instance, with SHA3-512, k=1024.

In an ideal hash function, since collisions are inevitable (since b - k > k/2), we'd expect that any
fixed bit pattern is uncorrelated to the actual output margin (the most number of bits which can
be the same). More formally our benchmarks are the following model:

    #(1, a xor b) = x
    #(1, (f(a) xor f(b))[0:y]) = z

Where x, y, and z are model parameters and #(1, k) are the number of 1s in the binary string k, and
k[0:y] is the first y characters of k. In all of our benchmarks, z = 0 and f = theta, rho, pi, and
chi. If the model is SAT, and if we extract fewer than y bits from the full state, we will not
discover a collision. If the model is UNSAT however, then extracting y bits will reveal that our two
messages differ. This allows us to evaluate different quantity of input differences to find one
which allows us to break SHA-3 at a given security margin.

For ease of use, please consider using some of the provided benchmarks. If desired, more complete timing
information can be provided and alternative parameters can be supplied.
