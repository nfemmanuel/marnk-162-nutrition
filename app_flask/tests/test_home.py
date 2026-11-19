import unittest

from app_flask.nutrition import create_app


class HomePageTest(unittest.TestCase):
    def test_home_page_loads(self):
        app = create_app({"TESTING": True})
        response = app.test_client().get("/")

        self.assertEqual(response.status_code, 200)
        page = response.get_data(as_text=True)
        self.assertIn("Nutrition App", page)
        self.assertIn("Simple tools to help you make mindful nutrition choices.", page)
        self.assertIn('href="/login"', page)
        self.assertIn('href="/register"', page)


if __name__ == "__main__":
    unittest.main()
