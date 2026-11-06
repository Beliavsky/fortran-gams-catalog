# Chebyshev-node quadrature check (GAMS H2a1b2)

[moments.f90](moments.f90) is a complete main program calling `chebexps`
with ITYPE=1 from `mrachh/boxcode2d-legacy`, pinned at
`68ba21fe3f5acac0ed59947b2bdbd90e0deb0f28`, file `src/chebexps.f`.

This is unweighted integration on [-1,1] using Chebyshev-root nodes and the
routine's interpolatory weights. It is not the weighted Gauss-Chebyshev rule
for the measure dx/sqrt(1-x**2). For orders 2,4,8,16, the driver checks every
monomial through degree N-1 against its exact integral: 2/(k+1) for even k,
and zero for odd k. It also checks ascending interior nodes and positive
weights. Any failed or NaN comparison exits nonzero.

All 30 polynomial moments passed with absolute tolerance 2e-13; maximum
error was 1.7347e-16 using GNU Fortran 17.0.0 20260510 (experimental) on
Windows. See the [saved results](results.json).

From the catalog root:

```sh
python drivers/boxcode-quadrature/run.py --compiler gfortran --report drivers/boxcode-quadrature/results.json
```

Python, internet access and gfortran are required. The runner fetches and
hashes the unmodified pinned upstream file. It compiles that legacy object
with `-O0 -g -std=legacy -ffixed-line-length-none -ffpe-trap=invalid,zero,overflow`.
It then compiles the main program and links the object using
`-O0 -g -Wall -Wextra -ffree-line-length-none -fcheck=all -ffpe-trap=invalid,zero,overflow`,
and executes the result in a temporary directory. Binary64 REAL(KIND=8)
and default integers match this GNU build.

The upstream file uses old length-one dummy array declarations for larger
actual arrays. Bounds checking is enabled in the main program but disabled
for that unchanged legacy object. Compiler array-bound warnings, including
warnings in unused companion routines, are retained in the report. This
check covers the specified numerical results, not modern Fortran conformance
or memory safety of the full legacy file. ITYPE=2 transforms, the Poisson
solver, other orders, compilers and extreme inputs remain untested.

The main program and runner were written for this catalog. No upstream source
is bundled; no redistribution grant was identified in the inspected upstream
root and numerical files. Source pins/hashes, build configuration and results
are recorded without changing that scoped license finding. These numerical
checks run separately from offline catalog/site tests.
