"""Build and run a pinned-source numerical check; no installed library is needed."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import platform
from pathlib import Path
import shutil
import subprocess
import tempfile
from urllib.request import urlopen

CONFIG = {'repository': 'sag2021/ndsm', 'name': 'poisson', 'gams_code': 'I2b1a1a', 'driver': 'poisson.f90', 'source_flags': ['-O0', '-g', '-Wall', '-Wextra', '-ffree-line-length-none', '-fcheck=all', '-ffpe-trap=invalid,zero,overflow'], 'driver_flags': ['-O0', '-g', '-Wall', '-Wextra', '-ffree-line-length-none', '-fcheck=all', '-ffpe-trap=invalid,zero,overflow'], 'sources': [{'path': 'fortran/ndsm_root.f90', 'revision': '6f5b44d76a33d247a0c73d721766a867f40b4ad3', 'sha256': 'bd5bd2c05d57ec935fbf051c5c99a78fdcce48e47eab99ce4c06a74c1e59f7a8'}, {'path': 'fortran/ndsm_interp.f90', 'revision': '6f5b44d76a33d247a0c73d721766a867f40b4ad3', 'sha256': '3fe9311d368ce4870653622a1e99886ab0cf35c5efd24c7d5572d47e1c48564f'}, {'path': 'fortran/ndsm_multigrid_core.f90', 'revision': '6f5b44d76a33d247a0c73d721766a867f40b4ad3', 'sha256': '258a2f3c2f88992fdb2a05f56368901b0d336da27e73d0853a97d132756db1a1'}, {'path': 'fortran/ndsm_optimized.f90', 'revision': '6f5b44d76a33d247a0c73d721766a867f40b4ad3', 'sha256': '465b1835964d861334ade6ea65760fe6b1e01590ee1470d6d106206af732b150'}, {'path': 'fortran/ndsm_poisson.f90', 'revision': '6f5b44d76a33d247a0c73d721766a867f40b4ad3', 'sha256': 'b809a18efc4d9d148f544dd6f24692b049459193c78571eee290795f6ee622b1'}]}
ROOT = Path(__file__).resolve().parent

def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--compiler', default='gfortran', help='Compiler executable; GNU flags are used')
    parser.add_argument('--report', type=Path, help='Save a JSON numerical check report')
    args = parser.parse_args()
    compiler = shutil.which(args.compiler)
    if compiler is None:
        parser.error('Compiler not found: ' + args.compiler)
    version = subprocess.run([compiler, '--version'], check=True, timeout=10, capture_output=True, text=True).stdout
    print(version.splitlines()[0], flush=True)
    with tempfile.TemporaryDirectory(prefix='catalog_numerical_') as directory:
        work = Path(directory)
        source_paths = []
        for item in CONFIG['sources']:
            url = 'https://raw.githubusercontent.com/' + CONFIG['repository'] + '/' + item['revision'] + '/' + item['path']
            with urlopen(url, timeout=30) as response:
                text = response.read().decode('utf-8').replace('\r\n', '\n')
            if digest(text) != item['sha256']:
                raise ValueError('Pinned source hash mismatch: ' + item['path'])
            target = work / Path(item['path']).name
            target.write_text(text, encoding='utf-8')
            source_paths.append(target)
        logs = []
        objects = []
        for index, source in enumerate(source_paths):
            obj = work / (str(index) + '.o')
            command = [compiler, *CONFIG['source_flags'], '-c', str(source), '-o', str(obj)]
            result = subprocess.run(command, cwd=work, check=True, timeout=60, capture_output=True, text=True)
            logs.append(result.stderr.replace(str(work), '<temporary>'))
            objects.append(str(obj))
        executable = work / 'check.exe'
        command = [compiler, *CONFIG['driver_flags'], str(ROOT/CONFIG['driver']), *objects, '-o', str(executable)]
        result = subprocess.run(command, cwd=work, check=True, timeout=60, capture_output=True, text=True)
        logs.append(result.stderr.replace(str(work), '<temporary>'))
        result = subprocess.run([str(executable)], cwd=work, check=True, timeout=60, capture_output=True, text=True)
        print(result.stdout, end='')
        report = {
            'checked_at': datetime.now(timezone.utc).isoformat(), 'platform': platform.platform(),
            'compiler': version.splitlines()[0], 'hash_convention': 'SHA-256 of UTF-8 text normalized to LF line endings',
            'checks': [{'name': CONFIG['name'], 'gams_code': CONFIG['gams_code'],
                'source': CONFIG['sources'][-1], 'dependencies': CONFIG['sources'][:-1],
                'driver': CONFIG['driver'], 'driver_sha256': digest((ROOT/CONFIG['driver']).read_text(encoding='utf-8')),
                'flags': CONFIG['driver_flags'], 'source_flags': CONFIG['source_flags'],
                'build_returncode': 0, 'run_returncode': result.returncode,
                'build_stderr': ''.join(logs), 'stdout': result.stdout, 'stderr': result.stderr}]
        }
        if any(logs):
            print('Compiler warnings are retained in the JSON report (' + str(len(''.join(logs))) + ' characters).')
        if args.report:
            args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
