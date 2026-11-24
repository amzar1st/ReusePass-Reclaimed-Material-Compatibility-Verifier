import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import {CONFIG} from './config.js';
const client=createClient({chain:studionet,endpoint:CONFIG.rpc});
export async function rpc(method,params=[]){
 const res=await fetch(CONFIG.rpc,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({jsonrpc:'2.0',id:Date.now(),method,params}),signal:AbortSignal.timeout(25000)});
 if(!res.ok)throw new Error(`Network HTTP ${res.status}`);const data=await res.json();if(data.error)throw new Error(data.error.message);return data.result;
}
export async function read(functionName,args=[]){if(!CONFIG.contract)throw new Error('Contract deployment is not configured');return JSON.parse(await client.readContract({address:CONFIG.contract,functionName,args,transactionHashVariant:'latest-final'}));}
export async function loadDashboard(){
 const chain=await rpc('eth_chainId');if(Number(chain)!==CONFIG.chainId)throw new Error('Unexpected chain ID; writes disabled');
 const records=await read('list_records');
 const [requirements,batches]=await Promise.all([Promise.all(records.requirements.map(async id=>({id,...await read('get_requirement',[id])}))),Promise.all(records.batches.map(async id=>({id,...await read('get_batch',[id])})))]);
 return {requirements,batches};
}
export async function transactions(){return await rpc('sim_getTransactionsForAddress',[CONFIG.contract]);}
