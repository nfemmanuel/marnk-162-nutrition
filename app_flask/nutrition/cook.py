"""The "what can I cook" page (NUT-29).

The user types the ingredients they have and sees the recipes they can make,
using match_recipes() from matching.py. The form is a POST, so the ingredients
are not saved in the page address.
"""

import re

from flask import Blueprint, render_template, request
from flask_login import current_user

from .matching import match_recipes
from .saved_service import saved_recipe_ids


cook_bp = Blueprint("cook", __name__)


@cook_bp.route("/cook", methods=["GET", "POST"])
def cook():
    """Show the form, and on a POST the recipes that fit the ingredients."""
    results = None
    empty = False
    text = ""
    if request.method == "POST":
        text = request.form.get("ingredients", "")
        have = [name.strip() for name in re.split(r"[,\n]", text) if name.strip()]
        if have:
            results = match_recipes(have)
        else:
            empty = True

    saved_ids = saved_recipe_ids(current_user.id) if current_user.is_authenticated else set()
    return render_template("cook.html", text=text, results=results, empty=empty, saved_ids=saved_ids)
