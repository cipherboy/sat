# SHA3 XOF State recreation

In this repository are arguments (in the `args` subfolder) and generators (`*.py`) used to generate
the attached instances. Note that the generators depend on `hash_framework` (available
[here](https://github.com/cipherboy/hash_framework)) and dependencies (namely `bc2cnf` from
[circuits](https://users.ics.aalto.fi/tjunttil/circuits)) being installed and configured properly.

Keccak/SHA-3 defines a new construct, called an eXtensible Output Function (XOF), which acts as a
psuedo-random function (PRF) seeded by hashing some input value. A variable number of bits can then
be extracted from the state; however, only `margin` bits can be extracted at a time, for a given
security margin `m`. We seek to evaluate the security of the XOF with respect to deriving the initial
state; that is, given several bits, is it possible to find the initial state, allowing us to predict
future output from the XOF?

For ease of use, please consider using some of the provided benchmarks. If desired, more complete timing
information can be provided and alternative parameters can be supplied.
