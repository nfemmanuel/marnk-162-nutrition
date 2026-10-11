import unittest

from nutrition import create_app


class FactoryTest(unittest.TestCase):
    def test_app_starts_in_testing_mode(self):
        # App is created in testing mode
        app = create_app({"TESTING": True})
        self.assertTrue(app.testing)

        # App starts and answers a request
        client = app.test_client()
        response = client.get("/hello")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()