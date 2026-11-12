"""Tests for the saved recipes pages (NUT-39, NUT-40).

Each test uses an in-memory database and Flask's test client, so it goes
through the real routes. Ana is logged in; Ben is a second user.
Run from the repo root:  python -m unittest discover -s app_flask/tests -t .
"""

import unittest

from flask import render_template
from flask_login import login_user, logout_user

from app_flask.nutrition import create_app
from app_flask.nutrition.db import db
from app_flask.nutrition.models import Recipe, RecipeIngredient, User
from app_flask.nutrition.saved_service import list_saved_recipes, save_recipe
from app_flask.nutrition.user_service import create_user


def add_recipe(name, ingredient):
    """Store a recipe with this name and one ingredient, and return its ID."""
    recipe = Recipe(name=name, source="test", source_id=name, source_url="")
    recipe.ingredients.append(RecipeIngredient(name=ingredient, amount="2"))
    db.session.add(recipe)
    db.session.commit()
    return recipe.id


class SavedPagesTestCase(unittest.TestCase):
    """Shared setup: two users, two recipes, and Ana logged in."""

    def setUp(self):
        """Make a test app with an in-memory database and log Ana in."""
        self.app = create_app(
            {"TESTING": True, "SECRET_KEY": "test", "SQLALCHEMY_DATABASE_URI": "sqlite://"}
        )
        self.context = self.app.app_context()
        self.context.push()
        db.create_all()
        self.ana = create_user("ana@example.com", "secret123").id
        self.ben = create_user("ben@example.com", "secret123").id
        self.omelette = add_recipe("Omelette", "Eggs")
        self.pancakes = add_recipe("Pancakes", "Flour")
        self.client = self.app.test_client()
        self.client.post("/login", data={"email": "ana@example.com", "password": "secret123"})

    def tearDown(self):
        """Throw the test database away."""
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
        self.context.pop()

    def saved_names(self, user_id):
        """Return the names of the recipes a user has saved."""
        return [recipe.name for recipe in list_saved_recipes(user_id)]


class SavedListTest(SavedPagesTestCase):
    """The /saved page and its Remove button."""

    def test_page_lists_my_saved_recipes(self):
        """The page shows what I saved, with each recipe's ingredients."""
        save_recipe(self.ana, self.omelette)

        page = self.client.get("/saved")

        self.assertEqual(page.status_code, 200)
        self.assertIn(b"Omelette", page.data)
        self.assertIn(b"2 Eggs", page.data)
        self.assertNotIn(b"Pancakes", page.data)

    def test_page_does_not_show_another_users_recipes(self):
        """What Ben saved never appears on Ana's page."""
        save_recipe(self.ben, self.pancakes)

        page = self.client.get("/saved")

        self.assertNotIn(b"Pancakes", page.data)

    def test_empty_list_says_so(self):
        """With nothing saved, the page explains that."""
        page = self.client.get("/saved")

        self.assertIn(b"No saved recipes yet.", page.data)

    def test_page_needs_login(self):
        """A logged-out visitor is sent to the login page."""
        self.client.post("/logout")

        response = self.client.get("/saved")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/login?next=%2Fsaved")

    def test_remove(self):
        """Remove takes the recipe off my list and returns to the page."""
        save_recipe(self.ana, self.omelette)

        response = self.client.post(f"/saved/{self.omelette}/remove")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/saved")
        self.assertEqual(self.saved_names(self.ana), [])

    def test_remove_does_not_touch_another_users_list(self):
        """Ana removing a recipe leaves Ben's saved copy alone."""
        save_recipe(self.ben, self.omelette)

        self.client.post(f"/saved/{self.omelette}/remove")

        self.assertEqual(self.saved_names(self.ben), ["Omelette"])

    def test_remove_is_post_only(self):
        """Opening the remove address as a link changes nothing."""
        save_recipe(self.ana, self.omelette)

        response = self.client.get(f"/saved/{self.omelette}/remove")

        self.assertEqual(response.status_code, 405)
        self.assertEqual(self.saved_names(self.ana), ["Omelette"])

    def test_navigation_links_to_the_page_when_logged_in(self):
        """The Saved recipes link shows only for a logged-in user."""
        self.assertIn(b'href="/saved"', self.client.get("/account").data)

        self.client.post("/logout")

        self.assertNotIn(b'href="/saved"', self.client.get("/login").data)


class SaveTest(SavedPagesTestCase):
    """Saving a recipe, and the Save button other pages include."""

    def test_save(self):
        """Posting to a recipe's save address puts it on my list."""
        response = self.client.post(f"/saved/{self.omelette}")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/saved")
        self.assertEqual(self.saved_names(self.ana), ["Omelette"])
        self.assertEqual(self.saved_names(self.ben), [])

    def test_save_returns_to_the_page_i_was_on(self):
        """After saving from another page of the app, I land back on it."""
        response = self.client.post(
            f"/saved/{self.omelette}", headers={"Referer": "http://localhost/account"}
        )

        self.assertEqual(response.headers["Location"], "http://localhost/account")

    def test_save_never_redirects_to_another_website(self):
        """A request that came from another site goes to my saved recipes instead."""
        response = self.client.post(
            f"/saved/{self.omelette}", headers={"Referer": "http://example.com/page"}
        )

        self.assertEqual(response.headers["Location"], "/saved")

    def test_saving_twice_keeps_one(self):
        """Saving the same recipe again doesn't fail or duplicate it."""
        self.client.post(f"/saved/{self.omelette}")

        response = self.client.post(f"/saved/{self.omelette}")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.saved_names(self.ana), ["Omelette"])

    def test_unknown_recipe_is_not_found(self):
        """Saving a recipe ID that doesn't exist gives a 404."""
        response = self.client.post("/saved/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(self.saved_names(self.ana), [])

    def test_save_needs_login(self):
        """A logged-out visitor is sent to the login page and nothing is saved."""
        self.client.post("/logout")

        response = self.client.post(f"/saved/{self.omelette}")

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers["Location"].startswith("/login"))
        self.assertEqual(self.saved_names(self.ana), [])

    def render_button(self, saved_ids, logged_in=True):
        """Render the Save button for Omelette and return its HTML."""
        with self.app.test_request_context():
            # Set the user here: the login from setUp belongs to the test client
            if logged_in:
                login_user(db.session.get(User, self.ana))
            else:
                logout_user()
            recipe = db.session.get(Recipe, self.omelette)
            return render_template("_save_button.html", recipe=recipe, saved_ids=saved_ids)

    def test_button_offers_to_save(self):
        """For a recipe I haven't saved, the button posts to its save address."""
        html = self.render_button(saved_ids=set())

        self.assertIn(f'action="/saved/{self.omelette}"', html)
        self.assertIn("Save</button>", html)

    def test_button_shows_saved(self):
        """For a recipe I already saved, there is no form, only "Saved"."""
        html = self.render_button(saved_ids={self.omelette})

        self.assertNotIn("<form", html)
        self.assertIn("Saved", html)

    def test_button_is_hidden_when_logged_out(self):
        """A logged-out visitor gets no button at all."""
        html = self.render_button(saved_ids=set(), logged_in=False)

        self.assertEqual(html.strip(), "")


if __name__ == "__main__":
    unittest.main()
