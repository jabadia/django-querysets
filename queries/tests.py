import json

from django.test import TestCase
import logging


class TestViews(TestCase):

    def setUp(self) -> None:
        super().setUp()
        # need to run tests with --debug-mode for this setting to be effective
        logging.getLogger('django.db').setLevel(logging.DEBUG)

    def tearDown(self) -> None:
        super().tearDown()
        logging.getLogger('django.db').setLevel(logging.INFO)

    def _assert_all_results_and_sqls_equal(self, data):
        # check that the result and SQL query is the same in all querysets
        query_results = set([json.dumps(qs['data']) for qs in data.values()])
        sqls = set([qs['query'] for qs in data.values()])
        self.assertEqual(1, len(query_results))
        self.assertEqual(1, len(sqls))

    def test__first(self):
        with self.assertNumQueries(1):
            response = self.client.get('/queries/first')
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual(2, len(data['users']))

    def test__and_operation(self):
        with self.assertNumQueries(4):
            response = self.client.get('/queries/and_operation')
        self.assertEqual(200, response.status_code)
        data = response.json()

        self._assert_all_results_and_sqls_equal(data)

    def test__or_operation(self):
        with self.assertNumQueries(2):
            response = self.client.get('/queries/or_operation')
        self.assertEqual(200, response.status_code)
        data = response.json()

        self._assert_all_results_and_sqls_equal(data)

    def test__not_equal(self):
        with self.assertNumQueries(2):
            response = self.client.get('/queries/not_equal')
        self.assertEqual(200, response.status_code)
        data = response.json()

        self._assert_all_results_and_sqls_equal(data)

    def test__in_filtering(self):
        with self.assertNumQueries(2):
            response = self.client.get('/queries/in_filtering')
        self.assertEqual(200, response.status_code)
        data = response.json()

        self.assertEqual(1, len(data['qs']['data']))
        self.assertEqual(1, len(data['bulk']['data']))

        self.assertCountEqual(data['qs']['data'], data['bulk']['data'].values())
        self.assertEqual(data['qs']['query'], data['bulk']['query'])

    def test__is_null(self):
        with self.assertNumQueries(2):
            response = self.client.get('/queries/is_null')
        self.assertEqual(200, response.status_code)
        data = response.json()

        self.assertEqual(0, len(data['is_null_qs']['data']))
        self.assertEqual(2, len(data['is_not_null_qs']['data']))

        self.assertIn('IS NULL', data['is_null_qs']['query'])
        self.assertIn('IS NOT NULL', data['is_not_null_qs']['query'])

    def test__like(self):
        with self.assertNumQueries(4):
            response = self.client.get('/queries/like')
        self.assertEqual(200, response.status_code)
        data = response.json()

        self.assertIn("LIKE Jo%", data['startswith_qs']['query'])
        self.assertEqual(1, len(data['startswith_qs']['data']))
        self.assertIn("LIKE %ya", data['endswith_qs']['query'])
        self.assertEqual(0, len(data['endswith_qs']['data']))
        self.assertIn("LIKE %oh%", data['contains_qs']['query'])
        self.assertEqual(1, len(data['contains_qs']['data']))
        self.assertIn("REGEXP ^D.e$", data['regex_qs']['query'])
        self.assertEqual(2, len(data['regex_qs']['data']))
