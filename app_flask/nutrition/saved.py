"""HTTP routes for a user's saved recipes (NUT-39).

The routes only handle the request and the response. Database work stays in
``saved_service``, and every call passes the logged-in user's ID, so a user
can only see and change their own list.
"""

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from .saved_service import list_saved_recipes, remove_saved_recipe


saved_blueprint = Blueprint("saved", __name__)


@saved_blueprint.route("/saved")
@login_required
def saved_list():
    """Show the logged-in user's saved recipes, newest first."""
    recipes = list_saved_recipes(current_user.id)
    return render_template("saved.html", recipes=recipes)


@saved_blueprint.route("/saved/<int:recipe_id>/remove", methods=["POST"])
@login_required
def remove(recipe_id):
    """Remove a recipe from the logged-in user's list and show the list again."""
    if remove_saved_recipe(current_user.id, recipe_id):
        flash("Removed from your saved recipes.")
    return redirect(url_for("saved.saved_list"))
