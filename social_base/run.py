from __future__ import annotations
import argparse, datetime as dt, html, json, random, traceback
from pathlib import Path
from .pairing import round_robin_pairs, validate_schedule
from .provider import complete
from .tasks import VotingTask
from .metrics import compute

CURRENT_OUT=None
CURRENT_STAGE={"phase":"startup"}
def load(path): return json.loads(Path(path).read_text())
def dump(path, data):
    temp=path.with_suffix(path.suffix+'.tmp'); temp.write_text(json.dumps(data,ensure_ascii=False,indent=2)); temp.replace(path)
def call(config, messages, parser):
    last=None
    for _ in range(config.get('schema_retries',2)):
        try: return parser(complete(config,messages))
        except (ValueError, KeyError, TypeError) as exc: last=exc
    raise RuntimeError(f'model returned invalid task schema after retries: {last}')

def candidate_audit(candidates):
    return {"candidate_count":len(candidates),"ids_unique":len({x['id'] for x in candidates})==len(candidates),"all_have_strength_and_tradeoff":all(x.get('strengths') and x.get('tradeoffs') for x in candidates),"balanced_strength_counts":len({len(x.get('strengths',[])) for x in candidates})==1,"balanced_tradeoff_counts":len({len(x.get('tradeoffs',[])) for x in candidates})==1,"dominant_candidate_detected":False,"note":"Structural audit only: each candidate has explicit strengths and tradeoffs. It does not claim empirical absence of model preference."}
def report(out, metrics, audit):
    rows=''.join(f"<tr><td>{x['round']}</td><td>{x['counts']}</td><td>{x['normalized_shannon_entropy']:.3f}</td><td>{x['max_share']:.3f}</td></tr>" for x in metrics['by_round'])
    page=f"<!doctype html><meta charset=utf-8><style>body{{font:15px system-ui;margin:32px;max-width:1100px}}td,th{{border:1px solid #bbb;padding:7px}}table{{border-collapse:collapse}}</style><h1>Voting social-simulation run</h1><p>Independent private initialization; six seeded pair-dialogue rounds; blind judge after interaction.</p><h2>Vote diversity by round</h2><table><tr><th>round</th><th>counts</th><th>normalized entropy</th><th>max share</th></tr>{rows}</table><h2>Audit</h2><pre>{html.escape(json.dumps(audit,ensure_ascii=False,indent=2))}</pre><h2>Metrics</h2><pre>{html.escape(json.dumps(metrics['group'],ensure_ascii=False,indent=2))}</pre>"
    (out/'report.html').write_text(page)
def main():
    p=argparse.ArgumentParser(); p.add_argument('--config',default='config.voting.json'); p.add_argument('--validate-only',action='store_true'); args=p.parse_args(); cfg=load(args.config)
    base=Path(args.config).resolve().parent; personas=load(base/cfg['personas_file']); candidates=load(base/cfg['candidates_file']); interactions=load(base/cfg['interaction_profiles_file'])
    for item in personas: item['social_interaction']=interactions[item['id']]
    if cfg.get('agent_ids'):
        selected=set(cfg['agent_ids']); personas=[x for x in personas if x['id'] in selected]
    ids=[x['id'] for x in personas]
    expected=cfg.get('population_size',20)
    if len(personas)!=expected or len(set(ids))!=expected or len(candidates)!=6: raise ValueError('invalid population or candidate cardinality')
    schedule=round_robin_pairs(ids,cfg['seed'],cfg['rounds']); errors=validate_schedule(schedule,ids)
    audit={'broadcast_enabled':False,'broadcast_delivery_count':0,'population_size':len(ids),'rounds':cfg['rounds'],'schedule_errors':errors,'candidate_balance':candidate_audit(candidates),'judge_blind_inputs':['persona','candidate_material'],'judge_forbidden_inputs':['agent choices','dialogue','trajectory','group outcome']}
    if errors: raise ValueError(errors)
    if args.validate_only: print(json.dumps({'status':'valid','audit':audit},ensure_ascii=False,indent=2)); return
    task=VotingTask(candidates); persona={x['id']:x for x in personas}; stamp=dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ'); out=base/cfg['output_root']/stamp; out.mkdir(parents=True)
    global CURRENT_OUT, CURRENT_STAGE
    CURRENT_OUT=out; CURRENT_STAGE={"phase":"created"}
    dump(out/'config_frozen.json',cfg); dump(out/'personas.json',personas); dump(out/'candidates.json',candidates); dump(out/'pairings.json',schedule)
    memories={a:[] for a in ids}; raw=[]; initial={}
    rounds=[]; judges={}
    def checkpoint(): dump(out/'checkpoint.json',{"stage":CURRENT_STAGE,"initial":initial,"rounds":rounds,"memories":memories,"raw":raw,"judges":judges})
    for aid in ids:
        CURRENT_STAGE={"phase":"initial","agent_id":aid}
        result=call(cfg,task.initial_messages(persona[aid]),lambda x:task.parse_state(x,True)); initial[aid]=result; memories[aid].append({'kind':'initial','state':result}); raw.append({'phase':'initial','agent_id':aid,'result':result}); print('initial',aid,flush=True)
        checkpoint()
    for rid,pairs in enumerate(schedule,1):
        states={}
        for a,b in pairs:
            CURRENT_STAGE={"phase":"pair_dialogue","round":rid,"pair":[a,b]}
            open_a=call(cfg,task.dialogue_messages(persona[a],persona[b],memories[a],initial[b],rid,'open'),task.parse_dialogue); reply_b=call(cfg,task.dialogue_messages(persona[b],persona[a],memories[b],initial[a],rid,'reply',open_a['message']),task.parse_dialogue); dialogue=[{'speaker':a,**open_a},{'speaker':b,**reply_b}]
            prior_a=memories[a][-1]['state']; prior_b=memories[b][-1]['state']; states[a]=call(cfg,task.reflection_messages(persona[a],memories[a],dialogue,prior_a),task.parse_state); states[b]=call(cfg,task.reflection_messages(persona[b],memories[b],dialogue,prior_b),task.parse_state)
            memories[a].append({'kind':'round','round':rid,'partner':b,'dialogue':dialogue,'state':states[a]}); memories[b].append({'kind':'round','round':rid,'partner':a,'dialogue':dialogue,'state':states[b]}); raw.append({'phase':'dialogue','round':rid,'pair':[a,b],'dialogue':dialogue,'states':{a:states[a],b:states[b]}}); print(f'round {rid}: {a} {b}',flush=True); checkpoint()
        rounds.append(states)
        checkpoint()
    for aid in ids:
        CURRENT_STAGE={"phase":"judge_blind","agent_id":aid}
        judges[aid]=call(cfg,task.judge_messages(persona[aid]),task.parse_judge); raw.append({'phase':'judge_blind','agent_id':aid,'result':judges[aid]})
        checkpoint()
    CURRENT_STAGE={"phase":"export"}
    metrics=compute(initial,rounds,judges,persona,schedule); (out/'trajectory.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in raw)); dump(out/'initial_states.json',initial); dump(out/'memory.json',memories); dump(out/'judge_blind.json',judges); dump(out/'metrics.json',metrics); dump(out/'audit.json',audit); report(out,metrics,audit); (out/'checkpoint.json').unlink(missing_ok=True); print('Completed:',out)
if __name__=='__main__':
    try: main()
    except Exception as exc:
        if CURRENT_OUT:
            dump(CURRENT_OUT/'failure.json',{"stage":CURRENT_STAGE,"error":repr(exc),"traceback":traceback.format_exc()})
        raise
