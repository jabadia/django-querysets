import json

from django.test import TestCase
from django.conf import settings
import logging


class TestViews(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        print('database configuration')
        print('-' * 90)
        for key, value in settings.DATABASES['default'].items():
            print(f'{key:20}: {value}')
        print('-' * 90)

    def setUp(self) -> None:
        super().setUp()
        # need to run tests with --debug-mode for this setting to be effective
        # logging.getLogger('django.db').setLevel(logging.DEBUG)
        self.assertEqual(settings.SETTINGS_FILE, 'test_settings.py')

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
        # self.assertIn("REGEXP ^D.e$", data['regex_qs']['query'])  # sqlite3
        self.assertEqual(2, len(data['regex_qs']['data']))

    def test__comparison(self):
        with self.assertNumQueries(4):
            response = self.client.get('/queries/comparison')
        self.assertEqual(200, response.status_code)
        data = response.json()

        self.assertIn(" > ", data['gt_qs']['query'])
        self.assertEqual(0, len(data['gt_qs']['data']))
        self.assertIn(" < ", data['lt_qs']['query'])
        self.assertEqual(1, len(data['lt_qs']['data']))
        self.assertIn(" >= ", data['gte_qs']['query'])
        self.assertEqual(1, len(data['gte_qs']['data']))
        self.assertIn(" <= ", data['lte_qs']['query'])
        self.assertEqual(2, len(data['lte_qs']['data']))

    def test__between(self):
        with self.assertNumQueries(1):
            response = self.client.get('/queries/between')
        self.assertEqual(200, response.status_code)
        data = response.json()

        self.assertIn(' BETWEEN ', data['between_qs']['query'])
        self.assertEqual(2, len(data['between_qs']['data']))

    def test__limit(self):
        with self.assertNumQueries(2):
            response = self.client.get('/queries/limit')
        self.assertEqual(200, response.status_code)
        data = response.json()

        self.assertIn('LIMIT 10', data['limit_qs']['query'])
        self.assertIn('LIMIT 10 OFFSET 10', data['offset_limit_qs']['query'])

    def test__orderby(self):
        with self.assertNumQueries(4):
            response = self.client.get('/queries/orderby')
        self.assertEqual(200, response.status_code)
        data = response.json()

        self.assertIn('ORDER BY "auth_user"."date_joined" ASC', data['by_date_joined_qs']['query'])
        self.assertIn(
            'ORDER BY "auth_user"."date_joined" ASC, "auth_user"."last_name" DESC',
            data['by_multiple_qs']['query']
        )
        self.assertIn('ORDER BY "auth_user"."date_joined" DESC', data['by_reverse_date_joined_qs']['query'])
        self.assertIn('ORDER BY RANDOM() ASC', data['by_random_qs']['query'])

    def test__get_single(self):
        with self.assertNumQueries(6):
            response = self.client.get('/queries/get_single')
        self.assertEqual(200, response.status_code)
        data = response.json()

        self.assertIn('LIMIT 1', data['user_using_limit']['query'])
        self.assertIn('WHERE "auth_user"."id" = 1', data['user_using_get']['query'])
        self.assertIn('ORDER BY "auth_user"."date_joined" ASC, "auth_user"."first_name" DESC LIMIT 1', data['user_using_first']['query'])
        self.assertIn('ORDER BY "auth_user"."first_name" DESC LIMIT 1', data['user_using_last']['query'])
        self.assertIn('ORDER BY "auth_user"."date_joined" ASC, "auth_user"."first_name" DESC LIMIT 1', data['user_using_earliest']['query'])
        self.assertIn('ORDER BY "auth_user"."first_name" DESC LIMIT 1', data['user_using_latest']['query'])

    def test__joins(self):
        with self.assertNumQueries(2):
            response = self.client.get('/queries/joins')
        self.assertEqual(200, response.status_code)
        data = response.json()

        self.assertEqual(4, len(data['users_with_group_name_qs']['data']))
        self.assertIn('JOIN "auth_user_groups"', data['users_with_group_name_qs']['query'])
        self.assertIn('JOIN "auth_group"', data['users_with_group_name_qs']['query'])

        self.assertEqual(5, len(data['groups_with_users_qs']['data']))
        self.assertIn('JOIN "auth_user_groups"', data['groups_with_users_qs']['query'])
        self.assertIn('JOIN "auth_user"', data['groups_with_users_qs']['query'])

    def test__annotations(self):
        with self.assertNumQueries(3):
            response = self.client.get('/queries/annotations')
        self.assertEqual(200, response.status_code)
        data = response.json()

        self.assertEqual(4, len(data['groups_with_user_count_qs']['data']))
        self.assertIn('COUNT("auth_user"."username")', data['groups_with_user_count_qs']['query'])
        self.assertIn('GROUP BY "auth_group"."id"', data['groups_with_user_count_qs']['query'])

        self.assertEqual(2, len(data['users_with_group_count_qs']['data']))
        self.assertIn('COUNT("auth_user_groups"."group_id")', data['users_with_group_count_qs']['query'])
        self.assertIn('GROUP BY "auth_user"."id"', data['users_with_group_count_qs']['query'])

        self.assertEqual(2, len(data['users_with_group_array_qs']['data']))
        self.assertIn('ARRAY_AGG("auth_group"."name" )', data['users_with_group_array_qs']['query'])
        self.assertIn('GROUP BY "auth_user"."id"', data['users_with_group_array_qs']['query'])
