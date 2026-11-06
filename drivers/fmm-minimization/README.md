# FMM scalar minimization

Complete main for `ForsytheMalcolmMoler::BrentMin` and `::Fmin`, mapped to
GAMS G1a1a (smooth univariate minimization without supplied derivatives).
The immutable source is `fmm.f90` at
[b850d06d29e348a803feaba58c0b68a8fdd5c5f1](https://github.com/Beliavsky/Computer-Methods-for-Mathematical-Computations/blob/b850d06d29e348a803feaba58c0b68a8fdd5c5f1/fmm.f90).
The runner downloads and hash-verifies that file, compiles it unmodified in
a temporary directory and links this main. Numerical source is not bundled.

```sh
python drivers/fmm-minimization/run.py --report drivers/fmm-minimization/results.json
```

The runner accepts `--compiler` but uses GNU flags. The saved report records
GNU Fortran 17.0.0 20260510 (experimental) on Windows. Module and main both
use `-O0 -g -Wall -Wextra -ffree-line-length-none -fcheck=all
-ffpe-trap=invalid,zero,overflow`. No permissive mismatch flags or source edits
are used. SHA-256 hashes use UTF-8 text normalized to LF endings; results.json
retains flags, source pin, warnings, output and return codes.

## Checks

Use DP=SELECTED_REAL_KIND(10,50), matching the module's double interface.
The callback supplies only scalar function values. The routine combines
parabolic interpolation with golden-section steps over a finite interval.

The main tries both public APIs on four smooth functions of
`t=(x-center)/width`: `t**2`, `t**4`, `exp(t)-t-1`, and
`t**2*(1+0.1*t+0.05*t**2)`, multiplied by a positive amplitude. Each has its
known unique minimum at t=0. Centers -3,0,4; widths .25,1,3; and amplitudes
1e-6,1,1e6 produce 216 API comparisons. Search intervals extend from
center-width to center+1.5*width. The search tolerance is 1e-10*width;
BrentMin has 500 iterations, while Fmin fixes its limit at 100.

Every result must be finite, remain inside the interval, have location error
<=5e-5 times width, and objective error <=1e-8 times amplitude. The value
returned by BrentMin must agree with a fresh callback evaluation within
1e-12 times amplitude, and NEVAL must equal an independently counted number
of calls. Both initial repeated callback evaluations are counted.
Maximum normalized location and objective errors were 7.381406e-8 and
2.664535e-15. These are finite empirical checks, not certified error bounds.
The exp-based objective suffers cancellation near its minimum, so a requested
small interval tolerance must not be interpreted as that much location accuracy.

## Important status limitation

BrentMin initializes errCode=0 but never sets it when maxIter is exhausted,
despite declaring 1 as the exhaustion code. A separate deliberate one-iteration
quadratic probe returns zero status while remaining about .036 from the known
minimizer. This is recorded as a reproduced limitation, not a successful
convergence case. Fmin additionally discards errCode and NEVAL and returns
only the last minimizer estimate. A caller cannot rely on either interface
to report nonconvergence; independently validate the returned estimate or
repair the status contract before relying on arbitrary objectives/budgets.
The driver does not patch this behavior.

Unimodality, valid ordered endpoints, positive tolerance and finite callback
values are caller responsibilities. Endpoints themselves are not explicitly
compared, no global minimum is guaranteed on multimodal inputs, and invalid
inputs are not rejected. Single precision, noisy/nonsmooth objectives,
endpoint minima, flat plateaus, extreme scales, other compilers and optimized
builds remain unchecked. Existing inherited-source license findings and other
FMM algorithm caveats remain unchanged.
