# Forsythe–Malcolm–Moler SVD and ODE checks

These complete catalog-owned main programs call `SVD` and `RKF45` in
module `ForsytheMalcolmMoler`, using unmodified `fmm.f90` from
[Beliavsky/Computer-Methods-for-Mathematical-Computations at b850d06d29e348a803feaba58c0b68a8fdd5c5f1](https://github.com/Beliavsky/Computer-Methods-for-Mathematical-Computations/tree/b850d06d29e348a803feaba58c0b68a8fdd5c5f1).

| Main | GAMS | Independent checks |
| --- | --- | --- |
| `svd.f90` | D6 | 48 square/tall matrices: reconstruction, orthogonality, energy and selected known spectra |
| `ode.f90` | I1a1a | 211 analytic decay/oscillator states, including continuation, backward integration and 176 one-step returns |

## Reproduce

```powershell
python drivers/fmm-svd-ode/run.py --compiler gfortran --report drivers/fmm-svd-ode/results.json
```

The runner downloads and hashes the pinned module, compiles it in a temporary
directory, and links/runs each main separately. Both the full module and the
mains use the private module's kind selection `selected_real_kind(10,50)`
(binary64 in this build) and these GNU flags:

```text
-O0 -g -Wall -Wextra -ffree-line-length-none -fcheck=all -ffpe-trap=invalid,zero,overflow
```

No repair or permissive argument-mismatch flag is used. The saved report
records GNU Fortran 17.0.0 20260510 (experimental), Windows, date, source/driver
hashes, flags, warnings and outputs. Failure uses `ERROR STOP`.

## SVD scope

The test uses N=1..4, M=N or N+2, separate arrays and both vector flags true.
Cases include known diagonal spectra, dense, zero and rank-one matrices,
and dense matrices scaled by 1e-30 or 1e30. It requires unchanged input,
finite nonnegative singular values and these independent invariants:

- `U*diag(W)*transpose(V)` reconstructs the matrix, scaled by its largest entry.
- Columns of U and V are orthonormal.
- Scaled squared singular values match the matrix's squared Frobenius norm.
- Selected diagonal/rank-one/zero cases match known spectral identities.

Tolerance is 5e-11. Maximum reconstruction, orthogonality and relative energy
errors were 6.661338e-16, 1.110223e-15 and 8.889787e-16.

Singular values are unsorted; preserve their pairing with vector columns.
Always supply U(M,N) for the checked usage: U is scratch even when MATU is
false, although its size guard is conditional. Check IERR before using outputs.
Wide/empty matrices, disabled-vector flags, aliasing, extreme dynamic range
and all error-return paths remain unverified.

## ODE scope and important portability finding

The driver checks `y'=-y`, `y(0)=1`, and the harmonic oscillator with
solution `[cos(t),-sin(t)]`, in both directions from zero. Normal controls
are relative tolerance 1e-9 and absolute tolerance 1e-11. It checks interval
status 2, one-step status -2, arrival times, directional progress, initial
equal-time requests and a deliberate status-3 tolerance adjustment/retry.
Work arrays and returned state are preserved during continuation.

All 211 analytic-state comparisons passed within normalized tolerance 5e-8;
maximum error was 8.110344e-10, using 2,507 derivative evaluations. These
are finite observed results, not a certified global-error bound.

**The continuation helper has an INTENT declaration issue.** `RkfsDouble`
declares preserved H, NFE, KOP and some saved tolerance arguments `INTENT(OUT)`
but reads retained values on continuation paths before defining them. Their
values are undefined on entry under Fortran semantics. This GNU `-O0` run
retains the storage; passing tests do not establish portable continuation
correctness. The source was not repaired, and optimized builds are unverified.

Use Y(NEQN), WORK(3+6*NEQN), IWORK(5), mutable T/TOUT/RELERR, and the exact-kind
assumed-shape callback interface. Other failure/recovery paths can terminate
through STOP and must not be treated as successful integration. Stiff systems,
events, resource-limit recovery, concurrency, single precision and other
compilers remain unverified. Compiling the full module does not check all its
other algorithms.

The collection attributes Forsythe, Malcolm, Moler and the Carmichael
modernization. Existing root MIT and inherited-source provenance findings
remain scoped. Only original checking programs and a downloader are bundled;
upstream numerical source is linked and downloaded for local checking.
