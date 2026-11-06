# FFTPack signal checks

These complete catalog-owned programs call the public generics in
[`keurfonluu/FFTPack` at f4b82af35a1a473d33593b3b6f7a03977bf3110e](https://github.com/keurfonluu/FFTPack/tree/f4b82af35a1a473d33593b3b6f7a03977bf3110e).

| Main | GAMS | Independent checks |
| --- | --- | --- |
| `convolution.f90` | J2 | 98 real/complex double-precision finite convolutions against nested direct sums; all length pairs 1–7 |
| `analytic.f90` | J4 | 44 analytic periodic signals from DC, sine/cosine and even-length Nyquist components |
| `real_dft.f90` | J1a1 | 33 real-input full complex spectra against direct negative-exponent DFT sums, including padding and truncation |

DFT/signal lengths are 1,2,3,4,5,7,8,9,10,16,17. Results must have the
expected length and finite components, with maximum absolute discrepancy
divided by `max(1,maxval(abs(reference)))` at most 5e-12. Failure uses
`ERROR STOP`. The analytic-signal checks use the default length only.

## Reproduce

```powershell
python drivers/fftpack-signals/run.py --compiler gfortran --report drivers/fftpack-signals/results.json
```

The runner downloads and hashes unmodified `src/fftpack5.f90` and
`src/fftpack.f90`, compiles them in that order in a temporary directory, and
links each main against both objects. The `forlab` module is not needed.

The backend uses:

```text
-O0 -g -ffree-line-length-none -fallow-argument-mismatch -ffpe-trap=invalid,zero,overflow
```

The wrapper and each main use:

```text
-O0 -g -Wall -Wextra -ffree-line-length-none -fcheck=all -ffpe-trap=invalid,zero,overflow
```

All 175 vector comparisons passed on Windows with GNU Fortran 17.0.0
20260510 (experimental). Maximum normalized errors were 3.608225e-16
(convolution), 2.258517e-15 (analytic signal), and 4.540382e-15 (real DFT).
The report records the date, exact compiler, source/driver hashes, separate
kernel/wrapper/main flags, warnings and outputs.

## Scope and limitations

The backend retains legacy mismatched argument/storage conventions and is
compiled **without bounds instrumentation**. The wrapper also passes complex
workspace arrays through implicit external interfaces expecting real storage.
The selected GNU ABI works in these tests; portable Fortran conformance and
full-backend memory safety have not been established. Kernel warnings are
retained. Numeric kind identifiers 4 and 8 must match the selected build ABI.

All input/effective lengths must be positive. Wrappers rebuild FFT workspaces
on each call and ignore backend status. Real-input FFT returns the full
complex spectrum via a complex kernel. Convolution is finite linear
convolution without conjugation. Hilbert output is a **periodic analytic
signal**, whose imaginary part follows the positive-sine transform of cosine;
this is not a general nonperiodic continuous integral.

The single-precision Hilbert overload returns a real array, discarding the
imaginary component. It is not the checked API. Other single-precision paths,
optional-length Hilbert behavior, large sizes, other compilers, filters,
correlations and chirp transforms remain unverified.

The bundled backend states GPL without a resolved version choice; the
wrapper's reviewed material provides attribution but no clear standalone
grant. These scoped findings are unchanged. Only original checking programs
and a downloader are stored here; no upstream numerical source is bundled.
