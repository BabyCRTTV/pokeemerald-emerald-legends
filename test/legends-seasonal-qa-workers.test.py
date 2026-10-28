"""Test complete coverage, isolation and failures without needing a ROM or mGBA."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT/'tools/legends/native_seasonal_encounters_qa/workers.py'
spec = importlib.util.spec_from_file_location('workers', SCRIPT)
workers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(workers)

FAKE = '''import os,sys,time
from pathlib import Path
mode=sys.argv[1];out=Path(sys.argv[2]);total,start,stop=map(int,sys.argv[-3:])
if mode.startswith('barrier:'):
 (out/'started').write_text(str(os.getpid()))
 deadline=time.monotonic()+5
 while len(list(out.parent.glob('worker-*/started')))<int(mode.split(':')[1]):
  if time.monotonic()>deadline:raise RuntimeError('workers did not overlap')
  time.sleep(.01)
if mode=='timeout':time.sleep(5)
if mode=='crash' and start==0:
 print('retained native failure',flush=True);sys.exit(3)
for scene in range(start,stop):
 (out/('scene-%02d-gui.rgba'%scene)).write_bytes(('pixels %d'%scene).encode())
 if mode=='missing' and scene==start:continue
 if mode=='wrong-range' and scene==start:scene=total
 print('PASS scene %d: 256 real wild creations'%scene,flush=True)
 if mode=='duplicate' and scene==start:print('PASS scene %d: duplicate'%scene,flush=True)
if mode=='missing-image':(out/('scene-%02d-gui.rgba'%start)).unlink()
if mode=='wrong-image':(out/('scene-%02d-gui.rgba'%total)).write_bytes(b'wrong')
'''


class WorkerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.fake = self.root/'fake.py'
        self.fake.write_text(FAKE)

    def tearDown(self):
        self.temporary.cleanup()

    def execute(self, mode='ok', jobs=4, name='run', total=11, timeout=10):
        return workers.execute([sys.executable, str(self.fake)], mode,
                               ['0', '0', '0'], total, jobs, self.root/name, timeout)

    def test_all_partition_boundaries_have_exact_once_coverage(self):
        for total in [1, 2, 3, 5, 11, 287, 288, 289]:
            for jobs in range(1, 5):
                ranges = workers.partitions(total, jobs)
                self.assertEqual([x for a, b in ranges for x in range(a, b)], list(range(total)))
                self.assertTrue(all(a < b for a, b in ranges))
                self.assertEqual(len(ranges), min(jobs, total))
        for args in [(0, 1), (288, 0), (288, 5)]:
            with self.assertRaises(ValueError):
                workers.partitions(*args)

    def test_cpu_cap_and_explicit_serial_option(self):
        self.assertEqual(workers.worker_count(1), 1)
        self.assertTrue(1 <= workers.worker_count() <= 4)
        for jobs in [0, -1, 5]:
            with self.assertRaises(ValueError):
                workers.worker_count(jobs)

    def test_real_processes_overlap_and_merge_in_global_order(self):
        report = self.execute('barrier:4')
        self.assertTrue(report['passed'] and report['exact_coverage'])
        self.assertEqual(report['wild_creations'], 11*256)
        folder = self.root/'run'
        self.assertEqual(len({p.read_text() for p in folder.glob('worker-*/started')}), 4)
        observed = [int(v) for v in workers.PASS.findall((folder/'emulator.log').read_text())]
        self.assertEqual(observed, list(range(11)))

    def test_missing_duplicate_and_wrong_range_passes_are_rejected(self):
        for mode in ['missing', 'duplicate', 'wrong-range']:
            with self.subTest(mode=mode), self.assertRaises(RuntimeError):
                self.execute(mode, name=mode)

    def test_missing_and_out_of_range_captures_are_rejected(self):
        for mode in ['missing-image', 'wrong-image']:
            with self.subTest(mode=mode), self.assertRaises(RuntimeError):
                self.execute(mode, name=mode)

    def test_failure_keeps_sibling_results_and_diagnostics(self):
        with self.assertRaises(RuntimeError):
            self.execute('crash')
        report = json.loads((self.root/'run/execution.json').read_text())
        self.assertFalse(report['passed'])
        self.assertEqual(len(report['worker_results']), 4)
        self.assertEqual(sum(row['passed'] for row in report['worker_results']), 3)
        self.assertIn('retained native failure', (self.root/'run/worker-0/emulator.log').read_text())

    def test_timeout_fails_and_keeps_machine_receipt(self):
        with self.assertRaises(RuntimeError):
            self.execute('timeout', jobs=1, timeout=.1)
        report = json.loads((self.root/'run/execution.json').read_text())
        self.assertFalse(report['passed'])
        self.assertIn('timed out', report['worker_results'][0]['error'])

    def test_serial_parallel_exact_logs_and_pixels(self):
        self.execute(jobs=1, name='serial')
        self.execute(jobs=4, name='parallel')
        report = workers.compare(self.root/'serial', self.root/'parallel')
        self.assertTrue(report['passed'])
        self.assertEqual(report['exact_raw_captures'], 11)
        capture = next((self.root/'parallel').glob('worker-*/*.rgba'))
        capture.write_bytes(b'changed pixels')
        with self.assertRaisesRegex(ValueError, 'pixels differ'):
            workers.compare(self.root/'serial', self.root/'parallel')

    def test_stale_output_is_rejected(self):
        self.execute()
        with self.assertRaisesRegex(ValueError, 'must be fresh'):
            self.execute()


if __name__ == '__main__':
    unittest.main()
