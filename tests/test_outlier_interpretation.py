import unittest
from app import app

class TestOutlierInterpretation(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_all_filters(self):
        for team in ('Los Angeles Lakers', 'Denver Nuggets'):
            for metric in ('PTS','REB','AST','STL','BLK','PF','FG3M'):
                with self.subTest(team=team,metric=metric):
                    response=self.client.get('/api/outlier-interpretation',query_string={'team':team,'metric':metric})
                    self.assertEqual(response.status_code,200)
                    body=response.get_json()
                    self.assertGreater(body['n'],0)
                    self.assertEqual(len(body['contagens']),7)
                    self.assertGreaterEqual(body['total_unicos'],body['tres_ou_mais'])

    def test_invalid_filter(self):
        self.assertEqual(self.client.get('/api/outlier-interpretation?metric=INVALID').status_code,400)

if __name__ == '__main__': unittest.main()
