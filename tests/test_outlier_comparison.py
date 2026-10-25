import unittest
from app import app
from analytics import TEAMS, METRICS

class OutlierComparisonTest(unittest.TestCase):
    def setUp(self):
        self.client=app.test_client()

    def test_all_team_metric_combinations(self):
        for team in TEAMS:
            for metric in METRICS:
                with self.subTest(team=team,metric=metric):
                    response=self.client.get('/api/outlier-comparison',query_string={'team':team,'metric':metric})
                    self.assertEqual(response.status_code,200)
                    data=response.get_json()
                    self.assertEqual(data['quantidade_unica'],len(data['jogos']))
                    self.assertEqual(len(data['metodos']),7)
                    self.assertTrue(all(1<=r['consenso']<=7 for r in data['jogos']))

    def test_invalid_filter(self):
        self.assertEqual(self.client.get('/api/outlier-comparison?metric=INVALID').status_code,400)

if __name__=='__main__':
    unittest.main()
