# Minila triangular-system checks

The complete main `triangular.f90` exercises public functions `prim::diag_sub`,
`prim::fwd_sub`, and `prim::bck_sub` for GAMS **D2a3** (real triangular systems),
using unmodified `src/prim.f90` from
[ghbrown/minila at 9f20969c68ce5b174d4a21cfc610c5ff276d183c](https://github.com/ghbrown/minila/tree/9f20969c68ce5b174d4a21cfc610c5ff276d183c).

## Reproduce

```powershell
python drivers/minila-triangular/run.py --compiler gfortran --report drivers/minila-triangular/results.json
```

The runner downloads the pinned module, verifies its normalized SHA-256,
compiles it in a temporary directory, and links/runs the main. Other minila
modules, FPM, BLAS and LAPACK are not needed. Both files use:

```text
-O0 -g -Wall -Wextra -ffree-line-length-none -fcheck=all -ffpe-trap=invalid,zero,overflow
```

The build reports **32-bit default REAL**. There is no precision-promotion
flag, source repair or permissive argument-mismatch flag. The saved report
records GNU Fortran 17.0.0 20260510 (experimental), Windows, date, flags,
source/driver hashes, warnings and output.

## Independent numerical checks

For each size N=1..12, the driver builds diagonal, lower-triangular and
upper-triangular matrices at scales 1e-8, 1 and 1e8. A prescribed alternating-
sign solution determines the right-hand side through `MATMUL`. Diagonals are
positive, with small off-diagonal entries. It verifies finite returned values,
unchanged matrices, relative solution error and a separately calculated
scaled residual:

```text
max(abs(A*x-b)) / (norm_infinity(A)*norm_infinity(x) + norm_infinity(b))
```

All **108 systems** passed tolerance 5e-6. Maximum relative solution error was
1.726479e-7; maximum scaled residual was 8.948365e-8. Failure uses `ERROR STOP`.

## Scope and source terms

Supply N>=1, matching dimensions, finite data, correct diagonal/triangular
structure and nonzero diagonal entries. These routines check squareness but
do not validate structure or zero pivots. Off-triangle entries are ignored.
Nonsquare error paths print a message and leave the result undefined; they
are not a status-based error protocol. There is no condition estimate or
certified error bound.

Ill-conditioning, negative/zero pivots, invalid shapes/structure, extreme
scales, other real kinds, optimized builds and other compilers remain
unverified. Only the direct routines are executed: no claim is made for the
automatic `strang` dispatcher, LU, inverse or SOR routines. Compiling the full
primitive module does not numerically check all its functions.

The existing root GPL version-3 text and unresolved version-choice finding
are retained. This directory contains original catalog checks and a pinned
downloader, not redistributed upstream numerical source.
