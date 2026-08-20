"""Aggregate completed full runs from different seeds; never treats a smoke run as evidence."""
from __future__ import annotations
import argparse, json, math, statistics
from pathlib import Path

KEYS=[('group','judge','initial_top1'),('group','judge','final_top1'),('group','judge','initial_top3'),('group','judge','final_top3'),('group','stability','changes_mean')]
def get(d,path):
    for k in path: d=d[k]
    return d
def main():
    p=argparse.ArgumentParser(); p.add_argument('runs',nargs='+'); p.add_argument('--output',default='aggregate.json'); a=p.parse_args()
    records=[]
    for run in map(Path,a.runs):
        cfg=json.loads((run/'config_frozen.json').read_text()); metrics=json.loads((run/'metrics.json').read_text())
        if cfg.get('population_size',20)==20 and cfg.get('rounds')==6: records.append({'run':str(run),'seed':cfg['seed'],'metrics':metrics})
    if not records: raise ValueError('no completed 20-agent, 6-round runs supplied')
    summary={'n_runs':len(records),'runs':[{'path':x['run'],'seed':x['seed']} for x in records],'metrics':{}}
    for key in KEYS:
        values=[float(get(x['metrics'],key)) for x in records]; mean=statistics.mean(values); se=statistics.stdev(values)/math.sqrt(len(values)) if len(values)>1 else None
        summary['metrics']['.'.join(key)]={'mean':mean,'sd':statistics.stdev(values) if len(values)>1 else 0.0,'approx_95_ci':None if se is None else [mean-1.96*se,mean+1.96*se]}
    Path(a.output).write_text(json.dumps(summary,ensure_ascii=False,indent=2)); print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
