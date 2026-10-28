"""Shared-build provenance and fail-closed publication, using small local fixtures."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('shared', ROOT/'tools/legends/shared_build.py')
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)


class SharedBuildTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        for args in [['init', '-q'], ['config', 'user.email', 'qa@example.test'], ['config', 'user.name', 'QA']]:
            subprocess.run(['git', *args], cwd=self.root, check=True, capture_output=True)
        (self.root/'VERSION').write_text('0.0.75\n')
        (self.root/'source.c').write_text('protected source')
        self.commit()
        for name in shared.BINARIES:
            (self.root/name).write_bytes(('private fixture '+name).encode())
        self.inputs = shared.record(self.root)
        self.folder = shared.workdir(self.root)
        for path, (variant, field) in shared.NATIVE.items():
            rom = 'pokeemerald.gba' if variant == 'Debug' else 'pokeemerald-release.gba'
            shared.write(self.root/'build'/path, {field: self.inputs['binaries'][rom], 'passed': True})
        shared.write(self.folder/'worker-start.json', dict(pid=os.getpid(), nonce=self.inputs['nonce']))
        shared.write(self.folder/'patch-worker.json', dict(passed=True, seconds=.1, nonce=self.inputs['nonce']))
        self.publication = self.folder/'publication'
        self.publication.mkdir()
        names = shared.patch_names('0.0.75')
        results = {}
        for name, rom in zip(names, ['pokeemerald-release.gba', 'pokeemerald.gba']):
            body = b'BPS1\x80\x80\x80' + (0x1f1c08fb).to_bytes(4, 'little') + bytes(4)
            (self.publication/name).write_bytes(body + zlib.crc32(body).to_bytes(4, 'little'))
            results[name] = dict(exact_native_ROM_match=True, target_sha256=self.inputs['binaries'][rom],
                                 patch_sha256=shared.sha(self.publication/name))
        shared.write(self.publication/'browser-decoder-verification.json',
                     dict(passed=True, source_SHA1='f3ae088181bf583e55daf962a92bb46f4f1d07b7', results=results))

    def tearDown(self):
        self.temporary.cleanup()

    def commit(self):
        subprocess.run(['git', 'add', '.'], cwd=self.root, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-qm', 'fixture'], cwd=self.root, check=True, capture_output=True)

    def check(self, manifest=None):
        return shared.check_publication(self.root, self.publication,
                                        manifest or shared.sha(self.publication/'verification.json'),
                                        self.inputs['source_commit'], self.inputs['source_fingerprint'])

    def test_complete_chain_binds_native_decoders_and_payload(self):
        result = shared.finalize(self.root)
        self.assertTrue(result['passed'] and result['patches_verified'])
        self.assertEqual(len(result['native_receipt_sha256']), 12)
        self.assertEqual(len(self.check()['payload_files']), 4)

    def test_each_compiled_rom_and_elf_is_immutable(self):
        for name in shared.BINARIES:
            original = (self.root/name).read_bytes()
            (self.root/name).write_bytes(b'changed')
            with self.subTest(name=name), self.assertRaisesRegex(ValueError, 'Shared build changed'):
                shared.unchanged(self.root, self.inputs)
            (self.root/name).write_bytes(original)

    def test_missing_and_wrong_variant_native_receipts_fail(self):
        path = self.root/'build/eon-roamers-qa/verification.json'
        path.unlink()
        with self.assertRaises(FileNotFoundError):
            shared.finalize(self.root)
        shared.write(path, {'ROM_sha256': self.inputs['binaries']['pokeemerald-release.gba']})
        with self.assertRaisesRegex(ValueError, 'Native receipt'):
            shared.finalize(self.root)

    def test_decoder_target_must_equal_native_tested_build(self):
        path = self.publication/'browser-decoder-verification.json'
        data = shared.read(path)
        next(iter(data['results'].values()))['target_sha256'] = '0'*64
        shared.write(path, data)
        with self.assertRaisesRegex(ValueError, 'target mismatch'):
            shared.finalize(self.root)

    def test_native_failure_and_patch_failure_reject_publication(self):
        path = self.root/'build/seasonal-encounters-qa/verification.json'
        data = shared.read(path)
        data['passed'] = False
        shared.write(path, data)
        with self.assertRaisesRegex(ValueError, 'Native receipt'):
            shared.finalize(self.root)
        data['passed'] = True
        shared.write(path, data)
        shared.write(self.folder/'patch-worker.json', dict(passed=False, nonce=self.inputs['nonce'], error='decoder failed'))
        with self.assertRaisesRegex(RuntimeError, 'decoder failed'):
            shared.finalize(self.root)

    def test_stale_worker_and_manifest_are_rejected(self):
        shared.write(self.folder/'patch-worker.json', dict(passed=True, seconds=.1, nonce='old'))
        with self.assertRaisesRegex(ValueError, 'Stale'):
            shared.join(self.root)
        shared.write(self.folder/'patch-worker.json', dict(passed=True, seconds=.1, nonce=self.inputs['nonce']))
        shared.finalize(self.root)
        with self.assertRaisesRegex(ValueError, 'manifest hash'):
            self.check('0'*64)

    def test_tampered_missing_and_extra_artifact_files_fail(self):
        shared.finalize(self.root)
        name = shared.patch_names('0.0.75')[0]
        original = (self.publication/name).read_bytes()
        (self.publication/name).write_bytes(b'tampered')
        with self.assertRaisesRegex(ValueError, 'hash/type'):
            self.check()
        (self.publication/name).write_bytes(original)
        (self.publication/'leaked.gba').write_bytes(b'never upload')
        with self.assertRaisesRegex(ValueError, 'Unexpected artifact'):
            self.check()
        (self.publication/'leaked.gba').unlink()
        (self.publication/name).unlink()
        with self.assertRaisesRegex(ValueError, 'Unexpected artifact'):
            self.check()

    def test_unexpected_rom_is_blocked_before_artifact_upload(self):
        (self.publication/'leaked.gba').write_bytes(b'never upload')
        with self.assertRaisesRegex(ValueError, 'refusing artifact upload'):
            shared.finalize(self.root)

    def test_only_bot_publication_outputs_may_advance(self):
        # Do not accidentally include the private fixture ROMs in this Git fixture.
        (self.root/'.gitignore').write_text('*.gba\n*.elf\nbuild/\n')
        subprocess.run(['git', 'add', '.gitignore'], cwd=self.root, check=True)
        subprocess.run(['git', 'commit', '-qm', 'ignore fixtures'], cwd=self.root, check=True)
        fingerprint = shared.fingerprint(self.root)
        for name in ['docs/downloads/a.bps', 'docs/wiki/windows-version.json', 'docs/wiki/android-version.json']:
            p = self.root/name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text('new bot output')
        self.commit()
        self.assertEqual(shared.fingerprint(self.root), fingerprint)
        (self.root/'source.c').write_text('new owner code/map edit')
        self.commit()
        self.assertNotEqual(shared.fingerprint(self.root), fingerprint)

    def test_new_source_head_blocks_old_payload(self):
        shared.finalize(self.root)
        (self.root/'.gitignore').write_text('*.gba\n*.elf\nbuild/\n')
        self.commit()
        with self.assertRaisesRegex(ValueError, 'Stale or incomplete'):
            self.check()

    def test_native_only_manual_result_cannot_be_published(self):
        result = shared.finalize(self.root, patches=False)
        shared.write(self.publication/'verification.json', result)
        with self.assertRaisesRegex(ValueError, 'Stale or incomplete'):
            self.check()

    def test_timeout_kills_command_group(self):
        with self.assertRaises(subprocess.TimeoutExpired):
            shared.run_group([sys.executable, '-c', 'import time;time.sleep(5)'], self.root, .1)

    def test_automatic_builds_have_one_owner_and_no_rom_transfer(self):
        native = (ROOT/'.github/workflows/mgba-gameplay-qa.yml').read_text()
        caller = (ROOT/'.github/workflows/build-release-patch.yml').read_text()
        trigger = native.split('on:\n', 1)[1].split('\npermissions:', 1)[0]
        self.assertNotIn('  push:', trigger)
        self.assertNotIn('  pull_request:', trigger)
        self.assertIn('workflow_call:', trigger)
        self.assertEqual(native.count('run: make -j"$(nproc)"\n'), 1)
        self.assertEqual(native.count('run: make -j"$(nproc)" release\n'), 1)
        self.assertNotIn('run: make ', caller)
        self.assertIn('uses: ./.github/workflows/mgba-gameplay-qa.yml', caller)
        self.assertIn('path: build/shared-build/publication/', native)
        self.assertNotIn('upload-artifact', caller)


if __name__ == '__main__':
    unittest.main()
