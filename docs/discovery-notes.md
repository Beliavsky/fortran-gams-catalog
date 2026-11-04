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
| [IntegralALL](https://github.com/neutrinomuon/IntegralALL) | Include under its current name, PyIntegral | GitHub resolves the former address to [neutrinomuon/PyIntegral](https://github.com/neutrinomuon/PyIntegral). The canonical identity is `github:neutrinomuon/pyintegral`; the original list address is retained in discovery metadata and `integralall` is a searchable topic. |

The discovery source was the [pinned Fortran code on GitHub list](https://github.com/Beliavsky/Fortran-code-on-GitHub/blob/f5ab25294a12ed004d5a8934200ca8e26ac2e825/README.md).
Repository descriptions can become outdated, so new entries are checked against
their own pinned documentation or source interfaces before classification.
