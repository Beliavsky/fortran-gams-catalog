# Review policy

This catalog covers Fortran numerical software regardless of build system or
playground compatibility. Inclusion is separate from compilation or verification.

Every classification should describe a problem the software actually implements.
Use the narrowest class supported by the reviewed evidence. A broad description
does not justify assigning every descendant. GAMS ancestry follows explicit parent
links; C1 and C10 are siblings.

## Evidence levels

* **Documentation reviewed:** a pinned author README/manual supports the claim.
* **Source reviewed:** a named procedure and pinned implementation have been
  inspected. Record module/procedure, file, hash, relevant lines and limitations.
* **Local checked driver:** a specific driver was built and run locally, with
  independent numerical checks and saved results.
* **Hosted checked driver:** the imported playground record supplies a checked
  problem-specific example and its verification report.

Apply levels to individual mappings and drivers, never to the whole repository.
An author's example is useful evidence and may be reused with its license, but its
existence alone does not establish that we have run or independently checked it.
Record platform/compiler/flags/precision/dependencies for every verified driver.
Successful execution does not establish performance superiority or general
correctness. Do not publish a “try” link that substitutes an unrelated default demo.

## Catalog-owned records

Edit `data/local.json`. Each project uses a lowercase canonical ID of the form
`github:owner/repository`. Local-only entries need name, description and repository;
classification records need code, level, full revision, evidence URL/path/SHA-256,
review date and scope notes. Evidence hashes use UTF-8 text with LF line endings.
Do not put imported records into this file.

### Licenses

Cards and repository details show **License**, separately from build support and
compilation status. An imported label is marked as imported metadata; it is not
an independent license-file review. Unknown imported identifiers such as
`NOASSERTION` display as "No license identified". With no recorded label, display
"License not yet reviewed" rather than inferring that no license exists.

A catalog-owned `license` overrides the displayed imported label while preserving
the imported record. Record `label`, optional `spdx_expression` (or null), full
`revision`, `reviewed_on`, `notes` describing scope, and `evidence` objects with
`path`, commit-pinned `url` and normalized UTF-8/LF `sha256`. The label links to
the first evidence file; details and the Markdown ledger retain all evidence.
Use an SPDX expression only when the reviewed terms establish it, including
whether a GPL version is "only" or "or later". Custom/multiple-license cases
retain descriptive labels and notes. A review of one component does not establish
the terms for all bundled or external dependencies.

Local descriptions replace imported descriptions. Local topics/classifications are
added to imported ones. Original imported metadata remains intact in the download.
Removing an incorrect imported claim requires correcting the publisher; local
additions do not silently erase upstream claims. Repository transfers/renames need
an explicit identity migration rather than creating duplicate entries.

Independent records may retain a broad documentation review alongside deeper
source reviews. Each `source-reviewed` classification must include `procedures`:
objects with `procedure`, `path`, `line_start` and `line_end`. The path must match
a hashed evidence file at the claim's pinned revision. Ranges identify the
inspected implementation or interface portions, not necessarily the complete
procedure body. Standalone programs and callback adapters may also be identified
when they explain usage. They are not checked drivers unless built and tested.
Procedure names participate in site search, and the site and Markdown ledger
link directly to their source ranges.

Where the calling interface has been inspected, add a `role`: `public-entry-point`,
`implementation-helper`, `program-entry-point`, `callback`, `implementation-evidence`
or `module-interface`. Leave it absent where the role is unreviewed; a source
mapping alone does not establish that a procedure is public. Store `module` and
`procedure` separately. Public module generics should use the generic name,
with private implementations recorded as helpers. A module qualifier is catalog
notation, not Fortran call syntax.
For a type-bound entry point, store the binding in `procedure` and the containing
type in `derived_type`, separately from `module`. The catalog displays
`module_name::type_name%binding_name`; the usage line uses an actual object, such
as `result = object%binding_name(x)`. Link the binding declaration and the
implementation's argument declarations so the passed-object argument is clear.

A public entry point needs a `summary`. Optional `signature` text supplies the
Fortran usage line (including `CALL` for a subroutine). It must have `declarations`:
objects with `path`, `line_start` and `line_end` pointing to hashed evidence in the
same claim. Clicking the usage line opens the first argument-declaration range;
additional links can cover other inspected generic bindings. Optional `examples`
use the same format to link author usage. `usage` supplies a calling sketch and
requires `usage_notes` explaining initialization, dependencies and limits. These
sketches and linked author examples are not checked drivers.

Optional `arguments` records annotate explicit Fortran intents for a particular
public callable signature. Each record has `name`, `intent` (`in`, `out` or
`inout`), `path`, `line_start` and `line_end`. For example:

