# Standalone numerical drivers

This directory contains problem-specific drivers for independently reviewed
repositories. See the [locally checked Riemann examples](riemann/README.md). Imported playground drivers remain in their original repository;
the catalog retains their source hashes, licenses, validation reports and links.

For each new driver, provide:

1. A main program with a stated GAMS problem class and named upstream procedure.
2. A small README with pinned source/dependency revisions and exact local build
   and run commands. FPM is optional.
3. Independent expected values, residuals or identities; explicit tolerances and
   precision; nonzero exit status on a failed check.
4. A saved result including compiler/version, flags, platform, date, source hashes
   and stdout/stderr. Record untested configurations.
5. License and attribution for borrowed code, including author examples.

A source-reviewed procedure mapping may precede a driver. Do not describe an
unrun driver as verified. The optional `local_driver` record on a reviewed procedure binds its full
main-program text, runner and saved report to normalized SHA-256 hashes. The
validator checks the upstream source pin/hash, GAMS class and successful named
result. Generated pages label and link these artifacts separately from unchecked
calling sketches. Catalog builds remain offline; compilation is an explicit
separate check.

## Available local checks

| Main program set | GAMS class | Numerical checks |
| --- | --- | --- |
| [Riemann solvers](riemann/README.md) | I2a2 | 17 scalar advection/Burgers flux and entropy cases |
| [NDSM Poisson](ndsm/README.md) | I2b1a1a | Manufactured Neumann solution, interior residual, gauge and two-grid refinement |
| [Chebyshev-node quadrature](boxcode-quadrature/README.md) | H2a1b2 | 30 polynomial moments and node/weight identities; documented legacy-bounds limitation |
| [NDSM interpolation](ndsm-interpolation/README.md) | E1a; E2a | 157 scalar, bilinear and trilinear known-value checks, including lower-side extrapolation |
| [Chebyshev spectral operations](boxcode-spectral/README.md) | E3c; E3a2; E3a3 | 116 polynomial basis/derivative/integral cases plus 30 endpoint checks; documented legacy-bounds and integration-degree limits |
| [FFTPack signal operations](fftpack-signals/README.md) | J2; J4; J1a1 | 175 direct convolution, analytic-signal and direct-DFT comparisons; documented legacy ABI/bounds limits |
| [FMM splines and quadrature](fmm-interpolation-quadrature/README.md) | E1a; E3a2; H2a1a1 | 499 spline values, 499 derivative vectors and 55 analytic integrals; full bounds instrumentation |
