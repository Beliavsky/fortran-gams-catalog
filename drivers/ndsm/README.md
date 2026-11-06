# Rectangular Poisson check (GAMS I2b1a1a)

[poisson.f90](poisson.f90) is a complete main program for
`NDSM_POISSON::solve_poisson_bvp`, using NDSM pinned at
`6f5b44d76a33d247a0c73d721766a867f40b4ad3`.

The setup and manufactured polynomial follow S.A. Gilchrist's
[BSD-3-Clause author test](https://github.com/sag2021/ndsm/blob/6f5b44d76a33d247a0c73d721766a867f40b4ad3/tests/unit_tests/unit_test_2D_solve.f90).
The complete copyright/license notice is retained in the main program.
The catalog check fixes the coefficients and adds nonzero exits on failed
convergence, analytic error, independent residual, gauge or refinement checks.

On [0,1] x [0,1.5], solve Laplacian(u) = a(2x-1) + b(2y-1.5),
with a=0.75, b=-0.4 and homogeneous Neumann data. The exact solution is
`a*x**2*(x/3-1/2) + b*y**2*(y/3-1.5/2)` up to a constant.
Both solutions use a zero arithmetic mean gauge. The compatible source has
zero integral. The driver uses 17x25 and 33x49 grids, with three/four levels
and five smoothing sweeps. All coarsest dimensions remain at least two.

The main program checks:

- Solver status zero and change-based V-cycle tolerance `1e-12`.
- Maximum analytic solution error below `0.5*h**2`.
- Independently coded interior five-point residual below `5e-8`.
- Absolute solution mean below `1e-11`.
- Fine-grid error below 0.35 times coarse-grid error.

The checked GNU build uses FP=binary64 and IT=C_INT64_T. With GNU Fortran
17.0.0 20260510 (experimental) on Windows, errors were 8.78906e-4 and
2.19727e-4, with a refinement ratio of 0.25. Maximum interior residual was
3.31402e-12. See the full [saved report](results.json).

From the catalog root, with Python, internet access and gfortran on PATH:

```sh
python drivers/ndsm/run.py --compiler gfortran --report drivers/ndsm/results.json
```

The runner fetches and hashes five unmodified, pinned source files, then
compiles them in this order: `ndsm_root.f90`, `ndsm_interp.f90`,
`ndsm_multigrid_core.f90`, `ndsm_optimized.f90`, `ndsm_poisson.f90`.
The exact flags for each object and the main program are
`-O0 -g -Wall -Wextra -ffree-line-length-none -fcheck=all -ffpe-trap=invalid,zero,overflow`.
It links the objects with `poisson.f90` and runs the resulting executable
in a temporary directory. Compiler details, all source/dependency hashes,
flags, warnings and stdout/stderr are saved. No installed numerical library
or data file is required.

This is a serial 2-D homogeneous-Neumann check. OpenMP is disabled; optimized
3-D operators, other boundary conditions, other compilers and irregular grids
were not tested. The library's stopping rule measures iterate changes; the
independent residual is deliberately checked separately. Run the driver checks
separately from the offline catalog/site tests.
