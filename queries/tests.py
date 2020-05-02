from django.test import TestCase


class TestViews(TestCase):
    def test__first(self):
        response = self.client.get('/queries/first')
        self.assertEqual(200, response.status_code)
