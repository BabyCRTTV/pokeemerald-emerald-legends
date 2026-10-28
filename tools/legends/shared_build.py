#!/usr/bin/env python3
"""Bind native QA and both patch decoders to one private pair of ROM/ELF builds."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import time
import uuid
import zlib

ROOT = Path(__file__).resolve().parents[2]
BINARIES = ['pokeemerald.gba', 'pokeemerald.elf', 'pokeemerald-release.gba', 'pokeemerald-release.elf']
NATIVE = {
    'legends-mgba-preview/results.json': ('Debug', 'rom_sha256'),
    'eon-roamers-qa/verification.json': ('Debug', 'ROM_sha256'),
    'ember-return-qa/verification.json': ('Debug', 'ROM_sha256'),
    'grotto-review/verification.json': ('Debug', 'ROM_sha256'),
    'grotto-encounters/verification.json': ('Debug', 'ROM_sha256'),
    'living-hoenn-qa/verification.json': ('Debug', 'base_ROM_sha256'),
    'seasonal-encounters-qa/verification.json': ('Debug', 'base_ROM_sha256'),
    'visual-repairs-qa/verification.json': ('Debug', 'ROM_sha256'),
    'eon-roamers-release-qa/verification.json': ('Release', 'ROM_sha256'),
    'ember-return-release-qa/verification.json': ('Release', 'ROM_sha256'),
    'grotto-encounters-release/verification.json': ('Release', 'ROM_sha256'),
    'bedroom-release-qa/verification.json': ('Release', 'ROM_sha256'),
}


def sha(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, indent=2) + '\n')
    temporary.replace(path)


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root)


def fingerprint(root):
    # Only existing bot-managed publication outputs may advance during verification.
    # Every other tracked input, including pipelines, harnesses and patcher, is bound.
    rows = git(root, 'ls-tree', '-rz', '--full-tree', 'HEAD').split(b'\0')
    retained = []
    for row in rows:
        if not row:
            continue
        path = row.split(b'\t', 1)[1]
        if path.startswith(b'docs/downloads/') or path in (
                b'docs/wiki/windows-version.json', b'docs/wiki/android-version.json'):
            continue
        retained.append(row + b'\0')
    return hashlib.sha256(b''.join(retained)).hexdigest()


def workdir(root):
    return root/'build/shared-build'


def patch_names(version):
    if not re.fullmatch(r'\d+(?:\.\d+){2,3}', version):
        raise ValueError('Invalid game VERSION')
    return ['Pokemon-Emerald-Legends-v%s.bps' % version,
            'Pokemon-Emerald-Legends-v%s-debug.bps' % version]


def record(root):
    folder = workdir(root)
    if folder.exists():
        raise ValueError('Shared build output must be fresh')
    version = (root/'VERSION').read_text().strip()
    patch_names(version)
    data = dict(version=version, source_commit=git(root, 'rev-parse', 'HEAD').decode().strip(),
                source_tree=git(root, 'rev-parse', 'HEAD^{tree}').decode().strip(),
                source_fingerprint=fingerprint(root), nonce=uuid.uuid4().hex,
                binaries={name: sha(root/name) for name in BINARIES})
    write(folder/'inputs.json', data)
    return data


def unchanged(root, inputs):
    if fingerprint(root) != inputs['source_fingerprint']:
        raise ValueError('Tracked verification inputs changed')
    for name, expected in inputs['binaries'].items():
        if sha(root/name) != expected:
            raise ValueError('Shared build changed: ' + name)


def run_group(command, cwd, timeout):
    process = subprocess.Popen(command, cwd=cwd, start_new_session=True)
    try:
        code = process.wait(timeout=timeout)
    except BaseException:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()
        raise
    if code:
        raise RuntimeError('Patch verification exited with code %d' % code)


def start(root):
    folder = workdir(root)
    if (folder/'worker-start.json').exists():
        raise ValueError('Patch worker already started')
    inputs = read(folder/'inputs.json')
    with (folder/'patch-worker.log').open('w') as log:
        process = subprocess.Popen([sys.executable, str(Path(__file__).resolve()),
                                    'work', '--root', str(root)], cwd=root,
                                   stdin=subprocess.DEVNULL, stdout=log,
                                   stderr=subprocess.STDOUT, start_new_session=True)
    write(folder/'worker-start.json', dict(pid=process.pid, nonce=inputs['nonce']))
    print('Started private canonical-base/BPS verification, PID', process.pid)


def work(root):
    folder = workdir(root)
    inputs = read(folder/'inputs.json')
    result = dict(passed=False, nonce=inputs['nonce'])
    begin = time.monotonic()
    try:
        unchanged(root, inputs)
        run_group(['bash', 'tools/legends/build_verified_patches.sh'], root, 1200)
        unchanged(root, inputs)
        result['passed'] = True
    except Exception as error:
        result['error'] = str(error)
    result['seconds'] = round(time.monotonic() - begin, 3)
    write(folder/'patch-worker.json', result)
    return result


def join(root, timeout=1260):
    folder = workdir(root)
    inputs, started = read(folder/'inputs.json'), read(folder/'worker-start.json')
    deadline = time.monotonic() + timeout
    while not (folder/'patch-worker.json').exists():
        if time.monotonic() > deadline:
            raise TimeoutError('Patch worker did not produce a result')
        try:
            os.kill(started['pid'], 0)
        except ProcessLookupError:
            raise RuntimeError('Patch worker exited without a receipt')
        time.sleep(1)
    result = read(folder/'patch-worker.json')
    if started['nonce'] != inputs['nonce'] or result['nonce'] != inputs['nonce']:
        raise ValueError('Stale patch worker receipt')
    if not result['passed']:
        raise RuntimeError(result.get('error', 'Patch verification failed'))
    print('PASS canonical base, Floating IPS and browser decoder in %.3fs' % result['seconds'])
    return result


def finalize(root, patches=True):
    folder = workdir(root)
    inputs = read(folder/'inputs.json')
    unchanged(root, inputs)
    targets = dict(Debug=inputs['binaries']['pokeemerald.gba'],
                   Release=inputs['binaries']['pokeemerald-release.gba'])
    native = {}
    for path, (variant, field) in NATIVE.items():
        receipt = root/'build'/path
        data = read(receipt)
        if (data[field] != targets[variant] or data.get('passed') is False
                or data.get('ROM_unmodified') is False or data.get('public_ROM_unchanged') is False
                or (variant == 'Release' and data.get('RAM_writes') is True)):
            raise ValueError('Native receipt mismatch/failure: ' + path)
        native[path] = sha(receipt)
    result = dict(passed=True, patches_verified=patches, inputs=inputs,
                  native_receipt_sha256=native, payload_files={})
    if patches:
        result['patch_worker'] = join(root)
        publication = folder/'publication'
        decoder = read(publication/'browser-decoder-verification.json')
        if not decoder['passed'] or decoder['source_SHA1'] != 'f3ae088181bf583e55daf962a92bb46f4f1d07b7':
            raise ValueError('Independent decoder did not verify the canonical base')
        names = patch_names(inputs['version'])
        for name, variant in zip(names, ['Release', 'Debug']):
            decoded = decoder['results'][name]
            if (not decoded['exact_native_ROM_match'] or decoded['target_sha256'] != targets[variant]
                    or decoded['patch_sha256'] != sha(publication/name)):
                raise ValueError('Native/patch decoder target mismatch: ' + variant)
        result['decoder'] = decoder
        sums = ['%s  docs/downloads/%s' % (sha(publication/name), name) for name in names]
        sums += ['%s  %s' % (inputs['binaries'][name], name)
                 for name in ['pokeemerald-release.gba', 'pokeemerald.gba']]
        (publication/'SHA256SUMS.txt').write_text('\n'.join(sums) + '\n')
        for name in [*names, 'SHA256SUMS.txt', 'browser-decoder-verification.json']:
            result['payload_files'][name] = sha(publication/name)
        if {p.name for p in publication.iterdir()} != set(result['payload_files']):
            raise ValueError('Unexpected publication file; refusing artifact upload')
        write(publication/'verification.json', result)
    write(folder/'verification.json', result)
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
            print('source_commit=' + inputs['source_commit'], file=output)
            print('source_fingerprint=' + inputs['source_fingerprint'], file=output)
            print('manifest_sha256=' + sha(folder/'verification.json'), file=output)
    return result


def check_publication(root, folder, expected_manifest, expected_source, expected_fingerprint):
    if ((folder/'verification.json').is_symlink()
            or not (folder/'verification.json').is_file()
            or sha(folder/'verification.json') != expected_manifest):
        raise ValueError('Publication manifest hash mismatch')
    data = read(folder/'verification.json')
    inputs = data['inputs']
    if (not data['passed'] or not data['patches_verified'] or inputs['source_commit'] != expected_source
            or inputs['source_fingerprint'] != expected_fingerprint or fingerprint(root) != expected_fingerprint):
        raise ValueError('Stale or incomplete publication inputs; refusing publication')
    version = (root/'VERSION').read_text().strip()
    if inputs['version'] != version:
        raise ValueError('Publication VERSION changed')
    expected_files = {*patch_names(version), 'SHA256SUMS.txt', 'browser-decoder-verification.json'}
    if set(data['payload_files']) != expected_files:
        raise ValueError('Unexpected publication payload')
    actual_files = {p.name for p in folder.iterdir()}
    if actual_files != expected_files | {'verification.json'}:
        raise ValueError('Unexpected artifact file; ROMs must remain private')
    for name, expected in data['payload_files'].items():
        path = folder/name
        if path.is_symlink() or not path.is_file() or sha(path) != expected:
            raise ValueError('Publication file hash/type mismatch: ' + name)
        if name.endswith('.bps'):
            patch = path.read_bytes()
            if (patch[:4] != b'BPS1' or len(patch) < 16
                    or int.from_bytes(patch[-12:-8], 'little') != 0x1f1c08fb
                    or zlib.crc32(patch[:-4]) != int.from_bytes(patch[-4:], 'little')):
                raise ValueError('Publication BPS CRC failed: ' + name)
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['record', 'start', 'work', 'join', 'finalize', 'check-publication'])
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--without-patches', action='store_true')
    parser.add_argument('--folder', type=Path)
    parser.add_argument('--manifest-sha')
    parser.add_argument('--source-commit')
    parser.add_argument('--source-fingerprint')
    args = parser.parse_args()
    root = args.root.resolve()
    if args.mode == 'check-publication':
        check_publication(root, args.folder, args.manifest_sha, args.source_commit, args.source_fingerprint)
    elif args.mode == 'finalize':
        finalize(root, not args.without_patches)
    else:
        result = globals()[args.mode](root)
        if args.mode == 'work' and not result['passed']:
            return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
