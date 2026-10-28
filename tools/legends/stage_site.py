#!/usr/bin/env python3
"""Stage one complete Pages snapshot; incomplete production evidence never deploys."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
import zipfile
import zlib

import yaml
sys.path.insert(0, str(Path(__file__).resolve().parent))
from shared_build import NATIVE

ROOT = Path(__file__).resolve().parents[2]
BOT_OUTPUTS = {'docs/wiki/android-version.json', 'docs/wiki/windows-version.json'}
GATES = ['legends-checks.yml', 'build-release-patch.yml', 'wiki-checks.yml',
         'wiki-apk.yml', 'wiki-windows.yml']
CRITICAL = ['index.html', 'patcher.html', 'patcher.js', 'changelog.html',
            'wiki/index.html', 'wiki/dex.html', 'wiki/dex-data.json',
            'wiki/dex-profiles.js', 'wiki/dex-sprite-atlas.js',
            'wiki/dex-sprite-atlas.webp', 'wiki/dex-portrait-sources.json',
            'wiki/map-hoenn.png', 'wiki/map-kanto.png', 'wiki/walkthrough-maps.json',
            'wiki/android-version.json', 'wiki/windows-version.json',
            'features/eon-roamers.md', 'downloads/SHA256SUMS.txt']
SHA = re.compile(r'[0-9a-f]{64}')


class Hold(Exception):
    """A normal not-ready state: retain the existing deployment."""


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')
    temporary.replace(path)


def tree(root, revision):
    result = {}
    for row in git(root, 'ls-tree', '-rz', '--full-tree', revision).split(b'\0'):
        if row:
            header, path = row.split(b'\t', 1)
            result[path.decode()] = header.decode()
    return result


def glob_match(path, pattern):
    # GitHub path filters: * does not cross /; ** includes zero or more segments.
    parts = pattern.split('/')
    expression = ''
    for i, part in enumerate(parts):
        if part == '**':
            expression += '.*' if i == len(parts)-1 else '(?:[^/]+/)*'
        else:
            expression += ''.join('[^/]*' if c == '*' else '[^/]' if c == '?'
                                  else re.escape(c) for c in part)
            if i < len(parts)-1:
                expression += '/'
    return re.fullmatch(expression, path) is not None


def paths_for(root, workflow):
    # BaseLoader preserves the key "on" instead of treating it as YAML 1.1 true.
    data = yaml.load((root/'.github/workflows'/workflow).read_text(), Loader=yaml.BaseLoader)
    push = data['on']['push'] or {}
    if 'paths-ignore' in push or any(p.startswith('!') for p in push.get('paths', [])):
        raise ValueError('Unsupported path filter; update the site guard explicitly')
    return push.get('paths')


def inputs(entries, workflow, patterns):
    selected = {}
    for path, blob in entries.items():
        if path.startswith('docs/downloads/') or path in BOT_OUTPUTS:
            continue
        if patterns is None:
            # Evidence/handoff text cannot alter the host tests or game outputs.
            if path in {'docs/DEVELOPMENT-HANDOFF.md', 'docs/DEVELOPMENT-PROCESS.md'} or path.startswith('docs/qa/'):
                continue
            keep = True
        else:
            keep = any(glob_match(path, pattern) for pattern in patterns)
        if keep:
            selected[path] = blob
    # A workflow's own change always invalidates its prior evidence.
    name = '.github/workflows/' + workflow
    selected[name] = entries[name]
    return selected


class SafeRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, message, headers, newurl):
        if urlsplit(newurl).scheme != 'https':
            raise ValueError('Refusing insecure redirect')
        redirected = super().redirect_request(request, fp, code, message, headers, newurl)
        if urlsplit(newurl).hostname != urlsplit(request.full_url).hostname:
            redirected.remove_header('Authorization')
        return redirected


class GitHub:
    def __init__(self, repository, token):
        self.base = 'https://api.github.com/repos/' + repository
        self.token = token
        self.opener = build_opener(SafeRedirect())

    def get(self, path, binary=False, limit=64*1024*1024):
        request = Request(self.base + path, headers={
            'Authorization': 'Bearer ' + self.token,
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
            'User-Agent': 'Legends-site-promotion'})
        with self.opener.open(request, timeout=45) as response:
            data = response.read(limit+1)
        if len(data) > limit:
            raise ValueError('GitHub response exceeds bounded size')
        return data if binary else json.loads(data)


def select_gate(root, api, workflow, current, cache):
    patterns = paths_for(root, workflow)
    expected = inputs(cache[current], workflow, patterns)
    for page in range(1, 4):
        runs = api.get('/actions/workflows/' + workflow
                       + '/runs?branch=master&event=push&per_page=100&page=' + str(page))['workflow_runs']
        for run in runs:
            revision = run['head_sha']
            if run['event'] != 'push' or run['head_branch'] != 'master':
                continue
            if subprocess.run(['git', 'merge-base', '--is-ancestor', revision, current],
                              cwd=root, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode:
                continue
            if revision not in cache:
                cache[revision] = tree(root, revision)
            if inputs(cache[revision], workflow, patterns) != expected:
                continue
            # The newest matching attempt governs; never skip a failed/in-flight run.
            if run['status'] != 'completed' or run['conclusion'] != 'success':
                raise Hold(workflow + ': newest matching production run is ' + run['status']
                           + '/' + str(run['conclusion']))
            return dict(id=run['id'], source_commit=revision, workflow=workflow,
                        run_attempt=run.get('run_attempt', 1),
                        input_sha256=sha(json.dumps(expected, sort_keys=True).encode()))
        if len(runs) < 100:
            break
    raise Hold(workflow + ': no successful matching production evidence in the bounded history')


def patch_payload(api, gate, version):
    artifacts = api.get('/actions/runs/%s/artifacts?per_page=100' % gate['id'])['artifacts']
    matches = [a for a in artifacts if a['name'] == 'legends-candidate-patches' and not a['expired']]
    if len(matches) != 1:
        raise Hold('Verified patch artifact missing/expired; rerun production verification')
    artifact = matches[0]
    if artifact['workflow_run']['head_sha'] != gate['source_commit']:
        raise ValueError('Patch artifact source mismatch')
    data = api.get('/actions/artifacts/%s/zip' % artifact['id'], binary=True)
    if artifact.get('digest') != 'sha256:' + sha(data):
        raise ValueError('Patch archive digest mismatch')
    names = ['Pokemon-Emerald-Legends-v%s.bps' % version,
             'Pokemon-Emerald-Legends-v%s-debug.bps' % version]
    expected = set(names) | {'SHA256SUMS.txt', 'browser-decoder-verification.json', 'verification.json'}
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        if (len(archive.infolist()) != len(expected) or set(archive.namelist()) != expected
                or sum(i.file_size for i in archive.infolist()) > 64*1024*1024):
            raise ValueError('Unexpected patch archive files/size; ROMs must remain private')
        payload = {name: archive.read(name) for name in expected}
    manifest = json.loads(payload['verification.json'])
    source = manifest['inputs']
    if (manifest.get('passed') is not True or manifest.get('patches_verified') is not True
            or source['source_commit'] != gate['source_commit'] or source['version'] != version
            or set(manifest['native_receipt_sha256']) != set(NATIVE)
            or not all(SHA.fullmatch(v) for v in manifest['native_receipt_sha256'].values())
            or set(manifest['payload_files']) != expected - {'verification.json'}):
        raise ValueError('Incomplete native/patch manifest')
    for name, digest in manifest['payload_files'].items():
        if sha(payload[name]) != digest:
            raise ValueError('Verified payload hash mismatch: ' + name)
    decoder = json.loads(payload['browser-decoder-verification.json'])
    if (decoder != manifest['decoder'] or decoder.get('passed') is not True
            or decoder['source_SHA1'] != 'f3ae088181bf583e55daf962a92bb46f4f1d07b7'):
        raise ValueError('Canonical-base decoder proof mismatch')
    for name, rom in zip(names, ['pokeemerald-release.gba', 'pokeemerald.gba']):
        patch = payload[name]
        proof = decoder['results'][name]
        if (len(patch) < 16 or patch[:4] != b'BPS1'
                or int.from_bytes(patch[-12:-8], 'little') != 0x1f1c08fb
                or zlib.crc32(patch[:-4]) != int.from_bytes(patch[-4:], 'little')
                or proof.get('exact_native_ROM_match') is not True
                or proof['target_sha256'] != source['binaries'][rom]
                or proof['patch_sha256'] != sha(patch)):
            raise ValueError('BPS/native proof mismatch: ' + name)
    return payload, dict(id=artifact['id'], digest=artifact['digest'],
                         manifest_sha256=sha(payload['verification.json']),
                         native_ROM_sha256={k:v for k,v in source['binaries'].items() if k.endswith('.gba')})


def validate_site(root, payload, version):
    docs = root/'docs'
    for path in docs.rglob('*'):
        if path.is_symlink() or (path.is_file() and path.suffix.lower() in {'.gba', '.elf', '.sav'}):
            raise ValueError('Unsafe site asset: ' + str(path.relative_to(docs)))
    for name, content in payload.items():
        if name.endswith('.bps') or name == 'SHA256SUMS.txt':
            path = docs/'downloads'/name
            if not path.is_file() or path.read_bytes() != content:
                raise Hold('Committed downloads are not the verified pair: ' + name)
    home = (docs/'index.html').read_text()
    if re.search(r'<div class="version">v([^<]+)</div>', home).group(1) != version:
        raise ValueError('Home version differs from VERSION')
    names = {p for p in payload if p.endswith('.bps')}
    if set(re.findall(r'downloads/(Pokemon-Emerald-Legends-v[^"\s]+\.bps)', home)) != names:
        raise ValueError('Home links do not identify both verified patches')
    patcher = (docs/'patcher.js').read_text()
    if re.search(r'const VERSION = ["\x27]([^"\x27]+)', patcher).group(1) != version:
        raise ValueError('Browser patcher VERSION differs')
    html = (docs/'patcher.html').read_text()
    if set(re.findall(r'v(\d+(?:\.\d+){2,3})', html)) != {version}:
        raise ValueError('Patcher labels differ from VERSION')
    changelog = (docs/'changelog.html').read_text()
    if re.search(r'<div class="version">v([^<]+)</div>', changelog).group(1) != version:
        raise ValueError('Changelog header differs from VERSION')
    if json.loads((docs/'wiki/dex-data.json').read_text())['gameVersion'] != version:
        raise ValueError('LegendsDex gameVersion differs')
    android = json.loads((docs/'wiki/android-version.json').read_text())
    if android['available'] and sha((docs/'downloads/Emerald-Legends-Wiki.apk').read_bytes()) != android['sha256']:
        raise ValueError('Android download/manifest mismatch')


def file_row(path, relative):
    data = path.read_bytes()
    return dict(path=relative, bytes=len(data), sha256=sha(data),
                Git_blob_sha1=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest())


def stage(root, api, output):
    if output.exists():
        raise ValueError('Site staging directory must be fresh')
    current = git(root, 'rev-parse', 'HEAD').decode().strip()
    cache = {current: tree(root, current)}
    gates = {name: select_gate(root, api, name, current, cache) for name in GATES}
    version = (root/'VERSION').read_text().strip()
    if not re.fullmatch(r'\d+(?:\.\d+){2,3}', version):
        raise ValueError('Invalid game VERSION')
    payload, artifact = patch_payload(api, gates['build-release-patch.yml'], version)
    validate_site(root, payload, version)
    temporary = output.with_name(output.name + '.partial')
    if temporary.exists():
        shutil.rmtree(temporary)
    try:
        shutil.copytree(root/'docs', temporary)
        files = [file_row(p, p.relative_to(temporary).as_posix())
                 for p in sorted(temporary.rglob('*')) if p.is_file()]
        manifest = dict(schema=1, version=version, source_commit=current,
                        gates=gates, verified_patch_artifact=artifact, files=files)
        write(temporary/'release-publication.json', manifest)
        expected = {row['path']:row for row in files}
        critical = CRITICAL + ['downloads/'+name for name in payload if name.endswith('.bps')]
        rows = [expected[name] for name in critical]
        rows.append(file_row(temporary/'release-publication.json', 'release-publication.json'))
        write(output.parent/'site-expected.json', dict(version=version, actual_live_files=rows))
        temporary.rename(output)
    except BaseException:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return manifest


def fresh(api, expected, gates=None):
    if api.get('/commits/master')['sha'] != expected:
        raise Hold('Master advanced while staging; a newer event must promote the new snapshot')
    for gate in (gates or {}).values():
        run = api.get('/actions/runs/%s' % gate['id'])
        if (run['head_sha'] != gate['source_commit'] or run['status'] != 'completed'
                or run['conclusion'] != 'success' or run['event'] != 'push'
                or run['head_branch'] != 'master' or run['run_attempt'] != gate['run_attempt']):
            raise Hold('Production gate changed during staging: ' + gate['workflow'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['stage', 'fresh'])
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--output', type=Path, default=ROOT/'build/site')
    parser.add_argument('--manifest', type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    api = GitHub(os.environ['GITHUB_REPOSITORY'], os.environ['GH_TOKEN'])
    report = dict(ready=False)
    try:
        if args.mode == 'stage':
            manifest = stage(root, api, args.output)
            fresh(api, manifest['source_commit'], manifest['gates'])
            report.update(ready=True, source_commit=manifest['source_commit'])
        else:
            manifest = json.loads(args.manifest.read_text()) if args.manifest else None
            current = git(root, 'rev-parse', 'HEAD').decode().strip()
            if manifest and manifest['source_commit'] != current:
                raise ValueError('Staged snapshot source differs from deployment checkout')
            fresh(api, current, manifest['gates'] if manifest else None)
            report['ready'] = True
    except Hold as error:
        report['hold'] = str(error)
    except Exception as error:
        report['error'] = str(error)
    write(root/'build/site-status.json', report)
    print(json.dumps(report))
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a') as stream:
            print('ready=' + str(report['ready']).lower(), file=stream)
            if report.get('source_commit'):
                print('source_commit=' + report['source_commit'], file=stream)
    return 1 if 'error' in report else 0


if __name__ == '__main__':
    sys.exit(main())
