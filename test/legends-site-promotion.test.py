"""Small real-git/ZIP fixtures for publication failures, holds and safe retries."""
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile
import zlib

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('site_guard', ROOT/'tools/legends/stage_site.py')
site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(site)


class API:
    def __init__(self, fixture):
        self.f = fixture
        self.master = fixture.base
        self.status = 'completed'
        self.conclusion = 'success'
        self.event = 'push'
        self.expired = False
        self.digest = None
        self.extra = None
        self.runs = None

    def archive(self):
        stream = io.BytesIO()
        with zipfile.ZipFile(stream, 'w') as archive:
            for name, data in self.f.payload.items():
                archive.writestr(name, data)
            if self.extra:
                archive.writestr(self.extra, b'unsafe')
        return stream.getvalue()

    def get(self, path, **kwargs):
        if path == '/commits/master':
            return dict(sha=self.master)
        if path == '/actions/runs/7':
            return dict(head_sha=self.f.base, status=self.status, conclusion=self.conclusion,
                        event=self.event, head_branch='master', run_attempt=1)
        if '/actions/workflows/' in path:
            runs = self.runs if self.runs is not None else [dict(
                id=7, head_sha=self.f.base, head_branch='master', event=self.event,
                status=self.status, conclusion=self.conclusion)]
            return dict(workflow_runs=runs)
        if '/artifacts?' in path:
            return dict(artifacts=[dict(id=17, name='legends-candidate-patches',
                expired=self.expired, digest=self.digest or 'sha256:'+site.sha(self.archive()),
                workflow_run=dict(head_sha=self.f.base))])
        if path == '/actions/artifacts/17/zip':
            return self.archive()
        raise AssertionError('Unexpected API path: '+path)


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.command('init', '-qb', 'master')
        self.command('config', 'user.name', 'Fixture')
        self.command('config', 'user.email', 'qa@example.test')
        for workflow in site.GATES:
            p = self.root/'.github/workflows'/workflow
            p.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT/'.github/workflows'/workflow, p)
        self.put('VERSION', '0.0.75\n')
        self.put('src/fixture.c', 'protected game')
        self.put('test/fixture.py', 'protected harness')
        self.put('docs/qa/history.json', '{}')
        for name in site.CRITICAL:
            self.put('docs/'+name, 'fixture asset')
        names = ['Pokemon-Emerald-Legends-v0.0.75.bps',
                 'Pokemon-Emerald-Legends-v0.0.75-debug.bps']
        self.put('docs/index.html', '<div class="version">v0.0.75</div>'
                 + ''.join('<a href="downloads/'+n+'">Patch</a>' for n in names))
        self.put('docs/changelog.html', '<div class="version">v0.0.75</div>')
        self.put('docs/patcher.html', 'Patch v0.0.75')
        self.put('docs/patcher.js', 'const VERSION = "0.0.75";')
        self.put('docs/wiki/dex-data.json', json.dumps(dict(gameVersion='0.0.75')))
        apk = b'signed fixture, not an actual APK'
        self.put('docs/downloads/Emerald-Legends-Wiki.apk', apk)
        self.put('docs/wiki/android-version.json', json.dumps(dict(available=True, sha256=site.sha(apk))))
        self.put('docs/wiki/windows-version.json', '{}')
        self.payload = {}
        results = {}
        binaries = {'pokeemerald-release.gba':'a'*64, 'pokeemerald.gba':'b'*64}
        for name, rom in zip(names, binaries):
            body = b'BPS1\x80\x80\x80'+(0x1f1c08fb).to_bytes(4, 'little')+bytes(4)
            data = body+zlib.crc32(body).to_bytes(4, 'little')
            self.payload[name] = data
            self.put('docs/downloads/'+name, data)
            results[name] = dict(exact_native_ROM_match=True, target_sha256=binaries[rom],
                                 patch_sha256=site.sha(data))
        self.payload['SHA256SUMS.txt'] = b'fixture sums'
        self.put('docs/downloads/SHA256SUMS.txt', self.payload['SHA256SUMS.txt'])
        self.base = self.commit()
        decoder = dict(passed=True, source_SHA1='f3ae088181bf583e55daf962a92bb46f4f1d07b7',results=results)
        self.payload['browser-decoder-verification.json'] = json.dumps(decoder).encode()
        self.manifest = dict(passed=True, patches_verified=True,
            inputs=dict(source_commit=self.base, version='0.0.75',binaries=binaries),
            native_receipt_sha256={name:'c'*64 for name in site.NATIVE}, decoder=decoder,
            payload_files={n:site.sha(d) for n,d in self.payload.items()})
        self.save_manifest()
        self.api = API(self)
        self.output = self.root/'build/site'

    def tearDown(self):
        self.temporary.cleanup()

    def command(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, stderr=subprocess.DEVNULL).decode().strip()

    def commit(self):
        self.command('add', '.')
        self.command('commit', '-qm', 'fixture')
        return self.command('rev-parse', 'HEAD')

    def put(self, path, content):
        path = self.root/path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode() if isinstance(content, str) else content)

    def save_manifest(self):
        self.payload['verification.json'] = json.dumps(self.manifest).encode()

    def gate(self, workflow='build-release-patch.yml'):
        current = self.command('rev-parse', 'HEAD')
        return site.select_gate(self.root, self.api, workflow, current,
                                {current:site.tree(self.root,current)})

    def test_complete_snapshot_binds_all_gates_and_exact_files(self):
        result = site.stage(self.root, self.api, self.output)
        self.assertEqual(set(result['gates']), set(site.GATES))
        self.assertEqual(result['verified_patch_artifact']['id'],17)
        expected = json.loads((self.output.parent/'site-expected.json').read_text())
        self.assertEqual(len(expected['actual_live_files']),len(site.CRITICAL)+3)
        for row in result['files']:
            self.assertEqual(row, site.file_row(self.output/row['path'],row['path']))
        self.assertFalse(self.output.with_name('site.partial').exists())

    def test_failed_cancelled_and_running_newest_gates_hold(self):
        for status, conclusion in [('completed','failure'),('completed','cancelled'),('in_progress',None)]:
            self.api.status,self.api.conclusion = status,conclusion
            with self.subTest(conclusion=conclusion),self.assertRaises(site.Hold):
                site.stage(self.root,self.api,self.output)
            self.assertFalse(self.output.exists())

    def test_candidate_success_is_not_production_evidence(self):
        self.api.event='pull_request'
        with self.assertRaises(site.Hold):
            self.gate()

    def test_same_version_with_changed_game_or_harness_is_not_reused(self):
        for path in ['src/fixture.c','.github/workflows/mgba-gameplay-qa.yml']:
            self.put(path,'changed verification input')
            self.commit()
            with self.subTest(path=path),self.assertRaises(site.Hold):
                self.gate()

    def test_doc_only_and_bot_outputs_reuse_identical_build_inputs(self):
        self.put('docs/qa/receipt.json','new evidence')
        self.put('docs/DEVELOPMENT-HANDOFF.md','new handoff')
        self.put('docs/wiki/windows-version.json','updated bot output')
        self.commit()
        self.assertEqual(self.gate()['source_commit'],self.base)
        self.assertEqual(self.gate('legends-checks.yml')['source_commit'],self.base)

    def test_changed_site_code_requires_new_host_gate(self):
        self.put('tools/legends/stage_site.py','new publication code')
        self.commit()
        with self.assertRaises(site.Hold):
            self.gate('legends-checks.yml')

    def test_newest_failed_matching_attempt_cannot_fall_back_to_success(self):
        self.api.runs=[dict(id=n,head_sha=self.base,head_branch='master',event='push',
            status='completed',conclusion=c) for n,c in [(9,'failure'),(7,'success')]]
        with self.assertRaises(site.Hold):
            self.gate()

    def test_corrupt_expired_and_unsafe_artifact_rejected(self):
        self.api.digest='sha256:'+'0'*64
        with self.assertRaisesRegex(ValueError,'digest'):
            site.stage(self.root,self.api,self.output)
        self.api.digest=None
        for path in ['pokeemerald.gba','../escape','nested/verification.json']:
            self.api.extra=path
            with self.subTest(path=path),self.assertRaisesRegex(ValueError,'archive'):
                site.stage(self.root,self.api,self.output)
        self.api.extra=None
        self.api.expired=True
        with self.assertRaises(site.Hold):
            site.stage(self.root,self.api,self.output)

    def test_manifest_native_and_decoder_mismatch_rejected(self):
        self.manifest['decoder']['results'][next(n for n in self.payload if n.endswith('.bps'))]['target_sha256']='0'*64
        self.payload['browser-decoder-verification.json']=json.dumps(self.manifest['decoder']).encode()
        self.manifest['payload_files']['browser-decoder-verification.json']=site.sha(self.payload['browser-decoder-verification.json'])
        self.save_manifest()
        with self.assertRaisesRegex(ValueError,'native proof'):
            site.stage(self.root,self.api,self.output)

    def test_pending_patch_commit_holds_without_mixing_frontend(self):
        self.put('docs/downloads/'+next(n for n in self.payload if n.endswith('.bps')),b'old patch')
        with self.assertRaises(site.Hold):
            site.stage(self.root,self.api,self.output)
        self.assertFalse(self.output.exists())

    def test_stale_labels_and_apk_manifest_are_rejected(self):
        for name in ['index.html','changelog.html','patcher.html','patcher.js','wiki/dex-data.json']:
            path=self.root/'docs'/name
            before=path.read_text()
            path.write_text(before.replace('0.0.75','0.0.74'))
            with self.subTest(path=name),self.assertRaises(ValueError):
                site.validate_site(self.root,self.payload,'0.0.75')
            path.write_text(before)
        self.put('docs/downloads/Emerald-Legends-Wiki.apk',b'wrong APK')
        with self.assertRaisesRegex(ValueError,'Android'):
            site.validate_site(self.root,self.payload,'0.0.75')

    def test_symlinks_roms_and_saves_cannot_enter_site(self):
        for name in ['rom.gba','symbols.elf','owner.sav']:
            p=self.root/'docs'/name;p.write_bytes(b'private')
            with self.subTest(path=name),self.assertRaisesRegex(ValueError,'Unsafe'):
                site.validate_site(self.root,self.payload,'0.0.75')
            p.unlink()
        p=self.root/'docs/link';p.symlink_to(self.root/'VERSION')
        with self.assertRaisesRegex(ValueError,'Unsafe'):
            site.validate_site(self.root,self.payload,'0.0.75')

    def test_interrupted_staging_cleans_partial_and_retry_is_identical(self):
        def interrupted(source,destination,*args,**kwargs):
            Path(destination).mkdir(parents=True)
            (Path(destination)/'index.html').write_text('incomplete')
            raise OSError('interrupted fixture')
        with patch.object(site.shutil,'copytree',side_effect=interrupted),self.assertRaises(OSError):
            site.stage(self.root,self.api,self.output)
        self.assertFalse(self.output.exists())
        self.assertFalse(self.output.with_name('site.partial').exists())
        first=site.stage(self.root,self.api,self.output)
        manifest=(self.output/'release-publication.json').read_bytes()
        shutil.rmtree(self.output)
        self.assertEqual(first,site.stage(self.root,self.api,self.output))
        self.assertEqual(manifest,(self.output/'release-publication.json').read_bytes())

    def test_master_advancing_refuses_promotion(self):
        site.fresh(self.api,self.base)
        gates={'host':self.gate('legends-checks.yml')}
        site.fresh(self.api,self.base,gates)
        self.api.status='in_progress'
        with self.assertRaises(site.Hold):
            site.fresh(self.api,self.base,gates)
        self.api.status='completed'
        self.api.master='0'*40
        with self.assertRaises(site.Hold):
            site.fresh(self.api,self.base)

    def test_github_globs_preserve_path_boundaries(self):
        for path,pattern,expected in [('Makefile','*.mk',False),('root.mk','*.mk',True),
            ('nested/root.mk','*.mk',False),('src/a/b.c','src/**',True),
            ('tools/legends/native_eon/a.py','tools/legends/native_*/**',True),
            ('docs/a.md','docs/**/*.md',True),('docs/a/b.md','docs/**/*.md',True)]:
            with self.subTest(path=path,pattern=pattern):
                self.assertEqual(site.glob_match(path,pattern),expected)

    def test_workflow_only_deploys_complete_master_snapshot(self):
        p=(ROOT/'.github/workflows/pages.yml').read_text()
        import yaml
        workflow=yaml.load(p,Loader=yaml.BaseLoader)
        self.assertEqual(workflow['jobs']['deploy']['needs'],'prepare')
        self.assertIn("pages_mode == 'workflow'",workflow['jobs']['deploy']['if'])
        self.assertIn("ready == 'true'",workflow['jobs']['deploy']['if'])
        self.assertIn('stage_site.py fresh',p)
        self.assertIn('actions/deploy-pages@v4',p)
        self.assertNotIn('pull_request_target',workflow['on'])


if __name__=='__main__':
    unittest.main()
