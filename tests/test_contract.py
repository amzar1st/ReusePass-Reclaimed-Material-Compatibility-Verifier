"""Contract unit tests with an explicit in-memory GenLayer host substitute.
These exercise real contract methods, not consensus, storage serialization or GenVM.
"""
import unittest,sys,types,importlib.util,json
from pathlib import Path
from types import SimpleNamespace
class Return:
    def __init__(self,v):self.calldata=v
class Host:
    sender='supplier'
    answer=None
    independent=None
    def execute(self,leader,validator):
        value=leader()
        self.answer,self.independent=self.independent or self.answer,None
        if not validator(Return(value)): raise Exception('Consensus disagreement')
        return value
host=Host()
gl=SimpleNamespace(Contract=object,public=SimpleNamespace(write=lambda f:f,view=lambda f:f),message=SimpleNamespace(sender_address='supplier'),vm=SimpleNamespace(Return=Return,run_nondet_unsafe=host.execute),nondet=SimpleNamespace(exec_prompt=lambda p, **kwargs:host.answer if kwargs.get('response_format')=='json' else json.dumps(host.answer)))
sys.modules['genlayer']=SimpleNamespace(gl=gl,TreeMap=dict,DynArray=list,__all__=['gl','TreeMap','DynArray'])
spec=importlib.util.spec_from_file_location('contract',Path(__file__).parents[1]/'contracts/reusepass.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
R=dict(title='Workshop',length_mm=1800,width_mm=100,thickness_mm=25,tolerance_mm=2,quantity=10,earliest_inspection=20260101,treatment='Untreated only',provenance='Origin and chain of custody required')
B=dict(label='Lot A',batch_ref='RP-A',description='Reclaimed boards',lots=[dict(length_mm=1800,width_mm=100,thickness_mm=25,quantity=10)])
CONTENT='Batch RP-A inspected 2026-11-01 by Yard. 10 boards 1800 x 100 x 25 mm. Untreated. Recovered warehouse, delivered by Yard.'
E=dict(title='Inspection',issuer='Yard',inspection_date=20261101,content=CONTENT,source_url='',source_sha256='')
def supported():return {k:dict(state='SUPPORTED',doc=0,quote=CONTENT) for k in c.FIELDS}
class ContractTests(unittest.TestCase):
    def setUp(self):
        gl.message.sender_address='supplier';host.answer=supported();host.independent=None
        self.x=c.ReusePass();self.x.requirements={};self.x.batches={};self.x.assessments={};self.x.requirement_ids=[];self.x.batch_ids=[]
        self.x.create_requirement('workshop',json.dumps(R));self.x.register_batch('a',json.dumps(B))
    def attach(self,e=E):self.x.attach_evidence('a',json.dumps(e))
    def assess(self,revision):
        self.x.assess_batch('workshop','a');return json.loads(self.x.get_requirement_findings('workshop','a',revision))
    def test_no_evidence_is_missing(self):self.assertEqual(self.assess(0)['status'],'MORE_EVIDENCE_NEEDED')
    def test_documented_match(self):self.attach();self.assertEqual(self.assess(1)['status'],'DOCUMENTED_MATCH')
    def test_missing_treatment(self):
        self.attach();host.answer['treatment']=dict(state='MISSING',doc=-1,quote='');self.assertEqual(self.assess(1)['status'],'MORE_EVIDENCE_NEEDED')
    def test_treatment_conflict(self):
        self.attach();host.answer['treatment']['state']='CONFLICT';self.assertEqual(self.assess(1)['status'],'REQUIREMENT_CONFLICT')
    def test_other_batch_cannot_qualify(self):
        self.attach();host.answer['coverage']=dict(state='MISSING',doc=-1,quote='');self.assertEqual(self.assess(1)['status'],'MORE_EVIDENCE_NEEDED')
    def test_forged_quote_rejected(self):
        self.attach();host.answer['treatment']['quote']='Invented nonexistent evidence'
        with self.assertRaisesRegex(Exception,'verbatim'):self.assess(1)
        self.assertEqual(self.x.assessments,{})
    def test_validator_disagreement(self):
        self.attach();host.independent=supported();host.independent['provenance']=dict(state='MISSING',doc=-1,quote='')
        with self.assertRaisesRegex(Exception,'disagreement'):self.assess(1)
    def test_expired_evidence_excluded(self):
        self.attach(dict(E,inspection_date=20250101));f=self.assess(1);self.assertEqual(f['status'],'MORE_EVIDENCE_NEEDED');self.assertEqual(f['excluded_expired_documents'],1)
    def test_snapshot_history_preserved(self):
        old=self.assess(0);self.attach();new=self.assess(1);self.assertNotEqual(old['status'],new['status']);self.assertEqual(json.loads(self.x.get_requirement_findings('workshop','a',0)),old)
    def test_supplier_ownership(self):
        gl.message.sender_address='attacker'
        with self.assertRaisesRegex(Exception,'Only supplier'):self.attach()
    def test_requirements_immutable(self):
        with self.assertRaisesRegex(Exception,'locked'):self.x.create_requirement('workshop',json.dumps(R))
    def test_duplicate_batch_rejected(self):
        with self.assertRaisesRegex(Exception,'registered'):self.x.register_batch('a',json.dumps(B))
    def test_duplicate_document(self):
        self.attach()
        with self.assertRaisesRegex(Exception,'Duplicate'):self.attach()
    def test_duplicate_assessment(self):
        self.assess(0)
        with self.assertRaisesRegex(Exception,'already exists'):self.assess(0)
    def test_tolerance_boundary(self):
        b=json.loads(json.dumps(B));b['lots'][0]['thickness_mm']=23;self.assertEqual(c.numerical_findings(R,b),[])
        b['lots'][0]['thickness_mm']=22;self.assertTrue(c.numerical_findings(R,b))
    def test_mixed_lots_count_only_usable(self):
        b=json.loads(json.dumps(B));b['lots'] += [dict(length_mm=300,width_mm=100,thickness_mm=25,quantity=99)];b['lots'][0]['quantity']=9
        f=c.numerical_findings(R,b);self.assertEqual(f[-1]['actual'],9)
    def test_bad_numeric_types(self):
        for v in [True,-1,1.1,'10',0]:
            with self.subTest(v=v),self.assertRaises(Exception):c.validate_requirement(dict(R,quantity=v))
    def test_bad_date(self):
        with self.assertRaises(ValueError):c.validate_requirement(dict(R,earliest_inspection=20260230))
    def test_bad_tolerance(self):
        with self.assertRaises(Exception):c.validate_requirement(dict(R,tolerance_mm=25))
    def test_arbitrary_url_rejected(self):
        with self.assertRaisesRegex(Exception,'immutable'):self.attach(dict(E,source_url='http://localhost/secrets'))
    def test_digest_mismatch(self):
        with self.assertRaisesRegex(Exception,'digest'):self.attach(dict(E,source_url='https://raw.githubusercontent.com/a/b/'+'a'*40+'/doc.txt',source_sha256='bad'))
    def test_valid_source_snapshot(self):
        self.attach(dict(E,source_url='https://raw.githubusercontent.com/a/b/'+'a'*40+'/doc.txt',source_sha256=c.digest(CONTENT)))
        self.assertEqual(json.loads(self.x.get_batch('a'))['revision'],1)
if __name__=='__main__':unittest.main()
