"""Publication verifier rejects stale/corrupt bytes without external network access."""
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'tools/legends/verify_public_release.py'
spec = importlib.util.spec_from_file_location('publication', SCRIPT)
publication = importlib.util.module_from_spec(spec)
spec.loader.exec_module(publication)


def entry(path, data):
    return dict(path=path, bytes=len(data), sha256=hashlib.sha256(data).hexdigest(),
                Git_blob_sha1=hashlib.sha1(b'blob ' + str(len(data)).encode()
                                          + b'\0' + data).hexdigest())


class PublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.responses = {}
        cls.calls = {}
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                path = self.path.split('?')[0]
                cls.calls[path] = cls.calls.get(path, 0) + 1
                status, data = cls.responses.get(path, (404, b''))
                if status == 503 and cls.calls[path] > 1:
                    status = 200
                self.send_response(status)
                self.send_header('Content-Length', str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            def log_message(self, *_args):
                pass
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.site = 'http://127.0.0.1:' + str(cls.server.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def receipt(self, path='index.html', data=b'reviewed', status=200):
        self.responses['/' + path] = (status, data)
        self.calls.pop('/' + path, None)
        return dict(version='fixture', actual_live_files=[entry(path, data)])

    def test_exact_live_bytes_and_git_blob(self):
        result = publication.verify(self.receipt(), self.site)
        self.assertTrue(result['passed'])
        self.assertEqual(result['files'][0]['HTTP'], 200)

    def test_stale_same_length_data_is_rejected_without_retry(self):
        receipt = self.receipt(data=b'approved')
        self.responses['/index.html'] = (200, b'obsolete')
        result = publication.verify(receipt, self.site)
        self.assertFalse(result['passed'])
        self.assertIn('hashes', result['files'][0]['error'])
        self.assertEqual(self.calls['/index.html'], 1)

    def test_truncated_and_oversized_responses_fail(self):
        for data in [b'short', b'too long for the expected file']:
            with self.subTest(data=data):
                receipt = self.receipt()
                self.responses['/index.html'] = (200, data)
                self.assertFalse(publication.verify(receipt, self.site)['passed'])

    def test_transient_server_error_retries_once(self):
        result = publication.verify(self.receipt(status=503), self.site)
        self.assertTrue(result['passed'])
        self.assertEqual(self.calls['/index.html'], 2)

    def test_missing_file_does_not_retry_and_other_files_are_checked(self):
        receipt = self.receipt(status=404)
        receipt['actual_live_files'] += self.receipt('other.txt')['actual_live_files']
        result = publication.verify(receipt, self.site)
        self.assertFalse(result['passed'])
        self.assertTrue(result['files'][1]['passed'])
        self.assertEqual(self.calls['/index.html'], 1)

    def test_bps_footer_crc_is_checked_even_when_expected_hashes_match(self):
        # Empty source/target BPS, then a deliberately corrupted patch checksum.
        body = b'BPS1\x80\x80\x80' + bytes(8)
        patch = body + zlib.crc32(body).to_bytes(4, 'little')
        receipt = self.receipt('fixture.bps', patch)
        receipt['actual_live_files'][0].update(source_CRC32='00000000', target_CRC32='00000000')
        self.assertTrue(publication.verify(receipt, self.site)['passed'])
        receipt['actual_live_files'][0]['target_CRC32'] = '00000001'
        self.assertFalse(publication.verify(receipt, self.site)['passed'])
        receipt = self.receipt('fixture.bps', patch[:-1] + bytes([patch[-1] ^ 1]))
        result = publication.verify(receipt, self.site)
        self.assertFalse(result['passed'])
        self.assertIn('patch CRC', result['files'][0]['error'])

    def test_empty_duplicate_and_traversal_receipts_fail_before_network(self):
        for paths in [[], ['index.html', 'index.html'], ['../outside'], ['/absolute'], ['x?query'], ['x#fragment']]:
            with self.subTest(paths=paths):
                with self.assertRaises(ValueError):
                    publication.verify(dict(actual_live_files=[entry(p, b'') for p in paths]), self.site)

    def test_cli_replaces_old_success_with_failure_and_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            receipt = folder/'receipt.json'
            output = folder/'report.json'
            receipt.write_text(json.dumps(self.receipt()))
            cmd = [sys.executable, str(SCRIPT), '--receipt', str(receipt),
                   '--output', str(output), '--base-url', self.site]
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertTrue(json.loads(output.read_text())['passed'])
            receipt.write_text('{}')
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            self.assertFalse(json.loads(output.read_text())['passed'])


if __name__ == '__main__':
    unittest.main()
