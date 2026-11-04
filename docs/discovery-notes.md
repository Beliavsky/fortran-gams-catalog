# Discovery notes

These are repository-discovery decisions, not failed compilation attempts. No
compiler or playground service was used for these reviews.

## Reviewed 2026-11-03

| Candidate | Decision | Evidence or reason |
| --- | --- | --- |
| [pytspack](https://github.com/noaa-oar-arl/pytspack) | Exclude the current revision from this Fortran catalog | Its [pinned README](https://github.com/noaa-oar-arl/pytspack/blob/306ca0771c4adc15ce346d99d8d178c38a464209/README.md) describes Python wrappers for a C implementation of TSPACK. The repository tree at that revision contains no Fortran source files. The older description in the discovery list is insufficient evidence for current Fortran coverage. |
| [F90-Extrapolation-Integration](https://github.com/irukoa/F90-Extrapolation-Integration) | Defer | The public GitHub URL returned “Repository not found” during review. The repository may have moved or become unavailable; this does not establish that the algorithm or original software is defective. Revisit if a current public source is identified. |
| [fDE](https://github.com/jklebes/fDE) | Defer | The public GitHub URL returned “Repository not found” during review. Revisit if the project moves or becomes publicly available again. No compilation was attempted. |
| [amber](https://github.com/octoflar/amber) | Defer | The public GitHub URL returned “Repository not found” during review. The older discovery-list description does not establish current source availability. No compilation was attempted. |
| [m_ad](https://github.com/octoflar/m_ad) | Defer | The public GitHub URL returned “Repository not found” during review. Revisit if a current public source is identified; no compilation was attempted. |
| [SELF](https://github.com/FluidNumerics/SELF) | Defer | The discovery-list public URL returned “Repository not found” during review. Revisit if a current public source is identified; no compilation was attempted. |
| [Knuth-Eve algorithm](https://github.com/ammrat13/knuth-eve-algorithm) | Defer | The public URL returned “Repository not found” during review. This is a source-availability decision, not an assessment of the algorithm. |
| [nlopt-wrap](https://github.com/awvwgk/nlopt-wrap) | Already covered under the current identity | GitHub resolves this address to [awvwgk/nlopt-f](https://github.com/awvwgk/nlopt-f), which is already present in the playground import. No second repository entry was added for the old address. |
| [IntegralALL](https://github.com/neutrinomuon/IntegralALL) | Include under its current name, PyIntegral | GitHub resolves the former address to [neutrinomuon/PyIntegral](https://github.com/neutrinomuon/PyIntegral). The canonical identity is `github:neutrinomuon/pyintegral`; the original list address is retained in discovery metadata and `integralall` is a searchable topic. |
| [HOPR at flexi-framework](https://github.com/flexi-framework/hopr) | Include the documented successor | The [old pinned README](https://github.com/flexi-framework/hopr/blob/45ab6435f242d6212e653ededda76a7656802104/README.md) says development moved to [hopr-framework/hopr](https://github.com/hopr-framework/hopr); its tree contains only documentation/license files. The successor is cataloged with pinned evidence, and the original list address is retained in discovery metadata. |
| [fmpl](https://github.com/supercomputerprimesearch/fmpl) | Defer | The listed public repository returned “Repository not found” during review. Revisit if a current public source is identified; no compilation was attempted. |
| [linprog](https://github.com/loiseaujc/linprog) | Defer numerical coverage | The reviewed README is a project placeholder; the [pinned module](https://github.com/loiseaujc/linprog/blob/b073fdfa908b17bbff5ddf88debdf2197baa0f79/src/linprog.f90) only implements `say_hello`, not linear programming. A solver classification based on the repository name would be unsupported. Revisit when a numerical implementation is available. |

## Reviewed 2026-11-04

| Candidate | Decision | Evidence or reason |
| --- | --- | --- |
| [PFLARE at stevendargaville](https://github.com/stevendargaville/PFLARE) | Include under its current organization | GitHub resolves the listed address to [PFLAREProject/PFLARE](https://github.com/PFLAREProject/PFLARE). The current identity is recorded once, with [pinned documentation](https://github.com/PFLAREProject/PFLARE/blob/20ca09c479461c12cf60970a53055d973765e0a2/README.md), while discovery metadata retains the original address. |
| [SciFortran at QcmPlab](https://github.com/QcmPlab/SciFortran) | Already covered by the maintained successor | The [pinned archived README](https://github.com/QcmPlab/SciFortran/blob/f343d32bc7578671096faa490b330eee4d4011ff/README.md) says development moved to [SciFortran/SciFortran](https://github.com/SciFortran/SciFortran), which is already in the catalog. No second entry was added for the archived predecessor. |
| [MRMCaov](https://github.com/brian-j-smith/MRMCaov) | Defer current Fortran coverage | The [reviewed repository tree](https://github.com/brian-j-smith/MRMCaov/tree/d79e49bcef42ef2a17195aae84ca84ae569f8702) has no `src/` files or Fortran source files. Its README describes an R statistical package. The older discovery-list description of underlying Fortran is insufficient evidence for direct Fortran coverage at this revision; this is not an assessment of the statistical methods. |
| [monolis_utils](https://github.com/nqomorita/monolis_utils) | Defer | The listed public GitHub address returned “Repository not found” on repeated checks. Revisit if a current public source is identified; this does not assess the algorithms or the separately cataloged monolis solver. |
| [Dario Maglio Numerical Methods](https://github.com/Dario-Maglio/Numerical_Methods) | Defer | The listed public GitHub address returned “Repository not found” on repeated checks. No compilation was attempted; revisit if the project moves or becomes publicly available again. |
| [rpn-calc-fortran](https://github.com/scivision/rpn-calc-fortran) | Already covered under its current name | The listed address redirects to [scivision/rpn-calculator-fortran](https://github.com/scivision/rpn-calculator-fortran), which is already cataloged. The [reviewed README](https://github.com/scivision/rpn-calculator-fortran/blob/7708e4949f17511d81f4e7dd0271a500f0bc3631/README.md) also uses the current name; no duplicate project was added. |

The discovery source was the [pinned Fortran code on GitHub list](https://github.com/Beliavsky/Fortran-code-on-GitHub/blob/f5ab25294a12ed004d5a8934200ca8e26ac2e825/README.md).
Repository descriptions can become outdated, so new entries are checked against
their own pinned documentation or source interfaces before classification.
