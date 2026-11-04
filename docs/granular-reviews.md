# Detailed GAMS review progress

This review examines individual implementations after broad discovery. A leaf
class is the most specific classification in that GAMS branch; a long code is
not inherently more precise than a short leaf such as G2i. Classification does
not establish correctness or successful compilation.

Reviewed on 2026-11-04. Fourteen repositories now have nineteen additional source-reviewed
mappings, seventeen at leaf classes. Full commit pins, file hashes, procedure names
and inspected line ranges are in [the generated review ledger](local-reviews.md)
and `data/local.json`.
The original broad documentation reviews remain available.

| Repository | Detailed classes | Implementation reviewed | Material limits |
| --- | --- | --- | --- |
| [ACRS](https://github.com/DerivativeFreeLibrary/ACRS) | G2i | Objective-only working-set search, weighted Price reflection and box projection | Implementation restricts bound magnitudes. Objective spread and resource limits do not prove global optimality. |
| [DDFSA](https://github.com/DerivativeFreeLibrary/DDFSA) | G2i | Bounded random proposals, exponential acceptance threshold and derivative-free box line searches | A working-set method is implemented; the name alone does not establish distributed-memory execution. Supplied target values and stopping tolerances are not accuracy certificates. |
| [DIRDFN](https://github.com/DerivativeFreeLibrary/DIRDFN) | G2i; G2h3b2 | DIRECT global partitioning, CS-DFN nonsmooth local search, value-only equality/inequality callbacks and penalties | Finite variable bounds are required. Nonsmooth scope does not imply arbitrary discontinuities are covered by convergence theory. |
| [DIRMIN](https://github.com/DerivativeFreeLibrary/DIRMIN) | G2i | DIRECT rectangle selection plus budget-triggered derivative-free local searches | Shared local-search code has discrete branches, but the inspected path initializes the integer indicators to zero; no integer-programming claim is added. |
| [MODIR](https://github.com/DerivativeFreeLibrary/MODIR) | G2i | Vector objectives, nondominated sets, rectangle subdivision and budgeted global/local phases | The supplied main sets the global-phase budget to zero. Enable that phase explicitly before using it as a MODIR example. No complete Pareto-front guarantee is claimed. |
| [FIRD](https://github.com/fsobral/fird) | G2h3b1 | Smooth objective/constraints, filter restoration, constraint linearization and actual Jacobian callbacks | Objective derivatives are not required, but constraint derivatives are. No derivative-specific leaf matches this mixed interface; the smooth parent is retained. ALGENCAN is an external dependency. |
| [Skinny](https://github.com/fsobral/skinny) | G2h3b | Relaxed nonlinear inequalities, extreme-barrier evaluations, compass restoration and compass/SDS improvement | The default restoration uses values only. ALGENCAN restoration and several advertised optimizer branches return before commented implementations. Smoothness assumptions are insufficiently established to select a leaf. The signed-constraint encoding in the toy example needs checking before treating it as an equality driver. |
| [AR4](https://github.com/johngardenghi/ar4) | G1b1c | User gradient/Hessian, optional third-derivative tensors, regularized Taylor models and ALGENCAN model solves | The mapped p=2/3 modes require supplied derivatives; p=3 needs a third derivative beyond those named by the class. No third-derivative GAMS child exists. The p=1 path is not mapped. |
| [Accelerated DF-SANE](https://github.com/johngardenghi/dfsaneacc) | F2 | Square residual interface, nonmonotone residual steps and QR-based sequential-secant acceleration | F2 is already a leaf. Internal least-squares acceleration does not establish a general rectangular least-squares solver. Root uniqueness and enumeration are not claimed. |
| [SDMINMAX](https://github.com/DerivativeFreeLibrary/SDMINMAX) | G1b2 | Finite minimax objective, log-sum-exp smoothing and derivative-free line searches | The executable exposes no linear-constraint or bound interface despite the cited paper's scope. No constrained-solver mapping is inferred. Smoothing accuracy and the author's benchmark minimum were not checked. |
| [Extrapolation Integration](https://github.com/irukoa/Extrapolation_Integration) | H2a1b2 | Equally spaced sampled-data Richardson quadrature with nested trapezoidal approximations | The result needs interval-length scaling. The non-dyadic fallback appears to weight natural-order samples incorrectly; see the source finding below. No adaptive error control or checked accuracy is claimed. |
| [KogAcc](https://github.com/venovako/KogAcc) | D6 | Real64 square-matrix cyclic/quasi-cyclic Kogbetliantz SVD and the libpvn 2-by-2 kernel boundary | D6 is already a leaf. This mapping does not certify rectangular, blocked, dynamic or complex variants. INFO has step-budget/sweep-count semantics, and the small kernel is an external dependency. |
| [Fortran introsort](https://github.com/suzuyuyuyu/Fortran-introsort) | N6a2a; N6a2b; N8 | Active integer/real sorting via partition, insertion and heap paths, plus companion-array permutations | The actual module is mod_introsort. History is caller-initialized; it does not make the sort passive. Empty inputs, stability, NaNs and performance were not checked. |
| [Fortran mergesort](https://github.com/suzuyuyuyu/Fortran-mergesort) | N6a2a; N6a2b; N8 | Active integer/real vector and matrix-column sorting, plus gather permutations | Descending wrappers reverse data without reversing history. A matrix sort uses one reference row to move complete columns. No passive-rank API is claimed. |

[G2i](https://gams.nist.gov/cgi-bin/serve.cgi/Class/G2i) covers global solution
to nonconvex optimization problems and has no subclasses.
[G2h3b2](https://gams.nist.gov/cgi-bin/serve.cgi/Class/G2h3b2) covers general
nonlinear functions with equality and inequality constraints, with no smoothness
assumption, and also has no subclasses. Mapping to these classes describes the
implemented problem scope, not a proven solution on every input.

No upstream program was built or run in this batch. Author main programs and
problem definitions are recorded as possible future driver starting points.

GAMS's derivative-specific leaves do not cover every mixed derivative interface.
Keep a parent class when a leaf would misstate requirements. A function-value
interface alone also does not establish convergence on nonsmooth functions.

## Source findings to follow up

These observations come from inspection, not execution of upstream programs.
They do not change the classification of the mathematical problem implemented.

* **Extrapolation Integration fallback:** at the
  [reviewed commit](https://github.com/irukoa/Extrapolation_Integration/blob/5472eb6f2b85c5ff2337f3e52acd2d689335c078/src/Extrapolation_Integration.F90#L308-L354),
  a non-dyadic sample count bypasses the endpoint-first reordering, but
  `trap_rdp` half-weights the first two array entries. Applying that displayed
  formula to the natural-order samples `[0, 1/3, 2/3, 1]` predicts `11/18`;
  the composite trapezoidal integral of the same linear data on `[0,1]` is
  `1/2`. Reproduce in a compiled driver before reporting or proposing a fix.
* **Mergesort descending history:** the
  [integer wrapper](https://github.com/suzuyuyuyu/Fortran-mergesort/blob/fb8d241576af567597f357cd1b2491f7b3b16dba/src/merge_sort.F90#L32-L58)
  moves history during ascending merges, then calls the reverse routine only
  on `arr`. The real and matrix wrappers follow the same pattern. For data
  `[2,1]` and initial history `[1,2]`, the source predicts descending data
  `[2,1]` with history `[2,1]`, which no longer indexes the original data into
  that order. This remains an inspection finding pending a compiled check.

Next numerical reviews: DNAD's reusable differentiation/discretization core,
the minimum-radius ball-covering routines, and other independently reviewed
numerical libraries. Benchmark collections remain separate from implemented
solvers.
