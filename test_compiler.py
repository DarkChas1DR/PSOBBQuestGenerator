import unittest,json,struct,tempfile,os,subprocess
from pathlib import Path
import compiler
ROOT=Path(__file__).resolve().parent
class CompilerTests(unittest.TestCase):
 def plan(self):return json.loads((ROOT/'examples/research-rescue.json').read_text(encoding='utf-8'))
 def test_binary_record_offsets(self):
  b=compiler.record(dict(type=68,floor=2,room=12,wave=9,position=[1,2,3],params=[1,2,3,4,5,6,7]),True)
  self.assertEqual(len(b),72);self.assertEqual(struct.unpack_from('<HH',b,12),(12,9));self.assertEqual(struct.unpack_from('<3f',b,20),(1,2,3));self.assertEqual(struct.unpack_from('<hh',b,64),(6,7))
 def test_reject_missing_positions(self):
  p=self.plan();p['waves'][0]['positions']=[]
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaisesRegex(ValueError,'explicit placement'):compiler.build(p,d,'not-called')
 def test_reject_duplicate_handler(self):
  p=self.plan();p['npcs'].append(p['npcs'][0].copy())
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaisesRegex(ValueError,'Duplicate'):compiler.build(p,d,'not-called')
 @unittest.skipUnless(os.environ.get('NEWSERV_PATH'),'Set NEWSERV_PATH for real compiler integration')
 def test_real_roundtrip(self):
  tool=os.environ['NEWSERV_PATH']
  with tempfile.TemporaryDirectory() as d:
   report=compiler.build(self.plan(),d,tool);d=Path(d)
   self.assertEqual(report['monster_records'],8);self.assertEqual(report['npc_records'],1)
   subprocess.run([tool,'decode-qst',str(d/'quest.qst'),'--bb'],check=True,capture_output=True)
   for ext in ['bin','dat']:
    decoded=list(d.glob('quest.qst-*.'+ext));self.assertEqual(len(decoded),1);self.assertEqual(decoded[0].read_bytes(),(d/('quest.'+ext)).read_bytes())
   mapping=(d/'map-check.txt').read_text(encoding='utf-8');self.assertEqual(mapping.count('[EnemySetEntry'),9);self.assertEqual(mapping.count('[ObjectSetEntry'),5)
   script=(d/'script-check.txt').read_text(encoding='utf-8');self.assertIn('.max_players 4',script);self.assertNotIn('.joinable',script);self.assertIn('sync_register2',script);self.assertIn('start_setevt',script)
if __name__=='__main__':unittest.main()
