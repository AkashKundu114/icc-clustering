import hashlib, json, tempfile, unittest, uuid
from pathlib import Path
import numpy as np
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from validate_run_manifest import validate
H='a'*64
def h(b): return hashlib.sha256(b).hexdigest()
class TraceValidatorTests(unittest.TestCase):
 def test_duplicate_run_id_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'m.json'; rec={'run_id':'same','execution':{'status':'failed'}}
   p.write_text(json.dumps({'records':[rec,rec]}),encoding='utf-8')
   out=validate(p); self.assertFalse(out['ok']); self.assertTrue(any('duplicate run_id' in x for x in out['errors']))
 def test_empty_manifest_valid(self):
  with tempfile.TemporaryDirectory() as td:
   p=Path(td)/'m.json'; p.write_text(json.dumps({'records':[]}),encoding='utf-8')
   out=validate(p); self.assertTrue(out['ok']); self.assertEqual(out['n_records'],0)
 def test_valid_partition_trace(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td); ix=np.array([0,2,4,6],dtype=np.int64); y=np.array([0,0,1,1],dtype=np.int64)
   part=root/'part.npy'; np.save(part,{'sub_idx':ix,'labels':y},allow_pickle=True)
   rec={'run_id':str(uuid.uuid4()),'source':{'config_sha256':H,'environment_sha256':H},'data':{'raw_sha256':H,'feature_sha256':H,'ordered_sample_ids_sha256':H,'labels_sha256':H},'sampling':{'indices_sha256':h(ix.tobytes())},'execution':{'status':'success'},'output':{'partition_path':'part.npy','partition_sha256':h(part.read_bytes()),'assignment_sha256':h(y.tobytes()),'n_samples':4,'observed_k':2,'cluster_sizes':[2,2]}}
   mf=root/'manifest.json'; mf.write_text(json.dumps({'records':[rec]}),encoding='utf-8')
   out=validate(mf); self.assertTrue(out['ok'],out['errors'])
 def test_partition_hash_mismatch_rejected(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(td); ix=np.array([0,1]); y=np.array([0,1]); part=root/'part.npy'; np.save(part,{'sub_idx':ix,'labels':y},allow_pickle=True)
   rec={'run_id':str(uuid.uuid4()),'source':{'config_sha256':H,'environment_sha256':H},'data':{'raw_sha256':H,'feature_sha256':H,'ordered_sample_ids_sha256':H,'labels_sha256':H},'sampling':{'indices_sha256':h(ix.tobytes())},'execution':{'status':'success'},'output':{'partition_path':'part.npy','partition_sha256':H,'assignment_sha256':h(y.tobytes()),'n_samples':2,'observed_k':2,'cluster_sizes':[1,1]}}
   mf=root/'manifest.json'; mf.write_text(json.dumps({'records':[rec]}),encoding='utf-8')
   out=validate(mf); self.assertFalse(out['ok']); self.assertTrue(any('partition SHA-256 mismatch' in e for e in out['errors']))
if __name__=='__main__':unittest.main()
