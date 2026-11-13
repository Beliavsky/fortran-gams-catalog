# Fortran software by GAMS classification

Every site build also publishes `reviewed-metadata.json`, a deterministic feed
of independently authored license and source-procedure reviews. Only the local
review layer is exported; saved playground imports, private implementation
helpers and execution-verification records are excluded. The FPM playground's
`xcatalog_reviews.py` can consume this feed, matching repository identities and
exact pinned revisions and preserving local overrides. This permits shared
review maintenance without a circular playground-import/export loop.
Uncompiled usage sketches remain explicitly unchecked; a local numerical test
does not become a hosted playground check. Selected FPM packages with independent
interface/data reviews cover all 298 selected packages, including PowellOpt, MINPACK,
QUADPACK, PCHIP, FFTPACK, polynomial roots and iterative linear solvers. Further
selected packages can gain local reviews using the same evidence format as any
other repository. Constants-only modules and template instantiations are explicitly
labeled; they are not presented as callable procedures. Playground-only adapters
are distinguished from upstream public APIs.

A static catalog for finding Fortran numerical software by mathematical problem.
It includes repositories that do not use FPM or run in an online playground.

The saved catalog imports **298 playground packages** and their classifications,
procedure evidence and checked driver links, alongside **1011 catalog-owned
repository reviews**. All 298 playground packages overlap catalog-owned reviews, giving 1,011
distinct repositories. Counts describe the saved snapshot and change on refresh.
Browse the GAMS hierarchy, search names/authors/topics/procedures, or filter for
independent reviews. Each repository has a detail page with evidence links.

