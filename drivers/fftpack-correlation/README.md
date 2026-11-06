# FFTPack finite cross-correlation

This complete main checks `fftpack::xcorr` at pinned commit
`f4b82af35a1a473d33593b3b6f7a03977bf3110e` of
[keurfonluu/FFTPack](https://github.com/keurfonluu/FFTPack).
Upstream numerical sources are downloaded, hash-verified and compiled in a temporary directory; they are not bundled.

```sh
python drivers/fftpack-correlation/run.py --report drivers/fftpack-correlation/results.json
```

GNU Fortran flags are used; `--compiler` can select its executable. The saved
report records GNU Fortran 17.0.0 20260510 (experimental) on Windows.

The output has `2*max(size(x),size(y))-1` entries, at lags
`1-max(size(x),size(y))` through `max(size(x),size(y))-1`.
At lag k the reference is `sum_j x(j+k)*conjg(y(j))`, restricted to valid
indices. There is no mean removal, variance normalization or division by the
number of overlaps. For unequal lengths, some end entries are zero. This is
finite, zero-extended cross-correlation, not circular correlation. Reversing
arguments reverses lags and conjugates the complex correlation.

The main checks all four real/complex KIND=4/8 overloads for both lengths
1..7, using dense nontrivial signals, separated endpoint impulses and a zero
first signal: 588 comparisons. Single-kind inputs are rounded before forming
the binary64 direct-sum reference. The tolerances are 2e-12 for double and
2e-6 for single, scaled by max(1,max(abs(reference))). Every vector must have
the expected length and finite real/imaginary components. Maximum normalized
errors were 3.717673e-16 and 5.062557e-8 respectively.

The wrapper and main use full bounds checks and floating-point traps at O0.
The unmodified legacy FFTPACK backend requires `-fallow-argument-mismatch`
and is compiled without bounds instrumentation. Its implicit external
real/complex storage conventions remain a portability/memory-safety limitation;
passing these finite cases does not certify the backend. Kernel, wrapper and
main flags and all build warnings are retained in results.json. Numeric KIND
values assume this GNU compiler ABI. Empty inputs, large lengths, extreme
amplitudes, NaNs, optimized builds and other compilers were not checked.
The wrapper ignores FFTPACK IERR values and rebuilds workspaces for each call.
Existing scoped license findings remain; public availability is not a new
license grant.
