import unittest,json,copy
from unittest.mock import patch
from pathlib import Path
import encounter_ai
class RecipeTests(unittest.TestCase):
 def recipe(self):return dict(name='Lost Research Team',brief='Rescue the researcher.',dialogue='Clear the enemies and return.',difficulty='Ultimate',party=4,waves=[dict(enemy='savage_wolf',count=6),dict(enemy='gobooma',count=8)],unsupported=[])
 def test_expands_positions_and_preserves_counts(self):
  p=encounter_ai.expand(self.recipe());self.assertEqual([len(w['positions']) for w in p['waves']],[6,8]);self.assertEqual(len(p['spawns']),4);self.assertEqual(p['waves'][0]['type'],67);self.assertTrue(all(x['params'][1]==0 for x in p['waves'][0]['positions']));self.assertTrue(all(x['params'][5]==1 for x in p['waves'][1]['positions']));self.assertEqual(p['npcs'][0]['dialogue'],'Clear the enemies and return.')
 def test_insufficient_anchors(self):
  r=self.recipe();r['waves']=[dict(enemy='booma',count=25)]
  with self.assertRaises(ValueError):encounter_ai.expand(r)
 def test_unsupported_request_not_silently_dropped(self):
  r=self.recipe();r['unsupported']=['Dragon boss']
  with self.assertRaisesRegex(ValueError,'Dragon'):encounter_ai.expand(r)
 def test_positive_boss_request_blocked_before_provider(self):
  with patch('encounter_ai.urllib.request.urlopen') as request:
   with self.assertRaisesRegex(ValueError,'boss'):encounter_ai.generate('Add the Dragon boss','test')
   request.assert_not_called()
 def test_negative_boss_instruction_allowed(self):encounter_ai.check_preset_request('Rescue quest without a boss')
 def test_real_adapter_shape_with_mock(self):
  recipe=self.recipe()
  class R:
   def __enter__(self):return self
   def __exit__(self,*args):pass
   def read(self,n):return json.dumps({'message':{'content':json.dumps(recipe)}}).encode()
  with patch('encounter_ai.urllib.request.urlopen',return_value=R()):self.assertEqual(encounter_ai.generate('rescue','test')['name'],'Lost Research Team')
if __name__=='__main__':unittest.main()
