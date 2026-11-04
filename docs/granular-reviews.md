# Detailed GAMS review progress

This review examines individual implementations after broad discovery. A leaf
class is the most specific classification in that GAMS branch; a long code is
not inherently more precise than a short leaf such as G2i. Classification does
not establish correctness or successful compilation.

Reviewed on 2026-11-04. Nineteen repositories now have twenty-seven source-reviewed
mappings. Full commit pins, file hashes, procedure names
and inspected line ranges are in [the generated review ledger](local-reviews.md)
and `data/local.json`.
The original broad documentation reviews remain available.

## Reviewed calling interfaces

Eighteen repository cards now identify public routines and link their usage lines
to pinned argument declarations. A nineteenth, DDFSA, identifies the supplied
program entry point and keeps its benchmark harness among implementation helpers.
Detail pages distinguish these roles. Module names and procedure names are stored
separately. All nineteen independently source-reviewed repositories now have an
entry-point annotation and a scoped license finding. These are source-inspected
interfaces, not new compilation or numerical checks or complete public-API audits.

| Repository | Entry points | Recorded license |
| --- | --- | --- |
| ACRS | `ACRS` (external subroutine) | GPL-3.0-or-later |
| DDFSA | `MAIN_GLOB` (program); `SENZADERGLOB` is a linked-problem benchmark harness | GPL-3.0-or-later |
| DIRDFN | `dirdfn` (external subroutine; linked problem routines and shared state) | GPL-3.0-or-later |
| DIRMIN | `nuovoglobale` (external subroutine; shared-state setup required) | GPL-3.0-or-later |
| MODIR | `wrapper` (external coordinator; separate MODIR/DFMO budgets and linked problem routines) | GPL-3.0-or-later |
| SDMINMAX | `MAINBOX` (external finite-minimax routine; workspace and COMMON setup required) | GPL-3.0-or-later |
| FIRD | `fird` (external wrapper; objective, constraint and constraint-Jacobian callbacks) | MIT |
| Skinny | `skinny::sksolve` (linked problem evaluators; some solver branches are stubs) | MIT |
| AR4 | `arp::arp_load`, `arp::arp_solve` | Multiple licenses; root GPL v3 and separate ALGENCAN notice |
| Accelerated DF-SANE | `bmdfsaneacc::dfsaneacc` | No license identified in reviewed Fortran material |
| Fortran introsort | `mod_introsort::sort`, `mod_introsort::apply_permutation` | MIT |
| Fortran mergesort | `merge_sort_mod::sort`, `merge_sort_mod::rearrange` | No license identified in reviewed material |
| Extrapolation Integration | `Extrapolation_Integration::extrapolation` (public generic function; inspected REAL(dp) binding) | GNU GPL version 3; version-only versus or-later scope unresolved |
| KogAcc | `DKSVD0` (external real64 square SVD; schedule/workspace initialization required) | MIT, unless noted otherwise |
| Fortran_DNAD | `dnadmod::exp`, `dnadmod::sin`; model-dependent `BAND_mod::ABDGXY`, `BAND_mod::BAND`, `BAND_mod::MATINV`; diffusion program `unsteady` | Custom DNAD component notices; project-wide terms unresolved |
| Minimum-radius ball covering | `VorCells_Polygons::VorCellInterConvPol`, `VorCells_Polygons::interCellBall` | No project-wide license identified in reviewed material |
| gfsolver | `mod_gfsolver::sub_newton`, `mod_gfsolver::sub_hybrid_nb` | MIT-style notice with a citation request |
| FortranConsoleSpline | `mod_splines::spline` constructor; `spline%value`, `spline%slope`, `spline%slope2` bindings | MIT |
| Legendre-Gauss-Lobatto Quadrature | `legendre_gauss_lobatto::LGL_nodes_weights`, `legendre_gauss_lobatto::LGL_quadrature` | GNU GPL version 3; version scope unresolved |

Pinned license evidence, declaration ranges, author examples and calling sketches
are retained in [the review ledger](local-reviews.md). A generic's private
implementation names are not promoted as public APIs. The mergesort descending
history issue below remains unresolved; the calling sketches use ascending sorts.
The integration sketch uses dyadic samples and retains the non-dyadic fallback
finding below. DDFSA's program writes `risultato.tex` and uses ten runs; it is not
presented as a general callback-driven library routine. KogAcc's `INFO` needs input
initialization as a step-budget/mode control, unlike an output-only error code.
MODIR's supplied main disables the global phase with a zero budget; the calling
sketch enables it explicitly. SDMINMAX's `MAINBOX` name does not imply bounds or
linear constraints. DNAD's specific `exp_d` and `sin_d` routines remain private;
cards show their public generics. Its model engine still requires the selected
model's shared arrays, module ordering and adapted absolute include paths.

