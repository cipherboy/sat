# MD4 and MD5 Collision Families

See this [paper](https://github.com/cipherboy/papers/raw/master/dsn-2018/hash_dsn_2018-update-0.pdf)
for background information.

In this repository are arguments (in the `args` subfolder) and generators (`*.py`) used to generate
the attached instances. Note that the generators depend on `hash_framework` (available
[here](https://github.com/cipherboy/hash_framework)) and dependencies (namely `bc2cnf` from
[circuits](https://users.ics.aalto.fi/tjunttil/circuits)) being installed and configured properly.

Per the paper, families in MD4 and MD5 form a heuristic lattice structure; the existance or
non-existance of a collision in `n` rounds implies something about the existance of a
collision in `n+4` rounds. Being able to find families of collisions for higher rounds (here `n=24`
for all attached benchmarks) and exhaustively searching all possible shapes gives us the maximum
amount of information before resorting to heuristics to find a full collision via other techniques.
In each of these benchmarks, a particular shape is requested, represented by `p$array` in the
file name. Each index marks a 32-bit word which must have a difference in the collision for the
benchmark to be satisifiable. For instance, `scheel-md4-families-r24-c4-p4-9-13-18.cnf` looks for a
collision in md4, reduced to 24 rounds (`r24`), with 4 rounds having a difference (`c4`), and the
indices of these rounds are 4, 9, 13, and 18 (`p4-9-13-18`). From the files in the `args` directory,
we can determine that this instance is hard and satisfiable, taking 3394480 ms (3394.480 seconds) to
run on the tested version of CMS (v5.0.1 release). Note that the runs which are easy are pruned to
not contain anything shorter than 75 seconds (shorter instances can take less than a second to run).
Further, only a random sampling of possible parameters were used to determine the submitted benchmarks.

For ease of use, please consider using some of the provided benchmarks. If desired, more complete timing
information can be provided and alternative parameters can be supplied. Alternatively, if higher round
versions of these functions are desired, results for r=28 can be provided.
