import unittest
from pathlib import Path
from analytics import load_data, METRICS, TEAMS
from statistical_synthesis import synthesize

class StatisticalSynthesisTest(unittest.TestCase):
    def test_all_metrics_and_teams(self):
        _, df = load_data(Path(__file__).resolve().parents[1] / 'data' / 'stats_times_regular_final.csv')
        result = synthesize(df)
        self.assertEqual(set(r['variavel'] for r in result['linhas']), set(METRICS))
        for row in result['linhas']:
            self.assertEqual(set(row['equipes']), set(TEAMS))
            for team in TEAMS:
                self.assertGreaterEqual(row['equipes'][team]['iqr'], 0)
                self.assertGreater(row['equipes'][team]['cv'], 0)
