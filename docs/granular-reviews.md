# Detailed GAMS review progress

This review examines individual implementations after broad discovery. A leaf
class is the most specific classification in that GAMS branch; a long code is
not inherently more precise than a short leaf such as G2i. Classification does
not establish correctness or successful compilation.

Reviewed on 2026-11-05. 116 repositories now have 136 source-reviewed
mappings. Full commit pins, file hashes, procedure names
and inspected line ranges are in [the generated review ledger](local-reviews.md)
and `data/local.json`.
The original broad documentation reviews remain available.

## Reviewed calling interfaces

112 repository cards now identify public routines and link their usage lines
to pinned argument declarations. Four further cards?DDFSA, CWT, polyfit and
StatTools?identify supplied program entry points and keep their internal/benchmark
routines among implementation helpers.
Detail pages distinguish these roles. Module names and procedure names are stored
separately. All 116 independently source-reviewed repositories now have an
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
| LAPACK | `DGESV`, `DGELS`, `DSYEV` (external double-precision drivers) | BSD-3-Clause-Open-MPI |
| lagrange_interpolator | `type_LagrangeInterpolator::LagrangeInterpolator%perform_1d_interpolation`, `%perform_2d_interpolation` | No license identified in reviewed material |
| FORTRAN-Roots | `MOD_Roots::fun_zero`, `MOD_Roots::poly_roots` | No license identified in reviewed material |
| GetRootsF | `roots::hybridD`, `roots::hybridSA` | No license identified in reviewed material |
| FORTRAN-ODE-Toolbox | `MOD_ODE_Toolbox::ODE_Numerical_Solve_RK4`, `::ODE_Numerical_Solve_RK4_Adaptive` | GNU GPL version 3; version scope unresolved |
| Akima with Derivatives | External `setup`, `SETUP_DV`, `interp` | Apache-2.0 |
| adjac | `adjac::adjac_reset`, `::adjac_set_independent`, `::adjac_get_dense_jacobian`, `::adjac_free` | BSD-3-Clause core; separate FFTPACK notice |
| generic_rk | `runge_kutta::rk_wrapper` | BSD-2-Clause |
| Interpolation in 2D and 3D | `quadratic_shepard_2d::qshep_2d%create_mesh`, `%interpolate_point`, `%gradient_point` | MIT wrappers; ACM numerical-core notice |
| chol-rev | External `DPO2FT`, `DPOFRT` (lower-factor reverse differentiation) | MIT and BSD-3-Clause-Open-MPI component notices |
| findiff | `findiffmod::findiff`, `::findiff_multiscale`, `::findiffhes` | No license identified in reviewed material |
| libdierckx FITPACK | External `splder`, `splint` | No license identified in reviewed material |
| ORTHPOL | External `dgauss` (rule generation from recurrence coefficients) | No license identified in reviewed material |
| triasymq | External `triasymq` (triangle nodes and weights) | BSD-3-Clause core; modified BSD notice for some helpers |
| NITSOL | External `nitsol` (square residual system; reviewed GMRES path) | No license identified in reviewed material |
| JFNK-Hookstep | External `newtonhook`; state in module `newton` | GNU GPL version 3; version scope unresolved |
| easydop853 | `easydop853_module::easydop853` | BSD-3-Clause and BSD-2-Clause component notices |
| fortran-rbf | `rbf_mod::rbf_type%build` (stencil matrices, not data-value evaluation) | No license identified in reviewed material |
| PPR | `ppr_1d::rcon1d`, `::rmap1d` (reviewed PCM path) | Custom research/noncommercial terms |
| newspline | `newsplinemod::newspline` (reviewed unbounded path) | Root GPL v3; Numerical Recipes utility terms unresolved |
| Expokit | External `DGPADM` (dense real full matrix exponential) | Custom noncommercial terms |
| NdSpline | `NdSpline::spline%init`, `%interpolate`, `%fin` | BSD-2-Clause |
| polynomial_interpolation | External `poly_interp`, `grid_interp` | GNU GPL version 3; version scope unresolved |
| autodiff (sgeard) | `AVD::init`, `::exp` (reviewed `avd_d4` overload) | MIT |
| dnad (joddlehod) | `dnadmod::exp` (public generic; seeded first-derivative vectors) | Custom DNAD copying/modification notices |
| FORbID | `newton_cotes_integrator%init`, `%integrate_1D`; `romberg_integrator%init`, `%integrate_1D` in their defining modules | README conditional GPL/BSD/MIT licensing notice |
| Cyclic banded matrix solvers | External `DCTSV` (cyclic) and `thomas` (ordinary tridiagonal) | Custom BSD-style terms with machine-learning restrictions |
| chebpak | `chebyshev_m::cheb_node`, `::bary_weights`, `::lag_intrp` (reviewed CGL interpolation path) | MIT; external MKL terms separate |
| Numerical Differentiation | `LIBRARY_REAL8::DIFF`, external `FDM` (finite-difference path) | Root GNU GPL version 3; component/version scope unresolved |
| L-BFGS (jmbr) | External `LBFGS` (reverse communication; `LB2` block-data defaults) | README BSD declaration; variant unspecified |
| NNLS Fortran 2018 | `nnls::solve` (Fortran and C binding) | GNU GPL version 3; version scope unresolved |
| QuadProg modern Fortran | `QuadProg::qp_problem`, `::solve` (standard dense constrained path) | Root GPL v3; driver GPL-2.0-or-later notice |
| Akima86 | External `uvipia` (reviewed general ND>=5 path) | Custom NRLMMD/GeoIPS redistribution and acknowledgment terms |
| FoLLiA | `follia::lagrange_interpolator%initialize_interpolator`, `%compute_coefficients`, `%compute_interpolations` | README conditional GPL/BSD/MIT licensing notice |
| SPRINT | `bilinear_interpolator_mod::bilinear_interpolator_type%init`, `%prepare`, `%apply` (restricted REAL(4) illustration) | No project license identified in reviewed material |
| FFTE | External `ZFFT1D` (complex 1D driver) | Custom use/modification grant; original-package redistribution |
| modern_fftpack | `type_FFTpack::FFTpack%fft`, `%ifft` (complex 1D bindings; facade `fftpack_library`) | MIT root notice; inherited FFTPACK terms not fully audited |
| FFTW3 wrapper | `fftw3_wrapper::fft`, `::ifft` (complex REAL64 1D bindings) | GNU GPL version 3; version scope unresolved; FFTW terms separate |
| gamma_f77 | `GAMMA_MOD::TGAMMA` (real Gamma in a selected 32-digit kind) | BSL-1.0 |
| elliptic_k_using_agm_fortran | `elliptic_k_using_agm_fortran::elliptic_k` (REAL64 overload) | MIT; external dependency terms separate |
| spherical_bessel_fortran | External `sbessj` (real spherical first-kind function) | LGPL-3.0-or-later routine; separate comparison-code notice |
| MINPACK (certik) | External `hybrd1`, `lmder1`; `minpack` module interface reviewed | MIT and original MINPACK redistribution notices |
| stroud_quad | `quad_mod::hermit` (Gauss-Hermite nodes/weights) | No license identified in reviewed material |
| modern_quadpack | External `dqag` (bundled legacy double-precision entry) | No license identified in reviewed material |
| fftlog-f90 | External `fhti`, `fftl` (log-grid sine/cosine library entries) | MIT root notice; inherited FFTLog components separate |
| ellipFor | `elliptic::complete_elliptic_integrals` | GPL v3 project notice; CC-BY-SA-4.0 adapted components |
| Polylogarithm | External `dli2` (real dilogarithm) | MIT |
| FTLib | `ftlib_quadrature::trapezoidal_rule`, `::gaussian_quadrature` (scoped overloads) | No license identified in reviewed material |
| spline_interpolation_fortran | External `splift`, `splint` | Source GPL v2 notices; inherited search terms unresolved |
| L-BFGS-B | External `SETULB` (reverse communication) | BSD-3-Clause |
| Subplex | External `SUBPLX` (objective callback; fork omits MODE) | GPL v3 text; version scope unresolved |
| UCMINF | External `UCMINF` (R runtime/bridge required) | GPL-2.0-or-later |
| HWODE | External `DOPRI5` (fork adds LOGICAL DEBUG) | BSD-2-Clause |
| DASKR | External `DASKR` (legacy fixed-form driver) | MIT root; inherited UC/LLNL BSD and DOE notice |
| minimize | External `steepest_descent` (scalar objective/vector gradient) | MIT |
| grid_interpolation | `interpolation::bilinear` | No license identified in reviewed material |
| finite_difference | `dq_coeff_mod::calc_dq_coeff` (root variable-precision binding) | GPL-3.0-or-later |
| ABSCAB Fortran | `mod_cel::cel` | Apache-2.0 |
| Mittag-Leffler function and derivative | `mod_mlf_garrappa::mlf_garrappa` (scalar binding) | Author public-domain statement and citation request; inherited terms not fully audited |
| Jacobi theta functions | `jacobitheta::theta3` | No license identified in reviewed material |
| fastspline | `mcspline::cspline` | MIT-form grant with unresolved copyright placeholders |
| FFTPack | `fftpack::fft`, `fftpack::ifft` (complex-double bindings) | Bundled GPL notice without version; wrapper terms unresolved |
| Computer Methods for Mathematical Computations | `ForsytheMalcolmMoler::BrentZero` | MIT root; inherited source provenance recorded separately |
| AFNL | `Integration::Trapecio`, `Integration::Simpson` (DP bindings) | GPL-2.0-or-later |
| fast_math | `fast_erf::ferf` (elemental real32/real64 generic) | MIT |
| PyIntegral | External `GaussLegendreQuadrature` (tabulated-data integration) | Custom noncommercial terms; redistribution requires permission |
| Alexander Mead library | `calculus::derivative` (1D binding) | No license identified in reviewed material |
| modforutils | `binomial_coefficients::binomialCoef`, `::binomialCoefsArray` | Custom six-condition license |
| numfor | `csplines::csplrep`, `csplines::csplev` | No grant identified for the reviewed spline module |
| PyFluxconserving | External `LINinterpol` (not the flux-conservation dispatcher) | Custom noncommercial terms; redistribution requires permission |
| CWT | `cwt` program; contained wavelet/quadrature helpers | GPL v3 text; version choice unresolved |
| Pade_approximants | `padem::acPade` (matrix/double-precision solve path) | MIT root; numerical dependency terms separate |
| libcoul90 | `libcoul90::coul90` (real Coulomb path) | MIT root; inherited numerical rights not fully resolved |
| Fortran_Davidson | `davidson_dense::generalized_eigensolver_dense` (ordinary DPR path) | Apache-2.0 |
| qrupdate-ng | External `DQR1UP` (real rank-one QR update) | GPL-3.0-or-later |
| PROPACK | External `DLANSVD` (nonrestarted real truncated SVD) | No grant identified in reviewed material |
| minila | `linsys::linsol` (vector binding) | GPL v3 text; version choice unresolved |
| Bolander linear algebra library | External `cholesky_factor` | No license identified in reviewed material |
| fortsparse | `fortsparse_csr::csr_matvec` (real64 service) | MIT core; backend licenses separate |
| Fortran_CSR | `csrmodule::CSRcomplex%matmul` (native fallback) | MIT |
| Linear System Solvers | `mod_lis_linear_solver::lis_linear_solver_t%Keep_lsys_ops_and_solve` | No adapter license identified |
| DualSimplex | `DUALSIMP_MOD::DUALSIMPLEX` | MIT |
| LightConvex | `lightconvex_lp::linear_program`, `lightconvex_lp::solve` (primal-simplex LP path) | MIT root; component terms separate |
| vc-sqnm | `sqnm::sqnm_optimizer%sqnm_step` (fixed-coordinate Fortran optimizer) | GPL-3.0-or-later |
| Differential-Evolution_f95 | `DE_mod::Diff_Evol` (built-in objective) | MIT |
| pso | `psomod::optimizer` (star topology) | GPL-2.0-or-later |
| TRDF | External `TRDF` (linked objective/constraints and ALGENCAN path) | No license identified in reviewed material |
| DFO mirror | External `dfo` (legacy linked-problem driver) | CPL-1.0 |
| LMBM | External `LMBMU` (linked objective/subgradient) | No redistribution grant identified in reviewed files |
| polyfit | Program `polyfit`; independent fitting helpers remain internal | GPL v3 text; version scope unresolved |
| samplestat | `SampleStatistics::ArithMean`, `::Variance`, `::StdDev` | GNU GPL notice; version/module scope unresolved |
| StatTools | Program `statistics`, installed as `st_statistics` | GPL v3 root; support source GPL-3.0-or-later |
| Fortran-Metrics | `metrics_mo::metrics_ty%calc` (vector overload) | MIT |
| normal-deviates | `pmnrg::MultiNormalGenerator%get` and constructor | MIT |
| mtprng | `mtprng::mtprng_init`, `::mtprng_rand_real2` | Original custom notices and GPL-3.0-or-later modifications |
| sobseq | `mod_sobseq::sobol_state%initialize`, `%next`, `%skip_ahead` | MIT |
| pcg-fortran | `pcg_fortran::pcg_state_oneseq_64_type%random_number_xsh_rr` | MIT |

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
| [LAPACK](https://github.com/Reference-LAPACK/lapack) | D2a1; D9a1; D4a1 | DGESV LU-solve dispatch, DGELS QR/LQ least-squares paths and DSYEV symmetric eigensolver dispatch | Driver/source review, not a complete kernel audit. Inputs are overwritten; DGELS assumes full rank. Query workspaces and match the library ABI. No numerical tests were run here. |
| [lagrange_interpolator](https://github.com/jlokimlin/lagrange_interpolator) | E1a; E2a | Adjacent-point 1D linear interpolation and repeated 1D interpolation on a 2D grid | The name does not establish higher-order Lagrange interpolation. Source findings affect constant extrapolation, status handling and the 2D temporary-vector initialization. Node-only author checks are not between-node verification. |
| [FORTRAN-Roots](https://github.com/bryand4140/FORTRAN-Roots) | F1b; F1a | Secant/bisection scalar search and balanced-companion double-QR polynomial roots | Strict endpoint sign test rejects endpoint roots. Interior NaN checking depends on printing. Polynomial accuracy hint is heuristic. |
| [GetRootsF](https://github.com/physicsfan/GetRootsF) | F1b | Newton/bisection and derivative-free accelerated-secant/bisection branches | Bracket-update operands need correction/checking; candidate-relative stopping can divide by zero. No returned convergence flag. Range scanning is not all-root enumeration. |
| [FORTRAN-ODE-Toolbox](https://github.com/bryand4140/FORTRAN-ODE-Toolbox) | I1a1a | Classical fixed RK4 and adaptive RK4 step doubling | Fixed and adaptive arrays have opposite orientations. Fixed output needs at least two time points. Adaptive discrepancy is absolute and not a global error bound. No stiff mapping added. |
| [Akima with Derivatives](https://github.com/andrewning/akima) | E1a; H1 | Smoothed Akima cubic construction, tangent coefficient propagation and analytic query/data derivatives | Ordered distinct nodes and n >= 3 required. End-polynomial extrapolation is not generally reliable. Sensitivities differentiate the interpolant, not an unknown sampled function. |
| [adjac](https://github.com/pv/adjac) | H1 | Real overloaded product rule, derivative tape and dense Jacobian extraction | Shared tape/mode lifecycle needs coordination. Only the real dense path is source reviewed; complex, COO, FFT and tapeless variants are not certified. |
| [generic_rk](https://github.com/cbcoutinho/generic_rk) | I1a1a | Active Dormand-Prince tableau selection and adaptive explicit stage path | Stage state accumulates across stages instead of resetting. Initial endpoint clipping needs attention. Hard-coded tolerances, unit-22 output and STOP on exhaustion; no stiff mapping. |
| [Interpolation in 2D and 3D](https://github.com/arjenmarkus/interpolation2d3d) | E2b | Planar modified quadratic Shepard fit, weighted local evaluation and interpolant gradients | Only the 2D path reviewed. Default REAL, at least six samples, construction/status checks required; unsupported queries are not general extrapolation. |
| [chol-rev](https://github.com/imurray/chol-rev) | H1 | Lower-factor reverse sensitivity propagation, unblocked and blocked BLAS updates | Upper path unimplemented, LDC not checked, blocked routine overwrites upper entries. Preserve triangular adjoint convention and match BLAS integer ABI. |
| [findiff](https://github.com/PunchesMalone/findiff) | H1 | Symmetric finite-difference square Jacobians and derivatives of a supplied Jacobian | Requires real128 and user-selected nonzero steps. order counts stencil points. Bundled real64 tests need consistent kinds; no automatic error estimate. |
| [libdierckx FITPACK](https://github.com/DaanVanVugt/libdierckx) | E3a2; E3a3 | B-spline derivative coefficients/evaluation and basis-integral contraction | Caller supplies valid representation; default REAL and degree at most five. Spline calculus is not arbitrary-function differentiation/integration. |
| [ORTHPOL](https://github.com/ivan-pi/orthpol) | H2c | Jacobi-matrix Gaussian nodes and weights from supplied recurrence coefficients | Caller supplies a valid measure and forms the weighted sum. deps controls node iteration, not integration accuracy. Other rule families not reviewed. |
| [triasymq](https://github.com/zgimbutas/triasymq) | H2c | Tabulated D3 triangle-rule expansion and affine area scaling | Prevalidate degree 1..50 and nondegenerate vertices. Initialize node-count capacity; no public status. Tables not numerically reverified. |
| [NITSOL](https://github.com/cmacmackin/nitsol) | F2 | Inexact Newton driver, GMRES products/corrections and residual backtracking | Small-step termination need not satisfy residual tolerance. Caller workspace, callbacks, common blocks and linked block-data defaults require care; other Krylov implementations not reviewed. |
| [JFNK-Hookstep](https://github.com/apwillis1/JFNK-Hookstep) | F2 | Newton trust-radius trials, GMRES and SVD-regularized hookstep | Caller supplies Jacobian action and shared-state initialization. GMRES flag overwritten in Newton wrapper; zero-norm normalization guards need checking. Some failures STOP. |
| [easydop853](https://github.com/GasinAn/easydop853) | I1a1a | Fixed-configuration wrapper and explicit adaptive DOP853 stage path | Fixed tolerances/step limit, endpoint-only output and ERROR STOP on failure. Stiffness detection does not establish stiff integration. |
| [fortran-rbf](https://github.com/dongli/fortran-rbf) | E3 | Local RBF matrix/inverse construction and stored derivative matrices | No fitted-value API, y unused. LAPACK build required; polynomial B initialization, node-ten debug output and Gaussian second derivative need correction/checking. |
| [PPR](https://github.com/dengwirda/PPR) | E1a | Piecewise-constant reconstruction, overlap integration and conservation-defect correction | Reviewed PCM with one mean per cell only. Matching domains/valid edge grids, initialized options and workspace required. Higher-order methods not fully reviewed. |
| [newspline](https://github.com/ARVE-Research/newspline) | E1a | Interval-mean control construction and unbounded cubic Hermite sampling | Requires >= 2 intervals and positive subdivision counts. Continuous constraints do not prove exact discrete sample means; optional bounded branches unverified. |
| [Expokit](https://github.com/rasmusgo/expokit) | D8 | Dense real Pade scaling-and-squaring and workspace result offset | Only DGPADM reviewed. Zero matrix/time and several failures STOP; caller handles identity cases. Sparse/complex/action variants remain unreviewed. |
| [NdSpline](https://github.com/Takayuki-Miyagi/NdSpline) | E2a | Tensor-product B-spline coefficient solves and target-grid basis products | Gridded data only. Solve info ignored; extrapolation flag shared across objects. k is order, so k=4 is cubic. Cleanup/reinitialization require care. |
| [polynomial_interpolation](https://github.com/jlm785/polynomial_interpolation) | E1b; E1a | Single shifted Lagrange polynomial and ordered-grid local stencils | Core evaluates at zero. Duplicate nodes invalid, high derivative correction entries may be unassigned, and grid dymax ignores negative signed corrections. |
| [autodiff](https://github.com/sgeard/autodiff) | H1 | Fourth-order scalar forward product and exponential composition rules in `src/avd.f90` | Call init before elementary functions. One scalar differentiation parameter; consistent eight-byte default REAL build requested. Other overloads and older root implementation unreviewed. |
| [dnad](https://github.com/joddlehod/dnad) | H1 | First-order dual-number product/exponential rules and derivative seeding | Compile-time ndv, default REAL kinds and explicit seed initialization required. Public generic retained; private specifics are helpers. |
| [FORbID](https://github.com/giacrossi/FORbID) | H2a1a2; H2a1a1 | Fixed closed Newton-Cotes weights and globally refined Romberg extrapolation | Higher-degree Newton-Cotes scaling appears incorrect; sketch uses n=1. Romberg exhausts its table on nonconvergence. Separate adaptive accumulator is undefined on entry; 2D/3D methods are stubs. No checked driver. |
| [Cyclic banded matrix solvers](https://github.com/mostlyharmlessone/cyclic-banded-matrix) | D2a1; D2a2a | Paired endpoint cyclic elimination with even/odd terminal solves; separate ordinary Thomas elimination | No pivoting. Cyclic intermediate determinant breakdown is not proof of full-matrix singularity. Thomas overwrites diagonal/RHS and has no status. Wider-band/OpenMP variants unreviewed. |
| [chebpak](https://github.com/saridut/chebpak) | E1b | CGL node generation, endpoint-halved barycentric weights and global polynomial evaluation | n is degree, arrays need n+1 elements. Pass ordering flag explicitly because its default is saved. Weight generator supports CGL only. MKL interfaces required; other paths unreviewed. |
| [Numerical Differentiation](https://github.com/theysy/Numerical_differentiation) | H1 | Central finite differences for gradient, Hessian diagonal and mixed entries | Fixed absolute steps and built-in objective selectors; not a callback library. Unsupported selectors lack safe failure reporting. Complex/hyper-dual correctness not audited. |
| [L-BFGS](https://github.com/jmbr/lbfgs) | G1b1b | Limited-memory inverse-Hessian action, reverse communication and line-search dispatch | Caller supplies gradient and preserves state/workspace. Saved/shared state is not reentrant. Initial zero-gradient step is unguarded; include LB2 defaults. No global/minimum certificate. |
| [NNLS Fortran 2018](https://github.com/cuamll/nnls) | D9b1 | Passive-set nonnegative least squares using normal equations | Actual normal MODE=1 differs from documented 0. DSYSV INFO is ignored and MAXITER counts only inner steps. Rank-deficient behavior and KKT accuracy unchecked. |
| [QuadProg modern Fortran](https://github.com/loiseaujc/Quadprog) | G2e1 | Positive-definite factorization and standard dense active-set QP driver | Objective uses minus q; constraints are rows with C*x>=d. No indefinite/semidefinite claim. Unconstrained obj is unset; constructor factorization status is not propagated. Author inequality test transposes C despite row-layout interface. |
| [Akima86](https://github.com/NRLMMD-GEOIPS/akima86) | E1a | Weighted endpoint-slope estimates and interval polynomial evaluation | General query loop prints thread/index diagnostics. Four-node cubic formula repeats one ordinate term; sketch uses seven nodes. Invalid input returns sentinel values without status. No shape-preservation claim. |
| [FoLLiA](https://github.com/giacrossi/FoLLiA) | E1b | Lagrange coefficient products and separate overlapping-stencil estimates | S>=2, 2*S-1 distinct ordered nodes and restricted target required. No automatic stencil combination. PENF/preprocessing required; initializer clears data. |
| [SPRINT](https://github.com/dongli/sprint) | E2a | Cached tensor-product bilinear weights and four-value application | Index/boundary defects, unassigned first apply return, unusual upper-corner order and no outside guard. REAL(4) sketch is strictly interior and explicitly prepared; general use needs fixes. Dependencies/curvilinear path unverified. |
| [FFTE](https://github.com/certik/ffte) | J1a2 | Complex driver setup, 2/3/5 factorization, radix dispatch and conjugate/scaled inverse | Initialize for current N; only 2/3/5-smooth lengths with compiled dimension limits. Large tables are saved state. No status or kernel/numerical audit. |
| [modern_fftpack](https://github.com/jlokimlin/modern_fftpack) | J1a2 | Complex 1D wrapper, setup/dispatch and inspected forward-normalization path | Forward scaled, inverse unscaled. Workspace/setup rebuilt per call. Positive N required; errors may terminate. Parent/submodule workspace INTENT differences need build checking. |
| [FFTW3 wrapper](https://github.com/kuanchihwang/fftw3_wrapper) | J1a2 | FFTW aligned-buffer planning/execution/cleanup for complex REAL64 1D | Forward unscaled, inverse divided by N. Optional length truncates/pads. New plan per call, allocatable distinct output required, failures STOP. External FFTW kernels not audited. |
| [gamma_f77](https://github.com/ckormanyos/gamma_f77) | C7a | Reciprocal-Gamma Horner expansion, recurrence, reflection and integer factorial branch | Poles return finite sentinel; large-argument INTEGER conversion/overflow unguarded. Last coefficient lacks kind suffix. File also contains a main program; separate module before reuse. No precision certification. |
| [elliptic_k_using_agm_fortran](https://github.com/dscf-1224/elliptic_k_using_agm_fortran) | C14 | Direct/complementary AGM and elliptic-nome dispatch for complete first-kind K(k) | k is modulus, not parameter. Large negative k passes signed input to AGM; sketch uses positive k. Unpinned dependencies, unconditional REAL128 declarations and external algorithms need checking. |
| [spherical_bessel_fortran](https://github.com/jlm785/spherical_bessel_fortran) | C10a3 | Real spherical j_n power series and upward recurrence | Half-integer cylindrical-order subset only. STOP on some errors/accuracy guards; no returned estimate. Guard is asymmetric in x. Complex/quad variants unreviewed. |
| [MINPACK](https://github.com/certik/minpack) | F2; K1b1a2 | Hybrid root-solver setup/finite-difference/QR/dogleg dispatch; Jacobian-supplied Levenberg-Marquardt driver | Distinct callback contracts and workspace formulas. Small-step/cost tests do not certify residual accuracy. LMDER1 module callback intents conflict with classic preservation/abort semantics; external entry illustrated. |
| [stroud_quad](https://github.com/ivan-pi/stroud_quad) | H2c | Gauss-Hermite root recurrence/Newton refinement and mirrored weights | Ten-iteration cap without convergence flag, altered initial estimate, pre-update derivative values and default-INTEGER normalization overflow risk. Prints diagnostics; rules not numerically checked. |
| [modern_quadpack](https://github.com/nshaffer/modern_quadpack) | H2a1a1 | Legacy DQAG/DQAGE adaptive Gauss-Kronrod dispatch and largest-error bisection | Workspace/status/error-handler policy required. Error estimates are not rigorous bounds. High-level API and all kernels remain unreviewed. |
| [fftlog-f90](https://github.com/coccoinomane/fftlog-f90) | J1a3 | FHTI setup and FFTL bias/reweight/transform/postscale path | Log-grid sine/cosine subset; RK ratio differs from KR product. Validate inputs despite OK flag. CLI only admits sine and adds different normalization. FFT/Gamma kernels unreviewed. |
| [ellipFor](https://github.com/seantrim/ellipfor) | C14 | Complete first-/second-kind integral wrapper and reciprocal-parameter transforms | Input is parameter m, outputs complex; negative m unsupported. REAL128 internally required. Complete associated kernels and continuation accuracy not audited. |
| [Polylogarithm](https://github.com/Expander/polylogarithm) | C19 | Real dilogarithm argument transformations and rational approximation | DLI2 returns real part above the real cut. Link log support for the complete source object. Complex/higher orders and claimed approximation error unverified. |
| [FTLib](https://github.com/fradevita/FTLib) | H2a1b2; H2a1a2 | Sampled composite trapezoid and fixed-order callback Gauss-Legendre rule | Gaussian orders 1..5 only; no default/error estimate. Parent/submodule definitions need build checking; callback trapezoid body absent in reviewed submodule. No runnable support claimed. |
| [spline_interpolation_fortran](https://github.com/jlm785/spline_interpolation_fortran) | E1a | Cubic-spline tridiagonal fit and value/derivative evaluation | Normal status is one. N>=4 for normal fit; reuse requires unchanged grid/workspace/boundary coefficients. End-cubic extrapolation flagged; repeated nodes can STOP. Integration not reviewed. |
| [L-BFGS-B](https://github.com/jonathanschilling/L-BFGS-B) | G2h1a2 | Workspace partition, bound projection, Cauchy/subspace and line-search dispatch | Reverse communication requires objective and gradient on FG requests; preserve workspace/state and inspect final TASK. No general nonlinear constraints or global guarantee. |
| [Subplex](https://github.com/kingaa/subplex) | G1b2 | Coordinate partitioning and derivative-free subspace simplex dispatch | This fork removed MODE and resets defaults. COMMON/SAVE state requires isolation; supporting routines and BLAS are needed. |
| [UCMINF](https://github.com/hdakpo/ucminf) | G1b1b | Supplied-gradient branch, soft line search and inverse-BFGS update | R frontend/C bridge owns runtime state. RHO is not an ordinary Fortran work buffer; the fork has no FDF callback argument. |
| [HWODE](https://github.com/cpmech/hwode) | I1a1a | DOPRI5 option checks, nonstiff embedded Runge-Kutta and step-control dispatch | LOGICAL DEBUG is an extra fork argument. Stiffness detection does not provide stiff integration. Dense output needs additional setup. |
| [DASKR](https://github.com/hugomvale/daskr) | I1a2 | Implicit BDF driver initialization and direct/Krylov dispatch | Fixed-form external DASKR entry, despite DDASKR prose. Consistent initial state, mode-specific callback/workspaces and status/continuation handling required. |
| [minimize](https://github.com/ryokbys/minimize) | G1b1b | Steepest-descent direction and line-search dispatch | Zero-gradient/zero-cost divisions and saved-array dimension reuse need attention. Other solver methods remain unreviewed. |
| [grid_interpolation](https://github.com/ChristianSteger/grid_interpolation) | E2a | Four-weight bilinear evaluation on a uniform rectangular grid | Data layout is (NY,NX). Boundary branches fall through because CONTINUE does not skip an iteration; outside and upper-endpoint queries are unsafe. |
| [finite_difference](https://github.com/jlr581/finite_difference) | H1 | Gaussian RBF differentiation-weight construction, LDL dispatch and adaptive precision | Root variable-precision API only. Check STAT; reject duplicate nodes/unknown tags; validate stencil accuracy. No full arithmetic/linear-kernel audit. |
| [ABSCAB Fortran](https://github.com/jonathanschilling/abscab-fortran) | C14 | Bulirsch complete elliptic integral duplication iteration | Require nonzero complementary modulus. The zero-modulus branch tests uninitialized B. Positive P illustrated; no principal-value or domain-API certification. |
| [Mittag-Leffler function and derivative](https://github.com/tranqv/mittag-leffler-function-and-its-derivative) | C19 | Scalar two-parameter entry, Gamma/EXP special cases and inverse-Laplace dispatch | Alpha>0; invalid input may leave output undefined. Saved tolerance/RNG side effects. Derivative and generalized-parameter APIs remain outside this review. |
| [Jacobi theta functions](https://github.com/fremling/Jacobi-Theta-function-Fortran) | C13 | THETA3 modular transforms, argument reduction and exponential-series summation | Period-one Z convention; Im(tau)>0. EXIT terminates the process on failures; MAXITER does not bound the inner series. |
| [fastspline](https://github.com/jamesorr/fastspline) | K5 | Structured cubic smoothing solve, trace score and output reconstruction | Regular samples; user chooses LAM. No automatic GCV minimization or input/status validation. Truncation and small-N indexing require care. |
| [FFTPack](https://github.com/keurfonluu/FFTPack) | J1a2 | Complex-double vector wrapper planning, transform dispatch and normalization | Forward unnormalized, inverse scaled by 1/N. Positive lengths, numeric-kind/ABI compatibility required; IERR ignored and workspaces rebuilt per call. |
| [Computer Methods for Mathematical Computations](https://github.com/Beliavsky/Computer-Methods-for-Mathematical-Computations) | F1b | Bracketed Brent root search with secant/inverse-quadratic steps and bisection | Continuous scalar problem, finite values, positive controls. Check error code; endpoint sign-product can overflow/underflow. Other textbook solvers not reviewed. |
| [AFNL](https://github.com/ramos/afnl) | H2a1a1 | Repeated trapezoid refinement and Simpson extrapolation | Absolute successive-estimate test, default 1e-2, fixed 26 refinements. Endpoint evaluations; nonconvergence STOPs the process. Not a rigorous error bound. |
| [fast_math](https://github.com/jalvesz/fast_math) | C8 | Fixed-coefficient elemental erf approximation | DP uses the same approximate coefficients as SP. No machine-precision/error-bound claim; extreme inputs can overflow. Other fast functions not reviewed. |
| [PyIntegral](https://github.com/neutrinomuon/pyintegral) | H2a1b2 | Gauss-Legendre rule generation, tabulated linear interpolation and weighted sums | Explicit positive N_INT required despite OPTIONAL declaration; no tolerance/error estimate. Interpolation indexing/status and finite Newton iteration limits need attention. |
| [Alexander Mead library](https://github.com/alexander-mead/library) | H1 | Centered differences with repeatedly halved width | Default REAL. Relative successive-derivative test divides by the old estimate; no status, fixed iteration budget and STOP on failure. |
| [modforutils](https://github.com/rweed/modforutils) | C1 | Binomial lookup table and Pascal-row recurrence | REAL64 output is not arbitrary-size exact-integer arithmetic. Require nonnegative N; large coefficients can round or overflow. Other utilities not reviewed. |
| [numfor](https://github.com/numericfor/numfor) | E1a | Endpoint-curvature cubic fit and scalar local-polynomial evaluation | N>=4, strictly ascending grid. Allocation condition relies on short-circuiting; outside/upper-end lookup can exceed coefficient columns. Other spline operations not reviewed. |
| [PyFluxconserving](https://github.com/neutrinomuon/PyFluxconserving) | E1a | Cached-interval search and affine interpolation | Saved state and search indexing are unsafe, including in-range cases. Header zero-outside behavior is not implemented. No flux-conservation claim. |
| [CWT](https://github.com/khaors/cwt) | J | Direct Morlet/Mexican-hat kernel sums and scalogram file output | Standalone program, not module API. Quadrature omits sample spacing; translations use indices, Morlet uses default COMPLEX, output loses phase. |
| [Pade_approximants](https://github.com/JohanSchott/Pade_approximants) | K4 | Even-coefficient rational fit, least-squares dispatch and evaluation | Inspected solver=0, precision=64, mtr=0 only. KIND=16/build dependencies still required; diagnostics unit 90, no returned convergence status. Thiele is unimplemented. |
| [libcoul90](https://github.com/banana-bred/libcoul90) | C12 | Real Coulomb continued fractions, order recurrences and normalization | X>1e-7, base-order-dependent zero-based output extent, IFAIL checks. Shared diagnostic modules; no Bessel/wrapper or JWKB accuracy audit. |
| [Fortran_Davidson](https://github.com/NLeSC-JCER/Fortran_Davidson) | D4a1 | Real-symmetric projection, Ritz residuals, DPR correction and basis expansion/restart | Ordinary dense path only. Sticky convergence flags require independent final residual checks; near-zero correction denominators and basis dimensions need safeguards. |
| [qrupdate-ng](https://github.com/mpimd-csc/qrupdate-ng) | D7 | Rank-one real QR update through rotations and retriangularization | Existing full/economy factors required; destructive U/V and workspace rules. No returned status; invalid dimensions invoke error handler. Other update variants not reviewed. |
| [PROPACK](https://github.com/poulson/PROPACK) | D6 | Nonrestarted Lanczos bidiagonalization, projected SVD and Ritz-vector dispatch | Both A and A-transpose callbacks; substantial mode-specific workspace. K is overwritten; check INFO and residuals. COMMON statistics and dependencies remain relevant. |
| [minila](https://github.com/ghbrown/minila) | D2a1 | Partial-pivot LU, RHS permutation and triangular substitutions | Default REAL; exact-zero singular checks. Error returns can leave the allocatable solution undefined/unallocated. Inverse and SOR not reviewed. |
| [Bolander linear algebra library](https://github.com/bolanderc/bolander-linear-algebra-library) | D2b1b | Lower Cholesky factorization with trailing rank-one updates | ERROR output is never assigned; no positive-pivot/size/symmetry checks. Upper triangle remains original input. Factorization only, not a solve. |
| [fortsparse](https://github.com/lazy-fortran/fortsparse) | D1b4 | Canonical real CSR validator and sparse matrix-vector sum | One-based storage, sorted distinct columns, externally checked X/Y shapes. Solver/AMG/backend claims remain documentation reviewed. |
| [Fortran_CSR](https://github.com/cometscome/Fortran_CSR) | D1b4 | Public complex type-bound product and native CSR row loop | Preprocessing selects MKL or fallback; native fallback reviewed. Y capacity unchecked; dimension failure STOPs. NONZERO returns terminal pointer, not NNZ. |
| [Linear System Solvers](https://github.com/M-Badri/linear_system_solvers) | D2a4 | CSR/LIS object setup and solve/result-copy dispatch | Adapter review, not a numerical-kernel audit. LIS index/ABI conventions and lifecycle required; IERR mostly ignored, RHS length not asserted. |
| [DualSimplex](https://github.com/thchang/DualSimplex) | G2a | Asymmetric dual revised simplex, LU basis solves and Dantzig/Bland pivoting | Supply initial basis despite OPTIONAL declaration; M>=N. EPS code defaults to epsilon rather than square-root prose. Check IERR and independent primal/dual conditions. |
| [LightConvex](https://github.com/loiseaujc/LightConvex) | G2a | Dense LP tableau assembly, feasibility dispatch and primal-simplex iteration | Maximization/nonnegative variables; RHS restrictions. Check status on problem, not solution. Y/T dual fields not populated; MAXITER is not a total phase-one budget. |
| [vc-sqnm](https://github.com/moritzgubler/vc-sqnm) | G1b1b | History-subspace stabilized quasi-Newton displacement | Caller supplies values/gradients and updates coordinates. Own stopping/budgets required; LAPACK failure STOPs. No variable-cell-wrapper or rigorous-bound claim. |
| [Differential-Evolution_f95](https://github.com/ian-mmm/differential-evolution_f95) | G2i | Stochastic differential mutation/crossover and selection | Fixed built-in objective. Bounds only initialize population; donor/crossover bugs and possibly undefined best-point output require repair. No global guarantee. |
| [pso](https://github.com/konrad1991/pso) | G2i | Callback swarm initialization, velocity update, bound clamp and best-state dispatch | Star topology only reviewed. Social index and current-versus-personal-best output findings; reevaluate returned vector. No status or returned objective. |
| [TRDF](https://github.com/fsobral/TRDF) | G2h3b | Feasibility/model/subproblem dispatch and trust-region outer iteration | Linked evaluators and constrained solver; fixed limits/COMMON state. Inconsistent CALFUN arity and early-output risks require checked repair. No termination flag. |
| [DFO mirror](https://github.com/jacobwilliams/dfo) | G2h3b | Input/scaling/interpolation setup and constrained trust-region solver dispatch | Legacy flat arrays, CHARACTER*256 and linked FUN; saved COMMON and default 50-dimensional model limits. Backend configuration/rights and INFO checks required. |
| [LMBM](https://github.com/WilmerHenao/lmbm) | G1b2 | Workspace initialization, bundle/update dispatch and termination tests | Linked objective/subgradient; no callback argument. Default-REAL time buffers mixed with double work. Distinguish stationarity from progress/budget exits in IOUT(3). |

| [polyfit](https://github.com/plopezrios/polyfit) | K1a1a2 | Independent polynomial fits via weighted normal equations and LAPACK symmetric inversion | Standalone program; internal helpers are not library APIs. Rank/scaling issues and skipped undersized data sets; other fitting branches unreviewed. |
| [samplestat](https://github.com/haniibrahim/samplestat) | L1a1a; L1a1b | Direct arithmetic mean, N-1 sample variance and square-root standard deviation | Separate N must fit the vector. Raw-moment cancellation and absent validation/status; confidence routines unreviewed. |
| [StatTools](https://github.com/AstroFloyd/StatTools) | L1a1 | Command-argument data summaries and dispatch to libSUFR median/stdev | Program, not a library. External statistical kernels unreviewed; zero-denominator and geometric-mean domain issues. |
| [Fortran-Metrics](https://github.com/tkdhss111/Fortran-Metrics) | L1 | Missing-pair filtering and prediction-error summaries | Default REAL and -999 sentinel. Vector MAPE uses signed observations; zero denominators unguarded. |
| [normal-deviates](https://github.com/patti-favaron/normal-deviates) | L6b14 | Ziggurat proposals, covariance Cholesky and row-wise affine transform | Global intrinsic RNG; nonuniform strip-index selection, unguarded log endpoints and absolute covariance thresholds. No distribution validation. |
| [mtprng](https://github.com/pdebuyl/mtprng) | L6a21 | Explicit single-seed MT19937 and 32-bit-to-real scaling | Explicit initialization essential: default-state lazy seeding is unreachable. INT64 storage does not mean 64 random bits. |
| [sobseq](https://github.com/daanvanvugt/sobseq) | L6a21 | Scalar Sobol coordinate, direction recurrence and Gray-code next/skip-ahead | Deterministic low-discrepancy sequence, not independent random draws. User direction parameters, default REAL rounding and unchecked exhaustion. |
| [pcg-fortran](https://github.com/dscf-1224/pcg-fortran) | L6a21 | Fixed initialization and oneseq 64-state/32-output XSH-RR update | Raw signed bit words; modular overflow/narrowing depends on compiler behavior. Other variants and author C comparisons unverified. |

The spherical-Bessel mapping uses the half-integer cylindrical-Bessel relation
in [NIST DLMF 10.47.3](https://dlmf.nist.gov/10.47.E3). Its integer spherical
index does not make it an arbitrary integer-order cylindrical `J_n` evaluator.
The card limits C10a3 coverage to that spherical subset.

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

* **lagrange_interpolator extrapolation/status:** the
  [constant-extrapolation branch](https://github.com/jlokimlin/lagrange_interpolator/blob/7b0f9014f49236dd6aff0afacc75cf5aeb441f9d/src/type_LagrangeInterpolator.f90#L172-L187)
  assigns an endpoint abscissa (`x`) instead of its ordinate (`y`). Early
  returns precede assignment of the optional success output, while normal
  cleanup resets the object's success property. Unsorted-input creation can
  return without allocated data, and the interpolation method does not check
  that failure before referencing its arrays. These are inspection findings.
* **lagrange_interpolator 2D temporary vector:** the
  [row loop](https://github.com/jlokimlin/lagrange_interpolator/blob/7b0f9014f49236dd6aff0afacc75cf5aeb441f9d/src/type_LagrangeInterpolator.f90#L251-L268)
  performs the final along-x interpolation after filling each individual
  temporary entry, so early iterations read entries not yet initialized. The
  last iteration has a complete vector, but intermediate behavior with traps
  or uninitialized-value checking remains untested. The
  [author checks](https://github.com/jlokimlin/lagrange_interpolator/blob/7b0f9014f49236dd6aff0afacc75cf5aeb441f9d/test/test.f90#L46-L65)
  query the supplied nodes; they do not establish off-node interpolation accuracy.

Next numerical reviews move to other independently reviewed linear-algebra,
quadrature and differential-equation libraries. Benchmark collections remain
separate from implemented solvers. The ball-covering derivative callbacks and
DNAD examples remain candidates for later compiled checks, not checked drivers.

## Further interface reviews: interpolation, differentiation and ODEs

Akima's sensitivity arrays are directional during construction and transposed
into coefficient-by-data arrays for evaluation; the author Python wrapper is
linked as a setup reference. These derivatives describe the interpolant.
Adjac's public generic names are retained rather than advertising their private
real overloads. Its real dense calling sketch explicitly resets tape mode.
The generic_rk mapping records the active explicit path and its stage-state
finding; its method name alone does not establish numerical order or stiff
capability. No upstream source was compiled or run for these reviews.

## Scattered interpolation and derivative primitives

E2b (scattered multivariate data) is recorded from the NIST classification
report, printed page 17 / PDF page 19. It has no more specific children in that
scheme. The reviewed Shepard bindings use `qshep_2d`, correcting the type name
shown in some author documentation, and link status checks and author examples.
The wrapper MIT notice does not replace the separate ACM notice for its core.

The chol-rev entries describe differentiation through an existing lower factor,
not ordinary Cholesky factorization or another review of the LAPACK repository.
The findiff tensor entry requires a Jacobian callback; it is not advertised as
a scalar-Hessian-from-values routine. No upstream program was compiled or run.

## Spline calculus and quadrature-rule services

H2c is the NIST service-routine class for quadrature weights/nodes (printed
page 20 / PDF page 22). ORTHPOL and triasymq return rules; their calling
sketches explicitly form weighted sums and identify analytic reference values,
without claiming executed comparisons or automatic error control.
FITPACK's reviewed derivative and integral routines act on an existing spline,
so E3a2 and E3a3 describe them more precisely than general differentiation or
integration classes. Its fitting/smoothing paths remain documentation reviewed.
None of the upstream routines or sketches in this batch was compiled or run.

## Nonlinear systems and simplified ODE integration

NITSOL and JFNK-Hookstep remain in F2, which is already a leaf in this taxonomy.
Their internal linear solves and residual minimization do not establish separate
general least-squares/optimization APIs. The NITSOL review covers its GMRES path;
other Krylov methods remain outside the implementation review. The hookstep
core requires an operator callback, with finite differences supplied in the
author template rather than automatically constructed by the core.
The easydop853 entry records its fixed tolerances and callback object argument,
and distinguishes stiffness detection from stiff-system capability.
These are source reviews and uncompiled calling fragments, not checked drivers.

## Cell means, interval means and RBF services

PPR's reviewed inputs are cell means and edge coordinates, while newspline's
inputs describe interval means and subdivision counts. Their sketches do not
treat those values as ordinary point samples. The PPR mapping is restricted to
the inspected PCM path and newspline to the unbounded path.
The fortran-rbf entry is scoped to E3 interpolation services: it exposes stencil
matrices, not a complete data-fitting or arbitrary-query value API. Its source
findings preclude presenting all advertised derivative/polynomial paths as
checked algorithms. No upstream code or calling sketch was compiled or run.

## Matrix exponentials and polynomial/spline representations

The Expokit review covers the dense real full-matrix exponential routine only.
D8 follows the matrix-function convention in the published
[NAG GAMS D8 index](https://www.afs.enea.it/software/libnag/nagdoc_fl24/pdf/INDEXES/GAMS/d8.html),
which lists matrix exponentials alongside other matrix equations. This does not
classify Expokit as a general Sylvester solver or verify its sparse actions.

The polynomial_interpolation mappings distinguish a single degree-n polynomial
(E1b) from changing local stencils (E1a). NdSpline instead builds a tensor-product
B-spline on a Cartesian-product grid (E2a). Flattening, query shifting, basis
order and result layouts are recorded with calling fragments. No upstream
program or numerical reference comparison was compiled or run in this batch.

## Polynomial fitting, summaries and sampling interfaces

The polynomial-fit and multivariate-normal branches use the detailed
K1a1a2 and L6b14 paths in the [Netlib GAMS taxonomy](https://netlib.org/bib/gams.html).
These additions preserve the imported taxonomy and record their source in
`data/gams-extensions.json`. The polyfit mapping is restricted to the ordinary
polynomial independent-coefficient path; it does not turn its internal normal
equations into a public least-squares API.

The sampling cards distinguish pseudorandom bit words, scaled uniform values,
a deterministic Sobol coordinate and intended multivariate normal samples.
Source findings qualify these classifications: mtprng needs explicit seeding;
normal-deviates has strip-index and logarithm-endpoint concerns; pcg-fortran
relies on compiler arithmetic behavior. The cards record the implementation
intent and calling contract, without certifying distribution quality.
StatTools delegates its median and standard-deviation kernels to libSUFR;
that dependency was not audited in this batch. No upstream code or calling
sketch in this batch was compiled or run.
