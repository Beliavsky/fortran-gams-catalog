# Expression parsers

Reviewed on 2026-11-12. The [expression-parser topic page](https://beliavsky.github.io/fortran-gams-catalog/topics/expression-parsers/) covers 15 projects: four existing reviews and 11 added repositories. This is catalog coverage, not an addition to the hosted FPM selection or a new compilation check.

Use the Topic selector or share `?topic=expression-parser`. Capability filters are `scalar-evaluation`, `array-evaluation`, `complex-evaluation`, `custom-functions`, `parser-derivatives`, `expression-code-generation`, `reusable-parser`, and `calculator-cli`. They combine with the existing license, source-review, collection and FPM filters. Internal navigation retains the topic and GAMS counts reflect its intersection with source-review, license and FPM filters.

Capabilities below summarize pinned author documentation and scoped interface reviews. Missing capabilities mean not established by this review, not necessarily unsupported. Array evaluation distinguishes array-valued arithmetic or batched inputs from an array of separate scalar expressions. A reusable parser is callable from a Fortran program; it need not be stateless or thread safe. Source-reviewed filtering applies to GAMS mappings, not to every capability on a card.

Parsing/evaluation is recorded under N3 (Character manipulation), following the existing parser reviews. It does not by itself justify O (Symbolic computation). fparse additionally has a documentation-reviewed H1 claim for first derivatives; no source review of all derivative kernels or new numerical validation is claimed. Its user-function derivative fallback may use finite differences.

## Capabilities and evidence

The evidence column identifies the reviewed documentation commit; SHA-256 hashes below use UTF-8 text normalized to LF. Existing source and license evidence remains in the project pages and [review ledger](local-reviews.md).

| Repository | Recorded capabilities | Pinned capability documentation |
| --- | --- | --- |
| [hassaniriad/calmat](https://github.com/hassaniriad/calmat) | Vector / matrix evaluation, Command-line calculator / interpreter, Complex arithmetic, User-defined functions / callbacks, Callable parser library, Scalar evaluation | [README.md](https://github.com/hassaniriad/calmat/blob/f4f3a40911af2f0a34f3e4d930c912fc0362f908/README.md) |
| [FluidNumerics/feq-parse](https://github.com/FluidNumerics/feq-parse) | Vector / matrix evaluation, Callable parser library, Scalar evaluation | [README.md](https://github.com/FluidNumerics/feq-parse/blob/2e80c5940b128a52c5070a3f56909674fb85a379/README.md) |
| [jacobwilliams/ffp](https://github.com/jacobwilliams/ffp) | Callable parser library, Scalar evaluation | [README.md](https://github.com/jacobwilliams/ffp/blob/e675c699db56aeb90fec35c2be5d9c4792946d37/README.md) |
| [FortranGoingOnForty/fortbite](https://github.com/FortranGoingOnForty/fortbite) | Vector / matrix evaluation, Command-line calculator / interpreter, Complex arithmetic, Scalar evaluation | [README.md](https://github.com/FortranGoingOnForty/fortbite/blob/a9a7856383a5b46ae172e490d376bfbf1c8f5591/README.md) |
| [muhammad-fiaz/fortran-calc](https://github.com/muhammad-fiaz/fortran-calc) | Command-line calculator / interpreter, Scalar evaluation | [README.md](https://github.com/muhammad-fiaz/fortran-calc/blob/fa8adacd038a60fff77e20ea93910b3c9582cc04/README.md) |
| [ivomarb/Fortran-Expression-Evaluator](https://github.com/ivomarb/Fortran-Expression-Evaluator) | Callable parser library, Scalar evaluation | [README.md](https://github.com/ivomarb/Fortran-Expression-Evaluator/blob/9d644395c979a837e5cb5bfc6ece664c9b1c7e42/README.md) |
| [jacobwilliams/fortran_function_parser](https://github.com/jacobwilliams/fortran_function_parser) | Callable parser library, Scalar evaluation | [README.md](https://github.com/jacobwilliams/fortran_function_parser/blob/4c977c925506bea3fb1ee44aac08114c5fa68a71/README.md) |
| [sdm900/fortran_parser](https://github.com/sdm900/fortran_parser) | Derivatives of parsed expressions, Callable parser library, Scalar evaluation | [README](https://github.com/sdm900/fortran_parser/blob/dde08ec09417f92a42ca4159294c999edd94a464/README) |
| [sdm900/fortran_script](https://github.com/sdm900/fortran_script) | Command-line calculator / interpreter, User-defined functions / callbacks, Scalar evaluation | [README.md](https://github.com/sdm900/fortran_script/blob/fd8efe16e23e20b919edadfea0b1ad1e42c686ab/README.md); [GUIDE.md](https://github.com/sdm900/fortran_script/blob/fd8efe16e23e20b919edadfea0b1ad1e42c686ab/GUIDE.md) |
| [jacopo-chevallard/FortranParser](https://github.com/jacopo-chevallard/FortranParser) | Callable parser library, Scalar evaluation | [README.md](https://github.com/jacopo-chevallard/FortranParser/blob/ead4ea2a5f20ce62c86427b9319e4a383672dd2e/README.md) |
| [jacobwilliams/fparse](https://github.com/jacobwilliams/fparse) | Vector / matrix evaluation, User-defined functions / callbacks, Fortran code generation, Derivatives of parsed expressions, Callable parser library, Scalar evaluation | [README.md](https://github.com/jacobwilliams/fparse/blob/5fdd81f5680ab7b46ba4910165544c18365f2b67/README.md) |
| [sgeard/hp](https://github.com/sgeard/hp) | Command-line calculator / interpreter, Complex arithmetic, Scalar evaluation | [README.md](https://github.com/sgeard/hp/blob/1fc3efba12ac3f1fd9769aef0544b08c327887da/README.md) |
| [urbanjost/M_calculator](https://github.com/urbanjost/M_calculator) | Command-line calculator / interpreter, Callable parser library, Scalar evaluation | [README.md](https://github.com/urbanjost/M_calculator/blob/b6bbc08f81eb158a6908a42016059815fe72217d/README.md) |
| [urbanjost/M_matrix](https://github.com/urbanjost/M_matrix) | Vector / matrix evaluation, Command-line calculator / interpreter, User-defined functions / callbacks, Callable parser library, Scalar evaluation | [README.md](https://github.com/urbanjost/M_matrix/blob/3450ca5585ada2d12942b91a6a50ebc8524a6199/README.md) |
| [14NGiestas/shunting-yard-fortran](https://github.com/14NGiestas/shunting-yard-fortran) | User-defined functions / callbacks, Callable parser library | [README.md](https://github.com/14NGiestas/shunting-yard-fortran/blob/ff62d83502bc5fdf77f2750c3538b8634a543b91/README.md) |

## Scope and relationships

- `fparse`: independently reviewed scalar parse/set/evaluate/get interfaces, derivative retrieval, callback registration and code-generation entry point. Input sizes must be set before generation; generated text is not compiled by that call. Status can be cleared by subsequent operations, so inspect each operation immediately. First-derivative capability is documented; no new derivative correctness check was run.
- `fortran_function_parser` and `FortranParser`: Schmehl-fparser descendants, not independent algorithm families. The former stores errors for inspection; the latter can terminate on a syntax error and has fixed text buffers. Both compile expression bytecode, which is different from emitting Fortran source. New calling sketches remain explicitly uncompiled.
- `feq-parse`: existing scalar and batched REAL64 calling sequences are retained. Batched X has shape (points, variables). Its constructor has no returned validity flag and its evaluation stack has fixed capacity.
- `M_calculator`: existing signatures retain shared module state, case sensitivity and left-associated successive powers. It reparses on each evaluation; no bytecode-reuse claim is made.
- `shunting-yard-fortran`: existing callback signatures are retained. The author labels it experimental and notes global token registration, fixed precedence and incomplete syntax validation. A reusable callback library is not necessarily safe for concurrent parser configurations.
- `calmat` and `M_matrix`: embedded mathematical languages with callable entry points and interactive use, rather than identical scalar-parser APIs. Numerical kernel coverage and accuracy were not reviewed in this batch.
- `fortbite`: its README explicitly says ::digits changes display precision only and computations use double precision. The introductory arbitrary-precision claim is not adopted. Complex and matrix features are documented, not newly tested.
- `fortran-calc`: nested arithmetic expressions do not imply complex-number arithmetic. This entry is a command-line tool, not a reviewed callable parser API.
- `ffp` is an unofficial mirror of the older LAB Fit parser; `Fortran-Expression-Evaluator` is a related author project. Shared origins do not establish file equality. Historical author timing comparisons are not current catalog benchmarks. The mirror's License: Free label is not treated as a specific reuse grant.
- `fortran_parser`: documented error-limit propagation is discoverable as a derivative-related capability, not a reviewed general Jacobian API or an inferred H1 mapping. Its optional error text can accompany a stale numerical result.
- `fortran_script`: a small, incomplete Fortran-like interpreter. Its guide documents user routines, arrays, loops and scalar double-precision expressions; arrays alone do not establish vectorized evaluation.
- `hp`: five-level RPN calculator with real/complex modes and statistics. Compiler restrictions in the README remain relevant; no gfortran build or arbitrary-precision claim is made.

## List entries outside this selection

The [Expression Parsers section](https://beliavsky.github.io/Fortran-code-on-GitHub/#expression-parsers) also contains:

- [FortFront](https://github.com/lazy-fortran/fortfront): a Fortran frontend and source transformation tool. It fits software-development discovery rather than this mathematical expression-evaluator selection. No new GAMS mapping was added in this batch.
- [spreadsheet-fortran](https://github.com/lwsinclair/spreadsheet-fortran): a deliberately FORTRAN IV/66 historical spreadsheet application. Its formula engine is relevant background, but it is outside the catalog's emphasis on reusable modern Fortran numerical software. No entry was added in this batch.

Neither was silently classified as a mathematical parser library. Repository-specific license notices and dependencies must still be checked before reuse.

## Capability document hashes

- `hassaniriad/calmat` / `README.md`: `48cec388218b9f919710686530ec59a52da28c8f36df93724581b06768059b81`
- `FluidNumerics/feq-parse` / `README.md`: `d6221482113b8da31e4d2aad6b5f11d10bb55792e3f2c633ce77532f4114f72e`
- `jacobwilliams/ffp` / `README.md`: `3d4c38dbd9b15f62b17a2481858cb899251f514dbf6cd307203276647d5c8967`
- `FortranGoingOnForty/fortbite` / `README.md`: `9a42b1ac0d9e0d2cf1731262ef464e9a3f38872d928fd1dae103a19dcf27b273`
- `muhammad-fiaz/fortran-calc` / `README.md`: `90fbd500ce4bfd4c3d640bbc41ee46ada4a1bb6a98ec160a86ea32e199afb11c`
- `ivomarb/Fortran-Expression-Evaluator` / `README.md`: `752e6c9ef0d39c1dbefede6247050ce31164c028d091b44a1cade316dea146f2`
- `jacobwilliams/fortran_function_parser` / `README.md`: `d3d6630ba1e901f35b9ae1ad5d5f14dd247d24242530a542dd63fb572f42d76b`
- `sdm900/fortran_parser` / `README`: `4af7c3fb17e532d7bda26326cdbc0cdfb628e2ed29cd47895570236fc524974a`
- `sdm900/fortran_script` / `README.md`: `9bd026f7f7a2a275eab0aca52a2542fcb0db99dd0ad8d849ca460ba7c624cbcb`
- `sdm900/fortran_script` / `GUIDE.md`: `6a1a2dced20b92f34771b53d36a0cfa5e9e01bcf421fc4db2d276450ba4da390`
- `jacopo-chevallard/FortranParser` / `README.md`: `f6d062ecf6eb4eb5fe2b616b16b9e656eda53d4c9767993d8b44c86fe571ffe1`
- `jacobwilliams/fparse` / `README.md`: `9e2a29e688e7cb4fc2bc8f5f0a24d31f9791c2307ab4aa68fae398d2ea54a560`
- `sgeard/hp` / `README.md`: `2d9d056f61f28c71ba93bf9891dda23026ef7b510b7dd2a599b419afb66db799`
- `urbanjost/M_calculator` / `README.md`: `03a8865e541ed87801e047709a18dd011d4ea361c59e6fa0280858dc6b13b58e`
- `urbanjost/M_matrix` / `README.md`: `a651ca785f1a377e50646ccfce83845f01339130e2fbccea47e3071170a05e71`
- `14NGiestas/shunting-yard-fortran` / `README.md`: `91a43a4d7e9e5127576576430faf455e7264daa40e36973cd7acc4804a95f3de`
