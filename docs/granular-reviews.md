# Detailed GAMS review progress

This review examines individual implementations after broad discovery. A leaf
class is the most specific classification in that GAMS branch; a long code is
not inherently more precise than a short leaf such as G2i. Classification does
not establish correctness or successful compilation.

Reviewed on 2026-11-04. Five repositories now have six additional source-reviewed
leaf mappings. Full commit pins, file hashes, procedure names and inspected line
ranges are in [the generated review ledger](local-reviews.md) and `data/local.json`.
The original broad documentation reviews remain available.

| Repository | Detailed classes | Implementation reviewed | Material limits |
| --- | --- | --- | --- |
| [ACRS](https://github.com/DerivativeFreeLibrary/ACRS) | G2i | Objective-only working-set search, weighted Price reflection and box projection | Implementation restricts bound magnitudes. Objective spread and resource limits do not prove global optimality. |
| [DDFSA](https://github.com/DerivativeFreeLibrary/DDFSA) | G2i | Bounded random proposals, exponential acceptance threshold and derivative-free box line searches | A working-set method is implemented; the name alone does not establish distributed-memory execution. Supplied target values and stopping tolerances are not accuracy certificates. |
| [DIRDFN](https://github.com/DerivativeFreeLibrary/DIRDFN) | G2i; G2h3b2 | DIRECT global partitioning, CS-DFN nonsmooth local search, value-only equality/inequality callbacks and penalties | Finite variable bounds are required. Nonsmooth scope does not imply arbitrary discontinuities are covered by convergence theory. |
| [DIRMIN](https://github.com/DerivativeFreeLibrary/DIRMIN) | G2i | DIRECT rectangle selection plus budget-triggered derivative-free local searches | Shared local-search code has discrete branches, but the inspected path initializes the integer indicators to zero; no integer-programming claim is added. |
| [MODIR](https://github.com/DerivativeFreeLibrary/MODIR) | G2i | Vector objectives, nondominated sets, rectangle subdivision and budgeted global/local phases | The supplied main sets the global-phase budget to zero. Enable that phase explicitly before using it as a MODIR example. No complete Pareto-front guarantee is claimed. |

[G2i](https://gams.nist.gov/cgi-bin/serve.cgi/Class/G2i) covers global solution
to nonconvex optimization problems and has no subclasses.
[G2h3b2](https://gams.nist.gov/cgi-bin/serve.cgi/Class/G2h3b2) covers general
nonlinear functions with equality and inequality constraints, with no smoothness
assumption, and also has no subclasses. Mapping to these classes describes the
implemented problem scope, not a proven solution on every input.

No upstream program was built or run in this batch. Author main programs and
problem definitions are recorded as possible future driver starting points.

Next numerical reviews: FIRD and Skinny (distinguish objective and constraint
derivative requirements), SDMINMAX (finite minimax and constraint scope), AR4
(higher-order derivatives), and accelerated DF-SANE (nonlinear systems).
Quadrature and linear-algebra procedures follow. Benchmark collections remain
separate from implemented solvers.
