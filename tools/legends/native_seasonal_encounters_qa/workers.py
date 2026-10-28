"""Run disjoint native scenario ranges in isolated emulator processes."""
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

PASS = re.compile(r'^PASS scene (\d+): ', re.MULTILINE)
CAPTURE = re.compile(r'^scene-(\d+)-(gui|animated|locked|FAIL)\.rgba$')


def worker_count(requested=None):
    if requested is not None and not 1 <= requested <= 4:
        raise ValueError('Use 1–4 seasonal QA workers')
    cpus = len(os.sched_getaffinity(0)) if hasattr(os, 'sched_getaffinity') else (os.cpu_count() or 1)
    return min(requested or 4, max(1, cpus))


def partitions(total, jobs):
    if total < 1 or not 1 <= jobs <= 4:
        raise ValueError('Positive scenario count and 1–4 workers required')
    jobs = min(total, jobs)
    return [(total * i // jobs, total * (i + 1) // jobs) for i in range(jobs)]


def captures(output):
    result = {}
    for path in sorted(Path(output).glob('worker-*/*.rgba')):
        if path.name in result:
            raise ValueError('Duplicate capture: ' + path.name)
        result[path.name] = path
    return result


def execute(host_command, rom, addresses, total, jobs, output, timeout=600):
    """Retain every worker result; a missing/duplicate case or any failure rejects QA."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    if any(output.iterdir()):
        raise ValueError('Worker output must be fresh: ' + str(output))
    plan = partitions(total, jobs)

    def worker(item):
        number, (start, stop) = item
        folder = output / ('worker-%d' % number)
        folder.mkdir()
        log = folder / 'emulator.log'
        command = [*host_command, str(rom), str(folder), *addresses,
                   str(total), str(start), str(stop)]
        row = dict(worker=number, start=start, stop=stop, passed=False)
        begin = time.monotonic()
        try:
            with log.open('w') as stream:
                process = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, timeout=timeout)
            row['returncode'] = process.returncode
            if process.returncode:
                raise ValueError('Native process exited with code %d' % process.returncode)
            observed = [int(value) for value in PASS.findall(log.read_text())]
            if observed != list(range(start, stop)):
                raise ValueError('Missing, duplicate or out-of-range PASS scenario')
            files = list(folder.glob('*.rgba'))
            for path in files:
                match = CAPTURE.fullmatch(path.name)
                if not match or not start <= int(match[1]) < stop or match[2] == 'FAIL':
                    raise ValueError('Unexpected/failure capture: ' + path.name)
            expected = {'scene-%02d-gui.rgba' % scene for scene in range(start, stop)}
            if not expected <= {path.name for path in files}:
                raise ValueError('Missing native GUI capture')
            row.update(passed=True, scenarios=len(observed))
        except Exception as error:
            row['error'] = str(error)
        row['seconds'] = round(time.monotonic() - begin, 3)
        return row

    begin = time.monotonic()
    with ThreadPoolExecutor(max_workers=len(plan)) as pool:
        rows = list(pool.map(worker, enumerate(plan)))
    # Global scenario order and the original log name stay stable for existing readers.
    combined = ''.join((output / ('worker-%d' % i) / 'emulator.log').read_text()
                       for i in range(len(plan)))
    (output / 'emulator.log').write_text(combined)
    passed = all(row['passed'] for row in rows)
    report = dict(passed=passed, workers=len(plan), scenarios=total,
                  wild_creations=total * 256, exact_coverage=passed,
                  separate_processes=True, seconds=round(time.monotonic() - begin, 3),
                  worker_results=rows)
    (output / 'execution.json').write_text(json.dumps(report, indent=2) + '\n')
    if not passed:
        raise RuntimeError('Seasonal QA worker failure; inspect ' + str(output / 'execution.json'))
    return report


def compare(serial, parallel):
    """Benchmark acceptance requires every PASS line and every raw capture to match."""
    serial, parallel = Path(serial), Path(parallel)
    left, right = captures(serial), captures(parallel)
    if (serial / 'emulator.log').read_bytes() != (parallel / 'emulator.log').read_bytes():
        raise ValueError('Serial/parallel native logs differ')
    if left.keys() != right.keys():
        raise ValueError('Serial/parallel capture sets differ')
    hashes = {}
    for name in left:
        if left[name].read_bytes() != right[name].read_bytes():
            raise ValueError('Serial/parallel pixels differ: ' + name)
        hashes[name] = hashlib.sha256(right[name].read_bytes()).hexdigest()
    return dict(passed=True, exact_logs=True, exact_raw_captures=len(hashes),
                capture_sha256=hashes)
