import unittest
from app import app

class TestEndpoints(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_paginas_e_dados(self):
        for url in ('/', '/api/overview', '/api/summary'):
            self.assertEqual(self.client.get(url).status_code, 200)

    def test_analise_e_kde(self):
        response = self.client.get('/api/analysis?team=Denver%20Nuggets&metric=PTS')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('kde', data)
        self.assertEqual(data['results']['Denver Nuggets']['n'], 76)

    def test_filtro_invalido(self):
        self.assertEqual(self.client.get('/api/analysis?metric=INVALID').status_code, 400)

if __name__ == '__main__':
    unittest.main()
