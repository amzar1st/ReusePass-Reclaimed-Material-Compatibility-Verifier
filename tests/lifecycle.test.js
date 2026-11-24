import test from 'node:test';import assert from 'node:assert/strict';import {classifyTransaction as c,validateHash,safeParse} from '../src/lifecycle.js';
test('pending, accepted and finalized are distinct',()=>{assert.equal(c({status:'PENDING'}).state,'PENDING');assert.equal(c({status:'ACCEPTED',execution_result:'SUCCESS'}).terminal,false);assert.equal(c({status:'FINALIZED',execution_result:'SUCCESS'}).state,'SUCCESS');});
test('finality does not imply execution success',()=>{assert.equal(c({status:'FINALIZED',execution_result:'ERROR'}).state,'FAILED');assert.equal(c({status:'FINALIZED'}).state,'UNVERIFIED');});
test('terminal failures',()=>{for(const status of ['UNDETERMINED','CANCELED'])assert.equal(c({status}).state,'FAILED');assert.equal(c(null).state,'UNKNOWN');});
test('invalid hashes and corrupt storage',()=>{assert.equal(validateHash('0x'+'a'.repeat(64)),true);assert.equal(validateHash('0x123'),false);assert.deepEqual(safeParse('oops',[]),[]);});
