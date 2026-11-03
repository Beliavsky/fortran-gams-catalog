# Initial independent repository reviews

These six repositories were discovered in the pinned Fortran code on GitHub list. Their author documentation was reviewed; none was compiled or run for this catalog. No root `fpm.toml` was present at the reviewed revision.

| Repository | GAMS | Scope |
| --- | --- | --- |
| [FFTE](https://github.com/certik/ffte) | J1 | Discrete Fourier transforms in one, two and three dimensions, including serial and parallel variants. |
| [Expokit](https://github.com/rasmusgo/expokit) | D | Matrix exponentials and exponential actions using dense approximations and sparse Krylov methods. |
| [BLZPACK](https://github.com/oamarques/BLZPACK) | D4 | Block Lanczos methods for sparse real symmetric standard and generalized eigenproblems. |
| [AMG4PSBLAS](https://github.com/sfilippone/amg4psblas) | D2 | Parallel algebraic multilevel preconditioners for sparse linear systems in the PSBLAS framework. |
| [eiscor](https://github.com/eiscor/eiscor) | D4 | Matrix eigenvalue algorithms based on small unitary core transformations. |
| [FFTLog-f90](https://github.com/coccoinomane/fftlog-f90) | J1a3 | Logarithmically sampled Fourier-Bessel transform code, currently restricted to the sine-transform case. |

## FFTE

Documents complex FFTs and real/complex transforms; multidimensional coverage is recorded at J1 rather than treating every routine as one-dimensional.

Reviewed 2026-11-03: [readme.txt](https://github.com/certik/ffte/blob/33b3400dcf9ced8576ce12282932ce772bdf0062/readme.txt) at `33b3400dcf9ced8576ce12282932ce772bdf0062`.
Document SHA-256 (UTF-8/LF): `20256f9e26f6e8735b5ae646410cabddca25f122b92421f8a91dd8442f556d3b`.

[Discovery list](https://github.com/Beliavsky/Fortran-code-on-GitHub/blob/f5ab25294a12ed004d5a8934200ca8e26ac2e825/README.md).

## Expokit

Documents exp(t*A), exp(t*A)v and phi-function actions for dense and sparse matrices. Linear algebra is supported; a more specific matrix-function mapping awaits procedure review.

Reviewed 2026-11-03: [README](https://github.com/rasmusgo/expokit/blob/db906c01150025eec83654b42feb66c5f09960a9/README) at `db906c01150025eec83654b42feb66c5f09960a9`.
Document SHA-256 (UTF-8/LF): `06301738b4db1db1a0b81f3b0b4cb907d36fa456cf5eee7744467ec912e9158a`.

[Discovery list](https://github.com/Beliavsky/Fortran-code-on-GitHub/blob/f5ab25294a12ed004d5a8934200ca8e26ac2e825/README.md).

## BLZPACK

Documents both standard and generalized real sparse symmetric eigenproblems. A D4 mapping avoids implying that only the ordinary eigenproblem is supported.

Reviewed 2026-11-03: [README](https://github.com/oamarques/BLZPACK/blob/2e5aa8f725e92e27e3aeec8c025eadc5bc521b1c/README) at `2e5aa8f725e92e27e3aeec8c025eadc5bc521b1c`.
Document SHA-256 (UTF-8/LF): `7e5ec3b864f759769b39a438f77f3242a996cbbd18d0cae934b04c102c631a48`.

[Discovery list](https://github.com/Beliavsky/Fortran-code-on-GitHub/blob/f5ab25294a12ed004d5a8934200ca8e26ac2e825/README.md).

## AMG4PSBLAS

Documents algebraic multilevel preconditioning used with PSBLAS Krylov solvers. This is a preconditioner component, not a standalone solver; MPI and PSBLAS are required.

Reviewed 2026-11-03: [README.md](https://github.com/sfilippone/amg4psblas/blob/1395c67d9c63cb8f879aa097c5c4f38de7603c03/README.md) at `1395c67d9c63cb8f879aa097c5c4f38de7603c03`.
Document SHA-256 (UTF-8/LF): `963ff57d2d462d5c9d838d24635277296ee16c0203b1be2be93a7ed609a439ea`.

[Discovery list](https://github.com/Beliavsky/Fortran-code-on-GitHub/blob/f5ab25294a12ed004d5a8934200ca8e26ac2e825/README.md).

## eiscor

Documents Fortran 90 matrix eigensolvers and related unitary QR research. Build requirements and individual routine interfaces have not yet been reviewed.

Reviewed 2026-11-03: [README.md](https://github.com/eiscor/eiscor/blob/fcdc0f454d00be218225aff0dd760906d8d09175/README.md) at `fcdc0f454d00be218225aff0dd760906d8d09175`.
Document SHA-256 (UTF-8/LF): `102ded6a223ddcd1e9715df2b3726f01be9ddbd8b8a1ca0157fa8bb4f88c987c`.

[Discovery list](https://github.com/Beliavsky/Fortran-code-on-GitHub/blob/f5ab25294a12ed004d5a8934200ca8e26ac2e825/README.md).

## FFTLog-f90

The README explicitly limits this version to mu=0.5 (the sine-transform case). This mapping does not claim a general-order Hankel transform implementation.

Reviewed 2026-11-03: [README.md](https://github.com/coccoinomane/fftlog-f90/blob/85c617abac1a6536f124f9bcc00b37b0f3cc9cec/README.md) at `85c617abac1a6536f124f9bcc00b37b0f3cc9cec`.
Document SHA-256 (UTF-8/LF): `314d876010fbc4e1f375b4c08d0b2dd851221b832167778a4ac83db8a3b580be`.

[Discovery list](https://github.com/Beliavsky/Fortran-code-on-GitHub/blob/f5ab25294a12ed004d5a8934200ca8e26ac2e825/README.md).
