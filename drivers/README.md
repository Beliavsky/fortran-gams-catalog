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