## Source mappings

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
| [Fortran_DNAD](https://github.com/nickbrady/Fortran_DNAD) | H1; D2a2; I2a1a | Forward first-derivative propagation, concentration/gradient seeds, block-band elimination and a one-dimensional diffusion example | Derivative count is tied to user_input. Block tridiagonal does not mean scalar tridiagonal. The example and module wiring contain absolute author-machine include paths and require adaptation before compiling. Scientific application models are outside this review. |
| [Minimum-radius ball covering](https://github.com/johngardenghi/bglcovering) | G2h3; P | Radius objective, covered-area constraint, derivative callbacks, Voronoi/polygon clipping and polygon/circle intersections | Optimization delegates to external ALGENCAN/HSL/BLAS. Smoothness-specific and equality/inequality branches remain pending review of geometric regularity and the external solver convention. P itself has no finer GAMS classes. |
| [gfsolver](https://github.com/gfell/gf_solver) | F1b | Scalar Newton search and sign-oriented Newton/bisection fallback using value/derivative subroutines | No bracket validation or failure status; failure paths STOP. Division precedes the small-derivative check. Fallback does not forward optional controls. |
| [FortranConsoleSpline](https://github.com/ja72/FortranConsoleSpline) | E1a | Cubic-spline construction and type-bound value/derivative evaluation | An interior coefficient mixes an abscissa with an index; arbitrary-grid correctness requires a compiled check. Extrema enumeration is not mapped. |
| [Legendre-Gauss-Lobatto Quadrature](https://github.com/SpirosZafeiris/Legendre-Gauss-Lobatto-Quadrature) | H2a1b2 | LGL node/weight construction and weighted integration of caller-sampled data | Sample at mapped rule nodes, not arbitrary grid points. Fixed iteration limits have no status; triplet-style constructors require compiler support or adaptation. No accuracy check was run. |

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
Likewise, a block-tridiagonal solver with wider scalar bandwidth and special
boundary couplings remains under D2a2 rather than scalar-tridiagonal D2a2a.
H1 and P are already leaves: specific procedures provide useful detail even
where the official taxonomy has no further subdivisions.

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

* **gfsolver division and fallback controls:** the
  [Newton loop](https://github.com/gfell/gf_solver/blob/0926b61db2c0fa3fa2e1b874ef5ac15d5d6df432/gf_solver.f90#L76-L93)
  divides by the derivative before testing whether it is small. On direct
  success, `fnorm` records the function value from before the final point update.
  The [fallback call](https://github.com/gfell/gf_solver/blob/0926b61db2c0fa3fa2e1b874ef5ac15d5d6df432/gf_solver.f90#L128-L135)
  omits optional controls, so the hybrid defaults apply instead of the Newton
  caller's tolerances/iteration limit. These are unexecuted source observations.
* **FortranConsoleSpline interior coefficient:** the
  [construction recurrence](https://github.com/ja72/FortranConsoleSpline/blob/88f138a0a8ad8e71c89237df5fc236097ab695cc/mod_splines.f90#L47-L51)
  uses `sig = (x(i)-(i-1))/(x(i+1)-x(i-1))`. The numerator uses an integer
  index where the arbitrary-grid cubic-spline recurrence uses the previous
  abscissa, `x(i-1)`. An independently checked arbitrary-grid driver is needed
  before relying on the coefficients or reporting a numerical error.
* **LGL compiler portability:** the
  [Gauss constructor](https://github.com/SpirosZafeiris/Legendre-Gauss-Lobatto-Quadrature/blob/8ff674ed77eff6ed7e0c1b58755a182c4a5e1260/lgl.f90#L100-L103)
  and [Jacobi-node helper](https://github.com/SpirosZafeiris/Legendre-Gauss-Lobatto-Quadrature/blob/8ff674ed77eff6ed7e0c1b58755a182c4a5e1260/lgl.f90#L188-L191)
  use triplet-style array constructors such as `[size_r:1:-1]`. Build support
  for that syntax and the intended node generation must be checked; no compiler
  failure is claimed from source inspection alone.

Next numerical reviews move to other independently reviewed linear-algebra,
quadrature and differential-equation libraries. Benchmark collections remain
separate from implemented solvers. The ball-covering derivative callbacks and
DNAD examples remain candidates for later compiled checks, not checked drivers.
