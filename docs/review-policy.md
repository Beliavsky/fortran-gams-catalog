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

A public entry point needs a `summary`. Optional `signature` text supplies the
Fortran usage line (including `CALL` for a subroutine). It must have `declarations`:
objects with `path`, `line_start` and `line_end` pointing to hashed evidence in the
same claim. Clicking the usage line opens the first argument-declaration range;
additional links can cover other inspected generic bindings. Optional `examples`
use the same format to link author usage. `usage` supplies a calling sketch and
requires `usage_notes` explaining initialization, dependencies and limits. These
sketches and linked author examples are not checked drivers.

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

## Drivers

Keep new standalone programs in `drivers/`, with build/run instructions, pinned
dependencies, reuse/license information and saved verification results. Prefer an
author's suitable example when it exercises the intended problem. A driver need
not use FPM or run in a browser. Do not redistribute upstream source without
checking its license; source links and hashes can be recorded independently.