Browse [automatic differentiation](https://beliavsky.github.io/fortran-gams-catalog/topics/automatic-differentiation/)
or use the Topic selector for forward/reverse mode, higher derivatives,
sparse Jacobians, matrix derivatives and conversion helpers. These curated facets
combine with the other filters and can be shared with `?topic=forward-mode`.
[Recorded capabilities and scope](docs/automatic-differentiation.md) distinguish
documented features from narrower source reviews. AD alone does not establish
symbolic expression manipulation: O links to the topic without blanket remapping.

Browse [expression parsers](https://beliavsky.github.io/fortran-gams-catalog/topics/expression-parsers/)
for 15 callable evaluators, calculators and embedded interpreters. The Topic
selector also supports scalar, array and complex evaluation, custom functions,
derivatives and Fortran code generation. Share, for example,
`?topic=expression-parser` or `?topic=parser-derivatives`. These filters combine
with license, source-review and FPM exclusions. [Capabilities and review scope](docs/expression-parsers.md)
identify pinned evidence, parser families, error-handling limitations and
documentation-only claims. Expression evaluation alone does not establish
symbolic algebra, arbitrary precision or a verified numerical result.

Select **Exclude known FPM packages** to hide repositories whose recorded build
systems include FPM, including independently reviewed ones. GAMS category counts
update and the selection follows catalog links; it can be shared with
`?exclude_fpm=1`. Repositories with unreviewed build support remain included, so
this filter is not proof that every remaining repository lacks FPM support.

Select **Only source-reviewed mappings** to restrict results, displayed class
labels and GAMS counts to classifications supported by reviewed source code.
This includes independent reviews and source-reviewed procedures imported from
the playground. On a GAMS page, a reviewed mapping must match that class or a
descendant. Combine it with the other filters or share `?source_reviewed=1`;
the selection follows catalog links. Repository detail pages retain the full
evidence record. Source review does not imply compilation or numerical testing.

For entries whose calling interfaces have been reviewed, cards identify public
entry points using `module_name::procedure_name` where applicable, with pinned
source paths and line numbers. Click a usage line to open the argument
declarations. Detail pages distinguish public generics, private helpers,
callbacks and standalone programs, and include calling sketches or author
examples where recorded. These are usage references, not new execution checks.

In **Filters**, select **Highlight output arguments** to italicize recorded
`intent(out)` arguments and show `intent(inout)` arguments in bold italic.
Input arguments and arguments without recorded intent remain unmarked.
Hover over or keyboard-focus an annotated argument to see its explicit intent;
click the usage link to read the source declarations. The preference is saved
in the browser when local storage is available and does not filter results.
Highlighting is off by default and applies to cards and project detail pages.

The saved review covers every recorded usage line: 1,786 checked records and
22 cases where Fortran argument intents do not apply. There are 6,203 argument
annotations in 1,340 usage records across 591 projects. An interface can recur
under multiple GAMS classifications, so these are metadata record counts, not
counts of unique upstream routines. Unannotated arguments can legitimately
lack explicit `INTENT`. The [argument-intent coverage page](https://beliavsky.github.io/fortran-gams-catalog/argument-intents/)
and downloadable Markdown/JSON reports regenerate with every site build and
identify new usages still awaiting review.

Annotations retain the pinned declaration, specific overload, source dummy name
when different from the displayed name, and call index for multi-call examples.
Function results and implicit passed objects are not assigned an intent.
Conditional intents remain unmarked; hover or focus to see the alternatives.
The MATLAB gateway invocation and an interoperability adapter with an
incompatible upstream Fortran declaration are explicitly documented exceptions.
These are interface reviews, not new compilation or numerical checks.

To check declarations again, run the conservative source-review utility:

```powershell
python xargument_intents.py --fetch
```

It retrieves missing files at pinned commits, verifies source hashes, and
writes `_site/argument-intent-review.md` and `.json`. It leaves catalog metadata
unchanged unless `--write` is added. Cached reruns can omit `--fetch`; ordinary
site builds use saved metadata and never download sources. Review findings
before using `--write`, then run `python xreviews.py` and the tests. Explicit
exceptions in `data/argument-intent-overrides.json` must match the exact source
revision and procedure record. See the [review policy](docs/review-policy.md)
for the annotation format and scope limitations.

Cards and detail pages also show **License**. Reviewed labels link to license
evidence at a pinned commit; imported labels are marked as imported metadata.
Entries without recorded terms say "License not yet reviewed". The review ledger
records the evidence and scope of independent license reviews.

The **License** filter groups recorded terms as permissive, weak copyleft,
strong copyleft, custom or mixed, or unclear/not yet reviewed. Select
**Reviewed license evidence only** to exclude imported license metadata and
unreviewed entries. A reviewed finding that no grant was identified remains in
the unclear group. Both filters combine with source-review and FPM filters,
update GAMS category counts, and follow catalog links. Share, for example,
`?license=permissive&license_reviewed=1`.

License groups describe recorded terms, not guaranteed compatibility with a
particular project. Check the pinned notices and component/dependency terms.
Standard license expressions respect `AND` (both required) and `OR` (a choice);
an available permissive option qualifies under Permissive. Scoped prose,
unrecognized terms, and license exceptions remain Custom or mixed until
explicitly supported. A missing SPDX identifier alone does not mean unlicensed.

Select **Include original GAMS/Netlib entries** to add an optional historical
source-available collection to searches and GAMS category pages. It is off by
default and shareable with `?legacy_gams=1`. The initial pilot lists nine
double-precision QUADPACK entry points from the Netlib index, which supplies
their GAMS codes. NIST's dynamic pages returned HTTP 403 during setup; these
are Netlib-derived records, not a retrieved copy of NIST's module database.

Each imported entry links its source, original GAMS classes, import provenance,
retrieval date, source/index checksums, and related modernized GitHub projects.
Related implementations are not assumed identical. These entries have not been
independently source-reviewed, compiled or checked here, and their licenses
remain unreviewed. Both review-only filters exclude them; the Unclear license
filter includes them when the collection is enabled. Proprietary references
such as IMSL and NAG are outside this pilot.

The collection stays in `data/imports/gams-netlib.json` and is published
separately as `legacy-gams.json`; it never overwrites our repository reviews or
changes `catalog.json`. Refresh it explicitly with:

```powershell
python ximport_gams.py
```

The refresh checks source availability and expected Fortran entry-point names,
then validates the complete snapshot before replacing it. It does not compile
the routines or download their dependencies. Normal site builds remain offline.
Without JavaScript, these optional entries remain hidden on listings; their
individual detail pages can still be opened directly.

New discovery reviews start with broad GAMS divisions. More granular classes
and procedure mappings are added through later reviews of individual repositories.
Detailed numerical-method reviews include source-linked
classifications and explicit limits where no leaf fits; see
[the review progress](docs/granular-reviews.md).

The existing [playground package catalog](https://beliavsky.github.io/fortran-playground/gams/)
continues to focus on selected packages and runnable examples. This broader
catalog starts with documentation reviews and can grow into granular procedure
mappings and locally runnable drivers. Review levels are separate from package
availability and build success.

## Build and preview

Requires Python 3.10 or later. No third-party Python packages, compiler, Modal
account or playground checkout is needed.

```powershell
python -m unittest discover -s tests
python xbuild.py
python -m http.server 8000 --directory _site
```

Open <http://localhost:8000/>. Every class and repository page is static HTML and
works without JavaScript. JavaScript adds search and bookmarkable query filters.
If Node.js is installed, the tests also exercise the browser search script. CI
installs Node.js so that this check always runs there.
The saved feed and local review data are small text files; no binaries or
precompiled packages are stored here.

## Update the imported data

```powershell
python xrefresh.py
python -m unittest discover -s tests
python xbuild.py
```

Or import a freshly generated local playground export:

```powershell
python xrefresh.py --feed ..\fortran-playground\catalog-export\catalog-v1.json
```

Refresh is explicit. Ordinary builds and page visits make no GitHub API or
compilation-service requests. Local reviews in `data/local.json` survive imports;
matching repositories are merged by canonical identity. The website provides the
layered JSON and taxonomy for other catalogs to reuse.

The seed was generated from the local playground checkout, with the feed's
original provenance retained. `vendor/provenance.json` pins the reused validator
and merger to their originating source version. The export function in that
vendored module is unused; builds do not depend on the playground's other tools.

## Add or review software

See [review policy](docs/review-policy.md), [independent reviews](docs/local-reviews.md)
and [driver requirements](drivers/README.md).
The [local Riemann checks](drivers/riemann/README.md) provide complete main
programs, a pinned-source build runner and saved numerical results.
Further checked main programs cover [NDSM Poisson](drivers/ndsm/README.md)
and [Chebyshev-node quadrature](drivers/boxcode-quadrature/README.md). Each new classification needs pinned
evidence and scope notes. Build systems can be Make, CMake, custom scripts or
unreviewed; FPM compatibility is not an inclusion criterion.

The independent reviews cover differentiation, interpolation, linear algebra,
multiple precision, nonlinear systems, quadrature, differential equations,
optimization, random sampling, special functions, sorting, computational geometry
and time-series methods. Some
repositories use FPM and others use Make, CMake or other build arrangements.
They are documentation-reviewed entries, not additional precompiled packages.
After editing `data/local.json`, regenerate the review ledger:

```powershell
python xreviews.py
```

## Audit calling-sequence coverage

Run the offline audit to find repositories needing interface documentation:

```powershell
python xinterface_audit.py
```

This writes `_site/calling-sequence-audit.md` and
`_site/calling-sequence-audit.json`. Use `--output DIRECTORY` for another
destination. Every `python xbuild.py` also regenerates these reports and the
[calling-sequence audit page](https://beliavsky.github.io/fortran-gams-catalog/calling-sequences/),
linked from the site footer. Reports use the current saved catalog metadata;
there is no separate committed snapshot to refresh after each review.

The audit distinguishes missing public calling sequences, missing argument
declaration links, and projects whose public API has not yet been identified.
Command usage, public data, templates and playground adapters are reported
separately. Private helper signatures and checked drivers do not count as
upstream public calling sequences. Identical procedure records attached to
multiple GAMS classes count once; distinct overloads remain separate.

Coverage means that the **recorded** public interfaces have signatures and
declaration links. It does not establish coverage of every upstream procedure
or GAMS class. A project with no recorded callable interface may be a library
awaiting review, an application, or another kind of tool; the report does not
automatically declare it unsuitable. The audit makes no network requests,
scans no upstream source and compiles nothing. Findings do not block publishing.

Discovery begins with [Fortran code on GitHub](https://beliavsky.github.io/Fortran-code-on-GitHub/).
Entries are reviewed before classification; its section headings are not imported
as claims of verified numerical functionality.
The [discovery notes](docs/discovery-notes.md) record candidates deferred or
excluded during review, separately from compilation failures.

## Publish on GitHub Pages

Create an empty GitHub repository named `fortran-gams-catalog`, push this project,
then select **Settings → Pages → Build and deployment → Source → GitHub Actions**.
The supplied workflow tests and builds the saved metadata, then publishes `_site`.
No backend deployment or service credentials are required. Relative links also
work under a different repository name or another static host.

To publish the latest playground metadata without a local commit, run the Pages
workflow manually with **Refresh playground feed** enabled. This validates the
remote feed, tests it, and publishes the result; it does not commit the refreshed
snapshot. For reproducible subsequent builds, refresh locally, review the diff
and commit `data/imports/fortran-playground.json`. Push builds always use the
committed snapshot.

After creating the empty remote repository:

```powershell
git add .
git commit -m "Create independent Fortran GAMS software catalog"
git remote add origin https://github.com/Beliavsky/fortran-gams-catalog.git
git push -u origin main
```

This project has not been published merely by creating these local files.

Project detail pages link to the independent [FORD documentation pilot](https://beliavsky.github.io/fortran-playground/documentation/), passing the repository and reviewed revision. Generation is optional and does not change the catalog's source-review or execution status.

Argument tooltips also show pinned source declarations and clearly attached trailing
or FORD documentation comments. Arguments without explicit INTENT remain unstyled.
Expand **Argument declarations and source comments** on project pages for full text
and per-declaration/comment source links. Tooltips isolate the hovered variable;
source details retain the original shared declaration. Group comments are labeled
Shared comment in tooltips. Template spellings stay unexpanded, and
missing/ambiguous comments are not inferred.
Regenerate saved details after interface updates with
`python xargument_details.py --fetch --write`. This verifies source hashes; normal
site builds remain offline. The pure renderer `argument_intents.py` is also used
by the playground as `catalog_argument_intents.py`; synchronize it when changing
rendering/schema, and refresh the revision-matched review feed. Coverage is saved
in `docs/argument-declarations-coverage.json`.

Calling-sequence displays put explicitly OPTIONAL named arguments in square brackets.
This is documentation notation, not Fortran syntax; runnable examples and saved
signatures are unchanged. Existing bracket groups are preserved. Optionality is
read only from pinned declarations, never from argument names or prose.

Calling sequences, declaration previews and expanded declarations are normalized
in the browser by default: Fortran code is lowercase with one space after commas
on the same line. Quoted strings, comments and line breaks are preserved.
The **Original formatting** checkbox restores author formatting, retaining optional
argument notation. The preference is saved across pages (and both catalogs when
served from the same origin). It changes display only; source links, metadata and
runnable examples are untouched. Without JavaScript the original text remains.
`assets/formatting.js` is shared with the playground's `site/gams/formatting.js`.

Argument declarations can be expanded with **Show declarations** beside Usage. The default view isolates each argument and uses lowercase code with ` :: ` between attributes and the declared entity, including older declarations that omit the separator. Arguments appear in calling-sequence order in one code box, with available source comments appended on the same line after `!`. Missing `intent` clauses remain absent; none are inferred. The **Original formatting** preference restores source declaration text, including shared declarations. Pinned source links remain on the usage signatures.
