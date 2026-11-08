# Detailed GAMS review progress

This review examines individual implementations after broad discovery. A leaf
class is the most specific classification in that GAMS branch; a long code is
not inherently more precise than a short leaf such as G2i. Classification does
not establish correctness or successful compilation.

Reviewed on 2026-11-07. 648 repositories now have 965 source-reviewed
mappings. Full commit pins, file hashes, procedure names
and inspected line ranges are in [the generated review ledger](local-reviews.md)
and `data/local.json`.
The original broad documentation reviews remain available.

## Reviewed calling interfaces

644 repository cards now identify public routines and link their usage lines
to pinned argument declarations. Fourteen further cards (DDFSA, CWT, polyfit, StatTools, GridSearch,
PSOclassicG, ACFbyFFT, TREAT, main_Gaussian, LHSDRV, TiktakGlobalSearch, Sparse Fortran examples, TISEAN and ElliFEM) identify supplied program entry points and keep their internal/benchmark
routines among implementation helpers.
Detail pages distinguish these roles. Module names and procedure names are stored
separately. All 648 independently source-reviewed repositories now have an
entry-point annotation and a scoped license finding. Source inspection alone establishes neither numerical correctness nor a
complete public-API audit. Individual local driver checks are identified separately.

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
| FFTPack | `fftpack::fft`, `fftpack::ifft` (complex-double bindings), `fftpack::conv`, `fftpack::hilbert`, `fftpack::fft` (real-double binding), `fftpack::xcorr` | Bundled GPL notice without version; wrapper terms unresolved |
| Computer Methods for Mathematical Computations | `ForsytheMalcolmMoler::BrentZero`, `::FMMspline`, `::NaturalSpline`, `::Seval`, `::Seval3`, `::Quanc8`, `::SVD`, `::RKF45`, `::BrentMin`, `::Fmin` | MIT root; inherited source provenance recorded separately |
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
| minila | `linsys::linsol` (vector binding), `prim::diag_sub`, `::fwd_sub`, `::bck_sub` | GPL v3 text; version choice unresolved |
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
| Fortran-parallel-sort | `mod_sort::parallel_sort` (REAL(8) passive ranking) | Root CC0; ORDERPACK component scope unresolved |
| Fortran-Timsort | `tim_sort_mod::sort` (INTEGER(INT32), no history) | MIT |
| fsort | `fsort_mod::fsort` (repair required) | No license identified in reviewed material |
| HeapSort | `heap_sort_module::heap_sort` | BSD-3-Clause |
| Fortran-Iterative-Quicksort | `sorting_module::quicksort` (integer and real overloads) | Informal README permission |
| Fortran-quicksort | `qsort_mod::indexx`, `::quick_sort_in_place` (real overloads) | MIT root; adapted-source scope unresolved |
| numerical-analysis | `numa__integrate::simpson_integrator_vals` | BSD-3-Clause with component notices |
| INTEGRAL | `integral_core::adaptive_integrator%integrate` | GPL v3 text; component/version scope unresolved |
| Audito | `FG_m::operator(*)`, `::operator(+)` (same-basis FG_t branch) | GPL v3 text; version scope unresolved |
| DNAOAD | `diff_mod::gradient` (selected GNU REAL64 sources) | MIT with citation request |
| auto-diff | `ad_types::tree_t%backward`, `%get_grad` | MIT |
| mp-interp | `mp_interp_killworth_subs::ainv_int` | GPL v3 text; version scope unresolved |
| libcoulcc | `libcoulcc::COULCC` (explicit status interface) | MIT packaging; numerical-core scope unresolved |
| FortVSH | `VSH::LEGENDRE`, `::SHGLQ` | BSD-3-Clause |
| Butterworth-Filter | External `buttlp`, `buttfilt` (normalized forward filter) | GPL-3.0-or-later |
| RKSUITE | `rksuite_90::setup`, `::range_integrate`, `::collect_garbage` | Custom free scientific-use/citation notice |
| libsparse | `modsparse_helpers::csrmv` (native raw-CSR helper) | MIT root; optional backends separate |
| SPOOF | `Spoof::CSRMatrix%multiply` | MIT wrapper; bundled SPARSKIT LGPL notice |
| sparseSET | `sparseset::array_to_sparse_line`, `::sparse_line_to_array` | BSD-2-Clause |
| tensor-algebra | `comMath::in1` (vector dot), `::dyad` (outer products) | MIT |
| VecFor | `vecfor_R8P::vector_R8P%dotproduct`, `%crossproduct` | GPL/BSD/MIT options under README use categories |
| fortran_lsp | External legacy `NNLS` | No license grant identified in reviewed material |
| vanhuffel | External `DTLS` | No license grant identified in reviewed material |
| lanczos_iterator | External `rs_lanczos` (real symmetric, matrix-free) | MIT; backends separate |
| Fortran_RNG | `xoshiro256::xoshiro256star2%random_number`, `%set_state` | MIT |
| xoshiro-fortran | `pkg_xoshiro::typ_xoshiro256star2%random_number`, `%set_state` | No license grant identified |
| fortran-splitmix64 | `pkg_splitmix64::splitmix64_next` (seed unchanged) | No license grant identified |
| fortran-xorshift-64-star | `random::RandomNumberGenerator%random_uniform`, `%random_normal` | GPL v3 text; version choice unresolved |
| ogata | External `fbt` (Fortran orders 0/1) | MIT documentation notice |
| fftlog | External `fhti`, `fht`, `fftl` (logarithmic grids) | CC0 additions; numerical-component notices separate |
| FortranCWT | `A19CWT::rA19CWT_zerobc` | GPL v3 text; version choice unresolved |
| wavepack | `wavepack::wavelet` (Morlet path) | MIT root; older restrictive source notices retained |
| fOptimize | `mOptimize::biss_1d`, `::newton_1d` (printed solutions) | GPL v3 text; version choice unresolved |
| Minimization | `SteepestDescent::Steep`, `GradientCalculator::CalculateGradient` | No license grant identified |
| fortran-grid-search | `GridSearch` program; edit its linked model calls | GPL-3.0-or-later |
| Particle-Swarm-Optimization-Fortran-95 | `PSOclassicG` program; included `fitness` is internal | MIT |
| MMA-in-Fortran | `MMA_Routines::MMA_Sub` (DP, one outer step) | Academic-use statement; grant unresolved |
| l-bfgs-b_wrapper_f90 | `LBFGSB_module::lbfgsb` (objective/gradient/observer callbacks) | BSD core notice; wrapper grant unresolved |
| osqp-fortran | `OSQP::OSQP_settings`, `::OSQP_solve`, `::OSQP_cleanup` | No wrapper license grant identified |
| quadprog | `quad_prog::quadprog` (Fortran generic) | GPL v3 root; GPL-2.0-or-later core notices |
| SHEPPACK | `QSHEP2D_MOD::QSHEP2`, `::QS2VAL`, `::QS2GRD` | ACM Software License Agreement |
| numfort (richardfoltyn) | `numfort_optimize_brent_real64::root_brentq` | LGPL v3 root; bundled notices separate |
| tensor_tools | `libtt_products::doubleContract` (3x3 scalar), `::dyad` | LGPL v2.1 text; version choice unresolved |
| Non-Neg_Matrix_Factorization | `mu_method::factoring` (printing experiment) | No license grant identified |
| lin_alg | External `CHOLESKY`, `GS` (educational routines) | All rights reserved; no reuse grant identified |
| pcgcoarray | `modcoarraysolver::cg%solve` | MIT; dependencies separate |
| libid | External `iddr_qrpiv`, `iddr_id` | BSD-3-Clause |
| maria-fortran | `maria_lr_tsvd_mod::dgersvd1` | MIT; backends separate |
| FortRAND | `fr_random::random`, `fr_sampling::normal_dist` | LGPL version 3 text; version choice unresolved |
| knuth-flrng | `RNFSTR`, `RNFARR` (F77 double-precision generator) | Public-domain dedication statement |
| melg-64-fortran | `type_melg19937_64%initialize`, `%genrand64_real2` | MIT |
| dsfmt_f03_interface | `dSFMT_init`, `get_rand_close_open`, `dSFMT_end` | BSD-3-Clause wrapper and C core |
| nsmarkov-fortran | `mod_lcrouwenhorst::lcrouwenhorst`, `mod_lctauchen::lctauchen` | MIT-style text with citation request |
| ACFbyFFT | `main` (file-based program); real FFT correlation paths | No license grant identified in reviewed material |
| signal_subspace | `subspace::esprit_c`, `covariance::autocov_c` | MIT |
| TOMS-Algorithm-675 | `SRCF`, `SRIF` (external square-root filtering routines) | ACM Software License Agreement per README |
| Torrence/Compo wavelets | External `WAVELET`; daughter-spectrum helper | Root MIT; retained Fortran non-sale notice unresolved |
| FSTPACK | `fstpack::cfst1f`, `::cfst1b`; `fftpack::cfft1_` | Root MIT; FFTPACK dependency terms separate |
| RFNG | `rng_m::rng_t%seed`, `%uint32` | BSD-3-Clause |
| besseleval | `besseleval::bessel_eval_init`, `::bessel_eval` | GPL-3.0-or-later |
| HOMPACK90 | `HOMPACK90::FIXPNF`; external `F`/`FJAC` callbacks | ACM Software License Agreement |
| EISCOR | External `d_symtrid_qr` | MIT |
| Fazang | `fz_var::grad`, `::reset_adj`; `fz_env::reboot_chain` via `fazang` | BSD-3-Clause |
| BLZPACK | External `DBLZDRV` in standard/generalized symmetric modes | BSD-style notice with additional enhancement grant |
| NITSOL2 | External `nitsol`, `nitdflts`; fork-specific residual/Jv callback contracts | No license grant identified in reviewed material |
| LRAP | `nonnegative_matrix_mod::nn_lrma_svd` | MIT; MARIA dependency separate |
| FortranMatrix | `matrix_mod_array::inverse` (real and complex rank-two overloads) | GPL-3.0-only; external libraries separate |
| Tensor Toolbox (ttb) | `Tensor::inv`, `Tensor::operator(.ddot.)` for selected second-order types | MIT |
| MEPACK | External `DLA_GELYAP`, `DLA_GESYLV` | GPL-3.0-or-later |
| curvefit | `linear_interp%interpolate`; scalar `linear_least_squares` | GNU GPL v3 text; version choice unresolved |
| gcvspline | External `GCVSPL`, `SPLDER` | Woltring restricted-use kernel; GPL v3 wrapper text |
| vector_fit | External `calculate_residues`, `calculate_fit_function` | Selected code GPL-3.0-or-later; EISPACK separately labeled LGPL |
| FilterSD | External `filterSD`, `checkd`; problem callbacks, COMMON blocks and matching dense/sparse backends required | EPL-1.0 |
| DEPP | `mod_class_optimizer::class_optimizer%init/%run`; `mod_class_DE_RAND_1::class_DE_RAND_1%get_trial` | GPL-3.0-or-later |
| Diver | `de::diver` with `MinusLogLikeFunc` objective callback | Custom academic-use license with citation requirement |
| libga | `Evolution::Init_Generation`, `Evolution::Next_Generation`; linked `Feval` | GPL-2.0-or-later; external utility library separate |
| OpenFSAM | `OpenFSAM::sa_cont_type%optimize` and energy callback | MIT |
| LCMIN | `lcmin::lcmin_load`, `lcmin::lcmin_optimize`; objective, gradient and Hessian callbacks | No license grant identified in reviewed material |
| Fast critical-line algorithm | External `calcturningpoints` | No license grant identified in reviewed material |
| VTdirect95 | `VTdirect_MOD::VTdirect` and objective callback | ACM Software License Agreement |
| gf_int_node | `mod_int_node::sub_int_node` scalar/vector overloads | MIT-style notice with citation request |
| ToolboxFortran | `mod_numerical::linint`, `mod_numerical::locate` | Root MIT notice; attributed-source scope unresolved |
| fortnum | `fortnum_quadrature::gauss_legendre`, `gauss_legendre_ab`, `gauss_lobatto_legendre` | MIT |
| NumericalHUB | `Lagrange_interpolation::Lagrange_polynomials` | No license grant identified in reviewed material |
| Fortran Numerical Methods | `numerical_integration::trapezoidal_method`, `romberg_method` | MIT |
| FOODIE | `foodie_integrator_runge_kutta_ssp::integrator_runge_kutta_ssp%initialize/%integrate` | Multi-license README; MIT option supplied |
| WenOOF | `wenoof::wenoof_create`; `wenoof_interpolator_js::interpolator_js%interpolate` | Multi-license options described in README |
| RALFit | `ral_nlls_double::nlls_solve` | BSD-3-Clause |
| NumLib | `rungekutta_explicit::rk4_explicit_step` scalar/vector overloads, implemented in a submodule | GNU GPL v3 text; version scope unresolved |
| Brito numerical methods | External `CG`; `bisec_code` standalone cubic-root demonstration | No license grant identified in reviewed material |
| Planelles numerical methods | `module_no_linear_equations::newton_raphson`, `fixPoint` | GNU GPL v2 text; version scope unresolved |
| Fortran Toolkit | `toolkit::brent` | MIT root notice; additional source instructions |
| SPRAL | `spral_lsmr::lsmr_solve`, `lsmr_free` | BSD-3-Clause root; BSD-2-Clause LSMR header |
| scivision L-BFGS-B | `solver_lbfgsb::setulb` | Apache-2.0 root; upstream component provenance separate |
| Bessel-Hankel | `Hankel_Transform::HankelJ0Transform`, `HankelJ1Transform` and Fast variants | MIT link in README; component scope not audited |
| rpact.as251 | External `MVNPRD`, `ALNORM` | LGPL-3 package declaration; legacy algorithm scope unresolved |
| EDAT | `pairwise_mean::mean`, `pairwise_variance::variance`; rank-one real64 specializations | BSD-3-Clause |
| lib_probability_distributions | `mod_discrete_dist::poisson_pmf`, `poisson_log_pmf`; `mod_continuous_dist::normal_pdf`, `normal_log_pdf` | MIT |
| statislib | `statislib_exponential::exponential_distribution_pdf`, `exponential_distribution_cdf` | BSD-3-Clause |
| FSML | `fsml_sts::f_sts_mean`, `f_sts_pcc` | MIT |
| Fortran-Code-Snippits | External `FINDI` | GPL v3 for author work; inherited-source terms unresolved |
| fortran-weno | `weno_square_mod::weno_square_type%init/%calc_ideal_coefs/%reconstruct` | No license grant identified in reviewed material |
| polynomial_arnoldi | `polynomial_arnoldi::gmres`, restricted to external `Poisson2D` | No license grant identified in reviewed material |
| tri_indices | `mod_tri_indices::pack_tri_indices`, `unpack_tri_indices`; selected INT64 overloads | MIT |
| NSWC | `DREXP`, `DLNREL` | Availability notice; explicit reuse grant unresolved |
| SLATEC | `special_functions::ALNREL`, `SPENC` | Government disclaimer; reuse grant unresolved |
| special_functions (ameli) | AMOS `ZBESJ`, `ZBESK` (split-real complex interface) | BSD-3-Clause root; bundled AMOS scope separate |
| GGQ | `chebyshev_quad::chebquad` | No explicit project reuse grant identified |
| StochOptim | `Evolutionary` constructor and `%optimize` (serial DE/rand1) | MIT |
| dfsaneacc | `bmqrf::bmqr`, `extractQ`, `extractR`, `bmqrsolve` | GPL-3 package metadata |
| MINUIT | `MNINIT`, `MNPARM`, `MNEXCM`, `MNSTAT`, `MNPOUT` | GPL version 2 text; version scope unresolved |
| Statlib | AS241 `PPND7`, `PPND16` | Royal Statistical Society no-fee distribution permission |
| Numerical_utilities | `kahan_summation_m::kahan_summation`, `%add/%val`, `kahan_babushka_sum`; `online_variance_m::online_variance%add/%mean/%var/%sample_var` | GPL version 3 text; version scope unresolved |
| Fortran-variable-transformation | `variable_transformation_mo::yeo_johnson_lambda`, `box_cox_lambda`, lambda selectors and `rnorm` | MIT |
| RKAdaptiveMethods | `rk54DormandMod::rk54DormandEachStep` (autonomous systems only in this review) | No license grant identified in reviewed material |
| SESAM | `utilclc::mkcov`, `mkcovweight` (Gram products, not automatic statistical covariance) | CeCILL-2.0 |
| appell | External `HYP_2F1`, `HYP_2F1_SUBROUTINE`; module supplies precision/helpers | GPL-3.0-or-later package metadata |
| fortran-gmm-em | `gmmEM::fit`, `initRandomGaussians`; `linalg::gramSchmidt` | GPL-3.0-or-later |
| spharm-interp | External `ylgndr`, `sheval3d` (basis/expansion evaluation, not MATLAB fit) | Apache-2.0 |
| EqualSpherePartition | `ACM_EqualSphere::eq_sphere`; appended demonstration main must be separated for library use | No license grant identified in reviewed material |
| LEcuyer-RNG-Fortran90 | External `RngStream_CreateStream`, `RngStream_RandU01`, reset and package-seed routines; `rng` supplies the type | GPL version 3 text; version scope unresolved |
| M_datapac | `M_datapac__d::mean`, `median`, `var` (REAL64) | CC0 root with original NIST notice |
| numFort | `numFort::fft`, sampled-array `trapZ` generic | No explicit project reuse grant identified |
| Numerical-Methods-in-Fortran | `Interpolation::lagrange`, `lagrangep`; `Polynomials::horner` | GPL version 3 text; version scope unresolved |
| library-of-numerical-analysis-msu | External `BS02R` | No license grant identified in reviewed material |
| insitu_array | `insitu::insitu_Array%init`, `%t` | No explicit reuse grant identified |
| MoA-Fortran | `mod_moa_take::moa_take`, `mod_moa_drop::moa_drop`; reexported by `moa` | BSD-3-Clause |
| pseudo_rng_modules | `lfsr258::rand`, `set_seed`, `rand_arr`; `RNGutil::GCD64_` | GPL version 3 text; inherited RNG scope unresolved |
| Fortran_rationals | `rationals::rational`, rational operators and component queries; `real`, `gcf`, `lcm` | MIT |
| HDMod | `HDMod::hdual`, `hdexp`, `hdsin` (selected scalar automatic differentiation) | MIT |
| compare | `compare::eq`, `setTol` | MIT |
| fortran-approx | `approx::aeq`, `haeq` (elemental absolute/hybrid comparisons) | No explicit reuse grant identified |
| em-fortranbox | `embox::normpdf`, `densitybox::normlogpdf` | No explicit project reuse grant identified |
| ecgmm_fortran | `ecgmm::iterate`, `get_p` | No license grant identified in reviewed material |
| twdtw | External `twdtwf90gt` legacy Fortran routine, with explicit boundary initialization | GPL-3.0-or-later |
| timeseries | External `CalcAlphaBeta`, `mean`, exposed by module `timeseries` interfaces | MIT |
| ODEPACK modernization | `M_odepack::DLSODE`, selected MF=10 Adams and MF=22 BDF paths | Declared public domain with LLNL notice |
| NUFFT (biotrump mirror) | External `nufft1d1f90`, centered complex type-1 transform | BSD two-clause with FreeBSD views notice |
| QD | `ddmodule` decimal assignment and double-double `operator(+)` | BSD-3-Clause root with additional LBNL notice |
| MPFUN2020 | Variant-1 `mpreal`, `mpinit`, `operator(+)`, `exp`, normally imported through `MPMODULE` | BSD-style terms with contribution license-back clause |
| FMPFR | `fmpfr_oper::fmpfr`, `operator(+)`, precision/rounding setters | MIT for src; dependency/build-tool terms separate |
| ga_lib | `selection::selection_tournament`; `benchmark::solve` target-value search harness | MIT |
| GARCH | `garch_mod::simulate_garch`, `obj_fun_mod::garch_sigma` | No explicit reuse grant identified |
| EnKF_analysis | External scalar-observation `analysis`; `m_ensmean::ensmean`, `m_ensvar::ensvar` | MIT |
| HiPPIS | `mod_adaptiveInterpolation::newtonPolyVal`, `mod_adaptiveInterpolation::divdiff`, `mod_adaptiveInterpolation::adaptiveInterpolation1D`, `mod_adaptiveInterpolation::adaptiveInterpolation2D` | No explicit reuse grant identified |
| acepack | `supsmu` | Permissive Friedman notice; MIT package declaration |
| SIGNAL | `signal::window_cos_`, `signal::apply_window_` | GNU GPL version 3 text |
| leaps | `REGCF`, `CLEAR`, `INCLUD`, `TOLSET` | GPL-2.0-or-later (package declaration) |
| mix | `ctrsc` | Unlimited (package declaration; no detailed grant reviewed) |
| tweedie | `GaussAdaptive`, `GaussQuadrature` | GPL-2.0-or-later (package declaration) |
| spam | `rowmeans`, `csrmsr` | Mixed package/component license declarations |
| MCMC F90 | `mcmcrand::random_normal`, `mcmcrand::random_gamma` | MIT |
| DFL | `sd_box` | GNU GPL version 3 text |
| BGW | `drglg` | GPL-3.0-only with ACM provenance statement |
| mknapsack | `mt1`, `mtp` | MIT root; historical routine provenance separate |
| gausscov | `fstepwise`, `lsqqr`, `qrdecom` | GPL-3.0-only (package declaration) |
| mclust | `me1e`, `dmvnorm` | GPL-2.0-or-later (package declaration) |
| TREAT | `treat` | GNU GPL version 3 text |
| GPKDE | `GridProjectedKDEModule::GridProjectedKDEType%ComputeDensity`, `GridProjectedKDEModule::GridProjectedKDEType%Initialize` | MIT |
| qap | `qaph4` | GPL-3.0-only (package declaration) |
| KernelyzeBase | `eigen_rankn_params_mod::eigen_rankn_params`, `brent_mod::brentZero` | AGPL-3.0-or-later; separate helper notices |
| ttcross | `dmrgg_lib::dtt_dmrgg` | MIT |
| GADfit | `gadfit::gadf_fit`, `ad::operator(*)` | Apache-2.0 |
| Random Fields Generation Library | `randomFieldND::gen_Std_Gauss` | CeCILL-C root; bundled dependency terms separate |
| libslam | `slam_interpolation::lagrange_interpolation`, `slam_interpolation::trigonometric_interpolation` | Apache-2.0 |
| Spectrum-Revealing CUR | `carrqr` | MIT/BSD notices scoped to LUSOL; QR grant not separately identified |
| TT Fortran core | `tt_lib::svd`, `tt_lib::dot` | MIT |
| KronLinInv | `kronlininv::posteriormean`, `kronlininv::calcfactors` | GPL-3.0-or-later |
| diaglib | `dgl_interface::dgl_davidson_driver`, `dgl_interface::dgl_lobpcg_driver` | MPL-2.0 |
| Exponential sum approximations | `main_Gaussian` | BSD-3-Clause |
| pypolsys | `polsyswrap::solve`, `polsyswrap::init_poly`, `polsyswrap::init_partition` | GPL version 3 root; historical POLSYS provenance separate |
| monolis | `mod_monolis_solve::monolis_solve_R` | MIT (README declaration) |
| Nonlinear Optimization Algorithms Multilang | `hooke` | Unlicense |
| PRIMA | `bobyqa_mod::bobyqa`, `lincoa_mod::lincoa`, `cobyla_mod::cobyla` | BSD-3-Clause |
| PyDQED | `dqed` | MIT wrapper notice; legacy DQED provenance separate |
| pyoptgra | `OGEXEC`, `OGINIT`, `OGDERI` | GPL-3 or ESCL 2.4 Weak Copyleft (author choice) |
| MPFUN90 | `mprealmod::operator(+)`, `mpdefmod::mpinit`, `mpgenmod::exp` | Bailey limited BSD license with contribution clause |
| Get Moments reconstruction | `integrate::integrate_trap`, `fsolve_mod::fsolve` | LGPL numerical solver; reconstruction grant not identified |
| M_random | `M_random::mtprng_rand_real2`, `M_random::scramble`, `M_random::mtprng_init` | MIT manifest; custom MT notices and unlicensed KISS component |
| SLICE sampler | `slice_mod::slice_walks` | No license identified |
| ScipyDIRECT | `Direct` | MIT |
| Contour 531 | `find_contours_reg_grid_m::find_contours_reg_grid` | GPL-3.0-only (root text) |
| PFAPACK Rust bindings | `DSKTRF`, `DSKPFA` | LAPACK-derived notice; PFAPACK grant not separately identified |
| Golden-section callback experiment | `goldenSectionSearch::gss` | No license identified |
| EnsDAM | `ensdam_meanstd::ensemble_meanstd`, `ensdam_covariance::update_meancov_vector`, `ensdam_interp::grid1D_locate`, `ensdam_interp::grid1D_interp` | CeCILL-2.0 |
| CohensdpLibrary | `hyg0f1`, `betacdf` | GPL-3 package declaration; numerical provenance separate |
| IEEE classification helpers | `ieee_class_fortran::is_ieee_quiet_nan`, `ieee_class_fortran::set_ieee_quiet_nan` | MIT |
| libsupermesh | `libsupermesh_tri_intersection::intersect_tris` | LGPL-2.1-only; bundled components separate |
| polyhomocont | `polyhomocont__solve::solve` | MIT |
| L-BFGS-B-NS | `setulb` | BSD-3-Clause declaration; referenced license file absent |
| copa | `copa__sampler::run_sampler` | GPL-3.0-only root text; manifest placeholder |
| MSOLV | `solver::solve_syst` | LGPL-3.0-only root; backend terms separate |
| EigenExa | `eigen_libs_mod::eigen_s`, `eigen_h`, `KMATH_EIGEN_GEV` | BSD-2-Clause core; LAPACK/ScaLAPACK notices separate |
| CUTEst | `CUTEST_uofg` | BSD-3-Clause |
| LHS | `LHSDRV` | LGPL-2.1 root text; Sandia provenance retained |
| EMSOL | `ems_sslv` | MIT |
| KFAS | `kfilter` | GPL-2.0-or-later |
| dae4py | `DDASKR` | BSD-style wrapper and UC/LLNL DASKR notices |
| faiNumber Fortran | `fnDecimalUtil::decToInt32`, `fnInt32Util::int32ToBinaryAsU`, `fnNumberStringUtil::isInteger` | MIT |
| Matran | `RmatSVD_m::SVD`, `RmatQR_m::QR` | Custom Stewart license; unmodified distribution restriction |
| cdaSQR / SQR | `quantilelassoNET1` | GPL-2.0-only |
| FEconv | `module_cuthill_mckee_fcnv::cuthill_mckee` | GPL-3.0 root; LGPL ordering-source notice |
| PSFUN | `psfun_d_krylov_mod::psfun_d_arnoldi` | BSD-3-Clause root notice |
| Zolo SVD | `ZOLOPD`, `ZoloEig` | No standalone license identified |
| NScluster | `simThom` | GPL-2.0-or-later package; MT19937 component notice |
| TikTak | `TiktakGlobalSearch` | MIT root; bundled numerical provenance requires review |
| SLATEC Modern | `special_functions::DDAWS`, `special_functions::DBETA`, `special_functions::DGAMI`, `special_functions::DBETAI` | Apache-2.0 root and original SLATEC disclaimer |
| BiCGSTAB and GMRES solver examples | `SOLVERS_base` | MIT |
| hyperBOB | `hyperBOB_module::hyperBOB` | MIT root; numerical dependencies separate |
| sht_py | `polynomial`, `forward` | GPL-3.0 license text |
| PDECHEB | `INICHB`, `PDECHB` | Original author rights retained; no standalone grant identified |
| urca | `ddnor`, `innorz` | GPL-2.0-or-later package; MacKinnon permission record |
| LinAlgf90 | `LinAlgLib::DSingularValueDecomposition%SVD`, `LinAlgLib::GenEigenSolSymD%DiagSym` | BSD-3-Clause |
| FortLearner | `mod_kmeans::kmeans%fit` | MIT with third-party notices |
| KohonenF03 | `self_organized_map_utilities::external_train_map` | GPL-3.0 license text |
| NN_MOD regressors | `NEURALNET_MOD::NEURALNET%BACKPROP`, `OPT_MOD::ADAM` | MIT |
| Fortran FilterSLP | `filterSLP` | MIT root; EMSOL separate |
| BMSL | `EmpiricalStats_tools::KDE`, `DimReduction_tools::PCA` | GPL-3.0 license text; DMSL dependencies separate |
| ASURV | `PLESTM` | MIT root; historical component provenance retained |
| Visual Fortran Solvers | `Solvers_Mod::Solvers_Mod_Dense_Cholesky_Factorization`, `Solvers_Mod::Solvers_Mod_Cg_No_Prec` | No standalone license identified |
| HPCSeriesCore | `hpcs_core_stats::hpcs_median`, `hpcs_core_rolling::hpcs_rolling_median` | Apache-2.0 |
| Fortran shape functions | `shapefuncs::shapefunc%eval` | MIT |
| Neural-network tangent and adjoint tests | `NOGWDNN_MOD::NN_TL`, `NOGWDNN_MOD::NN_AD` | MIT |
| Fortran Neural Network library | `fnn_network_sequential::SequentialNeuralNetwork%apply_tangent_linear`, `fnn_network_sequential::SequentialNeuralNetwork%apply_adjoint` | MIT |
| PolyChordLite | `interfaces_module::run_polychord` | Custom PolyChord noncommercial academic/research license |
| Stripy | `TRMESH`, `INTRC0` | LGPL-3.0 text plus retained Renka source notices |
| JKogb | `dtransf::DHSVD2` | MIT with named inherited components |
| FORCES | `mo_moment::mean`, `mo_moment::variance`, `mo_moment::covariance` | Conflicting Apache/GPL/LGPL notices; selected module says LGPLv3+ |
| TSSS | `UNICORF`, `CRSCORF` | GPL-2.0-or-later |
| Spaloess | `lowesf` | MIT package plus retained AT&T permissive source notice |
| Clustering via Nonsmooth Optimization | `dcclust_method::optim` | Academic teaching/research permission for reviewed DCDB subset |
| forApollo | `fa_kf_predict` | Proprietary designation; no standalone permission grant identified |
| MultiNest | `Nested::nestRun` | Custom MultiNest noncommercial research license |
| FFT overlap experiments | `overlapfft_mod::cufft2dTest_manystream` | No license identified in selected source/build files |
| M_blas | `M_blas::dgemm`, `M_blas::dtrsv` | MIT root with inherited Reference BLAS notices |
| Sherman Morrison update interfaces | `SM1_f` | BSD-3-Clause |
| Sparse Fortran examples | `test_mumps` | MIT |
| Sparse Iterative Parallel Linear Solver | `mSolver::SolverAxB` | MIT |
| npregfast | `Reg1D`, `lsq::startup` | MIT package declaration with inherited LSQ attribution |
| rrelaxiv | `RELAXALG` | Custom academic-institution license |
| BFpack | `draw_ju` | GPL-3.0-or-later |
| BVARmml | `VARutils::VARforecast` | No license identified |
| Singular surface operators | `cadaptri` | GPL-2.0 text; later-version election not established |
| Fitter MC | `bootstrap::monte_carlo_fit_data` | GPL-3.0 text with retained numerical-component notices |
| FC Tables | `mprlinalg::mprqr`, `mprlinalg::MPRSVDPLAN%iterate` | No license grant identified for selected project code |
| PaScaL TDMA | `PaScaL_TDMA_cuda::pascal_solver` | MIT |
| OptimusPrime | `mod_optSA::opt_runSA` | No license identified |
| PDFO | `BOBYQA`, `COBYLA` | BSD-3-Clause |
| S2HAT | `s2hat_alm2map_mod::s2hat_alm2map` | GPL-2.0-or-later |
| ODEPACK redistribution | `DLSODE` | No grant identified in selected redistribution documentation |
| GPROPT | `GOLDENSECTION` | MIT |
| HSSPACK | `HssCholSolver`, `DHSSMM` | No explicit license grant identified |
| libdlfind | `dlf_lbfgs_step` | LGPL-3.0-or-later with retained L-BFGS attribution |
| FM Algorithm 814 archive | `FMZM::GAMMA`, `FMZM::BETA` | No explicit license grant identified in reviewed distribution files |
| Induced Smoothed Lasso | `islasso` | GPL-2.0-or-later |
| tfQMRgpu | `tfqmrgpu::tfqmrgpu_bsrsv_complete` | MIT |
| AMG4PSBLAS | `amg_d_prec_mod::amg_dprec_type%build` | BSD-3-Clause |
| BDDCML | `module_bddcml::bddcml_solve` | LGPL-3.0-or-later |
| GALAHAD | `GALAHAD_EQP_double::EQP_solve`, `GALAHAD_QPB_double::QPB_solve` | BSD-3-Clause |
| BayesFM | `factor_normal_class::update_factor_normal` | GPL-3.0-only |
| Robust Library for R | `rlRWAGm2` | GPL-3.0-or-later |
| rrcov | `rlds` | GPL-3.0-or-later |
| SmoothHazard | `survWeib` | GPL-2.0-or-later |
| Robust Gauss Newton | `rgnMod::rgn` | MIT |
| Fortress | `filter::kalman_filter` | CC0-1.0 for project code; separate component notices |
| Timeslab | `arcv`, `arprt` | No explicit license grant identified |
| Parallel Structured Matrix Multiplication research code | `PSMMA_TOEPLITZ` | No explicit license grant identified |
| PSBLAS | `psb_linsolve_mod::psb_krylov` | BSD-3-Clause |
| PyGSLIB | `gamv` | MIT modifications with retained GSLIB notice |
| Implicit QR demonstration | `eigenvalues::eig`, `eigenvalues::eig_hessenberg_matrix` | No explicit license grant identified |
| Inference for physical sciences | `DCUHRE`, `ninfol` | BSD-3-Clause root notice; historical cubature terms need separate confirmation |
| glmnet MATLAB builds | `elnet`, `lognet` | GPL-3.0 license file; no later-version election identified |
| PDAF | `PDAF::PDAF_assimilate_etkf` | LGPL-3.0-or-later |
| TISEAN | `autocor`, `spectrum` | GPL-2.0-or-later |
| SpLLT | `spllt_mod::spllt_factor` | BSD-3-Clause |
| Minimum Split Checkerboard Decomposition | `Exponentials_mod::FullExp%lmult` | MIT |
| SparseReg MATLAB toolbox | `SPARSEREG::PENALIZED_L2_REGRESSION` | No explicit license grant identified |
| Higher Order Markov Fortran | `markov_core::predict_k_steps`, `markov_higher_order::fit_transition_matrix` | MIT-style permission notice (incomplete standard text) |
| Computational Economics Fortran examples | `toolbox::fzero`, `toolbox::poly_interpol`, `toolbox::legendre` | GPL-3.0 notice; Numerical Recipes adaptations need separate review |
| KohonenF08 | `self_organizing_map_utilities::self_organizing_map%train` | MIT |
| PDHGEQZ | `PDHGEQZ`, `PDGGHRD` | No explicit license grant identified |
| JACSD | `JACSVD::JACV0_EXECUTE` | MIT for selected Jacobi implementation |
| tidybench | `SLVAR` | MPL-2.0 |
| FAS | `fitnoiseF` | GPL-2.0-or-later |
| midasmlpy | `sparse_four` | GPL-2.0 license file; no later-version election identified |
| PDHSEQR Algorithm 953 | `PDHSEQR`, `PDGEBAL` | No explicit license grant identified |
| quantregpy | `rqfnb` | GPL-3.0 license file; no later-version election identified |
| Fortran time-series translations | `itsmr_mod::arma_acvf`, `itsmr_mod::arma_forecast`, `time_series_stats_mod::burg_fit` | BSD-2-Clause and MIT identifiers in reviewed sources; other package terms vary |
| ElliFEM | `femSolver (unnamed main program)` | No explicit license grant identified |
| heatcompact3d | `thomas_module::thomas`, `differentiate::differentiator_type%diff`, `time_integrator::RK3_integrator_type%integrate`, `time_integrator::euler_integrator_type%integrate`, `field_cpu::field_cpu_type%rhs` | GPL-3.0 license file; no later-version election identified |
| laplace-2D | `laplace::laplace_solve` | GPL-2.0 license file; no later-version election identified |
| LIBPARABOL / sippp | `SOLVERS::GMRES`, `RUNGE_KUTTA::runge_kutta_step` | No explicit license grant identified |
| Gaussian Mixture ARMA-GARCH prototype | `MODELS::ARMA%residuals`, `MODELS::ARMA_GARCH%variances` | No explicit project license grant identified |
| meshf | `delaunay2::bowyer_watson2` | AGPL-3.0 |
| ARPREC | `mprealmod::operator(+)`, `quadts`, `initqts` | Modified BSD/LBNL notices with additional terms |
| DLA-Future Fortran Interface | `dlaf_fortran::dlaf_pdsyevd`, `dlaf_fortran::dlaf_pdsygvd` | BSD-3-Clause |
| ELPA | `elpa_api::elpa_t%eigenvectors_double` | LGPL-3.0 |
| forSISL | `Curve_Interrogation::s1850` | Custom forSISL license plus separately licensed SISL |
| Powell optimization archive | `BOBYQA`, `COBYLA`, `LINCOA`, `NEWUOA`, `GETMIN` | LGPL-2.1-or-later for the five reviewed solver folders |
| ARPACK PARPACK modernization | `znaupd`, `zneupd` | No explicit license grant identified for the adaptation |
| Delaunay Density Diagnostic | `DELSPARSE_MOD::DELAUNAYSPARSES` | MIT root notice; bundled BQPD has research-distribution terms |
| Python BLS | `eebls` | MIT root notice |
| Unstructured finite volume | `operation_conjugate_gradient::conjugate_gradient%solve`, `operation_gmres::gmres%solve`, `operation_diffusion::diffusion_stencil` | GPL-3.0 license file; no later-version election identified |
| System Dynamics | `runge_kutta::rk4`, `math::akima`, `::mean`, `::avevar`, `::eigencov` | MIT root; Numerical Recipes-marked components unresolved |
| PyMC 2 historical implementation | `normcdf`, `poisson`, `exponweib_ppf` | AFL-3.0 root notice; bundled components have separate terms |
| wvdecomp | `atrouswv` | LPPL notice; version not specified |
| octree-mg | `m_multigrid::mg_fas_fmg`, `m_multigrid::mg_fas_vcycle`, `m_vlaplacian::vlaplacian_set_methods` | No explicit grant identified for selected multigrid modules |
| SLICOT System Identification | `MEXFUNCTION (sident gateway)` | BSD-3-Clause root notice |
| FERRE | `lin`, `lsq::poly_fit`, `nelder_mead::minim` | No explicit project-wide grant identified |
| HARMONIE Monitor | `calc_corr`, `contingency::acc_cont`, `contingency::ini_cont` | No explicit grant identified in selected Monitor sources |
| SciJIT | `quadpack_wrappers::dqags_wrapper`, `quadpack_wrappers::dqagi_wrapper`, `minpack_wrappers::hybrd_wrapper` | BSD-3-Clause wrappers; bundled QUADPACK/MINPACK notices apply |
| SciJIT | `quadpack_wrappers::dqagp_wrapper`, `quadpack_wrappers::dqawo_wrapper`, `quadpack_wrappers::dqaws_wrapper`, `quadpack_wrappers::dqawc_wrapper`, `minpack_wrappers::lmdif_wrapper`, `minpack_wrappers::lmder1_wrapper`, `minpack_wrappers::lmstr1_wrapper`, `minpack_wrappers::enorm_wrapper`, `odepack_wrappers::lsoda_wrapper`, `odepack_wrappers::lsodar_wrapper`, `fitpack_wrappers::curfit_wrapper`, `fitpack_wrappers::splev_wrapper`, `fitpack_wrappers::splder_wrapper`, `fitpack_wrappers::splint_wrapper`, `fitpack_wrappers::regrid_wrapper`, `fitpack_wrappers::bispev_wrapper`, `fitpack_wrappers::dblint_wrapper` | BSD-3-Clause wrappers; bundled numerical-component notices apply |
| ANN Fortran interface | `ANN_mod::ann_buildTree`, `ANN_mod::ann_kSearch`, `ANN_mod::ann_destroyTree` | LGPL-2.1-or-later upstream ANN notice; bridge scope not separately stated |
| SOSIE | `MOD_AKIMA_1D::AKIMA_1D`, `MOD_AKIMA_2D::AKIMA_2D`, `MOD_MANIP::FIND_NEAREST_POINT` | GPL-3.0 license text; version-option grant not separately identified |
| fsklearn | `Mod_Fsklearn_Essential::Neural_Network%Predict_One`, `Mod_Fsklearn_Essential::Decision_Tree%Predict_One`, `Mod_Fsklearn_Essential::Random_Forest%Predict_One` | BSD-3-Clause root notice |
| coordinates grids and maps | `interp1D::interp_linear`, `interp1D::interp_spline`, `interp2D::interp_bilinear`, `loess::loess_smooth`, `gaussian_filter::filter_gaussian`, `gaussian_filter::gaussian_kernel`, `gaussian_filter::convolve`, `gaussian_filter::hgrad`, `polygons::create_polygon`, `polygons::point_in_polygon` | No project-wide grant identified; selected modules retain component provenance |
| BaM | `BaM_tools::BaM_Fit` | GPL-3.0 root text; dependency terms separate |
| freeCappuccino legacy snapshot | `dpcg`, `bicgstab`, `GaussSeidel` | GPL-3.0-only root notice |
| NumX | `MCM`, `VARIAN`, `VOLAT`, `SKEWN`, `KURTOS`, `COVM`, `CORM`, `COVCOR`, `CORCOV`, `TENSORK`, `TENSORKK`, `getNormalPdf`, `GENNOR` | Apache-2.0 root text; selected RNG files retain conflicting proprietary notices |
| SAM Fortran library | `SKYSOLVE` | Apache-2.0 root and selected source notices |
| TOOLIB | `cholesky::choldc`, `cholesky::cholsl`, `least_squares::moindres_carres_lineaire`, `least_squares::moindres_carres`, `intpl::interp1D`, `intpl::interp2D`, `fftw3::tab_init_fftw3`, `fftw3::tab_calc_fftw3`, `fftw3::tab_end_fftw3`, `sort_arrays::sort_array2`, `tchebychev::tcheby`, `tchebychev::tab_tcheby` | GPL-3.0 root text; component notices and Numerical Recipes provenance retained |
| chunkmatc | `adapgauss`, `legewhts`, `legepol` | BSD-3-Clause-Modification for selected Rokhlin numerical sources |
| ForTrilinos | `fortrilinos_hl::TrilinosSolver%setup_matrix`, `fortrilinos_hl::TrilinosSolver%setup_solver`, `fortrilinos_hl::TrilinosSolver%solve`, `fortrilinos_hl::TrilinosEigenSolver%setup_matrix`, `fortrilinos_hl::TrilinosEigenSolver%solve`, `fortrilinos_hl::TrilinosEigenSolver%converged`, `fortrilinos_hl::TrilinosEigenSolver%setup_matrix_rhs`, `fortrilinos_hl::NOXSolver%setup`, `fortrilinos_hl::NOXSolver%solve` | BSD-3-Clause ForTrilinos interfaces |
| Skyborn | `dlinint1`, `linmsg_core::dlinmsg`, `dlinint2`, `compute_lanczos_weights`, `apply_filter_1d`, `apply_filter_1d_periodic`, `mann_kendall_core_mod::compute_s_value`, `mann_kendall_core_mod::compute_base_variance`, `mann_kendall_core_mod::compute_sen_slope` | BSD-3-Clause root; adapted component notices retain their scope |
| PIPPy | `svdfit` | Apache-2.0 root; Numerical Recipes component provenance requires separate review |
| ButterflyPACK | `d_BPACK_factor::d_BPACK_Factorization`, `d_BPACK_Solve_Mul::d_BPACK_Solution`, `z_BPACK_factor::z_BPACK_Factorization`, `z_BPACK_Solve_Mul::z_BPACK_Solution`, `d_BPACK_Solve_Mul::d_BPACK_Mult` | BSD-style root with additional enhancement-license clause |
| AUTO-07p | `AE::AUTOAE`, `BVP::AUTOBV`, `MESH::ADAPT2`, `MESH::INTWTS`, `MESH::GENWTS`, `MESH::WINT` | BSD-3-Clause numerical core; optional plotting dependencies separately scoped |
| Cedar | `BMG2_SymStd_restrict`, `BMG2_SymStd_interp_add` | BSD-3-Clause Cedar framework notices |
| Dataplot | `MEAN`, `MEDIAN`, `SD`, `RANK`, `SORT`, `RANKCR`, `LINFIT`, `NORCDF`, `NORPDF`, `NORPPF`, `LOGCDF`, `LOGPDF`, `LOGPPF`, `LOGGAM`, `POICDF`, `BETCDF`, `BETPDF`, `BETPPF`, `CHSCDF`, `CHSPDF`, `CHSPPF`, `TCDF`, `TPDF`, `TPPF`, `FCDF`, `FPDF`, `FPPF`, `GAMCDF`, `GAMPDF`, `GAMPPF`, `WEICDF`, `WEIPDF`, `WEIPPF`, `DLBETA`, `DBETAI` | NIST public-domain notice for Dataplot; bundled notices retain their scope |
| PFLARE | `pflare::PCRegister_PFLARE`, `pcair_shell::create_pc_air_shell`, `cf_splitting::compute_cf_splitting` | MIT PFLARE root notice |
| ScaLAPACK | `PDGESV`, `PZGESV`, `PDPOSV`, `PZPOSV`, `PDTRTRS`, `PDGELS`, `PDSYEV`, `PZHEEV`, `PDGESVD`, `PDGBSV` | BSD-3-Clause-Open-MPI-style ScaLAPACK root notice |
| pyOpt | `solvopt`, `SLSQP`, `COBYLA`, `NNLS`, `LSEI`, `HFTI`, `LDP`, `H12` | MIT selected solver components; LGPL-3.0-or-later pyOpt framework |
| fastSHT | `get_plm_recursive`, `map2fft`, `fft2map`, `t2alm`, `alm2t` | GPL-3.0 license text; HEALPix-derived recurrence provenance |
| FLAPWxHZ | `HIF_HZ::ZHZL1SA` | MIT FLAPWxHZ with retained contributor attribution |
| ecTrans | `DIR_TRANS`, `INV_TRANS`, `EDIR_TRANS`, `EINV_TRANS` | Apache-2.0 ecTrans notices with ECMWF privileges/immunities statement |
| Clawpack Riemann solvers | `rp1_ptwise` | BSD-3-Clause Clawpack Riemann solver notice |
| Boxcode2D legacy wrapper | `lbfmm2d`, `chebexps`, `chebinmt` | No license grant identified in reviewed root and wrapper files |
| NDSM | `NDSM_POISSON::solve_poisson_bvp`, `NDSM_INTERP::ninterp` | BSD-3-Clause NDSM source notices |

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
| [Fortran-parallel-sort](https://github.com/cphyc/fortran-parallel-sort) | N6a1b | OpenMP chunk ranking and adjacent merges, REAL(8) input retained | One-based permutation; kind-8/REAL64 agreement and OpenMP configuration required. Tiny/chunk-edge cases and scaling unverified. |
| [Fortran-Timsort](https://github.com/suzuyuyuyu/fortran-timsort) | N6a2a | Generated INT32 run detection, insertion extension and default shorter-run merging | Final-singleton overread risk; equal keys in reversed runs preclude a blanket stability claim. No history/real-path review. |
| [fsort](https://github.com/snljty/fsort) | N6a2b | Size-selected insertion, quick partitioning and heapsort intent | Repair required: malformed IF statements, heap offsets ignoring beg and insertion guard lacking guaranteed short circuit. |
| [HeapSort](https://github.com/SAG2021/HeapSort) | N6a2b | In-place maximum-heap construction/extraction with paired permutation swaps | Use C_SIZE_T/C_DOUBLE kinds. Actual permutation is sorted(i)=original(perm(i)), contrary to header formula. |
| [Fortran-Iterative-Quicksort](https://github.com/mustafa-ayyub/Fortran-Iterative-Quicksort) | N6a2a; N6a2b | Caller-workspace iterative Lomuto quicksort, integer and default real | Insufficient stack silently drops ranges; use 2*N workspace. Last pivots retain quadratic cases; NaNs unsupported. |
| [Fortran-quicksort](https://github.com/Beliavsky/Fortran-quicksort) | N6a1b; N6a2b | Pure real permutation sorting and overwrite-by-permutation wrapper | indexx returns identity on NaNs; overwrite wrapper lacks that guard. Automatic O(N) index storage; integer conversion path unreviewed. |
| [numerical-analysis](https://github.com/jeffirwin/numerical-analysis) | H2a1b2 | Composite sampled Simpson 1/3 with final 3/8 panel for even counts | Uniform grid, >=3 odd or >=4 even samples required. No error estimate, validation or automatic refinement. |
| [INTEGRAL](https://github.com/jchristopherson/integral) | H2a1a1 | Procedure-pointer wrapper and finite-interval DQAGS/DQAGSE adaptive-controller path | FERROR dependency; workspace-reuse flag and breakpoint-name findings require repair/checks. Numerical kernels not fully audited. |
| [Audito](https://github.com/michel-heinz/audito) | H1 | Forward first-gradient product/addition propagation with explicit seed vectors | Equal allocated seed bases required; distinct concatenating operator and Hessian/Laplacian modules unreviewed. |
| [DNAOAD](https://github.com/fpenunuri/DNAOAD) | H1 | Coordinate directional evaluations via dual arithmetic and order save/restore | Global order state; REAL64 GNU variant. Callback must retain dual components; higher-order and complex nonanalytic differentiation unverified. |
| [auto-diff](https://github.com/zoziha/auto-diff) | H1 | Pointer-graph reverse adjoint accumulation and scalar gradient access | REAL32 by default. Repeated backward calls accumulate; ownership, reassignment and node reclamation need validation. |
| [mp-interp](https://github.com/pjbartlein/mp-interp) | E1a | Cyclic adjusted-input mean interpolation via inverse mean matrix and piecewise-linear midpoint interpolation | Inputs are interval means. INFO ignored; coordinates debug-only; discrete mean agreement and padding must be checked. |
| [libcoulcc](https://github.com/banana-bred/libcoulcc) | C12 | Coulomb-wave interface, initialization and continued-fraction dispatch | Partial core review. Wrapper IFAIL uninitialized; convenience G function requests an F-only mode. Raw interface exposes status. |
| [FortVSH](https://github.com/justinelfritz/FortVSH) | C3a2; H2c | Ordinary Legendre recurrence and Gauss-Legendre node/weight generation | Validate degree/count. Fixed Newton tolerance/cap with no convergence status; other harmonic/coupling routines unreviewed. |
| [Butterworth-Filter](https://github.com/youshanliu/Butterworth-Filter) | L10a1c3 | Low-pass coefficient construction and causal recursive forward filtering | Normalize a(0)=1. Zero history; no streaming state or status. Validate cutoff/order; high-order conditioning unverified. |
| [RKSUITE](https://github.com/jacobwilliams/rksuite) | I1a1a | F90 setup, requested-output driver and explicit embedded-RK error-control paths | Stateful pointers need cleanup; callback is a function, not the F77 subroutine API. Stiffness warning is not stiff-solver support. |
| [libsparse](https://github.com/jvdp1/libsparse) | D1b4 | Native raw-CSR scaled matrix-vector row/scatter loops | Use initialized y and valid one-based CSR. The object mult wrapper has an INTENT(OUT) accumulation mismatch; the sketch uses the public native helper. |
| [SPOOF](https://github.com/samharrison7/spoof) | D1b4 | CSR object dispatch and SPARSKIT AMUX row products | Conversion statuses discarded; validate extents/indices. Empty raw matrices and zero trailing columns need explicit handling. |
| [sparseSET](https://github.com/dorivalpiedadeneto/SparseSet) | D1b9 | Dense/sparse line conversion with thresholding and duplicate accumulation | Preallocate dense output before SIZE check. Drop tolerance loses small values; empty assembly and fixed sorter stack are outside the sketch. |
| [tensor-algebra](https://github.com/cfku/tensor-algebra) | D1a4; D1b6 | Vector dot-product loop and vector/matrix dyadic outer products | Output first, separate dimension, REAL(8). Outer products do not contract indices; unrelated solver/decomposition paths unreviewed. |
| [VecFor](https://github.com/szaghi/VecFor) | D1a4; D1a11 | Shared-include R8P dot and Cartesian cross products | Three components only; requires preprocessing and PENF. Accurate-product/device variants and cancellation/range behavior unverified. |
| [fortran_lsp](https://github.com/ivan-pi/fortran_lsp) | D9b1 | NNLS active/passive sets, Householder/Givens updates and triangular solve | A/b overwritten; mode=1 succeeds. Workspace/ABI checks required; simplified wrapper source includes a test main. |
| [vanhuffel](https://github.com/ivan-pi/vanhuffel) | D9a4 | Augmented-data QR/SVD dispatch, rank adjustment and TLS solution recovery | Perturbs both A and B; not ordinary fixed-A residual minimization. Inspect IERR/IWARN and scaling; backend kernels not fully audited. |
| [lanczos_iterator](https://github.com/lanczos-iterator/lanczos_iterator) | D4a1 | Matrix-free real-symmetric wrapper, recurrence and Ritz/residual dispatch | ADD callback semantics; variance output is a residual norm. Saved state, polishing work and absent success flag require care. |
| [Fortran_RNG](https://github.com/vinceneede/Fortran_RNG) | L6a21 | Four-word xoshiro256 star-star output, recurrence and 52-bit real conversion | Explicit four-word seed; allocation alone does not initialize state. IEEE layout and wrapping integer arithmetic assumed. |
| [xoshiro-fortran](https://github.com/DSCF-1224/xoshiro-fortran) | L6a21 | Scalar star-star and REAL64 submodule dispatch | Real draws advance twice, integer draws once. Seed setter silently copies only the common prefix; require four words. |
| [fortran-splitmix64](https://github.com/DSCF-1224/fortran-splitmix64) | L6a21 | Stateless SplitMix mixing step | INTENT(IN) seed is unchanged; repeated seed repeats output. Assigning harvest to seed is not ordinary SplitMix progression. |
| [fortran-xorshift-64-star](https://github.com/jonas-finkler/fortran-xorshift-64-star) | L6a21; L6a14 | Limb-multiplied xorshift uniform output and cached Box-Muller normals | Nonzero seed; real conversion may round to 1. Normal cache is per procedure/thread, not per object; LOG endpoint unguarded. |
| [ogata](https://github.com/UCLA-TMD/ogata) | J; H2a3a2 | Mesh-spacing search and tabulated Bessel-zero quadrature | Fortran nu=0/1 and 1<=n<=98 only; node access precedes limit checks. No error estimate/Newton convergence flag. |
| [fftlog](https://github.com/emsig/fftlog) | J; J1a3 | Gamma-ratio multipliers, periodic logarithmic Hankel and half-order sine/cosine transforms | In-place data; initialize workspace and retain adjusted kr. Logarithmic-grid assumptions and singular/Nyquist handling matter. |
| [FortranCWT](https://github.com/wangyun1995/FortranCWT) | J | Real zero-boundary CBSW transform via spline coefficients and cumulative sums | Allocatable outputs use scale-first zero-based indexing; no status. Only selected A19 path reviewed. |
| [wavepack](https://github.com/zoziha/wavepack) | J | Mean removal, FFT/daughter/inverse Morlet transform and cone of influence | Time-first output; enforce 65535 scratch bound. Mutable default controls, dependency branch and source notices recorded. |
| [fOptimize](https://github.com/volpatto/foptimize) | G1a1a; G1a1c | Interior-point scalar interval reduction and derivative-supplied Newton stationary-point search | Results printed, not returned. Saved controls persist; Newton requires its nominally optional output unit. Stationarity alone does not identify a minimum. |
| [Minimization](https://github.com/bramvandeput/minimization) | G1b1a; H1 | Finite-difference negative-gradient steps and central-gradient evaluation | Source-defined objective, POINTER arrays and fixed difference step. Undefined initial gradient copy, pointer leaks and misleading limit message recorded. |
| [fortran-grid-search](https://github.com/jonbmay/fortran-grid-search) | G2i | Cell-center Cartesian sampling, best-cell retention and hierarchical refinement | Program reads Input.txt; sample model is 3D. Uninitialized MisExit/argument-parser state and optional-argument hazards need attention; no global guarantee. |
| [Particle-Swarm-Optimization-Fortran-95](https://github.com/zaman13/Particle-Swarm-Optimization-Fortran-95) | G2i | Inertial/personal/global-best velocity update and box-restricted objective evaluations | Program parameters are source-defined. VTR records but does not stop iterations; NIR=0 report indexing and partial NFE count recorded. |
| [MMA-in-Fortran](https://github.com/JeffreyGuevaraCorzo/MMA-in-Fortran) | G2h3b1b | Moving asymptotes, reciprocal first-derivative model and primal-dual subproblem dispatch | One step, not complete optimization; rank-two allocatable columns and history required. LAPACK overwrite/INTENT mismatch; no returned inner status. |
| [l-bfgs-b_wrapper_f90](https://github.com/snljty/l-bfgs-b_wrapper_f90) | G1b1b; G2h1a2 | Unbounded/box-constrained SETULB reverse-communication callback dispatch | func_tol is FACTR, max_cyc counts FG requests. Objective declaration mismatch and observer access before first evaluation recorded. Core not fully audited. |
| [osqp-fortran](https://github.com/osqp/osqp-fortran) | G2e1 | Positive-definite convex-QP subset through one-based CSC Fortran/C setup and solve bridge | Match backend kinds/configuration; bridge temporarily mutates INTENT(IN) indices. Setup-failure and process-exit paths require repair; inspect solver info as well as status. |
| [quadprog](https://github.com/pedro-ricardo/quadprog) | G2e1 | Row-constraint/sign conversion, bound appending and Cholesky QP setup/dispatch | Near-zero Hessian diagonals are changed, not validated. Equality-check logic can miss violations; res is criterion output, not constraint residual. |
| [SHEPPACK](https://github.com/vtopt/sheppack) | E2b; E3a2 | Scattered quadratic Shepard setup, compact weighted evaluation and fitted-function gradient | Retain consistent setup state; setup IER and query IER differ. Scalar evaluator returns zero outside support without a status. |
| [numfort](https://github.com/richardfoltyn/numfort) | F1b | REAL64 safeguarded secant/inverse interpolation and bisection | Residual callback is a subroutine. Invalid bracket can leave x0 undefined; inspect optional result status. Sign-product overflow/underflow not guarded. |
| [tensor_tools](https://github.com/llamm-de/tensor_tools) | D1a4; D1b6 | Fixed-3D Frobenius inner product and vector/matrix dyadic outer products | Scalar contraction initializes output; two rank-four contraction overloads do not and are excluded from the sketch. |
| [Non-Neg_Matrix_Factorization](https://github.com/petchma/non-neg_matrix_factorization) | K1b2a | Alternating nonnegative multiplicative least-squares approximation | W-loop and H-initializer dimensions need repair; printed Error is squared signed-residual sum. No returned factors/status or checked reduced-rank example. |
| [lin_alg](https://github.com/Quentin-Marecat/lin_alg) | D2b1b; D5 | Lower Cholesky factor and classical Gram-Schmidt columns | Factor upper triangle undefined; disable internal full-factor check and zero after return. Normalization lacks rank guard; no solution/error status. |
| [pcgcoarray](https://github.com/jvdp1/pcgcoarray) | D2b1b | Coarray CG recurrence, row products and synchronized reductions | Zero initial guess, binary RHS and collective participation required. Sum of local L2 norms, image-1 solution assembly, quadratic iteration scratch and eigenvalue getter finding recorded. |
| [libid](https://github.com/fastalgorithms/libid) | D5 | Fixed-rank pivoted Householder QR and interpolative-decomposition backsolve | A overwritten with packed coefficients; preserve original selected columns. Pivot swaps differ from composed column list; validate rank and approximation independently. |
| [maria-fortran](https://github.com/sbudzinskiy/maria-fortran) | D6 | Caller-sketched randomized SVD with QR/LQ power steps and projected SVD dispatch | Caller forms A*Omega and supplies multiplication pointers. Flat buffers, both workspace queries, kc<=min(m,n) and intermediate error handling matter. |
| [FortRAND](https://github.com/llamm-de/fortrand) | L6a21; L6a14 | Intrinsic uniform draws and Box-Muller/polar normal transforms | Every scalar draw reinitializes the intrinsic RNG; normal default/comment mismatch and zero-log endpoint recorded. |
| [knuth-flrng](https://github.com/marcoxa/knuth-flrng) | L6a21 | Lag-100/37 floating-point recurrence, scalar seed expansion and warm-up | RNFARR requires at least 100 outputs; separate scalar wrapper reseeds on refill. COMMON state is shared. |
| [melg-64-fortran](https://github.com/DSCF-1224/melg-64-fortran) | L6a21 | MELG19937-64 explicit state and upper-53-bit real conversion | Initialize before use; signed-wrap seed assumption. Other variants, jump polynomials and array seeds unreviewed. |
| [dsfmt_f03_interface](https://github.com/jsspencer/dsfmt_f03_interface) | L6a21 | Buffered Fortran/C dSFMT uniform draws | Match C exponent and even minimum buffer size; reset on distribution changes. State-pointer copies do not create independent streams. |
| [nsmarkov-fortran](https://github.com/gfell/nsmarkov-fortran) | M1a | Time-varying Rouwenhorst/Tauchen finite-state AR approximations | Builds grids and row-oriented transitions, not random paths; starts from zero. Validate dimensions, scales and probabilities. |
| [ACFbyFFT](https://github.com/lingtikong/ACFbyFFT) | L10a2a1; L10b2a | Real FFT auto/cross correlation and lag normalization | Use centered input with -nave to avoid uninitialized-tail mean calculation. Bound lag count; output is not unit-variance normalized. |
| [signal_subspace](https://github.com/scivision/signal_subspace) | L10a3a; L10a2a1 | Complex ESPRIT frequencies and delayed-window second moments | Pivot ABI and sigma extent require repair; covariance omits a window and uses N normalization. No mean removal. |
| [TOMS-Algorithm-675](https://github.com/ivan-pi/TOMS-Algorithm-675) | L10a2e | Square-root covariance/information pre-array updates | Mapping scoped to scalar observations; triangular factors, workspace and mutable output-request flags matter. SRCF does not update state estimates. |
| [Torrence/Compo wavelets](https://github.com/chris-torrence/wavelets) | L10a3a | Mean removal, padded FFT/daughter-spectrum multiplication and inverse transforms | Fixed 65535 scratch bound includes padding; writable default selectors and no returned status. Significance routines unreviewed. |
| [FSTPACK](https://github.com/thkrz/fstpack) | J; J1a2 | Gaussian-voice Stockwell construction and separately callable complex Fourier wrapper | Real-valued complex storage intended for Stockwell round trips; negative-frequency information discarded. FFT scratch INTENT mismatch recorded. |
| [RFNG](https://github.com/jeffirwin/rfng) | L6a21 | Object-owned MT19937 seed, twist, tempering and unsigned-output masking | INT64 return carries only 32 random bits; preprocessing and signed-wrap assumptions. Array seeds/reference sequences unreviewed. |
| [besseleval](https://github.com/jamescbremerjr/besseleval) | C10a3 | Real-order J/Y dispatch and tabulated Chebyshev phase/log reconstruction | Matching binary tables required; shared initialization and branch-dependent auxiliary outputs. Repeated init leaves DSIZE unassigned. |
| [HOMPACK90](https://github.com/vtopt/hompack90) | F2 | Dense normal-flow homotopy driver, step/tolerance control and endpoint dispatch | External residual/Jacobian-column callbacks; saved continuation state, mutable tolerances and resumable IFLAG=2/3. Optional switch is tested by presence. |
| [EISCOR](https://github.com/eiscor/eiscor) | D4a5 | Symmetric tridiagonal Cayley/core reduction and unitary QR dispatch | Short driver WORK section requires repair/checking; factor N=1 edge case. Complex vectors, scaling and INFO inspection required. |
| [Fazang](https://github.com/yizhang-yiz/fazang) | H1 | Reverse-mode tape, primitive chain rules and adjoint extraction | Reset adjoints before repeat sweeps; tape reboot invalidates handles. Convenience jac uses uninitialized n; Hessian path unreviewed. |
| [BLZPACK](https://github.com/oamarques/BLZPACK) | D4a1; D4b1 | Standard/generalized symmetric block-Lanczos reverse communication and step orchestration | Caller supplies products, shifted solves and inertia. Match storage-prefix formulas and definiteness assumptions; cited generalized example uses B=I and external MA47. |
| [NITSOL2](https://github.com/vadim-z/NITSOL2) | F2 | Inexact Newton/Krylov driver, backtracking and forcing-term control | Fork callback/control signatures, solver-specific workspaces and explicit real defaults. Small-step success need not imply a small residual; early invalid-control cleanup can use uninitialized IPUNIT. |
| [LRAP](https://github.com/sbudzinskiy/LRAP) | K | Entrywise nonnegativity transformation followed by truncated SVD | One step, not an internally converged fit or best-approximation certificate. Dual workspace queries; SVD status can be overwritten before return. |
| [FortranMatrix](https://github.com/knanagnostop/FortranMatrix) | D2a1; D2c1 | Real/complex LU dispatch and explicit inversion with workspace queries | Input copied; errors print and STOP. Nonempty square matrices, compatible ABI and containing module's PFAPACK dependency required. |
| [Tensor Toolbox](https://github.com/adtzlr/ttb) | D2a1; D1a4 | Fixed 3-by-3 cofactor inverse and scalar Frobenius contractions | Inverse has no singularity/conditioning guard. Compact symmetric double contractions weight off-diagonal entries twice. |
| [MEPACK](https://github.com/mpimd-csc/mepack) | D8 | Standard Lyapunov/Sylvester Schur-transform/solve/back-transform drivers | Integer LDWORK carries query result; initialize INFO, retain SCALE and inspect status before using X. Inner solver modes not fully audited. |
| [curvefit](https://github.com/jchristopherson/curvefit) | E1a; K1a1a2 | Piecewise-linear interpolation and through-origin degree-one least-squares dispatch | Initialize interpolation successfully before lookup; wrapper does not guard every error path. Scalar regression has no intercept and delegates polynomial solve to nonlin. |
| [gcvspline](https://github.com/charlesll/gcvspline) | K5; K6a2 | Natural B-spline smoothing and fitted-spline derivative evaluation | Half-order M gives degree 2*M-1. Preserve setup/work for negative-MD reuse; derivative quality depends on smoothing, and no new samples were checked. |
| [vector_fit](https://github.com/chrissmartt/vector_fit) | K1a1a3; K6a1 | Fixed-pole residue least squares and rational-response evaluation | Pole relocation excluded. Normal equations/default solve lack returned status; NEW_A/C_HAT unassigned. Avoid sample/pole coincidences. |
| [FilterSD](https://github.com/jacobwilliams/filtersd) | G2h3b1b; G4c | Smooth nonlinear constrained minimization with first derivatives; derivative consistency diagnostic | Shared state and backend setup required. `checkd` can leave X perturbed and has no numerical status. |
| [DEPP](https://github.com/gbertoldo/depp) | G2i | Configuration-driven MPI differential evolution, scoped to DE/rand/1 | Maximizes fitness; negate a minimization objective. Coordinator finalizes MPI; external fitness execution and uncapped retries require operational care. |
| [Diver](https://github.com/diveropt/diver) | G2i | Continuous ordinary differential evolution with objective callback | Mean-improvement stopping is offset-dependent and not an error bound. Academic-use license; no returned termination reason. |
| [libga](https://github.com/ramos/libga) | G2i | Real-genotype genetic-algorithm generation update | Caller evaluates initial fitness and drives iterations. Equal fitness gives zero selection sum; compatible genotype sizes required. |
| [OpenFSAM](https://github.com/nfherrin/openfsam) | G2i | Continuous simulated annealing with monotonic linear-additive cooling | Caller owns target-state lifetime. `max_step` is not an objective-evaluation cap; bounds are shared scalar limits. |
| [LCMIN](https://github.com/johngardenghi/lcmin) | G2h2a3 | Smooth minimization with linear equalities, bounds and supplied first/second derivatives | Current module interface differs from old wrapper. External numerical prerequisites, file output and module globals; dual assignments are commented out. |
| [Fast critical-line algorithm](https://github.com/afniedermayer/fast_critical_line_algorithm) | G2e1 | Long-only mean/variance frontier with positive-definite covariance | Not an arbitrary quadratic-programming interface. Degenerate inputs and capacity/error paths need caller care; SIG_TPS is standard deviation. |
| [VTdirect95](https://github.com/vtopt/vtdirect95) | G2i | Serial DIRECT box-constrained global search | Budget checks follow batches; normal stopping statuses are 1-4. Neither stopping nor a finite returned value certifies a global optimum. |
| [gf_int_node](https://github.com/gfell/gf_int_node) | N5b | Ordered interpolation-node searches, with clamped endpoint conventions | Does not evaluate an interpolant. Nonempty sorted queries required for vector path; exact-knot conventions differ between overloads. |
| [ToolboxFortran](https://github.com/aledinola/ToolboxFortran) | E1a; N5b | Piecewise-linear interpolation/extrapolation and ascending-grid binary search | Caller validates distinct ascending coordinates; search sentinels need checking. Legacy PAUSE and attributed-source provenance require care. |
| [fortnum](https://github.com/lazy-fortran/fortnum) | H2c | Gauss-Legendre and Legendre-Lobatto quadrature nodes/weights | Newton/recurrence implementation, not the header's eigenvalue-method wording. Fixed iteration cap without convergence status; no adaptive integrator claimed. |
| [NumericalHUB](https://github.com/jahrWork/NumericalHUB) | E3c | Lagrange cardinal-basis values and derivative recurrence | Preserve result bounds; distinct nodes required. Integral row has a source-selected lower limit; default REAL and conditioning limits apply. |
| [Fortran Numerical Methods](https://github.com/c4rlosr4ul/Fortran-Numerical-Methods) | H2a1a2 | Composite trapezoids and fixed-depth Romberg quadrature of a callback | Trapezoids require ascending limits; N means panels versus levels. No error estimates; the problematic Simpson one-third path is excluded. |
| [FOODIE](https://github.com/Fortran-FOSS-Programmers/FOODIE) | I1a1a | Standard three-stage third-order SSP Runge-Kutta stepping | Concrete integrand bindings and initialization required. Caller selects DT and advances T; NEW_DT is unchanged, not adaptive. |
| [WenOOF](https://github.com/Fortran-FOSS-Programmers/WenOOF) | E1 | Nonlinear Jiang-Shu interpolation from uniform point stencils | Scoped to S=3 standard rank-one interface interpolation. Debug SI is unassigned; rank-two reconstruction belongs to another concrete path. |
| [RALFit](https://github.com/ralna/RALFit) | K1b1a2 | Unconstrained smooth nonlinear least squares with analytic Jacobian | Explicit MODEL=1 overrides hybrid default; mandatory Hessian dummy is suitable only for that selected model. Status/stop flags do not certify global optimality. |
| [NumLib](https://github.com/ebrooker/NumLib) | I1a1a | Classical four-stage RK4, scalar/vector one-step interfaces | Compile parent plus implementation submodule. Caller advances time and chooses H; INOUT H is unchanged, with no adaptive error estimate. |
| [Brito numerical methods](https://github.com/brito-leonardo/numerical_methods) | D2b1b; F1a1 | Dense SPD conjugate gradient and a standalone fixed cubic bisection example | Separate external CG from demonstration MAIN before linking. No CG cap/breakdown check; exact initial residual can divide by zero. Bisection stops on residual alone. |
| [Planelles numerical methods](https://github.com/planelles20/Numerical-Methods-Fortran) | F2 | Newton/Jacobian and vector fixed-point iteration | Step-size stopping is not a residual check. Positive iteration limit required; unpivoted LU has no breakdown status. |
| [Fortran Toolkit](https://github.com/borjapetit/fortran_toolkit) | F1b | General scalar root search using inverse-quadratic/secant trials | Inspect safeguards rather than inferring standard Brent behavior from the name. Oriented sign bracket and status-dependent output handling required. |
| [SPRAL](https://github.com/ralna/spral) | D9a1 | Reverse-communication LSMR linear least squares | Add matrix products into U/V; do not overwrite recurrence terms. ACTION=0 includes failures; inspect INFORM%FLAG and recompute residuals. |
| [scivision L-BFGS-B](https://github.com/scivision/L-BFGS-B) | G2h1a2 | Limited-memory smooth box-constrained optimization with caller gradients | Pin-specific v2.3 workspace. Handle FG/NEW_X/terminal TASK states and distinguish projected-gradient from small objective-reduction stopping. |
| [Bessel-Hankel](https://github.com/TcheL/Bessel-Hankel) | J | Order-zero/one Hankel digital filters | Kernel callback takes a string and abscissa; the integral has d(lambda), without an extra lambda measure. Fixed tables have no error estimate. |
| [rpact.as251](https://github.com/rpact-com/rpact.as251) | L5b1n; C8a | Product-correlation normal rectangular probabilities and AS 66 univariate tails | N<=50 and default REAL/float kernel. Not arbitrary covariance support; inspect IFAULT, and account for hard-coded tail clipping. |
| [EDAT](https://github.com/koseiohara/EDAT) | L1a1a; L1a1b | Pairwise-reduced arithmetic mean and centered population/sample variance | Reduction remains in the selected kind. Empty input returns zero; singleton sample variance returns NaN. Preprocessed rank-one paths only. |
| [lib_probability_distributions](https://github.com/barisbarisgithub/lib_probability_distributions) | L5a1p; L5a1n | Poisson mass/log mass and normal density/log density | C_LONG_DOUBLE is platform-dependent. Check integer errors; Poisson rejects lambda=0, and sigma is a standard deviation. |
| [statislib](https://github.com/Jim-215-Fisher/statislib) | L5a1e | Real exponential PDF/CDF from Fypp templates | Lambda is a rate. Result is default REAL even for DP/QP inputs; invalid domains call error_stop. CDF can lose small-argument precision. |
| [FSML](https://github.com/sebastian-mutz/fsml) | L1a1a; L1b | Arithmetic mean and descriptive Pearson correlation | Wrappers reject size<=1 using printed diagnostics/NaN. Pearson path does not guard zero variance; no significance test is supplied. |
| [Fortran-Code-Snippits](https://github.com/aussie-pete/fortran-code-snippits) | N5c | Ascending-array exact-key binary search | FINDI returns one-based match or -1, not an insertion position. No first/last duplicate or approximate-match guarantee. |
| [fortran-weno](https://github.com/dongli/fortran-weno) | E2a | Tensor-polynomial WENO-Z reconstruction from 2D cell averages | Resolve inversion helper's unassigned success IERR before relying on setup. Uses REAL(16) setup; no positivity or accuracy guarantee. |
| [polynomial_arnoldi](https://github.com/loiseaujc/polynomial_arnoldi) | D2 | Restarted GMRES with reorthogonalized Arnoldi and Givens rotations | Poisson2D-only external operator API; internal tolerance, no returned status. Zero RHS and inner-cycle budget boundaries need care. |
| [tri_indices](https://github.com/yymmt742/tri_indices) | D1b9 | Index mapping for upper-triangle packed matrix storage | Index service only, without copying matrix values. Integer intermediates can overflow; inverse uses default-real SQRT even for INT64. |
| [NSWC](https://github.com/jacobwilliams/nswc) | C4b | Cancellation-aware double-precision exponential-minus-one and log-one-plus transformations | No returned status; logarithm requires finite a > -1. |
| [SLATEC](https://github.com/MehdiChinoune/SLATEC) | C4b; C5 | Single-precision log-one-plus and real Spence dilogarithm branches | ALNREL can ERROR STOP; SPENC returns a real continuation, not a complex branch. |
| [special_functions (ameli)](https://github.com/ameli/special_functions) | C10a4; C10b4 | AMOS J/K sequences for complex argument and nonnegative real orders; distinct scaling and underflow conventions | Split real/imaginary arrays; inspect IERR and NZ and link the AMOS dependencies. |
| [GGQ](https://github.com/JamesCBremerJr/GGQ) | H2c | Generalized Chebyshev rule construction from discretization-weighted basis samples | Requires weighted samples and an initialized discretization; no positive-weight guarantee. |
| [StochOptim](https://github.com/keurfonluu/stochoptim) | G2i | Serial bound-constrained differential evolution, explicitly selecting DE/rand1 | Strictly positive bound widths; biased boundary repair and objective-offset-dependent stopping. |
| [dfsaneacc](https://github.com/cran/dfsaneacc) | D5; D9a1 | Pivoted Householder QR support and its full-column-rank least-squares branch; nonlinear solver remains R code | Requires REXIT hooks; least-squares claim restricted to full column rank. |
| [MINUIT](https://github.com/ramos/minuit) | G1b1a | Unbounded smooth minimization through the derivative-free SIMPLEX command | Shared state and precision-dependent callbacks; covariance status is separate from command status. |
| [Statlib](https://github.com/jacobwilliams/statlib) | L5a2n | AS241 inverse standard-normal distribution functions | Finite 0<P<1; invalid inputs return a zero sentinel with IFAULT. |
| [Numerical_utilities](https://github.com/osada-yum/numerical_utilities) | A3a; L1a1a; L1a1b | Compensated REAL64 summation and univariate Welford mean/variance | Functional accumulator addition needs reassignment; covariance cross-update discrepancy excluded from supported algorithm scope. |
| [Fortran-variable-transformation](https://github.com/tkdhss111/fortran-variable-transformation) | L4a1a5; L6a14 | Yeo-Johnson/Box-Cox transformations and Box-Muller normal generation | Yeo-Johnson likelihood weights log standard deviation incorrectly relative to its Jacobian; RNG lacks zero-uniform guard. |
| [RKAdaptiveMethods](https://github.com/KayeJLLI/RKAdaptiveMethods) | I1a1a | Selected embedded explicit RK single-step routine for autonomous systems | Stage calls reuse t; exact-zero endpoints are rejected by IEEE_IS_NORMAL. Global controls and RHS replacement required. |
| [SESAM](https://github.com/brankart/sesam) | D1b6 | Unweighted and diagonally weighted column Gram products | Weights are squared; no automatic centering or covariance normalization. Preprocessed precision/configuration dependencies. |
| [appell](https://github.com/cran/appell) | C19 | Complex Gauss nonconfluent hypergeometric evaluation | External wrapper, REXIT dependency, no numerical status; real branch-cut arguments shifted below the cut. |
| [fortran-gmm-em](https://github.com/jonas-finkler/fortran-gmm-em) | L4c1a; D5 | Gaussian-mixture EM and modified Gram-Schmidt orthogonalization | EM has no iteration cap/status; Gram-Schmidt has no rank or zero-residual check. |
| [spharm-interp](https://github.com/ahbarnett/spharm-interp) | C9; K6a1 | Normalized associated Legendre functions and spherical-harmonic expansion evaluation | Fortran evaluator scope; scattered-point coefficient fitting is MATLAB. Normalization and lower-triangle storage matter. |
| [EqualSpherePartition](https://github.com/gongzheng-justin/EqualSpherePartition) | P | Unit-sphere representative points from zonal partition construction | Points only, not cell boundaries or a verified area/diameter guarantee; combined source contains a main program. |
| [LEcuyer-RNG-Fortran90](https://github.com/p-serna/lecuyer-rng-fortran90) | L6a21; L6c | Combined multiple-recursive uniform streams and reset/seed services | External procedures are outside the module. Seed validation has boundary/degeneracy omissions; shared initialization/state need care. |
| [M_datapac](https://github.com/urbanjost/M_datapac) | L1a1a; L1a1b | REAL64 mean, median and two-pass sample variance | Median uses 15000-value shared workspace; invalid counts can return undefined outputs without status. |
| [numFort](https://github.com/anthonykalaitzis/numfort) | J1a2; H2a1b2 | Radix-two complex FFT and sampled uniform-grid trapezoidal quadrature | FFT requires power-of-two length. Quadrature reuses one absolute spacing; module has external package dependencies. |
| [Numerical-Methods-in-Fortran](https://github.com/mrtkp9993/numerical-methods-in-fortran) | E1b; C3b | Direct global Lagrange interpolation and ordinary Horner evaluation | Distinct nodes and constant-first coefficients; spline/Broyden placeholders are excluded. |
| [library-of-numerical-analysis-msu](https://github.com/vadimanisaev/library-of-numerical-analysis-msu) | L1a1c | Sample skewness and excess kurtosis using the implemented N/N-1 normalization | Not bias-corrected estimators. Constant data returns zero sentinels for undefined normalized moments. |
| [insitu_array](https://github.com/paulstryck/insitu_array) | D1b3 | In-place storage permutation and pointer remapping for transpose | Associated contiguous target storage required. Allocates an unused full-size flag array; no constant-workspace claim. |
| [MoA-Fortran](https://github.com/wyphan/moa-fortran) | D1a11 | Fypp-generated pointer views for vector take/drop | Target lifetime matters; nonpositive drop has an off-by-one discrepancy, avoided by the sketch. |
| [pseudo_rng_modules](https://github.com/pointedsphere/pseudo_rng_modules) | L6a21; B | Selected LFSR258 uniforms and Euclidean GCD utility | Shared 64-bit RNG state; endpoints not certified. GCD requires positive ascending inputs and otherwise can STOP. |
| [Fortran_rationals](https://github.com/willklausler/fortran_rationals) | A2; A6a; B | Reduced finite-width rational arithmetic, continued-fraction conversion and integer GCF/LCM | Exact arithmetic is INT64-bounded; conversion may use a last-fitting convergent. Most-negative INT64 excluded from direct GCF/LCM usage. |
| [HDMod](https://github.com/atmmod/hdmod) | H1 | Selected scalar hyper-dual chain rules for exponential/sine and first/mixed second derivatives | Seed convention matters. No whole-overload, Hessian-driver or numerical derivative validation. |
| [compare](https://github.com/tcanich/compare) | A3a | Absolute-tolerance real/complex equality | REAL64 overload uses default-REAL tolerance; array equality reduces to one logical and is false for empty arrays. |
| [fortran-approx](https://github.com/suzuyuyuyu/fortran-approx) | A3a | Elemental absolute and absolute-plus-relative comparisons | Arrays produce masks; explicit tolerances match input kind. Nonfinite semantics and overflow are not specially handled. |
| [em-fortranbox](https://github.com/elmarmertens/em-fortranbox) | L5a1n | Scalar normal density and normal log density | sigma2 is variance. Whole-module Intel VSL/OpenMP and numerical dependencies remain; multivariate path excluded. |
| [ecgmm_fortran](https://github.com/minzastro/ecgmm_fortran) | L4a1a; L5a1n | Fixed-count error-corrected scalar Gaussian-mixture updates and normal-density helper | No convergence status. Responsibility underflow/empty-component behavior needs care; f2py and explicit Fortran calls differ. |
| [twdtw](https://github.com/vwmaus/twdtw) | L10d | Multichannel dynamic-time-warping costs with logistic cyclic-time penalty | Legacy sketch initializes boundaries and restricts M<=N for JB capacity. Callback entry has a separate boundary-intent discrepancy. |
| [timeseries](https://github.com/rhandberg/timeseries) | L10a3a2; L1a1a | Weighted sine/cosine least-squares periodogram path and weighted mean | Seconds versus microhertz and global sumWeights matter. No fitted intercept, singular-design guard or automatic significance test. |
| [ODEPACK modernization](https://github.com/jacobwilliams/odepack) | I1a1b; I1a2 | Selected Adams functional-iteration and stiff BDF finite-difference-Jacobian DLSODE modes | Array NEQ/RTOL/ATOL interface, continuation state/workspace and callback requirements; no complete kernel or accuracy audit. |
| [NUFFT](https://github.com/biotrump/nufft) | J1a2 | Nonuniform-to-uniform complex type-1 Gaussian-gridding transform | Centered modes, positive-exponent IFLAG>=0 convention and 1/NJ scaling; precision request is not a verified accuracy bound. |
| [QD](https://github.com/BL-highprecision/qd) | A3c | Selected double-double decimal input and addition through Fortran/C++ layers | Fixed two-double representation, 80-character input buffer, build-dependent addition branch and external ABI requirements. |
| [MPFUN2020](https://github.com/jacobwilliams/mpfun2020) | A3c; C4b | Variant-1 multiword real construction/addition and exponential | Working precision is in words within a compiled digit capacity; initialize support and use consistently built variants/constants. |
| [FMPFR](https://github.com/tkoenig1/fmpfr) | A3c | Selected allocated-object MPFR decimal construction and addition | Precision is in bits; initialize rounding explicitly. Existing result precision can persist; unallocated-component wrappers excluded. |
| [ga_lib](https://github.com/dacarnazzola/ga_lib) | G2i | Tournament parent selection and target-value evolutionary benchmark coordinator | Solver prints diagnostics rather than returning best point/status. Heterogeneous-bound initialization and concurrency semantics need follow-up. |
| [GARCH](https://github.com/Beliavsky/garch) | L6a20; L10a2 | Gaussian GARCH(1,1) generation and observed-data conditional-volatility filtering | Both return standard deviations; initialization differs. Admissible parameters, nonempty inputs and cached RNG state matter. |
| [EnKF_analysis](https://github.com/geirev/EnKF_analysis) | L10a2e; L1a1b | Selected scalar-observation ensemble Kalman update and per-state sample variance | Match real-8 caller/library/BLAS conventions. Analysis is not a full forecast/localization workflow; variance requires a supplied mean. |
| [HiPPIS](https://github.com/ouermijudicael/HiPPIS) | E1b; E1a; E2a | Newton coefficients/evaluation, adaptive pieces and 2D tensor dispatch | Ascending distinct grids, minimum sizes and in-range queries required; preservation not validated. |
| [acepack](https://github.com/vubiostat/acepack) | L8h | Weighted running-linear smoother dispatch and implementation | Periodic and terminal-tie indexing concerns; sketch selects strict increasing nonperiodic fixed-span data. |
| [SIGNAL](https://github.com/i-a-morozov/SIGNAL) | L10a1d | Cosine-power taper generation and interleaved-complex taper application | Build parent/submodules consistently; no spectrum/leakage validation or all-dependency audit. |
| [leaps](https://github.com/cran/leaps) | L8c1b1 | Raw-row orthogonal reduction and coefficient recovery | Not a full subset-search audit; design rows overwritten and rank/tolerance choices matter. |
| [mix](https://github.com/cran/mix) | L1a1 | Observed-column means, divisor-N scales and in-place standardization | Exact missing sentinel; all-missing means undefined; cancellation possible. |
| [tweedie](https://github.com/PeterKDunn/tweedie) | H2a2 | Fixed/adaptive finite quadrature for built-in inversion integrands | Requires initialized distribution globals; not a user-callback integrator or complete density audit. |
| [spam](https://github.com/cran/spam) | L1a1a; D1b9 | Sparse-row arithmetic means and CSR-to-MSR conversion | Initialize output means; validate pointers and unique diagonals; mixed component terms. |
| [MCMC F90](https://github.com/mjlaine/mcmcf90) | L6a14; L6a7 | Polar normal and Marsaglia-Tsang gamma variates | Gamma B is scale; cached normal state complicates reseeding/concurrency; no statistical test. |
| [DFL](https://github.com/DerivativeFreeLibrary/DFL) | G2c7; G2h1b | Mixed-integer and all-continuous bounded coordinate line-search paths | Separate main from solver for reuse; linked FUNCT objective; initialized counters; budgets can be exceeded. |
| [BGW](https://github.com/cran/bgw) | G1b1b | Reverse-communication first-derivative negative-log-probability minimization | This revision links a specific RHO objective; VALUE lengths require an explicit BIND(C) interface. |
| [mknapsack](https://github.com/jmyrberg/mknapsack) | G2c3; G2c2 | Binary knapsack branch-and-bound and bin-packing driver | Sorted admissible inputs, sentinel/work arrays and integer range matter; finite packing budget can be heuristic. |
| [gausscov](https://github.com/cran/gausscov) | L8c1a1; L8c1b1 | Gaussian-covariate forward selection and full-rank QR coefficients | Degenerate candidate/probability branches need checks; inverse path disabled by RSOLV early RETURN. |
| [mclust](https://github.com/cran/mclust) | L14a1b; L5b1n | Common-variance univariate Gaussian-mixture EM and multivariate Gaussian log density | Fixed component count/local likelihood; check sentinels; covariance overwritten; HOOD unchanged on success. |
| [TREAT](https://github.com/plopezrios/treat) | L4a1a6 | CLI tail-regression analysis and bootstrap/analytic-tail-moment dispatch | Internal routines are not public APIs; known-tail/model assumptions, independence, MPI and LAPACK required. |
| [GPKDE](https://github.com/upc-ghs/gpkde) | L4c1b | Grid-projected multivariate Gaussian-kernel density reconstruction | Initialized grids and shared module state; option-dependent scaling; not a normalization or boundary audit. |
| [qap](https://github.com/mhahsler/qap) | G2b | Simulated-annealing permutation assignment heuristic | Symmetric matrices required by swap delta; R RNG/interrupt runtime; no optimality guarantee. |
| [KernelyzeBase](https://github.com/kernelyze/kernelyze-base) | K4; F1b | Nystrom kernel approximation and explicit-status Brent root search | Strictly positive quadrature weights/nonzero retained singular values; concrete pure function/kernel objects required. |
| [ttcross](https://github.com/savostyanov/ttcross) | K4 | MPI adaptive tensor-train cross interpolation | Callback and process partition must match; sampled-pivot stopping is not a global residual certificate. |
| [GADfit](https://github.com/raullaasner/gadfit) | K1b1a1; H1 | AD-based Levenberg-Marquardt fitting and forward directional product derivatives | Global fitting means shared dataset parameters; active INDEX seeds and mode state matter; optional-argument guards need review. |
| [Random Fields Generation Library](https://github.com/cottereau/randomField) | L6b14 | Gaussian-intended finite spectral random-field synthesis | Repeated spectral square roots, double XRANGE restoration and possible zero slab size require fixes and validation. |
| [libslam](https://github.com/Space-Systems/libslam) | E1b; E1c | Global Lagrange polynomial and sine-product trigonometric interpolation | Distinct nodes required; select odd N for periodic trigonometric interpretation; shared error state can leave output unassigned. |
| [Spectrum-Revealing CUR](https://github.com/Rioghasarig/sr-cur) | D5 | Fortran blocked column-pivoted QR component | Not the whole MATLAB CUR workflow; enforce LDA independently of defective guard; current driver fixes one thread. |
| [TT Fortran core](https://github.com/oseledets/tt-fort) | K4; D1a4 | Dense tensor-to-TT SVD approximation and real core contractions | Explicit pointer-core cleanup; rank cap can override accuracy request; DOT returns a rank-one array. |
| [KronLinInv](https://github.com/inverseproblem/KronLinInv) | L4c1a | Separable linear-Gaussian posterior factorization and mean contractions | Repair progress-report zero divisors; consistent covariance factors, OpenMP runtime and tensor ordering required. |
| [diaglib](https://github.com/molecolab-pisa/diaglib) | D4a1; D4b1 | Few lowest ordinary and generalized real symmetric eigenpairs | Metric must be SPD; convergence OK and API INFO are separate outputs. |
| [Exponential sum approximations](https://github.com/alexey-kuznetsov-math/exponential_sum_approximations) | K4 | Supplied Gaussian exponential-sum approximation program | Program and internal helpers, not a general library API; MPFUN and build-target selection required. |
| [pypolsys](https://github.com/nennigb/pypolsys) | F2 | Polynomial-system homotopy continuation | Pass optional DENSE explicitly to avoid the inspected absent-dummy write; fixed N<=30 wrapper workspace. |
| [monolis](https://github.com/nqomorita/monolis) | D2b4; D2a4 | Real sparse CPU conjugate gradients and BiCGSTAB | Assembled matrix, communicator and preconditioner required; inspect status and independently check residuals. |
| [Nonlinear Optimization Algorithms Multilang](https://github.com/rgolubtsov/nonlinear-optimization-algorithms-multilang) | G1b2 | Derivative-free Hooke-Jeeves coordinate/pattern search | External objective and shared evaluation counter; separate supplied main; returned count is not a convergence flag. |
| [PRIMA](https://github.com/libprima/prima) | G2h1a1; G2h2a1; G2h3b1a | Derivative-free bound, linear and nonlinear-inequality constrained trust-region optimization | Modern nonlinear constraint sign is <=0; callback kinds/counts and termination reasons need interpretation. |
| [PyDQED](https://github.com/reactionmechanismgenerator/pydqed) | K1b2a | Bounded nonlinear least squares with linear constraints | Caller workspace and Jacobian/value callback required; saved state is not reentrant. |
| [pyoptgra](https://github.com/esa/pyoptgra) | G2h3b1b | Gradient-based constrained optimization | Initialize/configure shared state; CALVAL has a third status argument and derivative mode has two controls. |
| [MPFUN90](https://github.com/apn-pucky/mpfun90) | A3c; C4b | Multiword real addition and extended-precision real exponential | Initialize precision/constants; fixed capacity and shared error state; avoid default-kind promotion. |
| [Get Moments reconstruction](https://github.com/danieljprice/get_moments) | H2a1b2; F2 | Sampled-array trapezoidal quadrature and local square nonlinear-system solver | Callback quadrature has an indexing discrepancy; reconstruction uses fractional moments and consistent real-kind flags. |
| [M_random](https://github.com/urbanjost/m_random) | L6a21; L6a16; L6c | MT uniform variates, state initialization and random permutations | Explicit MT state differs from intrinsic RNG state; SCRAMBLE is not a uniform Fisher-Yates shuffle. |
| [SLICE sampler](https://github.com/ericlindsey/slice) | L6b | Bounded coordinate slice sampling | Linked negative-log-density model and initialized shared state; correlated samples and default-real output rounding. |
| [ScipyDIRECT](https://github.com/andim/scipydirect) | G2i | DIRECT box partitioning for derivative-free global search | Finite budget is not a global certificate; callback feasibility flags and fixed workspace capacities matter. |
| [Contour 531](https://github.com/lguez/contour_531) | Q | Regular-grid scalar isolines as polylines | Saved scratch state, unspecified orientation and default-real coordinates; geometry needs a separate renderer. |
| [PFAPACK Rust bindings](https://github.com/duumbo/pfapack-sys-rs) | D2a1 | Pivoted real skew-symmetric congruence reduction and Pfaffian consumer | D2a1 covers only the related factorization subset; preserve input, query workspace and link numerical dependencies. |
| [Golden-section callback experiment](https://github.com/huijunchen9260/gssfortran) | G1a1a | Derivative-free scalar golden-section search | Defaults to maximization; callback includes optional polymorphic data; no separate convergence status. |
| [EnsDAM](https://github.com/brankart/ensdam) | L1a1a; L1a1b; L1c1b; E1a | Means, sample dispersion, incremental covariance and local linear interpolation | Initialize covariance states explicitly; wrapper MEANREF is uninitialized; distinguish weights, values and variance normalizations. |
| [CohensdpLibrary](https://github.com/dcousin3/cohensdplibrary) | C11; L5a1b | Positive-real 0F1 limit series and beta-distribution CDF | 0F1 has no convergence status; beta wrapper merges errors and does not propagate every internal approximation status. |
| [IEEE classification helpers](https://github.com/dscf-1224/ieee_class_fortran) | R2 | IEEE class predicates and quiet-NaN setter | Compiler kind/IEEE support required; no trap or signaling-NaN portability guarantee. |
| [libsupermesh](https://github.com/firedrakeproject/libsupermesh) | P | Planar triangle intersection via half-plane clipping | Saved scratch requires serialization; use configured real kind; near-degenerate topology is unverified. |
| [polyhomocont](https://github.com/evadevacstab/polyhomocont) | F2 | Polynomial-system total-degree homotopy continuation | Inspect failed paths/endgame statuses and residuals separately from driver setup status; counts are not certificates. |
| [L-BFGS-B-NS](https://github.com/wilmerhenao/l-bfgs-b-ns) | G2h1a2 | Reverse-communication bounded limited-memory quasi-Newton optimization | Fork-specific work/state sizes; standard PGTOL/FACTR exits disabled; caller stopping logic required. |
| [copa](https://github.com/thomasbiekoetter/copa) | L6b | Serial ensemble stretch-move sampling | At least two walkers and ten steps; validate ranges shape, prior support and external RNG setup. |
| [MSOLV](https://github.com/tribo-pprime/msolv) | D2a4 | Real sparse direct-solver lifecycle dispatch | Backend formats/ownership and external libraries required; STOP errors, MPI ownership and cleanup allocations need review. |
| [EigenExa](https://github.com/riken-rccs/eigenexa) | D4a1; D4a3; D4b1 | Distributed real/complex Hermitian ordinary and real symmetric generalized eigenproblems | MPI/local storage setup; no public INFO; values-only cleanup and invalid-metric collective paths require review. |
| [CUTEst](https://github.com/ralna/cutest) | R | SIF problem objective/gradient evaluation service | Decode/setup and compiled problem routines required; evaluation is not optimization. |
| [LHS](https://github.com/nrel/lhs) | L6b5 | Supplied Latin-hypercube sampling design program | Program/configuration-file interface; shared modules and outputs; rank matching is not correlation certification. |
| [EMSOL](https://github.com/ergo-code/emsol) | G2a2 | Sparse bounded LP revised-simplex dispatch | Legacy equivalenced workspace/setup and separate LP status; supplied import supports EMS format. |
| [KFAS](https://github.com/helske/kfas) | L10a2e | Sequential Gaussian state-space Kalman filtering | Scalar sketch; predicted versus smoothed states, correlated observation transformations and diffuse rank matter. |
| [dae4py](https://github.com/jonasbreuling/dae4py) | I1a2 | Vendored implicit DASKR BDF integration | Residual includes CJ; consistent initial conditions, option-specific workspaces and IDID recovery are required. |
| [faiNumber Fortran](https://github.com/kevinhng86/fainumber-fortran) | A6b; R2 | Decimal parsing, binary formatting and numeric-string syntax validation | ASCII/32-bit assumptions; syntax validity does not imply representable range; inspect conversion error flags. |
| [Matran](https://github.com/beliavsky/matran) | D6; D5 | Real matrix-type SVD and QR interfaces | SVD padding/success-INFO/query-cleanup findings; QR sliced-array BLAS contracts and pointer lifecycle need validation. |
| [cdaSQR / SQR](https://github.com/karimoualkacha/cdasqr) | L8c | Smoothed penalized multiple-linear quantile regression | Median sketch; mutable predictors, compressed active coefficients and initialized JERR required. |
| [FEconv](https://github.com/victorsndvg/feconv) | D2e | Reverse Cuthill-McKee graph/matrix reordering | Private graph kernel; public mesh wrapper needs coordinate INTENT/permutation repairs before use. |
| [PSFUN](https://github.com/cirdans-home/psfun) | D | Sparse Krylov matrix-function actions | PSBLAS setup; zero-norm/happy-breakdown guards and projected dimensions need validation. |
| [Zolo SVD](https://github.com/shengguolsg/zolo-svd) | D; D4a1 | Distributed polar decomposition and partial symmetric eigensolving | Inspected ZOLOPD is QDWH; prototype eigensolver omits selected-rank output. |
| [NScluster](https://github.com/cran/nscluster) | L6b | Thomas clustered spatial point-pattern sampling | Periodic rectangle; mutable density, global RNG and finite parent/offspring capacities. |
| [TikTak](https://github.com/serdarozkan/tiktak) | G2i | Configuration-driven heuristic multistart global search | Program interface; objective/configuration adaptation and isolated filesystem state required. |
| [SLATEC Modern](https://github.com/zaneham/slatec) | C8c; C7b; C7e; C7f | Dawson, complete beta and incomplete gamma/beta functions | Modern module includes; normalized versus unnormalized definitions, domain termination and intermediate overflow matter. |
| [BiCGSTAB and GMRES solver examples](https://github.com/jnsresearcher/solvers_bcgstab_gmres) | D2a4 | CSR BiCGSTAB and unrestarted GMRES | Breakdown guards and exhausted-iteration slices need correction; ITER is not a success certificate. |
| [hyperBOB](https://github.com/maxentropyprod/hyperbob) | G2i | MPI Latin-hypercube multistart BOBYQA | Collective initialization and callback shape; MAXTIME is not implemented and ERR is not convergence. |
| [sht_py](https://github.com/hottahd/sht_py) | C9; J | Normalized Legendre polynomial evaluation and associated transforms | Explicit C interfaces; separate duplicate binding names and sufficient local latitude points. |
| [PDECHEB](https://github.com/ivan-pi/pdecheb) | I2a1a | One-dimensional parabolic PDE Chebyshev semidiscretization | Problem callbacks, workspace and saved COMMON required; time integration is delegated to DASSL. |
| [urca](https://github.com/cran/urca) | L5a1n; L5a2n | Normal CDF and inverse-CDF approximation routines | Tail clipping/cancellation, unsafe quantile endpoints and R error-support linkage. |
| [LinAlgf90](https://github.com/takayuki-miyagi/linalgf90) | D6; D4b1 | Thin real SVD and generalized symmetric eigensolver wrappers | V stores V-transpose; LAPACK INFO is hidden and generalized input preservation needs repair. |
| [FortLearner](https://github.com/naomatch/fortlearner) | L14a1b | Dense nonhierarchical K-means clustering | Integer constructor kinds, mutable global threading/RNG and iteration-state contracts need attention. |
| [KohonenF03](https://github.com/khaors/kohonenf03) | L14a1b | Nonhierarchical self-organizing-map clustering | Fixed seed/Euclidean wrapper; scaled data, grid selectors and array dimensions matter. |
| [NN_MOD regressors](https://github.com/thchang/nn_mod) | H1; G1b1b | Scalar-network backpropagation and gradient-supplied Adam minimization | Loss callback returns a derivative; gradient buffers overwrite parameters and success-status assignments need repair. |
| [Fortran FilterSLP](https://github.com/ergo-code/fortranfilterslp) | G2h3b | Legacy filter sequential linear nonlinear programming | Repository model state, EMSOL and packed workspace; local method with two-sided constraints. |
| [BMSL](https://github.com/benrenard/bmsl) | L4a1b2; L13b | Kernel density estimation and principal component analysis | DMSL dependency; mutable centered/scaled data and differing branch normalizations. |
| [ASURV](https://github.com/rsnemmen/asurv) | L15 | Product-limit survival curve and mean/error calculations | Mutable censoring-tail convention; all-censored, tied and small samples require boundary review. |
| [Visual Fortran Solvers](https://github.com/niceno/visual-fortran-solvers) | D2b1b; D2b4 | Dense SPD Cholesky and sparse symmetric CG demonstrations | Plotting/grid state; no controlled breakdown status; CG constructs and deallocates its system. |
| [HPCSeriesCore](https://github.com/hpcseries/hpcseriescore) | L4a1b1; L10a1c4 | Median/MAD/quantile summaries and nonlinear rolling-median filtering | SAFE propagates NaN with success; trailing-window leading values are missing; explicit C value arguments. |
| [Fortran shape functions](https://github.com/willklausler/fortran_shapefuncs) | E1b; H1 | Finite-line polynomial interpolation and analytic shape derivatives | Reference coordinates and node ordering; cubature dependency and physical derivative transformations. |
| [Neural-network tangent and adjoint tests](https://github.com/samhatfield/nn_tl_ad) | H1 | Fixed-network input tangent-linear and adjoint operators | Global weights/batch biases and BLAS kinds; derivatives concern inputs rather than training parameters. |
| [Fortran Neural Network library](https://github.com/cerea-daml/fnn) | H1 | Sequential-network state/parameter tangent and adjoint operators | Stored per-member forward trajectory and parameter packing; adjoint may overwrite output seeds. |
| [PolyChordLite](https://github.com/polychord/polychordlite) | L | Bayesian nested sampling and likelihood-constrained slice replacement | Likelihood/prior/dumper callback contracts; estimated stopping, outputs and noncommercial license. |
| [Stripy](https://github.com/underworldcode/stripy) | P; E2b | Planar Delaunay triangulation and scattered linear interpolation | Use matching included fixed-form REAL variants; distinguish interpolation/constraint/exterior results. |
| [JKogb](https://github.com/venovako/jkogb) | D | Two-by-two real signature-metric singular-value transformations | Overwritten matrix; signature validation, positive status bits and exceptional off-diagonals. |
| [FORCES](https://github.com/mhm-ufz/forces) | L1a1a; L1a1b; L1b | Masked mean, sample variance and bivariate covariance | Empty selections, n versus n-1 normalization and inconsistent license notices are explicit. |
| [TSSS](https://github.com/cran/tsss) | L10a2a1; L10b2a | Univariate and two-channel lagged covariance/correlation summaries | Exclusive observation bounds, total-count normalization and unguarded empty/constant selections. |
| [Spaloess](https://github.com/xiaosutong/spaloess) | K5 | Direct local polynomial smoothing | Versioned packed workspace, explicit Euclidean distance selector and C/R numerical diagnostics. |
| [Clustering via Nonsmooth Optimization](https://github.com/snta2019/clustering-via-nonsmooth-optimization) | L14a1b | DC-Clust minimum-sum-of-squares nonhierarchical clustering | Shared data/control modules and packed centers; selected DCDB-directory academic terms. |
| [forApollo](https://github.com/forkernels/forapollo) | L10a2e | Linear Kalman prediction and gated Joseph-form updates | Flat row-major C boundary, output gating flags, helper aliasing and proprietary designation. |
| [MultiNest](https://github.com/rjw57/multinest) | L | Bayesian nested sampling with likelihood and dumper callbacks | Pinned older v2.17 interface, normalized priors, pointer arguments and estimated stopping. |
| [FFT overlap experiments](https://github.com/dappelha/fft-overlap) | J1b | GPU plane-wise complex two-dimensional FFT round trip | CUDA Fortran dependency, unnormalized output, unchecked statuses/cleanup and unfinished 3D path. |
| [M_blas](https://github.com/urbanjost/m_blas) | D1b6; D2a3 | Dense matrix multiplication and real triangular substitution | Public module routines; configurable error handler, no singularity/condition estimate. |
| [Sherman Morrison update interfaces](https://github.com/trex-coe/sherman-morrison) | D2e | Additive column updates of a dense inverse | C pointer ABI and missing Fortran scalar are explicit; naive denominator threshold does not protect division. |
| [Sparse Fortran examples](https://github.com/scivision/sparse-fortran) | D2a4 | MPI/MUMPS sparse unsymmetric linear-system driver | Program-scoped helpers, external implementation and no residual validation. |
| [Sparse Iterative Parallel Linear Solver](https://github.com/tueboesen/sparse-iterative-parallel-linear-solver) | D2b4 | Real sparse preconditioned conjugate-gradient solve | CSR/OpenMP setup, optional-argument defects and public convergence-status limitations. |
| [npregfast](https://github.com/sestelo/npregfast) | K5; L8c1b1 | Local polynomial smoothing and sequential multiple-linear coefficient estimation | Bandwidth/packed coefficient semantics, overwritten rows and shared LSQ state. |
| [rrelaxiv](https://github.com/josherrickson/rrelaxiv) | G2d | Integer capacitated minimum-cost network flow | Supply sign conversion, destructive residual arrays, integer ranges and early-return flag caveat. |
| [BFpack](https://github.com/jomulder/bfpack) | L6b3 | Joe random correlation-matrix generation | R-hosted RNG lifecycle, row-wise triangle packing and unchecked internal inversion status. |
| [BVARmml](https://github.com/dingshutong/bvarmml) | L10c | Recursive multivariate autoregression forecasts | Lag/coefficient layout, deterministic versus innovation forecasts and Intel/IMSL requirements. |
| [Singular surface operators](https://github.com/jamescbremerjr/surfaces) | H2b2a1 | Adaptive complex-valued integration over a planar triangle | Local tolerance test, inconsistent node count, stack/depth status and embedded debugging main. |
| [Fitter MC](https://github.com/ndd21/fitter_mc) | L8e1b3 | Weighted derivative-free nonlinear fits with parametric Monte Carlo uncertainty | File-driven model-specific workflow, fixed replication count and unchecked fit status. |
| [FC Tables](https://github.com/mfontanaar/fctables) | D5; D6 | Arbitrary-precision QR and one-sided Jacobi SVD support | Classical Gram-Schmidt rank limits, even-column sweeps, unsorted singular values and progress-print defect. |
| [PaScaL TDMA](https://github.com/mpmc-lab/pascal_tdma) | D2a2a | Batched real tridiagonal systems on GPU/MPI | Destructive device arrays, reusable plans, CUDA-aware MPI and no pivot/status guarantee. |
| [OptimusPrime](https://github.com/rwatson54/optimusprime) | G2i | Bounded simulated annealing with a scalar objective callback | Clock reseeding, positive print interval, temperature degeneracy and heuristic termination. |
| [PDFO](https://github.com/pdfo/pdfo) | G2h1a1; G2h3b1a | Bounded quadratic-model and nonlinear inequality-constrained derivative-free optimization | Modified BOBYQA/COBYLA signatures, named callbacks, mutable controls and explicit termination/feasibility results. |
| [S2HAT](https://github.com/b3dcmb/s2hat) | J | Distributed scalar spherical-harmonic synthesis | Pointer layouts, MPI ownership/rings, selected FFT backend and scalar-only calling scope. |
| [ODEPACK redistribution](https://github.com/cfinch/odepack) | I1a1b; I1a2 | Variable-order Adams and stiff BDF ODE initial-value integration | Method-specific workspaces/Jacobians, local error control and preserved continuation state. |
| [GPROPT](https://github.com/iarlopes/gpropt) | G1a1a | Derivative-free one-dimensional golden-section minimization | Named external objective, fixed interval contraction and required unit-11 output setup. |
| [HSSPACK](https://github.com/shengguolsg/hsspack) | D2b1b; D1b6 | Hierarchical SPD approximate solve and compressed matrix product | Compression controls, nonpropagated status, panel remainder defect and reversed timing. |
| [libdlfind](https://github.com/digital-chemistry-laboratory/libdlfind) | G1b1b | Limited-memory BFGS direction generation from supplied gradients | External procedure/shared history, caller-side convergence/step control and curvature guards. |
| [FM Algorithm 814 archive](https://github.com/toms-algo/814-fm-2001) | C7a; C7b | Real multiprecision complete gamma and beta functions | Historical FM modules, decimal-string inputs, shared precision/cache state and explicit scope. |
| [Induced Smoothed Lasso](https://github.com/cran/islasso) | L8c | Induced-smoothed penalized Gaussian multiple-linear regression | R-hosted numerical helpers, input/output work arrays and masked factorization status. |
| [tfQMRgpu](https://github.com/real-space/tfqmrgpu) | D2c4 | Complex block-sparse transpose-free QMR solves on GPU | Public square-block convenience API, compiled block support, prescribed X sparsity and residual/status caveats. |
| [AMG4PSBLAS](https://github.com/sfilippone/amg4psblas) | D2e | Distributed algebraic multilevel preconditioner construction | PSBLAS/MPI setup, public type-bound build, hierarchy/smoother dispatch and explicit distinction from a solve. |
| [BDDCML](https://github.com/sistek/bddcml) | D2b4; D2a4 | BDDC-preconditioned conjugate-gradient and BiCGStab linear solves | Method/matrix type, iterative versus direct-only configuration, collective setup and downloaded solution state. |
| [GALAHAD](https://github.com/ralna/galahad) | G2e1; G2e2 | Convex equality-constrained and indefinite inequality-constrained quadratic programs | Precision facade, sparse layouts, EQP constraint sign, solver lifecycle and local versus global claims. |
| [BayesFM](https://github.com/cran/bayesfm) | L13a | Conditional Gaussian factor-score update | One Bayesian factor-analysis component, initialized covariance, custom RNG and R-hosted numerical helpers. |
| [Robust Library for R](https://github.com/valentint/robust) | L8c4 | Fixed-scale Huber W-iteration for robust multiple-linear regression | Concrete psi selector, QR updates, packed convergence metric and no general success return. |
| [rrcov](https://github.com/valentint/rrcov) | L4c1b | Projection-based robust multivariate location/scatter | Nonparametric scope, bounded random versus exhaustive subsets, squared-weight scatter and degenerate-weight checks. |
| [SmoothHazard](https://github.com/tagteam/smoothhazard) | L15 | Censored Weibull proportional-hazards fitting | R-hosted saved state, optimizer success code one, inverse-scale convention and optional confidence bands. |
| [Robust Gauss Newton](https://github.com/eachonly/robust-gauss-newton-algorithm) | K1b2 | Bounded nonlinear least squares | Consistent residual/objective callback, module kinds, finite-difference bounds and stopping-code interpretation. |
| [Fortress](https://github.com/eph/fortress) | L10a2e | Linear Gaussian state-space likelihood by Kalman filtering | Stationary non-SLICOT covariance initialization, likelihood-only output and unpropagated numerical statuses. |
| [Timeslab](https://github.com/beliavsky/timeslab) | L10a2a1; L10a2a2 | Theoretical AR autocovariances and model-implied partial autocorrelations | Default-real legacy kernels, overwritten coefficients, stationarity checks and caller-established sign convention. |
| [Parallel Structured Matrix Multiplication research code](https://github.com/shengguolsg/psmma_git) | D1b6 | Distributed dense-by-Toeplitz matrix multiplication | Replicated full generators, restricted block-cyclic layouts, RRQR compression and no public error/tolerance query. |
| [PSBLAS](https://github.com/sfilippone/psblas3) | D2b4 | Distributed preconditioned conjugate-gradient sparse solves | Explicit CG dispatch, SPD assumptions, PSBLAS vector layouts, collective setup and residual validation. |
| [PyGSLIB](https://github.com/opengeostat/pygslib) | L4c | Directional spatial lag-covariance analysis | Pair-count masking, flattened lag layout, broad spatial-statistics mapping and cloud-output limitations. |
| [Implicit QR demonstration](https://github.com/keksipurkki/keksipurkki-demos-qr) | D4a2; D4c1b2 | Real nonsymmetric eigenvalues and Householder Hessenberg reduction | Complex-output overload, callback failures, experimental QR limitations and no accumulated similarity matrix. |
| [Inference for physical sciences](https://github.com/tloredo/inference) | H2b1a1; H1 | Adaptive vector cubature and mode-specific information matrices | Hyperrectangular callback/workspace controls, numerical error estimates and positive-curvature mode assumptions. |
| [glmnet MATLAB builds](https://github.com/lachioma/glmnet_matlab) | L8c; L8 | Gaussian and binomial elastic-net regression paths | Default-real ABI, compressed coefficients, mutable inputs, weighted response rows and partial-path statuses. |
| [PDAF](https://github.com/pdaf/pdaf) | L10c | Ensemble-transform Kalman multivariate state-space assimilation | Public callback scheduling, reviewed SUBTYPE=1 algebra, MPI/precision consistency and analysis-step status interpretation. |
| [TISEAN](https://github.com/gazeek/tisean) | L10a2a1; L10a3a2 | FFT autocorrelation and Fourier periodogram command-line programs | Supplied executable entries, centering/periodicity conventions, fixed transform arrays and no callable module claim. |
| [SpLLT](https://github.com/nlafet/spllt) | D2b4 | Task-based sparse real-SPD Cholesky factorization and solves | Analysis/factor/solve phases, actual solve-job semantics, task completion and local-factorization status limitations. |
| [Minimum Split Checkerboard Decomposition](https://github.com/captainsifff/mscbdecomp) | D1b6 | Checkerboard exponential splitting applied to dense matrices | Hermitian graph conversion, edge coloring, paired matrix-action stages, supported methods and approximation scope. |
| [SparseReg MATLAB toolbox](https://github.com/hua-zhou/sparsereg) | L8c | Weighted penalized linear-regression coordinate descent | Native Fortran module, ENET parameter convention, precomputed curvatures and absent convergence/status output. |
| [Higher Order Markov Fortran](https://github.com/barisbarisgithub/markov_fortran-) | M; L10a2 | Finite-state probability propagation and categorical history-transition estimation | Row-stochastic orientation, uniform unseen-history fallback, exponential table size and distinction from greedy trajectories. |
| [Computational Economics Fortran examples](https://github.com/fabiankindermann/ce-fortran) | F1b; E1b; H2c | Scalar secant roots, global polynomial interpolation and Gauss-Legendre nodes/weights | Public overloads, duplicate-node/domain limits, quadrature service scope and retained Numerical Recipes provenance. |
| [KohonenF08](https://github.com/khaors/kohonenf08) | L14a1b | Online fixed-grid self-organizing-map prototype clustering | Initialized pattern/parameter objects, serial best-match restriction, neighborhood updates and output configuration. |
| [PDHGEQZ](https://github.com/nlafet/gevp-pdhgeqz) | D4b2; D4c1b2 | Distributed real generalized QZ and Hessenberg-triangular reduction | Prepared pencil forms, homogeneous eigenvalues, collective workspace queries and unassigned query status. |
| [JACSD](https://github.com/venovako/jacsd) | D6 | One-sided Jacobi SVD core | Aligned SIMD storage, integer ABI, prepared workspaces, packed counters and absent final normalization. |
| [tidybench](https://github.com/sweichwald/tidybench) | L10c | Selective multivariate autoregressive structure and lag estimation | Absolute coefficient scores, selected-edge lag semantics and unresolved QR-workspace validity. |
| [FAS](https://github.com/jstriaukas/fas) | L8c | Lasso bootstrap effective-noise quantiles and tuning | Supplied multipliers, initialized accumulated status, partial paths and threshold-crossing sentinel. |
| [midasmlpy](https://github.com/jstriaukas/midasmlpy) | L8c | Dense sparse-group-lasso regression path | Group metadata, undefined success status and inactive coefficient outputs require implementation repair. |
| [PDHSEQR Algorithm 953](https://github.com/nlafet/sevp-pdhseqr-alg953) | D4c2b; D4c1a | Distributed Hessenberg QR/Schur computation and matrix balancing | Schur factors versus eigenvectors, replicated spectra, permutation/scaling data and distributed storage. |
| [quantregpy](https://github.com/quantregpy/quantregpy) | L8c3 | Median/L1 multiple regression through quantile regression | Transposed design, coefficient signs, mutable workspaces and iteration-limit/status interpretation. |
| [Fortran time-series translations](https://github.com/beliavsky/time-series) | L10a2a1; L10a2d3; L10a2c2 | ARMA theoretical covariance/forecasting and Burg AR estimation | Supplied stable models, covariance sentinel, sample centering, conditional intervals and scoped source licenses. |
| [ElliFEM](https://github.com/md861/ellifem) | I2b1a1b | Standalone two-dimensional Helmholtz finite-element workflow | General quadrilateral meshes, source-defined problem data, dense storage, shell file operations and no callable solver claim. |
| [heatcompact3d](https://github.com/tlestang/heatcompact3d) | D2a2a; H1; I1a1a; I2a1b | No-pivot tridiagonal solve, compact differentiation, explicit stepping and periodic 3D heat RHS | Duplicated endpoints, spacing divisor, fixed time grid, stability and excluded AB2 history defect. |
| [laplace-2D](https://github.com/taraskuzyo/laplace-2d) | I2b1a1a | Rectangular Laplace/Poisson five-point SOR | Source normalization, change versus residual, saved iteration counter and actual five-point stencil. |
| [LIBPARABOL / sippp](https://github.com/nschloe/sippp) | D2a4; I2a1a | Operator GMRES and one-dimensional parabolic implicit Runge-Kutta stepping | Right preconditioning, fixed tolerances, callback contracts, persistent correction and absent returned solver status. |
| [Gaussian Mixture ARMA-GARCH prototype](https://github.com/saveriocolla90/fortran90-gaussian-mixture-arma-garch) | L10a2; L10a2d | Supplied-parameter ARMA residual and GARCH variance recursions | Squared-residual input, initialized component metadata, limited stability predicate and no fitting/forecast guarantee. |
| [meshf](https://github.com/ofgn/meshf) | P | Incremental planar Delaunay triangulation | Positive initial orientation, possible initialization hang, quad-kind predicates and development scope. |
| [ARPREC](https://github.com/bl-highprecision/arprec) | A3c; H2a2a1 | Multiword real arithmetic and endpoint-singular tanh-sinh quadrature | C++ bridge, compiled/global precision, mixed-precision callback ABI, shared tables and non-certifying warning/status returns. |
| [DLA-Future Fortran Interface](https://github.com/eth-cscs/dla-future-fortran) | D4a1; D4b1 | Real symmetric and symmetric-definite distributed eigenproblem bindings | External backend scope, host buffers, descriptor restrictions, C integer ABI and runtime setup. |
| [ELPA](https://github.com/marekandreas/elpa) | D4a1 | Distributed real-double symmetric eigenvectors through the configured object API | Full-matrix input, full local Q storage, replicated eigenvalues and native one/two-stage dispatch. |
| [forSISL](https://github.com/rweed/forsisl) | P | Spline-curve line/plane intersection binding | External SISL implementation, unresolved pointer/overlap-copy defects, stale outputs and scoped custom notices. |
| [Powell optimization archive](https://github.com/ralna/mjdp_software) | G2h1a1; G2h3b1a; G2h2a1; G1b1a; G2h2a2 | Original BOBYQA, COBYLA, LINCOA, NEWUOA and TOLMIN optimization entries | Local search scope, callback/workspace contracts, COBYLA default precision, internal LINCOA relaxation and TOLMIN status meanings. |
| [ARPACK PARPACK modernization](https://github.com/kingjgod/arpack_parpack) | D4a4 | Adapted complex implicitly restarted Arnoldi reverse communication | Persistent-state INTENT attributes need review, exact kind/workspace contract and separate extraction. |
| [Delaunay Density Diagnostic](https://github.com/llnl/ddd) | P; E2b | Bundled Delaunay simplex location and scattered-data interpolation | In-place coordinate normalization, per-query errors, projected extrapolation, native component scope and BQPD terms. |
| [Python BLS](https://github.com/dfm/python-bls) | L10a3a2 | Edge-wrapped box-least-squares periodogram | Extended phase-bin storage, eligible-window/denominator requirements, STOP paths and no significance estimate. |
| [Unstructured finite volume](https://github.com/komahanb/unstructured-finite-volume) | D2b4; D2a4; I2b1a1a | Sparse operator CG/GMRES and rectangular Poisson factory/workflow | Attachment, affine RHS, positivity assumptions, restart budgets, breakdown/status and supplied mesh labels. |
| [System Dynamics](https://github.com/quimbp/system_dynamics) | I1a1a; E1a | Classical RK4 stepping and cubic Akima interpolation | Actual RHS includes N, fixed time step, minimum sample count, saved interval state and component provenance. |
| [PyMC 2 historical implementation](https://github.com/pymc-devs/pymc2) | L5a1n; L5a1p; L5a2w | Historical native normal CDF, Poisson log mass and Weibull-family quantiles | Explicit Fortran lengths, in-place CDF, tails, broadcast/zero-rate limits and saved factorial cache. |
| [wvdecomp](https://github.com/avikhlinin/wvdecomp) | J2 | Separable dilated image convolution for adjacent smooth levels | Details require subtraction, fixed padded workspace, C float/int ABI and unversioned LPPL notice. |
| [octree-mg](https://github.com/jannisteunissen/octree-mg) | I2b1a1a; I2b1a3 | Rectangular Poisson FAS cycles and smooth variable-coefficient elliptic operators | One-cycle semantics, coarse-grid rank restriction, coefficient setup and periodic compatibility. |
| [SLICOT System Identification](https://github.com/slicot/slicot-systemidentification) | L10c | Subspace system-identification MATLAB MEX gateway | Processed Hankel factor input, A/C/B/D output order and external SLICOT/MATLAB ABI. |
| [FERRE](https://github.com/callendeprieto/ferre) | E2a; E1b; G1b2 | Grid interpolation, intended weighted polynomial fit and coupled Nelder-Mead search | Shared precision/context, endpoint requirements, polynomial workspace defect and objective coupling. |
| [HARMONIE Monitor](https://github.com/hirlam/monitor) | L4b3; L2b | Paired descriptive statistics and contingency-table tallying | Sample/population conventions, constant-series correlation and forecast-minus-observation input. |
| [SciJIT](https://github.com/shmuel-gilbaum/scijit) | H2a1a1; H2a3a1; H2a4a1; F2 | Finite, semi-infinite and whole-line quadrature plus nonlinear-system binding | Callback ABI, workspace/status, conditional thread-private state and differing nested-call behavior. |
| [SciJIT](https://github.com/shmuel-gilbaum/scijit) | H2a2a1; K1b1a1; K1b1a2; D1a3b; I1a1b; I1a2; E1a; H1; H2a2a2; E2a; H2b1 | Weighted quadrature, nonlinear least squares, norms, splines and ODE integration | Callback ABI/state, workspaces, modified spline signatures, status and representation-specific scope. |
| [ANN Fortran interface](https://github.com/box-tools/ann-fortran) | P | Fortran/C++ kd-tree nearest-neighbor bridge | Caller-owned output buffers, zero-based indices, squared distances and unresolved allocation/cleanup defects. |
| [SOSIE](https://github.com/brodeau/sosie) | E1a; E2a; P | Local Akima interpolation and regular-grid nearest-point lookup | Mixed precision, saved persistence/cache state, configuration dependencies and bounded geographic search. |
| [fsklearn](https://github.com/zhoutengye/fsklearn) | L8e | Native prediction for neural-network, decision-tree and random-forest regressors | External training/export, build precision, mutable activations and defective softmax path. |
| [coordinates grids and maps](https://github.com/alex-robinson/coordinates) | E1a; E2a; K5; J2; H1; P | Native linear/cubic and bilinear interpolation, smoothing, convolution, gradients and point containment | Mixed precision, optional-DX and boundary-index defects, missing/edge conventions and component provenance. |
| [BaM](https://github.com/bam-tools/bam) | M1b | Configured Bayesian-model adaptive Metropolis sampling entry | External BMSL/miniDMSL sampler, loaded prior/model state, output files and warning/error contract. |
| [freeCappuccino legacy snapshot](https://github.com/nikola-m/freecappuccino) | D2b4; D2a4 | Serial CSR conjugate gradients, BiCGStab and Gauss-Seidel | Shared mesh/control state, SPD/structure assumptions, cut-coupling limits and independent final residual checks. |
| [NumX](https://github.com/alpgodev/numx) | L1a1a; L1a1b; L1a1c; L1c1b; L1c1; L5a1n; L6a14 | Raw-data means, dispersion, shape, covariance, higher co-moments and normal density/sampling | Estimator/status conventions, workspace sizing, precision loss, RNG return-kind mismatch and conflicting license notices. |
| [SAM Fortran library](https://github.com/sap-archive/sam-lib) | D2b4 | Symmetric skyline LDL-transpose full-system solve | Packed profile bounds, pivot corrections, correction initialization, operation flags and overwritten storage. |
| [TOOLIB](https://github.com/tribo-pprime/toolib) | D2b1b; D9a1; K1b1a2; E1a; E2a; J1b; N6a2a; N6a2b; C3a2 | Dense SPD solves, linear/nonlinear fits, grid prolongation, FFTs, sorting and Chebyshev values | Mixed factor storage, fit termination/status, zero-based bounds, FFT signs/lifecycle and component terms. |
| [chunkmatc](https://github.com/zgimbutas/chunkmatc) | H2a1a1; H2a1a2; C3a2 | Adaptive/fixed Gauss-Legendre quadrature and Legendre polynomial values/derivatives | Per-leaf tolerance, callback ABI, legacy array extents, Newton limits and endpoint derivatives. |
| [ForTrilinos](https://github.com/trilinos/fortrilinos) | D2a4; D4a2; D4b2; F2 | Sparse linear solves, ordinary/generalized eigenproblems and nonlinear systems through C++ backends | Runtime/maps, parameter-selected algorithms, enum/logical status distinctions and eigenvalue extraction capacity defect. |
| [Skyborn](https://github.com/qianyesu/skyborn) | E1a; E2a; L10a1c2; L4a1d; L8a3 | Piecewise/grid linear interpolation, symmetric FIR filtering, sequence statistics and robust slopes | Sentinel/direction contracts, gap edges, reflection extents, clean-series buffers and unit-time slope semantics. |
| [PIPPy](https://github.com/auto-mech/pippy) | D9a1 | Weighted truncated-SVD fit using initialized invariant-polynomial basis | MPI/COMMON/basis initialization, physical dimensions, unreturned diagnostics and Numerical Recipes component provenance. |
| [ButterflyPACK](https://github.com/liuyangzhuan/butterflypack) | D2a1; D2c1; D1b4 | Real/complex general compressed solves and matrix-vector application | Precision-generated names/types, collective setup, local ordering, compression error and absent status outputs. |
| [AUTO-07p](https://github.com/auto-07p/auto-07p) | F2; I1b2; I1c; E1a; H1; H2a1b2 | Nonlinear algebraic/BVP continuation, mesh adaptation, interpolation, differentiation and sampled quadrature | Framework callbacks/state, collocation scaling, order/shape limits and distinct interpolation/quadrature nodes. |
| [Cedar](https://github.com/cedar-framework/cedar) | D2e | Native BoxMG restriction and residual-dependent prolongation components | Explicit BIND(C)/VALUE interfaces, initialized weights/ghosts, in-place residual scaling and correction semantics. |
| [Dataplot](https://github.com/usnistgov/dataplot) | L1a1a; L1a1b; N6a1b; N6a2b; L11; L8a1a1; L5a1n; L5a2n; L5a1l; L5a2l; C7a; L5a1p | Location/dispersion summaries, passive ranks and sorting, Spearman correlation, linear regression, normal/logistic/Poisson functions and log gamma | Promoted default-real ABI, common/output dependencies, inference/degeneracy limits, cutoff assignment defect and approximation/tail scope. |
| [PFLARE](https://github.com/pflareproject/pflare) | D2a4; D2e | PETSc sparse-system preconditioner integration and algebraic coarse/fine partitioning | Registration/context lifecycle, host AIJ scope, PETSc error/convergence channels and returned global index sets. |
| [ScaLAPACK](https://github.com/reference-scalapack/scalapack) | D2a1; D2c1; D2b1b; D2d1b; D2a3; D9a1; D4a1; D4a3; D6; D2a2 | Distributed real/complex general and positive-definite solves, triangular/banded solves, least squares, symmetric/Hermitian eigenproblems and SVD | Collective grids/descriptors, local workspaces, rank assumptions, nonunit diagonal-scan finding and distinct banded layout. |
| [pyOpt](https://github.com/madebr/pyopt) | G1b2; G2h3b2; G2h3b1b; G2h3b1a; D9b1; D9a1; G2e1; D1b11 | Native nonsmooth/SQP/derivative-free optimization, constrained and rank-deficient least squares, minimum-distance QP and Householder transformations | Patched callback signatures, executable workspace requirements, status/output limitations and scoped component licenses. |
| [fastSHT](https://github.com/liuhao-cn/fastsht) | C9; J1a1; J | Associated Legendre recurrence, ringwise real FFT and scalar spherical-harmonic analysis/synthesis | Shared state, CPU/MKL packing and normalization; allocator parameter bounds mismatch; unchecked post-initialization sketches. |
| [Dataplot: distributions and beta functions](https://github.com/usnistgov/dataplot) | L5a1b; L5a2b; L5a1c; L5a2c; L5a1t; L5a2t; L5a1f; L5a2f; L5a1g; L5a2g; L5a1w; L5a2w; C7b; C7f | Beta, chi-square, Student t, F, gamma and Weibull probability/quantile functions; complete log-beta and normalized incomplete-beta functions | Promoted-real ABI, integer versus real degrees, common initialization, fixed tolerances, clipping, boundary conventions and branch findings. |
| [FLAPWxHZ](https://github.com/venovako/flapwxhz) | D6; D4b3 | Complex generalized factor-pair SVD and factorized Hermitian-definite generalized eigenproblems | Aligned storage, signature/regularity assumptions, scheduling and thread capacity, promoted integers and sweep-count status. |
| [ecTrans](https://github.com/ecmwf-ifs/ectrans) | J; J1b | CPU spherical-harmonic and limited-area bifourier analysis/synthesis | Explicit generated interfaces, initialized geometry/distribution, packed storage, field-set ownership and abort behavior. |
| [Clawpack Riemann solvers](https://github.com/clawpack/riemann) | I2a2 | Scalar hyperbolic advection/Burgers interface solvers | Two complete local main programs: 17 flux/entropy/conservation cases; separate same-symbol source variants; no full PDE evolution check. |
| [Boxcode2D legacy wrapper](https://github.com/mrachh/boxcode2d-legacy) | I2b1a1 | Adaptive eighth-order free-space two-dimensional Poisson volume potential | Unit-root wrapper contract, rank-three data, default/four-byte integer compatibility, ignored selectors, unassigned timing and large workspaces; uncompiled. |
| [Boxcode2D legacy wrapper: quadrature](https://github.com/mrachh/boxcode2d-legacy) | H2a1b2 | Fixed-order unweighted quadrature on Chebyshev-root nodes | 30 checked monomial moments and node/weight checks; bounds checks disabled for unchanged legacy object, enabled for the main program. |
| [NDSM](https://github.com/sag2021/ndsm) | I2b1a1a | Rectangular two-dimensional homogeneous-Neumann Poisson multigrid | Checked manufactured solution on two grids, independent interior residual/gauge and refinement; serial binary64 and 64-bit index scope. |
| [NDSM: piecewise-linear interpolation](https://github.com/sag2021/NDSM) | E1a | Uniform-grid scalar interpolation and end-cell extrapolation | Seven checked values, including a non-affine nodal table; 64-bit IT and nondefault coordinate bounds. |
| [NDSM: multilinear interpolation](https://github.com/sag2021/NDSM) | E2a | Bilinear and trilinear interpolation on Cartesian grids | 150 checked cross-term polynomial values; unequal spacings and nonsquare grids; no arbitrary-data accuracy claim. |
| [Boxcode2D: Chebyshev basis conversion](https://github.com/mrachh/boxcode2d-legacy) | E3c | Dense Chebyshev nodal/coefficient transforms | 60 checked unit-coefficient/value cases; no FFT-speed claim. |
| [Boxcode2D: interpolant differentiation](https://github.com/mrachh/boxcode2d-legacy) | E3a2 | Spectral derivative matrix on Chebyshev-root nodes | 30 monomial derivatives plus 30 endpoint checks; legacy object has bounds instrumentation disabled. |
| [Boxcode2D: interpolant integration](https://github.com/mrachh/boxcode2d-legacy) | E3a3 | Spectral integration of fitted polynomials | 26 checked monomial integrals; input restricted to degree N-2 because higher coefficients are truncated. |
| [FFTPack: finite convolution](https://github.com/keurfonluu/FFTPack) | J2 | Real/complex binary64 linear convolution | 98 direct-sum comparisons, unequal/length-one inputs; no conjugation or circular-convolution claim. |
| [FFTPack: periodic analytic signal](https://github.com/keurfonluu/FFTPack) | J4 | Double-precision Hilbert/analytic-signal FFT mask | 44 Fourier-mode/DC/Nyquist checks; single-precision overload discards the imaginary result. |
| [FFTPack: real-input Fourier transform](https://github.com/keurfonluu/FFTPack) | J1a1 | Full complex spectrum via complex backend | 33 independent DFT comparisons with padding/truncation; unscaled negative-exponent convention. |
| [FMM collection: cubic splines](https://github.com/Beliavsky/Computer-Methods-for-Mathematical-Computations) | E1a | FMM and natural cubic construction with value evaluation | 499 analytic polynomial/piecewise checks; distinct endpoint conditions, nonuniform knots and extrapolation. |
| [FMM collection: spline derivatives](https://github.com/Beliavsky/Computer-Methods-for-Mathematical-Computations) | E3a2 | Value and first/second/third derivatives of fitted cubics | 499 checked output vectors; right-hand third derivative at an interior natural-spline knot. |
| [FMM collection: adaptive quadrature](https://github.com/Beliavsky/Computer-Methods-for-Mathematical-Computations) | H2a1a1 | Closed eight-panel Newton-Cotes with adaptive subdivision | 55 analytic integrals, including reversed/zero intervals; persistent limit state and estimated-error scope documented. |
| [FMM collection: real SVD](https://github.com/Beliavsky/Computer-Methods-for-Mathematical-Computations) | D6 | Householder/QR rectangular singular-value decomposition | 48 square/tall matrices; reconstruction, orthogonality, energy and selected known spectra; both vector flags true. |
| [FMM collection: RKF45](https://github.com/Beliavsky/Computer-Methods-for-Mathematical-Computations) | I1a1a | Adaptive explicit nonstiff initial-value integration | 211 analytic-state comparisons at GNU -O0; preserved helper state has an INTENT(OUT) portability issue. |
| [system_dynamics: means](https://github.com/quimbp/system_dynamics) | L1a1a | Arithmetic and optional weighted means | 114 closed-form datasets; conforming weights and nonzero weight sum required. |
| [system_dynamics: sample variance](https://github.com/quimbp/system_dynamics) | L1a1b | Corrected two-pass variance with N-1 denominator | Same 114 datasets; N>=2, no missing-data handling; Numerical Recipes notice. |
| [system_dynamics: covariance eigenvectors](https://github.com/quimbp/system_dynamics) | D4a1 | Householder/QL symmetric eigensystem | 96 PSD cases; negative eigenvalues clipped, exact-zero rank, STOP on QL failure. |
| [FMM: scalar minimization](https://github.com/Beliavsky/Computer-Methods-for-Mathematical-Computations) | G1a1a | Derivative-free Brent search and Fmin wrapper | 216 checked normal cases; exhausted-budget probe reproduces missing failure status. |
| [FFTPack: cross-correlation](https://github.com/keurfonluu/FFTPack) | L10b2a | Raw finite cross-correlations, real/complex KIND=4/8 | 588 direct-sum comparisons; conjugated second vector, symmetric maximum-length lag range; legacy ABI limits. |
| [minila: direct triangular solves](https://github.com/ghbrown/minila) | D2a3 | Default-REAL diagonal, forward and backward substitution | 108 known-solution/scaled-residual checks; 32-bit REAL, correct structure and nonzero pivots required. |

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

## Sorting contracts and sampled versus adaptive quadrature

Passive sorting preserves values and returns a permutation; active sorting
changes their order. Fortran-parallel-sort and the real `indexx` overload use
passive mappings. HeapSort, Timsort and the iterative quicksort change values.
Fortran-quicksort has both interfaces; its overwrite wrapper still uses O(N)
index storage. HeapSort's paired swaps and author test establish the intended
permutation convention in source, which differs from its header formula.

Source mappings include repair findings rather than hiding them: fsort contains
two malformed IF statements, Timsort run discovery can read past a final singleton,
and iterative quicksort silently ignores pushes into an undersized stack.
Usage sketches state their preconditions and do not assert successful execution.
The two quadrature cards distinguish fixed-grid sampled Simpson rules from an
adaptive callback wrapper. The latter retains workspace-reuse and breakpoint
source findings, and depends on FERROR for reporting failures.
No upstream routine or calling sketch in this batch was compiled or run.

## Differentiation, interval means and stateful numerical interfaces

The three differentiation entries distinguish forward gradient-vector seeds,
dual directional evaluations and reverse scalar adjoints. H1 is already a
leaf, so procedure names and interface scope supply the useful detail.
No higher-order or whole-library claim is inferred from an inspected first-order
path. The reverse implementation has gradient-reuse and node-lifecycle findings.

mp-interp takes interval averages and uses cyclic midpoint interpolation;
its coordinate arrays do not provide an arbitrary-query interface in the
reviewed path. FortVSH separately exposes ordinary Legendre values and quadrature
rules. A node/weight generator requires the caller to form a weighted sum.
The Butterworth entry uses the detailed L10a1c3 filtering branch from the
[Netlib GAMS taxonomy](https://netlib.org/bib/gams.html), with coefficient
normalization and zero-history semantics recorded. RKSUITE's F90 communication
object and array-valued derivative callback are distinct from its legacy F77
examples. libcoulcc's raw status-returning interface is shown because its
convenience wrappers have source findings.
No upstream routine, derivative, filter, interpolation or ODE example in this
batch was compiled or run.

## Sparse storage, vector products and least-squares contracts

The native libsparse helper and the SPOOF object use different CSR interfaces:
separate begin/end pointers versus a single row-pointer array. Their cards
record the actual indices, kinds and output initialization requirements.
The libsparse sketch avoids its object wrapper's output-intent mismatch.
sparseSET's reviewed round trip is a storage conversion, with drop tolerance
and an allocated-output precondition, rather than a solver mapping.

Dot products use D1a4; VecFor's Cartesian cross product uses D1a11. Tensor dyads
use D1b6 with explicit outer-product semantics. These services do not imply
that unrelated inverse, spectral or geometric routines have been reviewed.
The D1a4 and D9a4 taxonomy additions follow the
[Netlib GAMS index](https://netlib.org/bib/gams.html).

NNLS constrains x to be nonnegative while holding the original data matrix
fixed in the mathematical problem. DTLS instead permits perturbing both A and B.
The [Netlib vanhuffel index](https://netlib.org/vanhuffel/) lists DTLS under
D9a1 and D9a4; the catalog uses D9a4 here to make its total-least-squares scope
explicit. Lanczos requires a symmetric operator with overwrite/accumulate
callback semantics; its variance-named output is a residual norm. The seed
path was followed through its downstream normalization, so the wrapper's seed
packing is not presented as an uncorrected random-seed defect.
No upstream routine or calling sketch in this batch was compiled or run.

## Explicit random state and transform conventions

A state setter is not necessarily a seeding algorithm: two xoshiro interfaces
need all four words supplied explicitly. The SplitMix function does not modify
its seed, and its returned mixed value is not the next additive counter state.
The reviewed xorshift normal cache belongs to the procedure/thread rather than
the object. These details affect reproducibility even before distributional
quality is considered. Intended unsigned arithmetic is not assumed portable
merely because a translation uses signed INT64 storage.

Hankel and wavelet services remain under J where the taxonomy has no matching
child; implementation names and scopes supply additional specificity. FFTLog's
sine/cosine service does match J1a3. Ogata also matches H2a3a2 because it uses a
callback on a semi-infinite domain with user-chosen node count, not a requested
accuracy. The added quadrature and normal-sampling leaves follow the
[Netlib GAMS taxonomy](https://netlib.org/bib/gams.html).

Transform grids, normalization and index order must be read before comparing
results: logarithmic periodic samples, finite uniform samples with zero-boundary
extension, and time-first versus scale-first coefficients are different contracts.
No generator, transform or calling sketch in this batch was compiled or run.

## Optimization interfaces and independent stopping checks

The reviewed scalar routines print their solutions rather than returning them.
Newton convergence to a stationary point does not distinguish a minimum from a
maximum. Minimization estimates gradients internally, so its optimizer is mapped
to the no-user-derivatives leaf even though it steps along an estimated gradient.
Its derivative service receives a separate H1 mapping.

GridSearch and PSOclassicG are standalone source-configured search programs.
G2i records global-search intent without promising a global optimum. In contrast,
MMA_Sub performs one approximation/subproblem step and needs an outer driver with
fresh values, first derivatives, iterate history and stopping checks. The mapped
nonlinear-constraint leaf does not assert that this implementation accepts explicit
equalities. The author main's one-step limit is not a convergence demonstration.

The L-BFGS-B wrapper exposes FACTR under the name func_tol and counts evaluation
requests under max_cyc. The QP cards distinguish bridge success from solver
optimality, and criterion/objective values from independently computed feasibility
residuals. Detailed cards retain initialization, argument-intent, optional-argument
and reporting findings. No upstream routine, optimizer or calling sketch in this
batch was compiled or run.

## Factorization storage, approximation inputs and fitted derivatives

A Cholesky factor, orthogonal basis, interpolative decomposition and approximate
SVD expose different objects. The lin_alg card marks the assigned triangle;
libid records packed coefficient storage and selected original columns. MARIA
requires the caller to prepare its initial randomized sketch and its product
callbacks. No full LAPACK/kernel audit or numerical-error certificate is inferred
from inspecting their setup and dispatch paths.

Nonnegative matrix factorization is a bilinear least-squares approximation with
linear nonnegativity constraints, not an SVD. Its K1b2a mapping follows the
[Netlib GAMS taxonomy](https://netlib.org/bib/gams.html), and retains the actual
shape/update/reporting findings rather than suggesting a checked fit. The scalar
3x3 tensor contraction and outer products have scoped mappings; problematic
higher-rank accumulations do not inherit the scalar sketch.

SHEPPACK's gradient is a derivative of an already fitted interpolant. A zero
scalar evaluation does not distinguish no support from a successful zero;
QS2GRD provides status-bearing evaluation. The root-finder card likewise requires
checking status before using a potentially unassigned result. The coarray card
states its norm/ownership/file conventions and collective requirements.
No upstream routine, fit, root, coarray solve or calling sketch in this batch
was compiled or run.

## Random streams and time-series conventions

The random-generator cards distinguish intended distribution from verified sample
quality. FortRAND reinitializes the intrinsic generator for every scalar draw,
and the separate Knuth scalar wrapper reseeds on buffer refill. The selected
Knuth sketch uses the explicit seed/bulk routines instead. MELG keeps recurrence
state in an object; dSFMT wraps a C allocation whose pointer must not be treated
as an independently copied stream. Neither source inspection nor an interface
sketch certifies statistical independence or reference sequences.

The time-series cards identify the operation actually implemented. NSMarkov
constructs finite-state grids and transition probabilities without drawing paths.
ACFbyFFT is a standalone file-based program; its sketches disable the faulty mean
subtraction and assume already centered input. The signal_subspace covariance
routine returns uncentered delayed-window second moments, while its ESPRIT path
has recorded pivot-type and output-extent problems requiring repair. TOMS 675
coverage is scoped to scalar observations and square-root filter updates, with
SRCF providing a covariance/gain update rather than a complete state trajectory.
All new calling sketches are source-inspected and were not compiled or run.

## Transform conventions and callback-driven numerical services

Stockwell transforms remain at J because the original GAMS hierarchy supplies no
Stockwell leaf. FSTPACK's separately callable complex FFT wrapper supports J1a2;
its Stockwell reconstruction assumes real data carried in complex arrays. The
Torrence/Compo wavelet routine supports time-series spectral analysis at L10a3a.
The card records the fixed scratch limit and differing root/source license notices.
Neither transform mapping certifies normalization, reconstruction or significance.

The Bessel evaluator uses pinned binary tables as well as code. Its initialization,
real-order range and branch-dependent phase/log outputs are recorded explicitly.
RFNG's widened integer output contains a 32-bit payload, not 64 generated bits.
Fazang's selected reverse-mode path requires adjoint resets and tape-lifetime care;
its convenience jac helper has a recorded uninitialized bound and is not used in
the calling sketch. The forward-over-reverse Hessian path remains unreviewed.

HOMPACK90 requires problem-specific residual/Jacobian callbacks and preserves
continuation state between resumable returns. BLZPACK requires callers to service
reverse-communication requests, including shifted solves and inertia in generalized
mode; its author example also needs a separately supplied MA47 solver. EISCOR's
symmetric tridiagonal card records the driver/factor workspace-section mismatch
and small-dimension edge case. These calling sketches were not compiled or run;
recording an implemented method and its limitations is not a correctness claim.

## Projection steps, fitted functions and solver contracts

LRAP's selected routine performs one nonnegativity transformation and rank
truncation. It remains classified at K: source inspection does not establish a
converged least-squares optimizer against a fixed original target. In contrast,
vector_fit's fixed-pole residue solve is linear in its fitted coefficients and
supports K1a1a3; the separate rational evaluator supports K6a1. Pole relocation,
passivity and stability guarantees remain outside these selected mappings.

The spline cards separate constructing a smoothing fit (K5) from differentiating
the fitted spline (K6a2). GCVSPL's negative modes reuse saved setup/work state;
SPLDER consumes one compatible coefficient column. curvefit's scalar regression
fits through the origin, while its linear interpolator requires successful data
initialization before lookup. Its external polynomial fitting kernel was not
newly audited. The cards retain these distinctions and the separate Woltring
kernel/Python-wrapper license notices.

FortranMatrix's real/complex inverses dispatch LU and explicit inversion but stop
the process on errors; the containing module also imports PFAPACK. Tensor
Toolbox's selected inverse is a fixed 3-by-3 cofactor formula without conditioning
or singularity guards. MEPACK's selected matrix-equation drivers instead expose
INFO and SCALE, and return workspace queries through integer LDWORK. NITSOL2
requires its fork-specific controls/callbacks, explicit real defaults and an
independent residual check even after small-step termination. These reviews
identify implemented paths and calling contracts; none of the new sketches or
upstream numerical programs was compiled or run.

## Optimization state, fitness conventions and stopping rules

The FilterSD, DEPP, Diver, libga, OpenFSAM, LCMIN, critical-line and
VTdirect95 reviews pin the selected source and separate public entry points
from internal helpers. Their cards record callback declarations, state ownership,
workspace or configuration requirements and scoped license findings.
DEPP maximizes fitness, whereas the selected Diver and libga paths minimize it.
OpenFSAM's accepted-step counter and DIRECT's batch limits are not interchangeable
with a strict objective-evaluation budget. A stopping condition does not establish
global optimality. The derivative checker is a consistency heuristic and can
return with a perturbed input vector.

All new calling sketches remain uncompiled and unrun. The source review does
not audit the full GLCPD, HSL or other dependency stacks, parallel execution,
or numerical accuracy. Root license findings do not replace dependency terms.

## Numerical services and caller-controlled accuracy

These reviews distinguish finding interpolation intervals from evaluating a
curve, basis evaluation from fitting data, and quadrature-rule generation from
an automatic integrator. The cards retain actual array bounds, precision kinds,
callback declarations and endpoint conventions. Their evidence links identify
the source paths used for the scoped claims.

The selected FOODIE method leaves time-step selection and time advancement to
the caller. The selected RALFit usage explicitly requests its first-order model
instead of inheriting the hybrid default. WenOOF's selected standard rank-one
path is kept separate from debug outputs and reconstruction overloads.
All new sketches are uncompiled and unrun; author examples are linked as
references, not presented as checked hosted drivers. License findings preserve
modified notices, multi-license context and unresolved upstream provenance.

## Reverse communication, stopping tests and transform conventions

SPRAL's selected LSMR path asks for accumulated matrix products, while the
selected L-BFGS-B interface asks for objective/gradient values through TASK.
Their cards preserve state/workspace requirements and distinguish terminal
returns from successful convergence. NumLib's fixed RK4 step and Planelles'
step-size tests similarly need caller-side accuracy or residual checks.

The scalar Toolkit root routine is described by its inspected interpolation
steps and failure paths; its name alone is not evidence of a standard Brent
safeguard. Brito's external CG routine is separate from the MAIN in the same
file. Its cubic bisection example is explicitly a program, not a generic API.
The Hankel mapping remains at J because the original taxonomy has no dedicated
Hankel child. The card gives the exact transform measure and kernel signature.
The normal-probability mapping records the product-correlation restriction and
single-precision ABI, separately from the AS 66 tail helper.

All new sketches remain uncompiled and unrun. The reviews identify implemented
paths and contracts, not numerical certification or complete dependency/license
audits. Pinned line links, hashes and author examples remain in the ledger.

## Statistical conventions, generated precision and storage indices

The EDAT and FSML cards distinguish public wrappers, selected template
specializations and implementation helpers. They record empty/singleton input
behavior, population versus sample denominators, and correlation without
inferential claims. The probability cards distinguish mass/density evaluation
from cumulative/inverse probabilities and random generation. In particular,
C_LONG_DOUBLE is not a fixed-width quadruple kind, and statislib's inspected
exponential PDF/CDF result declarations remain default REAL.

FINDI is an exact-key search, while tri_indices is an address-mapping service
for packed storage. Their indexing conventions and arithmetic limits are part
of the recorded calling contracts. The WENO review records the unassigned
inversion-success status and restricts its claim to a selected 2D cell-average
reconstruction path. The GMRES card retains a broad D2 mapping because its
public operator type comes from an external dependency; it does not claim an
arbitrary-matrix or unrestricted sparse-solver interface.

All new sketches remain uncompiled and unrun. Source review and linked upstream
examples do not establish numerical accuracy, successful builds or complete
component-license provenance. The generated ledger retains pins and file hashes.

The special-function interfaces retain their actual precision, scaling and error
conventions: AMOS J and K use different KODE=2 factors, and AS241 returns a zero
sentinel with IFAULT for invalid probabilities. The GGQ sketch requires weighted
basis data and an initialized Legendre discretization; it is not an automatic
integrand-to-rule example. The dfsaneacc mappings describe its Fortran QR support,
not the R nonlinear algorithm, and require compatible REXIT error hooks. MINUIT
command status and covariance quality are recorded separately. All new usage
sketches are source-inspected and were not compiled or run.

The compensated-summation bindings return new objects and require reassignment;
the supported streaming-statistics mapping is univariate. The separately reviewed
covariance recurrence accumulates two old-mean deltas and needs correction.
The Yeo-Johnson selector has a relative likelihood/Jacobian coefficient discrepancy.
The Box-Cox objective instead differs by an overall positive factor that alone
does not change its maximizer; its selector still requires strictly positive data.
The selected adaptive RK routine is limited to autonomous equations because its stage times are unchanged;
its normal-value test also rejects zero/subnormal endpoints. SESAM's Gram products
use squared weights and do not center or normalize statistical data. The spherical
harmonic Fortran routines evaluate bases/expansions; MATLAB performs the repository's
scattered-point least-squares fit. These findings and the new calling sketches are
source reviews, not compilation or numerical checks.

The RNG stream interfaces distinguish module-defined types from separately defined
external functions and retain the incomplete seed-validation finding. DATAPAC
entries explicitly select the REAL64 module and record count/workspace limits.
MoA take/drop return aliases into a persistent target; they do not copy data, and
the nonpositive-drop branch needs correction. The transpose implementation does
rearrange storage and still allocates a full-size unused flag array. Numerical
calculus/FFT sketches state their uniform-grid and radix-two preconditions.
All new calling sketches remain uncompiled and unrun.

The Sherman-Morrison candidate remains deferred from source-reviewed mappings:
at pinned commit `0ba978e78727cb4c70e17d50153b09b4839d5c0a`,
[the Fortran SM1 interface](https://github.com/TREX-CoE/Sherman-Morrison/blob/0ba978e78727cb4c70e17d50153b09b4839d5c0a/src/finterface_mod.f90#L18-L24)
declares five arguments with allocatable arrays, whereas
[the C++ SM1_f wrapper](https://github.com/TREX-CoE/Sherman-Morrison/blob/0ba978e78727cb4c70e17d50153b09b4839d5c0a/src/SM_Standard.cpp#L282-L286)
expects six arguments (including a by-value breakdown threshold) and raw
pointer-to-pointer buffers. The interfaces need reconciliation and a checked
interop driver before promoting a usable Fortran calling example. This is a
source finding, not a reproduced build/runtime failure.

Rational arithmetic and real-to-rational conversion have separate scopes: exact
finite-width arithmetic does not imply an exact binary/decimal conversion for
every input. Hyper-dual usage spells out the two first-direction seeds and mixed
seed. The comparison cards distinguish array reductions from elemental masks and
record the actual tolerance kinds. Normal log-density arguments use variance,
while error-corrected mixture fitting takes per-observation error widths. The
legacy TWDTW sketch initializes boundary costs and limits candidate-buffer use;
the C-bound callback path requires a separate intent correction. Spectral fitting
requires the global weight sum to match the input weights and uses frequencies
in microhertz with times in seconds. These are source-reviewed calling sketches,
not newly compiled or numerically verified drivers.

The extended-precision cards distinguish fixed two-double QD storage, MPFUN
working word counts bounded by build-time capacity, and FMPFR bit precision.
They record wrapper dispatch/build requirements without implying complete
backend arithmetic verification. FMPFR sketches explicitly initialize rounding
and avoid wrappers that pass unallocated components to MPFR initialization.
The ODEPACK review separates method flags and retains the modernization's array
argument shapes and stateful continuation requirements. NUFFT records centered
mode storage, normalization and transform sign. The EnKF example selects the
single-observation update and real-8 ABI, while the GARCH examples separate
simulation from observed-return variance recurrence and return standard deviations.
The GA coordinator targets a supplied objective value and returns printed diagnostics;
its initialization and concurrent counters remain review limitations. All new
calling sketches are uncompiled and unrun.

The statistical/interpolation interfaces distinguish standalone numerical components
from package-wide runtime dependencies. In particular, sparse mean outputs need
initialization, gamma scale differs from rate, and Tweedie quadrature requires
prepared distribution state. ACEPACK periodic and terminal-tie indexing concerns
are recorded as source findings, with strictly increasing nonperiodic data in the
calling sketch. None of these new sketches was compiled or run.

Optimization and statistical cards retain the selected implementation scope.
QAP uses a symmetric-matrix swap formula and R runtime services; finite-budget
packing is not necessarily optimal. Gaussian-covariate selection has degenerate
candidate/probability branches to validate, and its optional inverse-related
triangular helper returns before solving. MCLUST log-density output is distinct
from its unassigned-on-success HOOD scalar. TREAT remains a program entry point
with internal analysis helpers. These are source reviews; no new calling sketch
was compiled or run.

Tensor and kernel approximation cards distinguish sampled/truncated approximations
from global error guarantees. TT contractions preserve their rank-one array result
type. The inspected Fortran component in SR-CUR is pivoted QR, not the complete
CUR workflow. KronLinInv progress arithmetic and randomField geometry/amplitude
findings need correction before meaningful numerical validation; the cards retain
these limitations explicitly. GADfit global fitting refers to shared dataset
parameters, with forward and reverse AD state treated separately. All newly added
calling sketches remain uncompiled and unrun.

The PRIMA, DQED, OPTGRA, MONOLIS, Diaglib, exponential-sum, PyPOLSYS and
Hooke-Jeeves interfaces have pinned source evidence and calling sketches. These
sketches were not compiled or run. Their scoped findings distinguish callback and
workspace contracts, convergence from API status, and supplied programs from
reusable routines. No new checked hosted drivers or numerical certifications are
claimed. License findings retain separate wrapper and legacy-core qualifications.

The DIRECT, slice sampling, M_random, contour extraction, PFAPACK, MPFUN90,
get_moments and GSSFortran cards identify pinned interfaces and calling sketches.
The sketches were not compiled or run. Distribution and convergence claims are
limited to inspected paths: random permutation probabilities, finite optimization
budgets, moment definitions, real-kind build choices and shared state require
particular care. The PFAPACK mapping covers a skew-symmetric related factorization,
not a generic solver or QR decomposition.

The IEEE-class, L-BFGS-B-NS, CoPA, polyhomocont, MSOLV, EnSDAM, libsupermesh
and CohensdpLibrary cards now identify pinned interfaces, argument declarations
and calling sketches. The sketches were not compiled or run. Findings include
disabled standard stopping tests in L-BFGS-B-NS, the uninitialized reference mean
in EnSDAM covariance, CoPA control/shape guards and separate continuation path
statuses. Those limitations remain explicit rather than implying checked numerical
results or complete algorithm/API audits.

KFAS, dae4py/DASKR, EigenExa, LHS, EMSOL, faiNumber, CUTEst and Matran
now have pinned procedure or program interfaces and calling sketches. The sketches
were not compiled or run. This review distinguishes LHS configuration-driven
program use, CUTEst evaluation services and sparse/distributed solver setup.
Matran padding/status/cleanup limitations, EigenExa mode-specific cleanup and
invalid-metric collective behavior, and legacy workspace/kind/encoding assumptions
remain explicit; no numerical results or complete API audit are implied.

PSFUN, SOLVERS, FEconv, NScluster, CDASQR, Zolo-SVD, TikTak and the SLATEC
modernization now have pinned source interfaces and calling sketches. The sketches
were not compiled or run. Broad classes are retained for matrix-function/polar
operations and smoothed penalized quantile regression where narrower leaves
would overstate the inspected algorithms. The review distinguishes program
entry points from routines, documents prototype solver breakdown/status/rank
limitations, and keeps component license notices separate from root declarations.

hyperBOB, PDECHEB, linalgf90, KohonenF03, nn_mod, FortLearner, sht_py and
urca now have pinned source interfaces and calling sketches. These sketches
were not compiled or run. Review distinguishes spatial semidiscretization
from time integration, gradients from loss values, normalized Legendre values
from classical unnormalized polynomials, and wrapper status from convergence.
Collective/workspace/kind requirements, prototype state-contract limitations
and component-specific licensing remain explicit.

nn_tl_ad, FNN, Visual-Fortran-Solvers, ASURV, FortranFilterSLP, HPCSeriesCore,
fortran_shapefuncs and BMSL now have pinned source interfaces and calling
sketches. These sketches were not compiled or run. Review preserves the
distinctions between input and parameter derivatives, reference and physical
coordinates, raw MAD and scaled dispersion, and reusable kernels versus
grid-driven demonstrations. Censoring-tail conventions, filter boundaries,
normalization differences, and legacy workspace/dependency/status limits
remain explicit.

FORCES, ForApollo, PolyChordLite, the DC-Clust subset of Clustering-via-
Nonsmooth-Optimization, JKogb, Stripy, TSSS and Spaloess now have pinned
source interfaces and calling sketches. These sketches were not compiled
or run. Review distinguishes matrix layouts, signature-metric versus ordinary
decomposition, covariance normalization, gating outputs, boundary extrapolation
and estimated sampler convergence. Conflicting/proprietary/academic-use notices
are retained rather than assigning an unsupported blanket permissive license.

Sherman-Morrison, Sparse-Iterative-Parallel-Linear-Solver, npregfast,
rrelaxiv, MultiNest, fft-overlap, M_blas and Sparse Fortran examples now
have ten additional pinned mappings and source calling sketches. These were
not compiled or run. Review distinguishes raw C pointers from allocatable
Fortran descriptors, accessible status from actual convergence, coefficients
from derivatives, and integration examples from numerical implementations.
The MUMPS example remains a program entry point. The GPU mapping covers only
the inspected 2D round-trip path, with the unfinished 3D path explicitly excluded.

PaScaL TDMA, FC Tables, OptimusPrime, BFpack, BVARmml, Fitter MC, Singular
surface operators and PDFO now have ten additional pinned mappings with
source calling sketches. These were not compiled or run. The review separates
GPU device/MPI contracts, R RNG state, file-driven model fitting and
Intel/IMSL linkage from ordinary standalone calling interfaces. It records
local adaptive tolerance rather than a global quadrature bound, derivative-free
optimization termination rather than proof of optimality, and explicitly
documents source status, counter and progress-reporting limitations.

FM (TOMS 814), the cfinch ODEPACK redistribution, islasso, tfQMRgpu, GPopt,
libdlfind, HSSPACK and S2HAT now have eleven additional pinned mappings
with source calling sketches. These were not compiled or run. Method
flags, public versus private wrappers, external versus module procedures,
shared solver history and runtime dependencies are explicit. HSS status/panel/
timing limitations, L-BFGS curvature and zero-gradient guards, and sparse
GPU residual checks are retained alongside the usage lines. Spherical
harmonic synthesis remains in broad J because this taxonomy has no
dedicated spherical-harmonic leaf.

AMG4PSBLAS, BDDCML, BayesFM, robust, rrcov, SmoothHazard, the Robust
Gauss-Newton Algorithm and GALAHAD have ten additional pinned mappings.
Calling sketches were not compiled or run. The reviews distinguish
preconditioner construction from a complete solve, PCG from BiCGStab,
a conditional factor draw from posterior fitting, fixed-scale M-estimation
from a complete MM workflow, and convex from indefinite quadratic programs.
R-hosted dependencies, random-subset limits, Weibull inverse-scale and
success conventions, EQP constraint signs and solver termination diagnostics
are recorded with the public interfaces.

The QR demo, Timeslab, fortress, PSBLAS, PSMMA, PyGSLIB, inference and
GLMnet MATLAB distribution have twelve additional pinned mappings and
calling sketches, which were not compiled or run. Reviews document
complex versus real eigenvalue output, Hessenberg reduction, AR coefficient
and partial-correlation signs, stationary Kalman likelihood initialization,
distributed CG and structured products, spatial lag covariance, adaptive
vector cubature, numerical information matrices and penalized regression
paths. Missing statuses, inherited source notices, overwritten inputs,
compressed coefficients and scoped algorithm restrictions remain explicit.

CE-Fortran, the Markov modules, TISEAN, KohonenF08, SparseReg, SpLLT, PDAF
and mscbdecomp have twelve additional pinned source-reviewed mappings.
Their calling sketches were not compiled or run. TISEAN is annotated as
supplied command-line programs rather than a callable library. Reviews
record scalar versus vector overloads, quadrature-node generation,
finite-state probability versus greedy paths, ETKF subtype selection,
SOM serial/OpenMP restrictions, regression convergence limitations,
SpLLT solve-job semantics and matrix-exponential splitting order.
Historical component provenance and license scope remain explicit.

The distributed QZ/QR implementations, JACSD, quantregpy, tidybench, midasmlpy,
fas and time-series have twelve additional pinned source-reviewed mappings.
Their calling sketches were not compiled or run. Reviews distinguish prepared
matrix forms, Schur factors, SIMD/ABI contracts, quantile-regression conventions,
bootstrap components and supplied-model forecasting. The midasmlpy success-status
and inactive-output defects and tidybench QR-workspace concern remain explicit;
these interfaces are not presented as checked numerical drivers. License notes
identify selected-source scope and missing explicit grants where applicable.

Heatcompact3d, SIPPP, laplace-2d, meshf, ElliFEM and the Gaussian-mixture
ARMA-GARCH model repository have eleven additional source-reviewed mappings.
Calling sketches were not compiled or run. Reviews identify periodic endpoint
layout and derivative scaling, fixed-step time integration, preconditioned
operator solves, change-based SOR termination and its saved iteration counter,
triangulation initialization risks, supplied-model statistical recursions and
the standalone finite-element workflow. ElliFEM is a program entry rather than
a callable solver; source-defined parameters, mesh data, dense storage and file
operations remain explicit. No project-wide grant is inferred from a bundled
dependency license, and numerical correctness is not inferred from source review.

The Powell optimization archive, DLA-Future-Fortran, ELPA, ARPACK_PARPACK,
forSISL and ARPREC have twelve additional pinned source-reviewed mappings.
Their calling sketches were not compiled or run. Reviews distinguish original
solver interfaces from external bindings, default-real versus double-precision
callbacks, linear-constraint relaxation, first-order stopping, distributed
storage/runtime setup and multiword precision state. ARPACK adaptation
persistence concerns and forSISL pointer/overlap-copy defects remain explicit.
The tanh-sinh review records mixed-precision bounds/callbacks and the fact that
a returned approximation with zero shared error status need not meet its target.
Folder-specific and custom license notices remain scoped to the reviewed code.

Historical PyMC2, system_dynamics, unstructured-finite-volume, DDD, wvdecomp
and python-bls have twelve additional pinned source-reviewed mappings.
Calling sketches were not compiled or run. Reviews distinguish probability
function evaluation from sampling/fitting, local Delaunay queries from a complete
triangulation, adjacent smooth levels from wavelet detail coefficients, and box
periodogram statistics from significance estimates. Saved interpolation state,
minimum sample counts, explicit RHS callback shape, solver attachment/status,
phase-bin wrapping limits and in-place coordinate normalization remain explicit.
The DDD root MIT notice is not substituted for the bundled BQPD terms; historical
component provenance and the unversioned wavelet license notice remain scoped.

Octree-mg, FERRE, HIRLAM Monitor, SLICOT-SystemIdentification and SciJit
have twelve additional pinned source-reviewed mappings. Calling sketches were
not compiled or run. FERRE polynomial fitting is marked as an intended mapping
with a suspected workspace dimension defect, rather than a checked driver.
The SLICOT entry is a MATLAB MEX gateway; SciJit entries document native
callback bindings without claiming independent verification of their backends.
Cycle semantics, shared state, precision settings and component licenses remain scoped.

SciJit and ANN-Fortran have twelve additional mappings and twenty newly
annotated public entry points. Calling sketches were not compiled or run.
SciJit coverage separates finite weighted quadrature, derivative-free and
user-Jacobian least squares, norms, spline representation operations and
Adams/BDF integration. Binding review does not certify every numerical backend.
ANN-Fortran contracts remain commented post-repair sketches: the reviewed bridge
has allocation/deallocation and public cleanup defects, with no execution check.

Coordinates, SOSIE and FSKlearn have ten additional source-reviewed mappings
and sixteen public entry-point annotations. Calling sketches were not compiled
or run. Reviews distinguish gridded interpolation from scattered inputs, native
regression prediction from external training, symmetric convolution from generic
weighted correlation, and gradient magnitude from gradient components. Mixed
precision, persistent flags/caches, missing-value/edge conventions and source
defects remain explicit. These findings do not certify the implementations.

NUMX, freeCappuccino and BaM have ten additional mappings and seventeen
public entry-point annotations. Calling sketches were not compiled or run.
Reviews separate descriptive statistics from inference, raw co-moments from
standardized shape measures, SPD from general sparse solves and configured
posterior sampling from a standalone density sampler. The NUMX normal-generator
contract remains commented until its uniform-return-kind mismatch is repaired.
Shared state, status limitations, residual checks and conflicting file-level
license notices remain explicit. No implementation is certified by these mappings.

TOOLIB, chunkmatc and SAM-lib have thirteen additional source-reviewed
mappings and sixteen distinct public entry-point annotations. Calling sketches
were not compiled or run. Reviews distinguish factor storage from original
matrices, normal equations from rank-revealing least squares, grid prolongation
from arbitrary-coordinate interpolation, fixed from adaptive quadrature and
per-leaf tolerance from global error control. FFT sign/normalization conventions,
legacy array extents, nonlinear-fit termination limits and skyline pivot
corrections remain explicit. Component license findings retain their scope.

Skyborn, ForTrilinos and pippy have ten additional source-reviewed mappings.
Calling sketches were not compiled or run. The review distinguishes native
Fortran numeric components from Python dispatch, statistics from complete
hypothesis tests, unit-index slopes from irregular-time regression, and public
Fortran wrappers from the C++ solver algorithms they select. Interpolation
directions, filter boundaries, initialized model state, solver error/status
channels and the Anasazi extraction capacity defect remain explicit. The
Skyborn nearest-grid assignment path is not promoted to an interpolation
mapping: its nonexact regular-grid branch uses uninitialized planar offsets.
Numerical Recipes provenance in pippy remains separately scoped.

ButterflyPACK, AUTO-07p and Cedar have ten additional source-reviewed
mappings. Calling sketches were not compiled or run. Reviews identify
precision-generated real/complex compressed linear algebra, initialized
continuation callbacks, collocation mesh services and independent polynomial
interpolation/differentiation/quadrature weight generators. AUTO Newton-Cotes
weights act on equally spaced samples, whereas its derivative weights are
evaluated at interior collocation nodes. Cedar transfer kernels require exact
C-interoperable interfaces and initialized BoxMG hierarchy data; correction
prolongation scales RES in place and includes residual terms. License findings
preserve the ButterflyPACK enhancement clause and optional dependency scope.

Dataplot has twelve additional source-reviewed mappings and fifteen public
entry-point annotations spanning statistical summaries, ranking/sorting,
Spearman correlation, straight-line fitting, distribution functions and
positive-real log gamma. Calling sketches were not compiled or run. The
reviewed Makefile promotes default REAL to eight bytes despite historical
single-precision comments. Character status, shared output dependencies,
workspace rules and degenerate-input conventions remain explicit. RANKCR
leaves CUTL99 unassigned; its full calling sketch is marked post-repair.
Historical distribution approximations are distinguished from full-precision
error-certified evaluations, including logistic-PDF overflow and large-rate
Poisson normal dispatch. The root NIST notice remains scoped to its evidence.

ScaLAPACK and PFLARE have twelve additional source-reviewed mappings and
thirteen public entry-point annotations. Calling sketches were not compiled
or run. ScaLAPACK reviews emphasize collective BLACS contexts, distributed
descriptors, local storage/workspace queries and driver-level status limits.
The triangular solve sketch selects the unit-diagonal path; the nonunit scan
resets its diagonal offset and can miss later zeros within a block. The banded
solver uses a distinct blocked layout and preallocated workspace. Optional SVD
back-transform calls can overwrite an earlier DBDSQR status. PFLARE
entries separate outer PETSc KSP solves from registered preconditioners and
fine/coarse splitting services; GPU, convergence and all kernel internals
remain outside the reviewed claims. Scoped license notices are preserved.

pyOpt and fastSHT have eleven additional source-reviewed mappings and
fourteen public entry-point annotations (SOLVOPT appears in two problem classes).
Calling sketches were not compiled or run. Native pyOpt interfaces differ
from their original solver headers: callbacks and explicit work arrays follow
the pinned executable calls. SLSQP workspace sizing follows the executable
check; COBYLA output values are reevaluated after final vertex selection.
The fastSHT CPU scope distinguishes raw ring FFTs from full spherical
transforms and records an allocator bounds mismatch that requires correction
before relying on initialization. These mappings do not certify numerical
accuracy, arbitrary parameter regimes or complete dependency licensing.

Dataplot has fourteen additional source-reviewed probability and special-
function mappings with twenty public routine annotations. These cover six
central distribution families and their inverses, plus log-beta and the
regularized incomplete-beta ratio. Calling sketches were not compiled or run.
Contracts distinguish integer chi-square/F degrees from real Student t
degrees, unit-scale gamma/Weibull families, promoted-real ABI and initialized
machine/output common blocks. Fixed stopping tolerances, numeric error
sentinels, support-boundary conventions, clipping and the integer 7-30 t
quantile branch inconsistency are documented without asserting numerical
verification. Existing reviews and scoped license evidence are retained.

ecTrans and FLAPWxHZ have four targeted source-reviewed mappings,
covering two previously documentation-only repositories. The six public
entry-point annotations identify five distinct routines; ZHZL1SA serves
two mathematical problem classes. Calling sketches were not compiled or
run. Transform entries distinguish spherical Legendre/Fourier work from
limited-area bifourier work and require initialized geometry/distribution.
The factor-based decomposition entries retain the author schedule/setup
example, alignment and OpenMP capacity requirements, and the non-LAPACK
INFO convention: a positive sweep count may represent normal completion.
No transform round trip, decomposition residual or kernel accuracy was
verified; the existing documentation reviews remain available.

Clawpack Riemann solvers and boxcode2d-legacy add two targeted PDE
mappings. Two [complete Riemann main programs](../drivers/riemann/README.md)
were compiled and run locally with GNU Fortran 17.0.0 20260510 (experimental)
on Windows, using bounds checks and floating-point traps. All 17 finite
Godunov-flux, jump/speed and conservation checks passed with zero maximum
discrepancy; [saved results](../drivers/riemann/results.json) retain compiler,
flags and normalized source/driver hashes. These checks apply only to the
two selected pointwise kernels, not a whole PDE time integrator. Their pages
distinguish locally checked main programs from uncompiled calling sketches
and provide downloadable source, runner and reports. The Poisson wrapper
remains uncompiled; review notes document unit-root scaling assumptions,
ignored selectors, default/four-byte integer compatibility, large workspaces
and unassigned TIMEINFO. No redistribution grant was found in its inspected
root/wrapper files, and its source is linked rather than bundled.

Two further mappings have complete locally checked main programs.
[NDSM Poisson checks](../drivers/ndsm/README.md) solve a manufactured
homogeneous-Neumann problem on 17x25 and 33x49 rectangular grids. The
maximum solution error decreases from 8.78906e-4 to 2.19727e-4 (ratio 0.25),
with independent interior residuals below 3.4e-12 and a zero-mean gauge.
[Chebyshev-node quadrature checks](../drivers/boxcode-quadrature/README.md)
verify 30 unweighted polynomial moments for orders 2,4,8,16, with maximum
error 1.7347e-16. Both use GNU Fortran 17.0.0 20260510 (experimental) on
Windows; reports retain exact flags, pins, dependency hashes and warnings.
The unmodified legacy quadrature object uses length-one dummy arrays and
was built without bounds instrumentation, while the main program was checked.
Only these specified numerical configurations are verified; the legacy
Poisson wrapper, OpenMP, 3-D optimized operators and other configurations
retain their separate unverified scope.

Two NDSM interpolation mappings now have [complete locally checked main
programs](../drivers/ndsm-interpolation/README.md): univariate piecewise-linear
interpolation (E1a) and gridded multilinear interpolation (E2a). All 157
known-value cases passed with bounds checks and floating-point traps using
GNU Fortran 17.0.0 20260510 (experimental) on Windows. Maximum errors were
1.655814e-16 and 6.692324e-16, below tolerance 5e-13. Tests include nondefault
coordinate bounds, unequal spacings, nonsquare grids, polynomial cross terms,
and lower-side extrapolation; scalar tabular checks distinguish piecewise
interpolation from a global fit. The function discards bracketing status and
extrapolates without clipping. General nonuniform, repeated-node, decreasing,
and high-dimensional cases remain unverified; source review and these finite
numerical checks do not certify arbitrary-data accuracy.

Three further Boxcode2D mappings have [complete checked spectral drivers](../drivers/boxcode-spectral/README.md):
Chebyshev nodal/coefficient basis conversion (E3c), derivative evaluation
(E3a2), and integration of fitted polynomials (E3a3). GNU Fortran 17.0.0
20260510 (experimental) on Windows passed all 116 polynomial cases and
30 additional endpoint checks at N=2,4,8,16. Maximum normalized errors were
3.275158e-15, 8.668621e-13 and 4.451610e-16, below tolerance 2e-11.
The unchanged legacy source object requires bounds instrumentation to be
disabled; main programs retain bounds checks and floating-point traps.
The integral matrix truncates to N coefficients, so exact-value checks and
the supported polynomial claim stop at input degree N-2. No arbitrary-data
accuracy, full-file memory safety, higher-order, threading or Poisson-solver
verification follows from these finite checks. Upstream source remains
linked rather than bundled under the existing scoped license finding.

Three FFTPack mappings now have [complete locally checked signal drivers](../drivers/fftpack-signals/README.md):
finite convolution (J2), the periodic analytic signal/Hilbert transform (J4),
and the real-input DFT (J1a1). GNU Fortran 17.0.0 20260510 (experimental) on
Windows passed all 175 direct-sum or analytic vector comparisons. Maximum
normalized errors were 3.608225e-16, 2.258517e-15 and 4.540382e-15, below
5e-12. Coverage includes unequal convolution lengths, odd/even and several
prime/mixed-radix FFT lengths, DC/Nyquist behavior, padding and truncation.
The wrapper and mains have bounds checks and floating-point traps; the legacy
backend has bounds instrumentation disabled and uses permissive argument
mismatch handling. Its storage conventions and ignored status remain explicit
ABI/portability limits. The single-precision Hilbert overload discards the
imaginary result and is outside the checked API. The original complex-wrapper
review remains historical source evidence; these finite checks do not certify
all kernels or arbitrarily sized transforms. Existing GPL/version and wrapper
license-scope findings are retained, and upstream source is not bundled.

Three Forsythe?Malcolm?Moler mappings now have [complete locally checked drivers](../drivers/fmm-interpolation-quadrature/README.md):
cubic spline construction/value evaluation (E1a), spline derivatives (E3a2),
and adaptive closed Newton-Cotes quadrature (H2a1a1). GNU Fortran 17.0.0
20260510 (experimental) on Windows passed 499 spline-value checks, 499
value/derivative vectors and 55 analytic integrals, with bounds checks and
floating-point traps on both the full module and the mains. Maximum normalized
errors were 2.220446e-16, 5.667141e-15 and 9.219847e-13. The spline reference
includes an independently derived non-affine natural spline; endpoint
conditions, extrapolation and a third-derivative jump remain explicit. Quadrature
uses 1,738 callbacks and checks reliability/evaluation outputs alongside analytic
values. Error estimates are not certified bounds; cached interval indices and
persistent resource-limit state constrain concurrency/history claims. Other
textbook algorithms and their earlier source reviews remain separate, and the
root MIT/inherited-source license finding is unchanged.

Two further FMM mappings have [complete checked SVD and ODE drivers](../drivers/fmm-svd-ode/README.md):
real rectangular SVD (D6) and explicit RKF45 initial-value integration (I1a1a).
All 48 square/tall matrix cases passed reconstruction, orthogonality, energy
and selected analytic-spectrum checks; maximum errors were 6.661338e-16,
1.110223e-15 and 8.889787e-16. All 211 analytic ODE states passed, including
forward/backward continuation, 176 one-step returns, initial equal-time output
and explicit tolerance adjustment/recovery. Maximum normalized state error was
8.110344e-10 with 2,507 callbacks. The unmodified module and mains used GNU
Fortran 17.0.0 20260510 (experimental), Windows, -O0, bounds checks and floating-
point traps. RKF45 helper state has INTENT(OUT) declarations despite retained-
value reads on continuation: this is an unresolved portability issue, and the
recorded passing run is not portable or optimized continuation verification.
SVD flags/shapes outside the stated contract, extreme scales, other recovery
paths and other compilers remain unverified. Existing source/license findings
are unchanged and the numerical source is not bundled.

Minila now has a [complete locally checked triangular-system driver](../drivers/minila-triangular/README.md)
for D2a3, with public `prim::diag_sub`, `::fwd_sub` and `::bck_sub` interfaces.
All 108 diagonal/lower/upper systems passed known-solution and independent
scaled-residual checks, covering N=1..12 and scales 1e-8, 1 and 1e8. GNU
Fortran 17.0.0 20260510 (experimental), Windows, used 32-bit default REAL,
full bounds checks and invalid/zero/overflow traps. Maximum relative solution
error was 1.726479e-7 and maximum scaled residual 8.948365e-8, below 5e-6.
These low-level routines do not validate triangularity or zero pivots, and
nonsquare error paths leave results undefined. The checked usage therefore
requires finite, correctly structured square systems with nonzero diagonals;
no error-bound, conditioning, invalid-input, dispatch-wrapper, LU/inverse/SOR
or double-precision claim is added. Existing source/license findings remain.

FFTPack now also has a [complete locally checked cross-correlation main](../drivers/fftpack-correlation/README.md)
for L10b2a. All four real/complex single/double overloads passed 588 comparisons
against independent finite direct sums, including unequal lengths, endpoint
impulses and zero inputs. Output lags are symmetric about zero using the longer
input length; complex Y is conjugated. Results are raw sums without centering,
variance normalization or overlap-count division. Maximum normalized errors
were 3.717673e-16 (binary64) and 5.062557e-8 (binary32). Wrapper/main bounds
checks and traps passed under GNU Fortran 17 O0 on Windows. The unchanged
legacy kernel still uses permissive argument matching without bounds checks;
its implicit storage ABI, large lengths, optimized builds and other compilers
remain unverified. Existing source and license findings are retained.

The FMM collection now has a [complete scalar-minimization main](../drivers/fmm-minimization/README.md)
for G1a1a using `ForsytheMalcolmMoler::BrentMin` and `::Fmin`. Both double
APIs passed 216 known-minimum tests on four smooth unimodal objectives,
three centers, widths and amplitude scales. Maximum width-normalized location
error was 7.381406e-8 and amplitude-normalized value error 2.664535e-15.
The main also checks callback counts and independently reevaluates the
reported function values. A deliberately exhausted one-iteration quadratic
probe reproduces a source defect: BrentMin leaves ERRCODE=0 although its
minimizer is wrong by about .036. Fmin hides status entirely. The mapping,
usage notes and driver README explicitly distinguish this probe from the
successful normal cases. Full bounds checks and floating-point traps passed
under GNU Fortran 17 O0 on Windows; no upstream source was modified.
No endpoint/global/non-smooth guarantee, optimized-build certification or
repair of the existing RKF45 continuation issue follows from these checks.

system_dynamics now has [complete statistics and covariance-eigenproblem mains](../drivers/system-dynamics-math/README.md).
L1a1a and L1a1b use the same 114 arithmetic-progression datasets for means,
weighted means and corrected sample variance; they are shared checks rather
than 228 distinct datasets. Maximum normalized statistic error was 2.197555e-16.
D4a1 is limited to positive-semidefinite input: EIGENCOV clips negative values,
sorts eigenpairs descending, uses exact-zero rank counting and STOPs on QL
failure. All 96 diagonal/rank-one/Toeplitz/dense-Gram cases passed residual,
orthogonality and trace checks. Module/main bounds checks and traps passed
under GNU Fortran 17 O0 on Windows. Modules additionally need GNU
-fno-range-check for the author's NaN/infinity constant initializers; no source
was modified. The extended review includes explicit Numerical Recipes notices
in AVEVAR/TRED2/TQLI/PYTHAG, so the license record now flags unresolved component
terms alongside the root MIT notice. No upstream numerical code is bundled.
Existing RK4/Akima source evidence remains unchanged and was not newly executed.

PowellOpt now has an independently maintained G2h1a1 interface review at the
same commit selected by the FPM playground. The public
`bobyqa_module::bobyqa` call has ten arguments, with the objective callback last
and workspace allocated internally. Links identify the complete argument list,
assumed-shape callback declarations and REAL64 precision selection. X is updated;
there is no returned F, status or evaluation count. The illustrative calling
program was not compiled or run for this review, and the pre-existing checked
playground quadratic driver remains separate. LICENSE.md records the BSD
three-clause modifications and the original Powell unrestricted-use notices;
the README's LICENSE link is outdated. The reverse metadata feed now has its
first selected-package match. This adds a local review of an already imported
repository rather than another distinct repository.

A selected-FPM interface batch adds 13 calling sequences across lbfgsb, fmin,
minpack and quadpack, with eight source-reviewed classifications. MINPACK covers
LMDIF1/LMDER1 least squares and HYBRD1/HYBRJ1 nonlinear systems. QUADPACK covers
DQAG, DQAGS, DQAGI, DQAGP, DQAWC, DQAWO and DQAWS, including the distinct callback
meanings and workspace formulas for weighted/singular problems. L-BFGS-B retains
its reverse-communication state contract and optional iteration-file argument;
fmin puts its scalar objective first and returns no convergence status. The
reviews use the exact selected upstream commits and record callback/precision
declarations and scoped license findings. Existing hosted numerical checks remain
separate; no new main programs were compiled or run. Four existing imported
repositories gain catalog-owned reviews, so the number of distinct repositories
remains 1,000. These interfaces feed the package catalog automatically after
refresh; each matching checked example is linked alongside its calling sequence.


A further selected-FPM interface review adds **23 calling sequences across ten
packages**: PCHIP (construction, evaluation and integration), FFTPACK (complex
forward/inverse transforms), specfun (Bernoulli numbers), specfunc-fullerton
(gamma, reciprocal gamma and digamma), Carlson elliptic integrals (RC/RD/RF/RJ),
fortran-bessels (I0/I1/K0/K1), polyroots-fortran (real Jenkins-Traub and real/complex
companion matrices), LSMR, MINRES and KISS conjugate gradients. The twelve
source-reviewed class claims use the exact selected package revisions. Links
identify argument declarations, callback contracts, public precision kinds and
reexports. The review records FFTPACK's unnormalized inverse, Fullerton's default
REAL interfaces, specfun's unwritten odd Bernoulli entries, and LSMR's executable
stopping codes where old comments disagree. MINRES's original CPL component is
kept separate from its MIT additions. These ten existing imported repositories
receive independent reviews; the catalog still has 1,000 distinct repositories.
No new main programs were compiled or run, and existing hosted driver claims
remain separate from the source/interface reviews.


A statistics and matrix-interface batch adds **23 calling sequences across ten
more selected FPM packages**: Fstats (eight descriptive-statistics array overloads),
forinv, foreig, forsvd, fordot, formatmul, FJsample, fortsa, lib_statistics and
econ-toolchain. Twelve source-reviewed claims document explicit storage, real
kinds, optional controls and diagnostic limitations at the selected package pins.
Generic names are retained alongside links to their specific implementations.
The notes distinguish sample and pooled variance, quantile interpolation, in-place
trimming, an absolute pseudoinverse cutoff, caller-supplied SVD factor buffers,
SYEV versus the default nonsymmetric eigensolver, and real jackknife bias scaling.
The CTSA-backed autocovariance interfaces count lag zero in their output length;
the Tauchen and stationary-vector routines require opposite matrix orientations.
The reviewed lib_statistics and econ-toolchain files do not establish a repository
reuse license, so neither is assigned a standard SPDX grant by inference.
These are independent reviews of existing imported packages, keeping 1,000
distinct repositories. Existing checked drivers remain separate; no new main
programs were compiled or run for this interface batch.


An object-interface batch adds **25 calling sequences across ten more selected
FPM packages**: roots-fortran (Brent), quadrature-fortran (1D/2D), bspline-fortran
(1D/2D auto-knot interpolation), DOP853, DDEABM, SLSQP, simulated-annealing, NumDiff,
LSQR and qdldl-fortran. Twelve source-reviewed claims describe initialization,
callback registration and numerical operations as object-bound calls. Public
module/type/binding names are recorded separately from implementation routine
names. Calls omit the implicit passed object; declaration links retain it and
identify callback parent classes and precision kinds. The notes distinguish
required outputs after optional controls, rank-one tolerance arrays, spline order
versus degree, LSQR stopping codes, and nonpivoted QDLDL's quasi-definite scope.
Error estimates and solver statuses are not promoted into correctness guarantees.
All reviews use the selected upstream pins; existing driver execution records
remain separate and no new main programs were compiled or run. The catalog still
contains 1,000 distinct repositories, with 35 playground imports now also having
independent local reviews.


A transforms/quadrature/interpolation batch adds **25 calling sequences across
ten more selected FPM packages**: Spectrum, fortran-primes, geodesic-fortran,
pointsets, GaussJacobiQuad, integrate_fortran, fortranlib, fortran-utils,
interpolation and fastmath. Seventeen source-reviewed claims distinguish full
and centered convolution, half-spectrum length/normalization, prime-value cutoffs,
degree-valued geodesic angles and required masked outputs, normalized random
spacings, allocatable-character quadrature selectors, nested integration bounds,
scalar/vector interpolation, trapezoid sums, limited real quadratic roots,
consistent-boundary splines, interval-versus-point mesh sizes and approximate
floating-point functions. Source comments referring to CC-BY-NC-4.0 components
in fortran-primes are retained alongside its root MIT notice; no MIT-only grant
is inferred for the complete library. pointsets retains its manifest MIT
declaration, while integrate_fortran's placeholder license is not promoted to a
resolved SPDX license. The 45 overlapping playground imports keep the catalog at
1,000 distinct repositories. These are interface/source reviews; no new main
programs were compiled or run, and numerical checked-driver scope remains separate.


A further public-interface review adds **25 calling sequences across ten selected
FPM packages**: finterp, mersenne-twister-fortran, fortran_function_parser,
orderpack, regridpack, splpak, pikaia, nlesolver-fortran, daglib and rklib.
The 13 scoped GAMS reviews include initialization/evaluation workflows for
linear and rectangular interpolation, MT19937-64 seeding and uniform draws,
expression parsing and error queries, ranking and partial sorting, least-squares
splines, genetic fitness maximization, dense nonlinear solving, dependency-graph
ordering and fixed-step classic RK4 integration. Bound calls use the public
binding and concrete type; signatures omit the implicit passed object and link
to argument, kind, callback and inherited-binding declarations.

The review records short-output ranking semantics, caller-validated partial-sort
bounds, extrapolation policies, object-status conventions and the pinned SPLPAK
evaluator's incorrect COEF INTENT(OUT) declaration. That defect is documented
rather than represented as a portable interface guarantee. No new numerical
drivers were compiled or run, and no package pin or hosted verification claim
was changed. Independent reviews now overlap 55 playground imports; the catalog
still contains 1,000 distinct repositories. Scoped license findings preserve
original and modernized component notices.


A numerical-utilities interface batch adds **25 calling sequences across ten
more selected FPM packages**: peaks, specialmatrices, fastconv, forpca,
rng-fortran, lookup-table-fortran, fordiff, fortran-search-and-sort, stringsort
and codata. The 12 scoped GAMS reviews cover signal-extremum searching,
structured tridiagonal construction/conversion/solving, valid convolution,
PCA, seeded uniform/normal/Poisson draws, linear lookup, numerical derivatives,
array searching/sorting, lexical/natural string sorting and physical-constant
lookup. Each signature links to exact pinned argument declarations, with
supporting links for generic overloads, bound objects, callback interfaces and
included/submodule implementations.

The notes distinguish confirmed signal extrema from endpoint candidates,
valid convolution from full convolution, uniform endpoint conventions,
normal-cache behavior on reseeding, lookup-table clamping and the caller's
column-index validation responsibility. PCA notes identify the pinned default
SVD variance convention, partially filled score outputs, reconstruction and
object-reuse limitations; the tridiagonal solver notes its lack of propagated
public error status. Derivative method strings, exact-match search semantics,
natural-sort integer limits and CODATA absent-entry behavior are explicit.
These are source/interface reviews, with no new numerical execution claims or
changes to hosted package pins. License findings retain incomplete root grants
and component notices where applicable. Independent reviews now overlap 65
playground imports; the catalog remains at 1,000 distinct repositories.


A cubature/geometry/graphics interface batch adds **25 calling sequences across
ten more selected FPM packages**: fortran_cubatures, dcuhre, rkf45, geompack,
rndgen-fortran, forcolormap, fsparse, iapws, rational_number and forimage.
The 11 scoped GAMS reviews cover reference-element integration rules, adaptive
hyperrectangle integration, retained-workspace ODE integration, planar geometry,
seeded random draws, palette lookup, dense/coordinate sparse conversion,
water saturation curves, bounded-integer rational arithmetic and PNM image
construction/transformation/export. Public generic, bound and external calling
conventions retain their distinct declaration links; no synthetic module name
is attached to external DCUHRE.

Notes specify quadrature reference measures and degree conventions, DCUHRE
callback/workspace/restart rules, RKF45 precision selection and continuation
flags, GEOMPACK point-order restoration on success, random integer scaling
limits, zero-based palette levels, sparse conversion initialization and a TINY
boundary defect, IAPWS MPa/kelvin units, rational denominator/overflow limits,
and image pixel layout and appended filename extensions. Scoped license
findings preserve ACM noncommercial terms, component palette notices and
incomplete manifest-only license evidence where applicable. No new numerical
drivers were compiled or run, package pins were not changed, and hosted
verification scope was not expanded. Independent reviews now overlap 75
playground imports; the catalog still contains 1,000 distinct repositories.


A solver/interpolation interface batch adds **25 calling sequences across ten
more selected FPM packages**: dvode, fitpack, nonlin, linalg, kdtree2,
differentia, stiff3, blas-interface, odrpack95 and nlopt-f. The 11 scoped GAMS
reviews cover object-aware Adams/BDF integration, spline loading/interpolation/
evaluation, Brent callback registration and solving, reusable square LU factors,
full dense SVD, pointer-owned nearest-neighbor trees, dual-number derivatives,
autonomous stiff integration, assumed-shape BLAS products, orthogonal-distance
regression and retained-callback local optimization.

Notes specify tolerance-array and continuation-workspace contracts, spline
degree/status conventions, procedure-pointer versus ordinary callback actuals,
LU singularity handling, full versus economy SVD storage, column-oriented
k-d tree data lifetimes and squared distances, allocatable AD error messages,
STIFF3 autonomous callbacks and half-step conventions, BLAS dimension/ABI
requirements, ODR model objects and weight ranks, and NLopt callback-wrapper
lifetimes and termination codes. Optional markers are checked against actual
OPTIONAL declarations, excluding comments and dimension-expression references.
Pinned declaration links include the relevant callbacks, kind parameters,
generic bindings and supporting types. Scoped license findings preserve
original/component notices. No new numerical driver was compiled or run and
no hosted package pin or verification scope changed. Independent reviews now
overlap 85 playground imports; the catalog remains at 1,000 distinct repositories.


A data-handling interface batch adds **25 calling sequences across ten more
selected FPM packages**: csv-fortran, json-fortran, toml-f, datetime-fortran,
m_sets, functional-fortran, fortran-fast-float, fortran-string-to-real,
fortran-shlex and forgex. Twelve scoped GAMS reviews cover tabular input,
document parsing and serialization, date construction and formatting, set
operations, functional array transformations, numeric parsing, command-line
tokenization and regular-expression matching.

Notes distinguish required status outputs from optional error channels,
allocatable results from caller-sized messages, missing values from parse
failures, and next-position parsing indices from counts of consumed characters.
They also record TOML default insertion, fixed date offsets and omitted timezone
suffixes, integer membership flags, pure callback contracts, restricted numeric
input grammars, tokenization without command execution, and regex validation
without a match guarantee. Every signature has pinned source and argument
declaration links; optional markers are checked against the declarations.
License notes preserve alternative licenses and explicitly identify absent
license evidence. No new driver was compiled or run, and no hosted package pin
or verification scope changed. Independent reviews now overlap 95 playground
imports; the catalog remains at 1,000 distinct repositories.


A utility interface batch adds **25 calling sequences across ten more selected
FPM packages**: test-drive, fortran_test_helper, ferror, fortime, argv-fortran,
popen-fortran, m_sort, m_list, m_color and flist. Twelve scoped GAMS reviews
cover test registration and execution, numerical assertions, error handling,
wall-clock timing, argument retrieval, process-output capture, sorting,
allocatable storage, key searches and color conversion.

The notes specify callback lifetimes and failure-count initialization, scalar
versus array tolerance boundaries, fatal-by-default error reporting, timing
state and loop averaging, absent process-status channels, in-place versus
permutation sorting, descending-order search/insertion conventions, color
ranges and status codes, and polymorphic list ownership. Component license
notices remain explicit, including the compact quicksort attribution. Every
sequence links its pinned implementation and argument declarations; public
generics and type-bound calls use their actual exposed names. No new driver
was compiled or run and hosted package pins and verification scope did not
change. Independent reviews now overlap 105 playground imports; the catalog
remains at 1,000 distinct repositories.


A text/input interface batch adds **25 calling sequences across ten more
selected FPM packages**: m_strings, m_io, m_time, m_cli2, m_attr, jonquil,
strff, iso_varying_string, utf8-f and ryu_fortran. Eleven scoped GAMS reviews
cover tokenization, wildcard matching, file/table/record input, calendar
conversion, command-option parsing, terminal markup, JSON parsing/serialization,
varying strings, Unicode byte validation and numeric-to-text formatting.

Notes distinguish delimiter sets from substrings, padded token arrays from
varying strings, record completion from raw IOSTAT, local offsets from UTC,
optional parser diagnostics from stopping paths, terminal escapes from HTML,
polymorphic JSON roots from object-only assumptions, and code points from
graphemes or display columns. Limitations of the pinned implementations remain
explicit: unimplemented Unicode escape decoding, incomplete calendar validation,
malformed numeric table rows, bounded formatting buffers, subnormal-to-zero
formatting and incomplete serializer error reporting. License evidence records
root/manifest discrepancies and absent project grants. Each sequence links its
pinned source and argument declarations; no new numerical driver was compiled
or run, and hosted pins and verification scope were not changed. Independent
reviews now overlap 115 playground imports; the catalog remains at 1,000 distinct
repositories.


A numerical/container interface batch adds **25 calling sequences across ten
more selected FPM packages**: fhash, kissfft-f, maptran3d, m_la,
fortran-simplify, forwarddiff, dnaoad-fpm, fglm, fortran_vector and rearrayfx.
Eleven scoped GAMS reviews cover hash-table storage/search, FFT planning and
execution, coordinate transformations, special matrices and row reduction,
polyline reduction, forward automatic differentiation, graphics transforms
and capacity-backed array containers.

Notes record key construction and getter type/status contracts, C-plan
initialization/finalization and precision, default-real geographic units and
optional height outputs, split-complex leading dimensions, row-oriented curve
points and stopping preconditions, dual-number callbacks and compile-time
derivative orders, graphics matrix layout/composition, and logical lengths
versus backing capacity. Ownership notes distinguish copied data, borrowed
pointers and invalidated views. Licenses preserve embedded/component notices,
the explicit BSD patent grant and absent licensing evidence. Public module
interfaces link their declarations and the implementing submodule evidence.
No new driver was compiled or run and no hosted package pin or execution scope
changed. Independent reviews now overlap 125 playground imports; the catalog
remains at 1,000 distinct repositories.


A file/configuration/native-binding interface batch adds **25 calling sequences
across ten more selected FPM packages**: ffilesystem, npy-for-fortran,
fortran-sqlite3, fortran-zlib, fortran-zstd, fortran-pcre2, fortran-regex,
m_match, config-fortran and paramcard. Twelve scoped GAMS reviews cover local
filesystem services, binary array output, database access, compression,
pattern encoding/search and typed configuration parsing.

Notes specify lexical versus filesystem path operations, native-endian NPY
assumptions and Fortran array order, SQLite callback and close/error-buffer
ownership, compression byte capacities versus lengths/status, PCRE2 handle
cleanup and zero-based code-unit offsets, integer flags versus indices, bounded
regex grammars, required configuration values and stopping validation summaries.
Direct C bindings retain their actual interoperable kinds and argument order;
Fortran wrappers use their exposed optional arguments. Evidence includes pinned
include files, C compatibility code and the full ISC grants named LICENCE.
Root/manifest license discrepancies remain explicit. No new driver was compiled
or run and no hosted pin or execution-verification scope changed. Independent
reviews now overlap 135 playground imports; the catalog remains at 1,000 distinct
repositories.


A numerical-interface batch adds **25 calling sequences across ten more selected
FPM packages**: rngff, opti, fortimize, forsolver, sparse_fortran, amosf90,
linalg_fortran, feq-parse, hrweno and diffeq. Fourteen scoped GAMS reviews cover
owned random streams, bounded optimization, linear/nonlinear systems, sparse
storage/products, complex Bessel sequences, symmetric eigenproblems, expression
evaluation, WENO reconstruction and ODE integration.

Notes distinguish public generics from private implementations, inherited
passed-object methods from the LINALG singleton's NOPASS bindings, callback
lifetimes, required initialization, caller-owned array shapes and optional
arguments. They record discarded solver status, fixed thresholds, storage-order
orientation, distinct Bessel scaling conventions, parser variable order, WENO's
unsafe omitted K and fixed-step endpoint overshoot. License notes preserve
component declarations and gaps instead of inferring grants from public access.
All calls and declaration ranges were checked against pinned source files; no
new numerical driver was compiled or run, and no hosted pin or verification
scope changed. Independent reviews now overlap 145 playground imports; the
catalog remains at 1,000 distinct repositories.


A containers/text/service interface batch adds **31 calling sequences across ten
more selected FPM packages**: collections, integer_set, scanner, array_range,
enclose, errstat, fed, for_fifo_queue, fortran-tokenizer and uint-fortran. Eleven
scoped GAMS reviews cover owned and borrowed container values, integer-set
initialization, cursor-based character reading, array-bound metadata, delimiter
construction, structured errors, edit-descriptor formats, fixed-width FIFO
allocation, callback tokenization and unsigned numeric conversions.

Notes distinguish copied values from borrowed pointers, constructor requirements
and explicit cleanup, scanner advance-before-read behavior, bounds-vector order,
paired-bracket reversal, success-status constants, descriptor constructors
from numeric intrinsics, token-list index/status limitations and integer-to-real
rounding. The native FIFO C source establishes ownership transfers and why
control-block destruction does not release queued payloads; allocator and
nonstandard LOC restrictions remain explicit. Every sequence links pinned
argument/result declarations and public exports. No new driver was compiled or
run, and no hosted pin or execution-verification scope changed. Independent
reviews now overlap 155 playground imports; the catalog remains at 1,000
distinct repositories.


A numerical-interface batch adds **25 calling sequences across ten more selected
FPM packages**: scifortran, qdutillib, forlab, nafpack, odepack, friction,
dynamics, nufft1d, nufft2d and conmin. Thirteen scoped GAMS reviews cover
sampled integration, orthogonal polynomial bases/operators, array generation,
variance normalization, Cholesky factors, direct and nonuniform Fourier
transforms, stateful ODE integration, simulation-model evaluation, structural
eigenmodes and constrained minimization.

Notes record sample-count restrictions, configured result precision, matrix and
basis storage, Hermite/Legendre normalization, direct DFT versus planned FFT,
NUFFT sign/centering and unequal type-1/type-2/type-3 scaling, collapsed-span
restrictions, ODE callback lifetimes and continuation status, friction sign and
zero-velocity behavior, angular versus cyclic frequencies and reverse-
communication workspaces. Fixed-form external routines retain their actual
non-module names and star-size declarations; public generics link to their
pinned implementations/declarations. Root license grants, public-domain notices
and adapted hosted subsets remain explicit. All sequences were checked against
pinned source; no new driver was compiled or run, and no hosted pin or numerical
verification scope changed. Independent reviews now overlap 165 playground
imports; the catalog remains at 1,000 distinct repositories.


A plotting/data-handling interface batch adds **30 calling sequences across ten
more selected FPM packages**: pyplot-fortran, befor64, fortran_stb_image, fmmap,
fortran-messagepack, h5fortran, nc4fortran, io-fortran-library, fortran_huffman
and ncio. Eleven scoped GAMS reviews cover script-based plotting, Base64,
RGB image storage, memory mapping, MessagePack, HDF5/NetCDF datasets, numeric
text I/O, string conversion and custom Huffman compression.

Notes distinguish plot construction from Python execution, character DPI and
required line labels/styles, allocated encoded output from fixed-length decoded
storage, image width/height order and value-returning loads, borrowed mapped
pointers and unmapping, codec construction and polymorphic payloads, explicit
file modes/closing, preallocated versus allocatable read destinations, rank-one
slice arrays, differing read/write header arguments and native stopping errors.
Huffman notes retain custom-format and fresh-tree restrictions. License evidence
includes the British-spelled LICENCE, embedded ncio grant, BeFoR64's stated
multi-licensing choices, fmmap's conflicting root/source notices and the absence
of an identified Huffman grant. All source hashes, calls and declaration ranges
were checked at exact pins; no new driver was compiled or run, and no hosted
pin or numerical verification scope changed. Independent reviews now overlap
175 playground imports; the catalog remains at 1,000 distinct repositories.

A parsing/container interface batch adds **30 calling sequences across ten more
selected FPM packages**: argparse-f, io_utilities, rojff, sqliteff, erloff,
smart-pointers, any, slinked-list, string-utf-8 and jeyemhex-regex. Ten scoped
GAMS reviews cover command/configuration input, JSON, SQLite, error reporting,
resource ownership, polymorphic storage, linked lists, UTF-8 and regular expressions.

The annotations distinguish required defaults from optional arguments, parser
STOP behavior, live TARGET associations, fallible JSON wrappers, explicit SQLite
cleanup and non-mutating error accumulation. Counter notes identify the pinned
last-release/finalization hazard; container notes retain exact-type/rank and
shallow-copy restrictions. UTF-8 notes avoid claiming full validation or grapheme
handling. Regex notes describe trimming, fixed output buffers and conflicting
root LGPL/source MIT notices without resolving those notices automatically.
Source hashes, formal arguments and declaration ranges were checked at exact
pins. No new driver was compiled or run and no hosted package pin changed.
Independent reviews now overlap 185 playground imports; the catalog remains at
1,000 distinct repositories.

An optimization/sparse-algebra/representation batch adds **27 calling sequences
across ten more selected FPM packages**: conmax, psqp, optgra, y12m, lusol,
strith, bstrith, list, penf and orbs. Ten scoped reviews document public solves,
setup/cleanup, sparse matrix norms, diagnostics, decimal and binary arithmetic,
linked-list sorting, numeric text conversion and bitset operations.

The calls link callback/kind declarations, workspace layouts and exact source
pins. Notes cover CONMAX's abstract solver and workspace error return, PSQP's
retained callbacks and advanced workspace entry, OPTGRA's merit slot, Y12M's
column/row arrays and destructive solve, and LUSOL's intermediate-error handling.
Utility annotations distinguish fixed capacity from arbitrary precision,
uninitialized binary-error results, list constructor/copy stubs, PENF sign and
parse-error behavior and stdlib-backed bit positions. License findings preserve
upstream notice requirements and choices, including Y12M's unidentified
library-wide grant. No new driver was compiled or run, no hosted pin changed,
and no backend redeployment is needed. Independent interface reviews now overlap
195 playground imports; the catalog remains at 1,000 distinct repositories.
