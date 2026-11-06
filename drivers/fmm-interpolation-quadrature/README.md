# Forsythe–Malcolm–Moler spline and quadrature checks

These complete catalog-owned programs call module `ForsytheMalcolmMoler` from
[Beliavsky/Computer-Methods-for-Mathematical-Computations at b850d06d29e348a803feaba58c0b68a8fdd5c5f1](https://github.com/Beliavsky/Computer-Methods-for-Mathematical-Computations/tree/b850d06d29e348a803feaba58c0b68a8fdd5c5f1).

| Main | GAMS | Independent checks |
| --- | --- | --- |
| `spline.f90` | E1a | 499 spline values against exact polynomial and piecewise-natural-spline references |
| `derivatives.f90` | E3a2 | 499 output vectors containing value and first, second and third derivatives |
| `quadrature.f90` | H2a1a1 | 55 analytic definite integrals, with status/error-estimate/evaluation-count checks |

The spline drivers use 2,3,4,6,9 nonuniform knots. FMM splines reproduce
polynomials through degree `min(3,N-1)`; natural splines are checked for
constant/linear reproduction. A separate natural spline through (0,0),
(1,1),(2,0) has explicitly derived cubic pieces, exercising nonzero curvature.
Queries include knots, interior points, both exterior sides and nonmonotone
orders. The derivative reference uses the right-hand piece at the interior
knot, where the natural spline's third derivative jumps.

The quadrature driver integrates monomials of degrees 0–12 on [0,1], [-1,2],
[2,-1] and [1,1], plus exponential, sine and rational functions with known
integrals. It requires finite values, `FLAG=0`, nonnegative `ERREST`, and
appropriate callback counts. Zero-width integrals must use no evaluations.

## Reproduce

```powershell
python drivers/fmm-interpolation-quadrature/run.py --compiler gfortran --report drivers/fmm-interpolation-quadrature/results.json
```

The runner downloads unmodified `fmm.f90` at the pinned revision and verifies
its normalized SHA-256. It compiles the full module in a temporary directory,
then separately links and runs each main. All sources use:

```text
-O0 -g -Wall -Wextra -ffree-line-length-none -fcheck=all -ffpe-trap=invalid,zero,overflow
```

No repairs or permissive argument-mismatch flags are used. The selected kind
is `selected_real_kind(10,50)`, matching the module's private double-precision
kind; it is binary64 in the recorded GNU build.

All 1,053 comparisons passed with GNU Fortran 17.0.0 20260510 (experimental)
on Windows. Maximum normalized errors were 2.220446e-16 (values),
5.667141e-15 (derivatives) and 9.219847e-13 (integrals). Normalization uses
`max(1,maxval(abs(reference)))`, or the scalar equivalent. Spline tolerance
is 5e-11. Quadrature requests positive absolute/relative controls of 1e-11
and independently checks analytic error against 5e-10. It used 1,738 callback
evaluations. A failed check exits through `ERROR STOP`; the report retains
date, platform, compiler, flags, normalized hashes, warnings and outputs.

## Scope and provenance

Spline arrays must have matching lengths, with at least two strictly
increasing, distinct knots. Ordering and sizes are not generally validated.
FMM and natural end conditions differ; natural splines do not generally
reproduce cubics. Evaluators extrapolate their end polynomials and cache an
interval index in `SAVE` state. Parallel safety is not established.

QUANC8 samples endpoints and returns an estimated error, not a certified bound.
Its resource-limit branch can reduce initialized persistent `LEVMAX` state
for later calls. That branch, singular/discontinuous integrands, single
precision, concurrent calls, other compilers and other textbook algorithms
remain unverified. Compiling the full module does not numerically check its
other routines.

The collection credits Forsythe, Malcolm, Moler, and the Ralph Carmichael
modernization. The existing root MIT notice and inherited-source provenance
finding remain scoped; no new project-wide SPDX assertion is made. These
original checking programs do not copy author examples or numerical source.
The runner downloads source for local checking; upstream code is not bundled.
