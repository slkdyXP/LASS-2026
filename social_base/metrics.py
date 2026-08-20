from __future__ import annotations
import math, statistics
from collections import Counter, defaultdict

CHOICES=list("ABCDEF")
def entropy(counts:dict[str,int], n:int)->float:
    return -sum((v/n)*math.log(v/n) for v in counts.values() if v)
def vote_metrics(states:dict[str,dict])->dict:
    n=len(states); c=Counter(s["choice"] for s in states.values()); h=entropy(c,n); p=[v/n for v in c.values()]
    return {"counts":{x:c.get(x,0) for x in CHOICES},"shares":{x:c.get(x,0)/n for x in CHOICES},"candidates_with_votes":len(c),"max_share":max(p),"shannon_entropy":h,"normalized_shannon_entropy":h/math.log(6),"effective_choices":math.exp(h),"simpson_blau":1-sum(x*x for x in p),"hhi":sum(x*x for x in p)}
def js_tv(a:dict,b:dict)->dict:
    pa=[a[x] for x in CHOICES]; pb=[b[x] for x in CHOICES]; m=[(x+y)/2 for x,y in zip(pa,pb)]
    kl=lambda p,q:sum(x*math.log(x/y) for x,y in zip(p,q) if x)
    return {"js_divergence":(kl(pa,m)+kl(pb,m))/2,"total_variation":sum(abs(x-y) for x,y in zip(pa,pb))/2}
def rank_change(a:list[str],b:list[str])->float:
    return sum(abs(a.index(x)-b.index(x)) for x in CHOICES)/30
def categorical_assortativity(edges:list[tuple[str,str]], labels:dict[str,str])->float|None:
    if not edges:return None
    same=sum(labels[a]==labels[b] for a,b in edges)/len(edges)
    freq=Counter(labels.values()); expected=sum((v/len(labels))**2 for v in freq.values())
    return None if expected==1 else (same-expected)/(1-expected)
def compute(initial:dict, rounds:list[dict], judges:dict, personas:dict, pairs:list[list[tuple[str,str]]])->dict:
    series=[{"round":0,**vote_metrics(initial)}]; previous=initial
    changes=defaultdict(int); switched_to_partner=defaultdict(int); persuaded=defaultdict(int); transition=Counter(); reasons=Counter(); confidence_delta={}; rank_delta={}; edges=[]
    for r, states in enumerate(rounds,1):
        series.append({"round":r,**vote_metrics(states)})
        partner={a:b for a,b in pairs[r-1]}|{b:a for a,b in pairs[r-1]}; edges+=pairs[r-1]
        for aid,s in states.items():
            old=previous[aid]; rank_delta[aid]=rank_delta.get(aid,0)+rank_change(old["ranking"],s["ranking"]); confidence_delta[aid]=s["confidence"]-initial[aid]["confidence"]
            if s["choice"]!=old["choice"]:
                changes[aid]+=1; transition[(old["choice"],s["choice"])]+=1; reasons[s.get("evidence_type","no_clear_reason")]+=1
                if s["choice"]==previous[partner[aid]]["choice"]: switched_to_partner[aid]+=1; persuaded[partner[aid]]+=1
        previous=states
    final=rounds[-1]; init_shares=series[0]["shares"]; final_shares=series[-1]["shares"]
    agent={}
    for aid, state in final.items():
        j=judges[aid]; chosen=state["choice"]; rank=j["ranking"]; scores=j["scores"]
        agent[aid]={"initial_choice":initial[aid]["choice"],"final_choice":chosen,"choice_changes":changes[aid],"retained_initial":chosen==initial[aid]["choice"],"returned_to_initial":any(r[aid]["choice"]!=initial[aid]["choice"] for r in rounds[:-1]) and chosen==initial[aid]["choice"],"ranking_change":rank_delta.get(aid,0),"confidence_change":confidence_delta.get(aid,0),"judge_rank":rank.index(chosen)+1,"judge_score":scores[chosen],"judge_gap":max(scores.values())-scores[chosen],"judge_confidence":j["confidence"],"switched_to_partner":switched_to_partner[aid],"influenced_others":persuaded[aid],"net_influence":persuaded[aid]-switched_to_partner[aid]}
    def mean(xs): return statistics.mean(xs) if xs else 0
    def sd(xs): return statistics.stdev(xs) if len(xs)>1 else 0
    ranks_i=[judges[a]["ranking"].index(initial[a]["choice"])+1 for a in initial]; ranks_f=[x["judge_rank"] for x in agent.values()]
    degree=Counter(x for edge in edges for x in edge)
    group={"initial_final_distance":js_tv(init_shares,final_shares),"change_reasons":dict(reasons),"transition_matrix":{f"{a}->{b}":v for (a,b),v in transition.items()},"pairing":{"unique_edges":len(set(tuple(sorted(e)) for e in edges)),"repeated_pairs":len(edges)-len(set(tuple(sorted(e)) for e in edges)),"degree":{"per_agent":dict(degree),"distribution":dict(Counter(degree.values()))},"choice_assortativity_initial":categorical_assortativity(edges,{a:initial[a]["choice"] for a in initial}),"choice_assortativity_final":categorical_assortativity(edges,{a:final[a]["choice"] for a in final})},"judge":{"initial_top1":mean([x==1 for x in ranks_i]),"final_top1":mean([x==1 for x in ranks_f]),"initial_top2":mean([x<=2 for x in ranks_i]),"final_top2":mean([x<=2 for x in ranks_f]),"initial_top3":mean([x<=3 for x in ranks_i]),"final_top3":mean([x<=3 for x in ranks_f]),"final_low_compatibility_rate":mean([x["judge_rank"]>=5 for x in agent.values()])},"stability":{"changes_mean":mean(list(changes.values()) or [0]),"changes_sd":sd(list(changes.values()) or [0]),"immediate_partner_adoption_rate":sum(switched_to_partner.values())/max(1,sum(changes.values())),"no_clear_reason_change_rate":reasons["no_clear_reason"]/max(1,sum(changes.values()))}}
    return {"by_round":series,"per_agent":agent,"group":group}
