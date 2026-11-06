"""Compile and run mathematical checks against pinned upstream Riemann routines."""
import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path
import shutil
import subprocess
import tempfile
from urllib.request import urlopen

SOURCES = {'advection': {'path': 'src/rp1_advection_ptwise.f90', 'sha256': '80b314b5f00f5186154b4de536efdc72d0d470e07469a8f296c6da896a922d65', 'revision': '008d4921ea46878a97a96c8b8daa399a2e7b9078'}, 'burgers': {'path': 'src/rp1_burgers_ptwise.f90', 'sha256': '91ea080bb93c8b0c3eff3baefc08a0fdf676e0765db9496d657943d751648072', 'revision': '008d4921ea46878a97a96c8b8daa399a2e7b9078'}}
ROOT = Path(__file__).resolve().parent

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiler', default='gfortran', help='Fortran compiler executable (GNU flags are used)')
    parser.add_argument('--report', type=Path, help='Save compiler, source/driver hashes, flags and results as JSON')
    args = parser.parse_args()
    compiler = shutil.which(args.compiler)
    if not compiler:
        parser.error('Compiler not found: ' + args.compiler)
    version = subprocess.run([compiler, '--version'], check=True, timeout=10, capture_output=True, text=True).stdout
    print(version.strip(), flush=True)
    report = {'checked_at': datetime.now(timezone.utc).isoformat(), 'platform': platform.platform(),
              'compiler': version.splitlines()[0], 'checks': [],
              'hash_convention': 'SHA-256 of UTF-8 text normalized to LF line endings'}
    with tempfile.TemporaryDirectory(prefix='catalog_riemann_') as directory:
        work = Path(directory)
        for name, record in SOURCES.items():
            url = 'https://raw.githubusercontent.com/clawpack/riemann/' + record['revision'] + '/' + record['path']
            with urlopen(url, timeout=30) as response:
                source = response.read().decode('utf-8').replace('\r\n', '\n')
            if hashlib.sha256(source.encode()).hexdigest() != record['sha256']:
                raise ValueError('Pinned source hash mismatch: ' + name)
            upstream = work / (name + '_upstream.f90')
            upstream.write_text(source, encoding='utf-8')
            executable = work / (name + '.exe')
            flags = ['-O0', '-g', '-Wall', '-Wextra', '-fcheck=all', '-ffpe-trap=invalid,zero,overflow']
            command = [compiler, *flags, str(upstream), str(ROOT / (name + '.f90')), '-o', str(executable)]
            print('Checking ' + name + ' at ' + record['revision'], flush=True)
            build = subprocess.run(command, cwd=work, check=True, timeout=60, capture_output=True, text=True)
            result = subprocess.run([str(executable)], cwd=work, check=True, timeout=10, capture_output=True, text=True)
            print(build.stderr.replace(str(work), '<temporary>'), end='')
            print(result.stdout, end='')
            report['checks'].append({'name': name, 'gams_code': 'I2a2', 'source': record,
                'driver': name + '.f90', 'driver_sha256': hashlib.sha256((ROOT/(name+'.f90')).read_text(encoding='utf-8').encode()).hexdigest(),
                'flags': flags, 'build_returncode': build.returncode, 'run_returncode': result.returncode,
                'build_stderr': build.stderr.replace(str(work), '<temporary>'),
                'stdout': result.stdout, 'stderr': result.stderr})
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
