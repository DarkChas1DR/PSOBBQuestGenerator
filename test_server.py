import unittest,json
from unittest.mock import patch
import server
class Tests(unittest.TestCase):
 def fixture(self):
  a=next(a for a in server.REF['floors'] if a['area']==1);v=a['variants'][0];g=next(g for g in server.REF['geometry'] if g['map']==v['setup_basename']);e=next(e for e in server.REF['entities'] if e['kind']=='monster')
  return dict(schema=1,name='Test',brief='Test',difficulty='Ultimate',party=4,npcs=[],waves=[dict(episode=1,floor=1,area=1,layout=v['layout'],entities=v['entities'],map=v['object_basename'],table=v['table'],room=g['section_ids'][0],type=e['id'],wave=1,count=6)])
 def test_valid(self):self.assertEqual(server.validate(self.fixture())['waves'][0]['positions'],[])
 def test_unknown_room(self):
  p=self.fixture();p['waves'][0]['room']=65535
  with self.assertRaises(ValueError):server.validate(p)
 def test_invalid_count(self):
  p=self.fixture();p['waves'][0]['count']=-1
  with self.assertRaises(ValueError):server.validate(p)
 def test_invented_variant(self):
  p=self.fixture();p['waves'][0]['map']='invented'
  with self.assertRaises(ValueError):server.validate(p)
 def test_ai_response(self):
  class Response:
   def __enter__(self):return self
   def __exit__(self,*a):pass
   def read(self,n):return json.dumps({'message':{'content':json.dumps(Tests().fixture())}}).encode()
  with patch('server.urllib.request.urlopen',return_value=Response()):self.assertEqual(server.generate('make a quest',None,'test')['party'],4)
if __name__=='__main__':unittest.main()
