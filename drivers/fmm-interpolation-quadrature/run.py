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

CONFIG = {'repository': 'Beliavsky/Computer-Methods-for-Mathematical-Computations', 'source_flags': ['-O0', '-g', '-Wall', '-Wextra', '-ffree-line-length-none', '-fcheck=all', '-ffpe-trap=invalid,zero,overflow'], 'driver_flags': ['-O0', '-g', '-Wall', '-Wextra', '-ffree-line-length-none', '-fcheck=all', '-ffpe-trap=invalid,zero,overflow'], 'sources': [{'path': 'fmm.f90', 'revision': 'b850d06d29e348a803feaba58c0b68a8fdd5c5f1', 'sha256': 'f2c3d0c63b0e126cd093df644f9720e16e50b8eb56e5219a418a5b9e4c634a10'}]}
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
        report = {
            'checked_at': datetime.now(timezone.utc).isoformat(), 'platform': platform.platform(),
            'compiler': version.splitlines()[0], 'hash_convention': 'SHA-256 of UTF-8 text normalized to LF line endings',
            'checks': []}
        for name, code in [('spline', 'E1a'), ('derivatives', 'E3a2'), ('quadrature', 'H2a1a1')]:
            executable = work / (name + '.exe')
            driver = ROOT / (name + '.f90')
            command = [compiler, *CONFIG['driver_flags'], str(driver), *objects, '-o', str(executable)]
            built = subprocess.run(command, cwd=work, check=True, timeout=60, capture_output=True, text=True)
            result = subprocess.run([str(executable)], cwd=work, check=True, timeout=60, capture_output=True, text=True)
            print(result.stdout, end='')
            report['checks'].append({
                'name': name, 'gams_code': code,
                'source': CONFIG['sources'][-1], 'dependencies': CONFIG['sources'][:-1],
                'driver': driver.name, 'driver_sha256': digest(driver.read_text(encoding='utf-8')),
                'flags': CONFIG['driver_flags'], 'source_flags': CONFIG['source_flags'],
                'build_returncode': built.returncode, 'run_returncode': result.returncode,
                'build_stderr': ''.join(logs) + built.stderr.replace(str(work), '<temporary>'),
                'stdout': result.stdout, 'stderr': result.stderr})
        if any(logs):
            print('Compiler warnings are retained in the JSON report (' + str(len(''.join(logs))) + ' characters).')
        if args.report:
            args.report.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
