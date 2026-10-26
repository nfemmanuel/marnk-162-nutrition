"""HTTP routes for registration, login, logout, and account access.

The routes translate form submissions into calls to ``user_service``. Database
queries stay in that service so this module remains focused on HTTP behavior.
"""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from .user_service import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    is_valid_email,
    normalize_email,
)


auth_blueprint = Blueprint("auth", __name__)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    """Restore ``current_user`` from the ID stored in the login session."""
    return get_user_by_id(user_id)


@auth_blueprint.route("/register", methods=["GET", "POST"])
def register():
    """Display the registration form and create a valid, unique user on POST."""
    if current_user.is_authenticated:
        return redirect(url_for("auth.account"))

    if request.method == "POST":
        normalized_email = normalize_email(request.form.get("email", ""))
        submitted_password = request.form.get("password", "")

        if not normalized_email or not submitted_password:
            flash("Email and password are required.")
        elif len(submitted_password) < 8:
            flash("Password must be at least 8 characters.")
        elif not is_valid_email(normalized_email):
            flash("Enter a valid email address.")
        elif get_user_by_email(normalized_email) is not None:
            flash("An account with that email already exists.")
        else:
            create_user(normalized_email, submitted_password)
            flash("Account created. Please log in.")
            return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    """Display the login form and start a session for valid credentials."""
    if current_user.is_authenticated:
        return redirect(url_for("auth.account"))

    if request.method == "POST":
        submitted_email = request.form.get("email", "")
        submitted_password = request.form.get("password", "")
        authenticated_user = get_user_by_email(submitted_email)

        if authenticated_user is None or not authenticated_user.check_password(
            submitted_password
        ):
            flash("Incorrect email or password.")
        else:
            login_user(authenticated_user)
            return redirect(url_for("auth.account"))

    return render_template("login.html")


@auth_blueprint.route("/logout", methods=["POST"])
@login_required
def logout():
    """End the current login session and return the user to the login page."""
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("auth.login"))


@auth_blueprint.route("/account")
@login_required
def account():
    """Show a minimal protected page proving that authentication is required."""
    return render_template("account.html")