```json
{"name": "INFO", "intent": "out", "path": "src/solver.f90", "line_start": 42, "line_end": 42}
```

The source range must lie within a recorded argument-declaration range in the
same hashed claim evidence. Names are unique ignoring case within each call and
must occur in its argument list (or operand positions for an overloaded operator
or assignment). Optional zero-based `call_index` distinguishes calls in a
multi-call usage line; omitted means the first call. Optional `dummy` records
the source dummy name when the displayed actual name differs. Inspect the exact overload: a generic name can
cover declarations with different intents. Preserve explicit `inout` on work
arrays or status flags even when their names sound like pure outputs. Do not
infer intent from comments, variable names or assignments. Leave arguments
without explicit declarations unannotated; no `intent(in)` default is assumed.
Function results and an implicit passed object are not displayed dummy
arguments. Public constants, template instantiations and command usage do not
receive Fortran argument-intent annotations. Update the claim review date when
adding reviewed annotations.

When preprocessing genuinely changes an intent, use `intent: "conditional"`
with source-linked `variants`. Each alternative has `intent`, `condition`,
`path`, `line_start` and `line_end`; all alternatives must fit recorded
declaration ranges. Conditional annotations are not given a fixed italic or bold
style. Their hover/focus text states the alternatives. Do not assume an active
compiler definition from the filename or from a previously tested configuration.

An optional `argument_intent_review` records `reviewed_on`, `status` (`checked`,
`partial` or `not-applicable`), `sources` and `issues`. Each source names a
procedure and a pinned file/range. A checked record has no issues and can have
no annotations when no explicit INTENT is declared. A partial record retains
specific issues. Not-applicable records require explanatory `notes`; a lack of
source parsing is not a valid exemption. The full pass uses exact-pin exceptions
in `data/argument-intent-overrides.json` for a MATLAB gateway invocation, a
user-supplied C adapter and a preprocessing-dependent declaration.

The optional `xargument_intents.py --fetch` utility verifies source hashes,
examines scopes and logical declarations, and produces a review queue. It
understands continuations, fixed/free source forms, separate INTENT statements,
generic/type-bound bindings, templates, positional/keyword actuals and multiple
calls. It is a conservative metadata-review aid, not a complete Fortran parser
or preprocessor. Unsupported or ambiguous cases must be reviewed rather than
silently assigned an intent. `--write` is explicit; normal site generation uses
only saved metadata. The coverage report flags future recorded usage lines
without an intent review.

The site offers optional output highlighting and exposes explicit annotations
on hover or keyboard focus. Raw signature text remains unchanged and its link
still opens the declaration source. Metadata exports retain these optional
records; receiving catalogs may choose whether to display them. This is
interface documentation, not a numerical or compilation verification claim.

Cards show at most three reviewed public/program entry points that match the
current GAMS scope, with module names, source paths, line numbers and clickable
usage lines where recorded. Details retain helper and callback evidence alongside
the entry points, summaries, argument declarations and calling sketches. Module
names and source paths participate in search.

Additional NIST classes absent from the imported snapshot belong in
`data/gams-extensions.json`, with their official label, parent, source URL and
review date. These extend the local taxonomy without modifying the imported
feed. Conflicting definitions and parent cycles are rejected. Extend the local
validator and renderer together before adding locally verified drivers; do not
label source inspection as numerical verification.

## Imports and ownership

`xrefresh.py` validates a complete playground feed and its snapshot hash before
atomically replacing the saved snapshot. The build merges it with local records by
canonical repository identity. `data/local.json` is never changed by a refresh.
An imported-only project removed upstream disappears on the next build; to retain
one independently, adopt sufficient metadata into its local record first.

The playground remains authoritative for its package build recipes, checks and
driver references. This catalog owns independent repository reviews. Shared
metadata can move here later, one field at a time, with explicit ownership to avoid
two competing editable copies. The feed retains its taxonomy/source provenance.

## Historical GAMS/Netlib imports

Historical GAMS/Netlib records are a separate discovery collection, hidden by
default. A downloaded source file and matching entry-point name establish the
recorded availability check, not an independent source review or a numerical
test. The pilot imports GAMS codes from Netlib because NIST dynamic pages were
inaccessible during setup; preserve this provenance rather than claiming a
direct NIST module import. License and source-review filters must retain these
distinctions. Modernized related projects do not inherit or confer verification,
source equivalence, or license terms. The separate import snapshot can be
refreshed without altering local classifications or the playground feed.

## Drivers

Keep new standalone programs in `drivers/`, with build/run instructions, pinned
dependencies, reuse/license information and saved verification results. Prefer an
author's suitable example when it exercises the intended problem. A driver need
not use FPM or run in a browser. Do not redistribute upstream source without
checking its license; source links and hashes can be recorded independently.
