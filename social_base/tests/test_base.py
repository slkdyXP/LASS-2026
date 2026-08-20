import json, unittest
from pathlib import Path
from social_base.pairing import round_robin_pairs, validate_schedule
from social_base.tasks.voting import VotingTask

ROOT=Path(__file__).resolve().parents[2]
class BaseTests(unittest.TestCase):
    def setUp(self):
        self.personas=json.loads((ROOT/'social_base/data/personas.json').read_text())
        self.interactions=json.loads((ROOT/'social_base/data/interaction_profiles.json').read_text())
        self.candidates=json.loads((ROOT/'social_base/data/candidates.json').read_text())
    def test_persona_and_candidate_cardinality(self):
        self.assertEqual(len(self.personas),20); self.assertEqual(len({x['id'] for x in self.personas}),20)
        self.assertEqual(set(self.interactions),{x['id'] for x in self.personas})
        self.assertGreaterEqual(len({x['style'] for x in self.interactions.values()}),12)
        self.assertEqual(len(self.candidates),6); self.assertEqual({x['id'] for x in self.candidates},set('ABCDEF'))
    def test_six_rounds_are_perfect_nonrepeating_matchings(self):
        ids=[x['id'] for x in self.personas]; schedule=round_robin_pairs(ids,20260820,6)
        self.assertEqual(validate_schedule(schedule,ids),[])
        self.assertTrue(all(len(round_pairs)==10 for round_pairs in schedule))
        self.assertEqual(schedule,round_robin_pairs(ids,20260820,6))
    def test_judge_prompt_is_blind(self):
        prompt=VotingTask(self.candidates).judge_messages(self.personas[0])[-1]['content'].lower()
        self.assertNotIn('initial_choice',prompt); self.assertNotIn('final_choice',prompt); self.assertNotIn('dialogue',prompt)
        self.assertIn('deliberately unavailable',prompt)
    def test_no_broadcast_field_or_prompt(self):
        for p in self.personas: self.assertNotIn('persona_broadcast',p)
        self.assertNotIn('persistent persona signal',Path(ROOT/'social_base/tasks/voting.py').read_text().lower())
if __name__=='__main__': unittest.main()
