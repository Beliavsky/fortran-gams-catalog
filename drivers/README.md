# Standalone numerical drivers

This directory is reserved for problem-specific drivers for independently reviewed
repositories. Imported playground drivers remain in their original repository;
the catalog retains their source hashes, licenses, validation reports and links.

For each new driver, provide:

1. A main program with a stated GAMS problem class and named upstream procedure.
2. A small README with pinned source/dependency revisions and exact local build
   and run commands. FPM is optional.
3. Independent expected values, residuals or identities; explicit tolerances and
   precision; nonzero exit status on a failed check.
4. A saved result including compiler/version, flags, platform, date, source hashes
   and stdout/stderr. Record untested configurations.
5. License and attribution for borrowed code, including author examples.

A source-reviewed procedure mapping may precede a driver. Do not describe an
unrun driver as verified. Add support in the local metadata validator and site
renderer when the first local driver is ready.
