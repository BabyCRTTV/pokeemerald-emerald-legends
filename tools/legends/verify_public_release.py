#!/usr/bin/env python3
"""Recheck live bytes against a reviewed publication receipt; no ROMs or remote writes.

This checks publication only. It does not replace builds, native gameplay,
artifact provenance or independently applying both patches to the clean base.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
import zlib

DEFAULT_SITE = 'https://babycrttv.github.io/pokeemerald-emerald-legends/'


def validate_entries(receipt):
    entries = receipt['actual_live_files']
    if not entries:
        raise ValueError('Receipt has no expected live files')
    paths = set()
    for entry in entries:
        path = entry['path']
        parts = PurePosixPath(path)
        if (not path or parts.is_absolute() or '..' in parts.parts
                or str(parts) != path or re.search(r'[?#\\\s]', path)):
            raise ValueError('Expected a relative site path: ' + path)
        if path in paths:
            raise ValueError('Duplicate expected path: ' + path)
        paths.add(path)
        for field, size in [('sha256', 64), ('Git_blob_sha1', 40)]:
            if not re.fullmatch('[0-9a-f]{%d}' % size, entry[field]):
                raise ValueError('Invalid ' + field + ': ' + path)
        if not 0 <= entry['bytes'] <= 128 * 1024 * 1024:
            raise ValueError('Invalid expected file size: ' + path)
    return entries


def download(url, limit, timeout):
    request = Request(url, headers={'Cache-Control': 'no-cache',
                                   'Accept-Encoding': 'identity',
                                   'User-Agent': 'Legends-publication-verifier/1'})
    for attempt in range(2):
        try:
            with urlopen(request, timeout=timeout) as response:
                if response.status != 200:
                    raise ValueError('Expected HTTP 200')
                data = response.read(limit + 1)
                if len(data) > limit:
                    raise ValueError('Response exceeds expected file size')
                return data
        except HTTPError as error:
            if attempt or (error.code != 429 and error.code < 500):
                raise
        except (URLError, TimeoutError, ConnectionError):
            if attempt:
                raise
        time.sleep(0.5)


def check_file(entry, base_url, timeout):
    path = entry['path']
    try:
        data = download(base_url.rstrip('/') + '/' + path
                        + '?_legends_verify=' + str(time.time_ns()),
                        entry['bytes'], timeout)
        if len(data) != entry['bytes']:
            raise ValueError('File size differs from reviewed bytes')
        sha256 = hashlib.sha256(data).hexdigest()
        blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if sha256 != entry['sha256'] or blob != entry['Git_blob_sha1']:
            raise ValueError('Live bytes differ from reviewed hashes')
        row = dict(path=path, passed=True, HTTP=200, bytes=len(data),
                   sha256=sha256, Git_blob_sha1=blob)
        if path.endswith('.bps'):
            if len(data) < 16 or data[:4] != b'BPS1':
                raise ValueError('Invalid BPS header')
            if zlib.crc32(data[:-4]) != int.from_bytes(data[-4:], 'little'):
                raise ValueError('BPS patch CRC failed')
            for field, value in [('source_CRC32', data[-12:-8]),
                                 ('target_CRC32', data[-8:-4])]:
                crc = '%08x' % int.from_bytes(value, 'little')
                if field in entry and crc != entry[field]:
                    raise ValueError('BPS ' + field + ' differs from receipt')
                row[field] = crc
            row['patch_CRC_passed'] = True
        return row
    except Exception as error:
        return dict(path=path, passed=False, error=str(error))


def verify(receipt, base_url=DEFAULT_SITE, workers=4, timeout=20):
    if urlsplit(base_url).scheme not in ('http', 'https'):
        raise ValueError('Site must use HTTP or HTTPS')
    if not 1 <= workers <= 8 or not 0 < timeout <= 60:
        raise ValueError('Use 1–8 workers and a timeout of 1–60 seconds')
    entries = validate_entries(receipt)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(lambda entry: check_file(entry, base_url, timeout), entries))
    return dict(version=receipt.get('version'),
                verified_at_UTC=datetime.now(timezone.utc).isoformat(),
                passed=all(row['passed'] for row in rows), files=rows,
                scope='Fresh live HTTP bytes, reviewed SHA256/Git blobs and BPS footer CRCs only; not a gameplay, build or clean-base reconstruction test.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--receipt', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--base-url', default=DEFAULT_SITE)
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--timeout', type=int, default=20)
    args = parser.parse_args()
    try:
        raw = args.receipt.read_bytes()
        report = verify(json.loads(raw), args.base_url, args.workers, args.timeout)
        report['expected_receipt_sha256'] = hashlib.sha256(raw).hexdigest()
    except Exception as error:
        report = dict(passed=False, error=str(error))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + '.tmp')
    temporary.write_text(json.dumps(report, indent=2) + '\n')
    temporary.replace(args.output)
    for row in report.get('files', []):
        print(('PASS ' if row['passed'] else 'FAIL ') + row['path']
              + (': ' + row['error'] if 'error' in row else ''))
    if 'error' in report:
        print('FAIL ' + report['error'])
    return 0 if report['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
