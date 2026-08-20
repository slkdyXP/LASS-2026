from __future__ import annotations
import json

CHOICES = list("ABCDEF")

def _json(text: str) -> dict:
    a,b=text.find("{"),text.rfind("}")
    if a<0 or b<a: raise ValueError("no JSON object in model response")
    return json.loads(text[a:b+1])

class VotingTask:
    task_id="fictional_presidential_vote"
    def __init__(self, candidates: list[dict]): self.candidates=candidates
    @property
    def candidate_text(self): return json.dumps(self.candidates, ensure_ascii=False, indent=2)
    def initial_messages(self, persona: dict) -> list[dict[str,str]]:
        return [{"role":"system","content":"You are an autonomous participant in a fictional social simulation. No human user is present. Make a private, good-faith choice from your own persona. Do not try to optimize group diversity or stability. Return JSON only."},{"role":"user","content":f"YOUR PERSONA (private):\n{json.dumps(persona,ensure_ascii=False)}\n\nFICTIONAL CANDIDATES (same for all participants):\n{self.candidate_text}\n\nPrivately vote. Return exactly {{\"environment_summary\":string,\"ranking\":[six candidate IDs best-to-worst],\"choice\":one ID,\"reason\":string,\"confidence\":number 0-100,\"factors\":[strings],\"concerns\":[strings]}}."}]
    def dialogue_messages(self, self_persona: dict, other_persona: dict, own_memory: list[dict], other_initial: dict, round_id: int, turn: str, prior: str="") -> list[dict[str,str]]:
        history=json.dumps(own_memory[-8:],ensure_ascii=False)
        partner=json.dumps({"id":other_persona["id"],"name":other_persona["name"],"communication":other_persona["communication"]},ensure_ascii=False)
        instruction="Begin a brief two-person discussion naturally. Let your persona determine whether you state a preference, offer advice, ask a question, challenge a claim, or first listen." if turn=="open" else "Respond naturally to your partner. Let your persona determine whether to advise, question, challenge, acknowledge, or simply clarify your view."
        return [{"role":"system","content":"You are an autonomous participant in a fictional social simulation. No human user is present. Discuss candidates naturally from your persona. Do not state that you are following a prompt. Return JSON only."},{"role":"user","content":f"YOUR PRIVATE PERSONA:\n{json.dumps(self_persona,ensure_ascii=False)}\n\nCANDIDATES:\n{self.candidate_text}\n\nYOUR PRIVATE MEMORY:\n{history}\n\nPARTNER'S COMMUNICATION STYLE ONLY:\n{partner}\n\nROUND {round_id}. {instruction}\n{('PARTNER MESSAGE:\n'+prior) if prior else ''}\nReturn {{\"message\":string,\"question\":string}}."}]
    def reflection_messages(self, persona:dict, own_memory:list[dict], dialogue:list[dict], prior_state:dict) -> list[dict[str,str]]:
        return [{"role":"system","content":"You are an autonomous participant privately updating your own record after a conversation. No human user is present. Return JSON only. Do not optimize for diversity, stability, or any evaluator."},{"role":"user","content":f"YOUR PRIVATE PERSONA:\n{json.dumps(persona,ensure_ascii=False)}\n\nCANDIDATES:\n{self.candidate_text}\n\nYOUR PRIOR PRIVATE STATE:\n{json.dumps(prior_state,ensure_ascii=False)}\n\nYOUR MEMORY:\n{json.dumps(own_memory[-8:],ensure_ascii=False)}\n\nJUST-FINISHED DIALOGUE:\n{json.dumps(dialogue,ensure_ascii=False)}\n\nReturn {{\"ranking\":[six IDs],\"choice\":one ID,\"changed\":boolean,\"change_reason\":string,\"evidence_or_argument\":string,\"evidence_type\":one of [\"new_information\",\"reasoned_argument\",\"repetition_or_pressure\",\"no_clear_reason\",\"none\"],\"confidence\":number 0-100,\"memory_note\":string}}."}]
    def judge_messages(self, persona:dict) -> list[dict[str,str]]:
        return [{"role":"system","content":"You are an independent blind evaluator. Return JSON only. You must assess compatibility, not prescribe a correct vote."},{"role":"user","content":f"PERSONA:\n{json.dumps(persona,ensure_ascii=False)}\n\nCANDIDATES:\n{self.candidate_text}\n\nThe participant's actual choices, conversations, trajectory, and group outcome are deliberately unavailable. For every A-F, assign compatibility 0-100 using only this persona and candidate material. Return {{\"scores\":{{\"A\":number,\"B\":number,\"C\":number,\"D\":number,\"E\":number,\"F\":number}},\"ranking\":[six IDs],\"most_likely\":one ID,\"other_reasonable\":[IDs],\"rationale\":string,\"confidence\":number 0-100,\"persona_tensions\":[strings]}}."}]
    def parse_state(self, raw:str, initial:bool=False) -> dict:
        d=_json(raw); ranking=d.get("ranking",[]); choice=d.get("choice")
        if sorted(ranking)!=CHOICES or choice not in CHOICES or not isinstance(d.get("confidence"),(int,float)): raise ValueError("invalid vote state schema")
        d["confidence"]=max(0,min(100,float(d["confidence"])))
        if initial:
            for key in ("environment_summary","reason","factors","concerns"):
                if key not in d: raise ValueError(f"missing initial field {key}")
        else:
            for key in ("changed","change_reason","evidence_or_argument","evidence_type","memory_note"):
                if key not in d: raise ValueError(f"missing reflection field {key}")
        return d
    def parse_dialogue(self,raw:str)->dict:
        d=_json(raw)
        if not isinstance(d.get("message"),str) or not d["message"].strip(): raise ValueError("invalid dialogue")
        return {"message":d["message"][:1500],"question":str(d.get("question", ""))[:500]}
    def parse_judge(self,raw:str)->dict:
        d=_json(raw); scores=d.get("scores",{}); rank=d.get("ranking",[])
        if set(scores)!=set(CHOICES) or sorted(rank)!=CHOICES or d.get("most_likely") not in CHOICES: raise ValueError("invalid judge schema")
        d["scores"]={k:max(0,min(100,float(v))) for k,v in scores.items()}; d["confidence"]=max(0,min(100,float(d.get("confidence",0))))
        return d
