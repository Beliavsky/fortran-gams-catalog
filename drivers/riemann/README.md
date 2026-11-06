# Scalar hyperbolic Riemann checks (GAMS I2a2)

These complete main programs call two separate `rp1_ptwise` implementations
from [Clawpack Riemann solvers](https://github.com/clawpack/riemann), pinned at
`008d4921ea46878a97a96c8b8daa399a2e7b9078`:

- [advection.f90](advection.f90): nine cases compare fluctuations with the exact
  upwind flux for positive, negative and zero constant velocities.
- [burgers.f90](burgers.f90): eight cases compare with the exact scalar Godunov
  flux for positive/negative rarefactions, a transonic rarefaction, stationary
  and moving shocks, and constant states.

Both check flux conservation, the state jump and the reported wave speed.
They use the source's `REAL(KIND=8)` interface (binary64 in the checked GNU
build), default integers, and a tolerance of `2e-13` times the largest of one
and the relevant flux magnitudes. A failed or NaN comparison exits nonzero.
The routines are solver components; these checks do not evolve a full PDE.

From the catalog root, with Python and gfortran on PATH:

```sh
python drivers/riemann/run.py
```

To select a compiler executable and save a fresh report:

```sh
python drivers/riemann/run.py --compiler gfortran --report drivers/riemann/results.json
```

The runner downloads the two pinned upstream source files, verifies their
normalized SHA-256 hashes, and compiles each main program separately in a
temporary directory. Both upstream files define the same external symbol and
must not be linked together. No Clawpack, Python numerical library or BLAS
installation is needed. Internet access is needed for those source downloads.
The exact compile command for each downloaded source is equivalent to:

```sh
gfortran -O0 -g -Wall -Wextra -fcheck=all -ffpe-trap=invalid,zero,overflow rp1_advection_ptwise.f90 drivers/riemann/advection.f90 -o advection
./advection
gfortran -O0 -g -Wall -Wextra -fcheck=all -ffpe-trap=invalid,zero,overflow rp1_burgers_ptwise.f90 drivers/riemann/burgers.f90 -o burgers
./burgers
```

[Saved results](results.json) record the platform, compiler/version, date,
flags, normalized source/driver hashes, warnings and program output. Both
programs passed with zero maximum discrepancy on the 17 finite cases using
GNU Fortran 17.0.0 20260510 (experimental) on Windows. Other compilers,
optimized builds, entire time integrators and extreme-value inputs remain
untested. Unused-auxiliary-argument warnings come from the upstream routines.

The main programs and runner were written for this catalog; no author driver
was copied. The downloaded Clawpack source retains its
[BSD-3-Clause license](https://github.com/clawpack/riemann/blob/008d4921ea46878a97a96c8b8daa399a2e7b9078/LICENSE).
Upstream source is not bundled here. Numerical checks run separately from the
offline catalog tests. If a driver, runner or saved report changes, update its
`local_driver` hashes in `data/local.json` after reviewing/rerunning the checks.
