import unittest

from app_flask.nutrition import create_app


class FactoryTest(unittest.TestCase):
    def test_app_starts_in_testing_mode(self):
        # App is created in testing mode
        app = create_app({"TESTING": True})
        self.assertTrue(app.testing)

        # App starts and answers a request
        client = app.test_client()
        response = client.get("/hello")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(as_text=True), "Hello, Nutrition App!")


if __name__ == "__main__":
    unittest.main()