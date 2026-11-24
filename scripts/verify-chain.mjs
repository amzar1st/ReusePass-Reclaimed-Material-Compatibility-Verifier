import fs from 'node:fs';
import crypto from 'node:crypto';
import {read,rpc} from '../src/chain.js';
import {CONFIG} from '../src/config.js';
const result={checked_at:new Date().toISOString(),chain_id:Number(await rpc('eth_chainId')),contract:CONFIG.contract,records:await read('list_records'),findings:{},transactions:[]};
const txs=await rpc('sim_getTransactionsForAddress',[CONFIG.contract]);
for(const tx of txs){
 const hash=tx.hash||tx.transaction_hash;const full=await rpc('eth_getTransactionByHash',[hash]);
 const summary={hash:full.hash,status:full.status,execution_result:full.txExecutionResultName,from:full.from_address,to:full.to_address,type:full.type,created_at:full.created_at,execution_mode:full.execution_mode,validators:full.num_of_initial_validators,votes:full.consensus_data?.votes};
 result.transactions.push(summary);
 const receipts=[...(full.consensus_data?.leader_receipt||[]),...(full.consensus_data?.validators||[])].map(r=>({mode:r.mode,vote:r.vote,execution_result:r.execution_result,result:r.result,eq_outputs:r.eq_outputs,stderr:r.genvm_result?.stderr}));
 fs.writeFileSync(`evidence/receipt-${hash.slice(2,10)}.json`,JSON.stringify({...summary,receipts},null,2));
 if(full.type===1&&full.data?.contract_code){const deployed=Buffer.from(full.data.contract_code,'base64');result.source_sha256=crypto.createHash('sha256').update(deployed).digest('hex');result.deployed_source_matches_checkout=deployed.equals(fs.readFileSync('contracts/reusepass.py'));}
}
for(const id of result.records.batches){const b=await read('get_batch',[id]);result.findings[id]=await read('get_requirement_findings',[result.records.requirements[0],id,b.revision]);}
fs.writeFileSync('evidence/verification.json',JSON.stringify(result,null,2));
console.log(JSON.stringify({...result,findings:Object.fromEntries(Object.entries(result.findings).map(([k,v])=>[k,v.status||'UNASSESSED']))},null,2));
