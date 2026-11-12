"""List catalog calling-sequence gaps without network access or compilation."""
import argparse
from pathlib import Path

from catalog import ROOT, assemble
from interface_audit import STATUSES, audit, write_report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'_site', help='Directory for Markdown and JSON reports')
    args = parser.parse_args()
    _, projects, _ = assemble()
    report = audit(projects)
    write_report(args.output, report)
    print(f"Repositories audited: {report['project_count']}")
    for status, label in STATUSES.items():
        print(f"{report['status_counts'][status]:4d}  {label}")
    print('Reports: '+str(args.output/'calling-sequence-audit.md')+' and .json')


if __name__ == '__main__':
    main()
