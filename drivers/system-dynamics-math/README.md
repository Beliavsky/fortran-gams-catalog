# system_dynamics statistics and covariance eigenvectors

Two complete catalog mains use the unmodified `types`, `constants`, `utils`
and `math` modules from [quimbp/system_dynamics](https://github.com/quimbp/system_dynamics)
at commit `366339d9f6fea2e4242f8a73b700f8ea0af07797`.
Upstream numerical code is downloaded and hash-verified, not bundled.

```sh
python drivers/system-dynamics-math/run.py --report drivers/system-dynamics-math/results.json
```

The runner accepts `--compiler` and uses GNU flags. The saved check used GNU
Fortran 17.0.0 20260510 (experimental) on Windows. Module and main flags include
`-O0 -g -Wall -Wextra -ffree-line-length-none -fcheck=all
-ffpe-trap=invalid,zero,overflow`. Modules additionally require
`-fno-range-check` because constants.f90 initializes NaN/infinity parameters
with constant zero divisions. This GNU accommodation is recorded explicitly;
it is not source repair or a claim of portable standard-conforming initialization.
The flags, compiler warnings, source hashes and results are in results.json.

## L1a1a/L1a1b: location and dispersion

`math::mean(A[,W])` returns SUM(A)/N or SUM(W*A)/SUM(W), not the weighted
sum divided by N suggested by its comment. `math::avevar(A,AVE,VAR)` returns
the mean and corrected two-pass sample variance with denominator N-1.
`types::dp` is KIND(0D0), binary64 in the recorded build.

The same statistics main is run for each leaf classification; these are shared
checks, not twice as many distinct datasets. The main checks N=2..20, offsets 0/10 and steps .25/1/4, forming 114 arithmetic
progressions. Independent closed forms are offset+step*(N+1)/2 for the mean,
step**2*N*(N+1)/12 for sample variance, and offset+step*(2*N+1)/3 for weighted
mean when W(i)=i. All four scalar outputs per case must be finite and agree
within normalized tolerance 2e-12. Maximum error was 2.197555e-16.

The checked contract needs N>=2, finite values, conforming positive weights
and nonzero total weight. The routines do not validate weights or lengths.
Empty input returns the module NaN; a singleton AVEVAR divides by zero.
Signed weights, huge offsets, cancellation, overflow and missing data were
not checked. Negative computed variances are not clamped and no accuracy
estimate is returned. These are summaries, not inferential statistics.

## D4a1: positive-semidefinite covariance eigenproblem

`math::eigencov(N,P,U,D,RANK,VERBOSE)` copies P into U, calls private symmetric
Householder reduction and QL iteration, clips every negative eigenvalue to
zero, and sorts eigenvalues/eigenvector columns in descending order. RANK is
COUNT(D/=0), with no numerical-rank threshold. Require N>=1, matching shapes,
finite symmetric positive-semidefinite input and compatible default INTEGER.
The reduction reads the lower triangle; no symmetry/definiteness check is made.
Clipping means this is not a valid general indefinite symmetric eigensolver.
QL exhaustion STOPs after its iteration limit; no output convergence status
is exposed. VERBOSE prints trace diagnostics only.

The main checks 96 matrices: N=1..8, four families (known diagonal spectrum,
rank-one outer products, Toeplitz 0.5**abs(i-j), and dense Gram+.25*I), and
scales 1e-8/1/1e8. It independently computes eigenpair residuals, U-transpose U,
trace preservation, sorted nonnegative eigenvalues, the routine's exact-zero
rank convention and unchanged input. Residual/trace errors are normalized by
the matrix infinity norm, including at small scales. Tolerance is 2e-11;
maxima were 7.993606e-16 (residual), 2.109424e-15 (orthogonality) and
8.162378e-16 (trace). The rank check tests the documented counting convention,
not correct numerical rank for the rank-one family. Indefinite/asymmetric
inputs, QL failure, zero matrices, large N, optimized builds and other compilers
were not checked. Other module routines were compiled but not executed.

## License scope

The root MIT notice remains recorded. AVEVAR and the private TRED2, TQLI and
PYTHAG sections carry explicit Numerical Recipes copyright notices. Their
redistribution terms are not resolved by this review; the catalog license
record is updated to flag the mixed provenance. This directory contains
original catalog checking programs and a downloader, not copied upstream
implementations. Existing RK4/Akima source reviews are unchanged and were not
newly executed here.
