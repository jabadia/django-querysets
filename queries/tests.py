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

        # check that the result and SQL query is the same in all querysets
        query_results = set([json.dumps(qs['data']) for qs in data.values()])
        sqls = set([qs['query'] for qs in data.values()])

        self.assertEqual(1, len(query_results))
        self.assertEqual(1, len(sqls))
