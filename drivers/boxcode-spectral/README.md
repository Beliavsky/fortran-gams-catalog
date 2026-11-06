# Chebyshev spectral checks

Three complete catalog-owned main programs check routines from
[`mrachh/boxcode2d-legacy` at 68ba21fe3f5acac0ed59947b2bdbd90e0deb0f28](https://github.com/mrachh/boxcode2d-legacy/blob/68ba21fe3f5acac0ed59947b2bdbd90e0deb0f28/src/chebexps.f).

| Main | Procedure and GAMS class | Independent checks |
| --- | --- | --- |
| `basis.f90` | `CHEBEXPS`, E3c | Each Chebyshev polynomial maps to a unit coefficient vector and back to its analytically evaluated nodal values: 60 cases |
| `derivative.f90` | `CHEBINMT`, E3a2 | 30 monomial derivatives and 30 right-endpoint evaluations |
| `integral.f90` | `CHEBINMT`, E3a3 | 26 monomial integrals from -1 to each node |

All use N=2,4,8,16 and binary64 arithmetic. Results must be finite and
normalized maximum error must not exceed 2e-11. Normalization divides the
maximum absolute error by `max(1,maxval(abs(expected)))`. Endpoint errors
are checked separately against 2e-11. Failure exits through `ERROR STOP`.

## Reproduce

```powershell
python drivers/boxcode-spectral/run.py --compiler gfortran --report drivers/boxcode-spectral/results.json
```

The runner downloads only the pinned `src/chebexps.f`, verifies its normalized
SHA-256, compiles it in a temporary directory, and separately builds/runs the
three mains. It requires no preinstalled library. Commands use:

```text
gfortran -O0 -g -std=legacy -ffixed-line-length-none -ffpe-trap=invalid,zero,overflow -c chebexps.f -o 0.o
gfortran -O0 -g -Wall -Wextra -ffree-line-length-none -fcheck=all -ffpe-trap=invalid,zero,overflow <main>.f90 0.o -o <main>.exe
```

All checks passed with GNU Fortran 17.0.0 20260510 (experimental), Windows.
Maximum normalized errors were 3.275158e-15 (basis), 8.668621e-13
(derivative), and 4.451610e-16 (integral). The report saves the date,
source/driver hashes, flags, compiler warnings and outputs.

## Important scope limits

The source uses length-one dummy arrays and scratch remapping; some helper
dummy extents are smaller than their actual scratch regions. **The unmodified
legacy object is compiled without bounds instrumentation.** The mains retain
bounds checks and floating-point traps. This is numerical evidence for the
selected configurations, not a conformance or full-file memory-safety check.

Use default integers, compatible REAL*8 arguments, and N>=2. The transform
matrices are dense, not fast transforms. `CHEBINMT` requires scratch storage
of at least `3*N*N+2*N+50` REAL*8 elements. ITYPE=2 leaves the integral matrix
unassigned; ITYPE=1 leaves the derivative matrix unassigned. Neither output is
read in the corresponding driver.

Integration raises the degree, but the matrix retains only N coefficients.
The integral tests therefore stop at input degree N-2; they do not claim exact
integration of degree N-1. Arbitrary-data accuracy, higher orders, threading,
the Poisson solver and other companion routines remain unverified.

No redistribution grant was identified in the earlier reviewed upstream
material. This directory stores original catalog checking programs and a
pinned-source downloader, not the upstream numerical source.
