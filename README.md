# Fortran software by GAMS classification

A static catalog for finding Fortran numerical software by mathematical problem.
It includes repositories that do not use FPM or run in an online playground.

The saved catalog imports **298 playground packages** and their classifications,
procedure evidence and checked driver links, alongside **126 independent
repository reviews**. Counts describe the saved snapshot and change on refresh.
Browse the GAMS hierarchy, search names/authors/topics/procedures, or filter for
independent reviews. Each repository has a detail page with evidence links.

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
and [driver requirements](drivers/README.md). Each new classification needs pinned
evidence and scope notes. Build systems can be Make, CMake, custom scripts or
unreviewed; FPM compatibility is not an inclusion criterion.

The independent reviews cover differentiation, interpolation, linear algebra,
multiple precision, nonlinear systems, quadrature, differential equations,
optimization, random sampling, special functions and time-series methods. Some
repositories use FPM and others use Make, CMake or other build arrangements.
They are documentation-reviewed entries, not additional precompiled packages.
After editing `data/local.json`, regenerate the review ledger:

```powershell
python xreviews.py
```

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
