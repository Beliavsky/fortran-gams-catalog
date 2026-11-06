# NDSM interpolation checks

These complete main programs call `NDSM_INTERP::ninterp`:

- `linear.f90`: GAMS **E1a**, univariate piecewise-linear interpolation.
  Seven known-value checks include a linear function and a non-affine nodal
  table with explicitly calculated between-node and extrapolated values.
- `multilinear.f90`: GAMS **E2a**, Cartesian gridded interpolation.
  A polynomial with bilinear/trilinear cross terms gives 150 exact-value
  checks on 4x5 and 4x5x3 grids with unequal coordinate spacings.

Both include nodes, endpoints, interior points, lower-side extrapolation and
coordinate vectors allocated with lower bounds of -2. Sample storage uses
Fortran order. The programs require finite results and errors below 5e-13;
failure exits through `ERROR STOP`. The multivariate error is normalized by
`max(1,abs(expected))`; the two additional scalar table checks use absolute error.

## Reproduce

```powershell
python drivers/ndsm-interpolation/run.py --compiler gfortran --report drivers/ndsm-interpolation/results.json
```

The runner downloads and hashes two unmodified sources from
[sag2021/NDSM at 6f5b44d76a33d247a0c73d721766a867f40b4ad3](https://github.com/sag2021/NDSM/tree/6f5b44d76a33d247a0c73d721766a867f40b4ad3):
`fortran/ndsm_root.f90`, followed by `fortran/ndsm_interp.f90`. It compiles
these in a temporary directory, then separately links each main with both
objects and runs it. No preinstalled NDSM library or FPM is required.

All sources and mains use these GNU flags:

```text
-O0 -g -Wall -Wextra -ffree-line-length-none -fcheck=all -ffpe-trap=invalid,zero,overflow
```

The saved report records GNU Fortran 17.0.0 20260510 (experimental), Windows,
the check date, normalized source/driver hashes and compiler warnings.
Both programs passed: maximum errors were 1.655814e-16 and 6.692324e-16.

## Scope and source terms

Use `FP` and `IT` from `NDSM_ROOT`: `IT` is a 64-bit integer kind. Initialize
the module `DEBUG` flag. Each coordinate axis must be increasing and uniformly
spaced, with at least two nodes. The public function ignores the bracketing
helper's status and extrapolates beyond the end cell without clipping or a
returned status. These tests cover lower-side extrapolation only. Assertions
can stop for inconsistent dimensions; nonuniform, decreasing, repeated-node,
large-dimensional, and arbitrary-data accuracy cases are unverified.

The upstream modules carry S.A. Gilchrist's BSD-3-Clause notices. They are
downloaded unmodified, not bundled here. The catalog mains independently
construct their test functions and expected values; they do not copy the
upstream implementation or author test programs.
