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

The initial independent records are documentation reviews. The site currently
renders their evidence and the imported source/procedure/driver records. Extend the
local record validator and renderer together when adding local procedures or
verified drivers; do not label notes as verification.

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
