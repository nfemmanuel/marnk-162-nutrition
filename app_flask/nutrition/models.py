"""Database tables for the app, written as SQLAlchemy models.

Passwords are never stored: set_password() saves a salted werkzeug hash, and
check_password() compares a password against it.
"""

from datetime import datetime, timezone

from werkzeug.security import check_password_hash, generate_password_hash

from .db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    source = db.Column(db.String(40), nullable=False)
    source_id = db.Column(db.String(40), nullable=False)
    source_url = db.Column(db.String(255), nullable=False)
    __table_args__ = (db.UniqueConstraint("source", "source_id"),)
    ingredients = db.relationship(
        "RecipeIngredient", backref="recipe", cascade="all, delete-orphan"
    )


class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredients"

    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.String(100), nullable=False)


class Food(db.Model):
    """A food from USDA FoodData Central, with its calories and macros per 100 g.

    fdc_id is USDA's own ID, so every row can be checked on fdc.nal.usda.gov.
    """

    __tablename__ = "foods"

    fdc_id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)


class Ingredient(db.Model):
    """An ingredient name used in recipes (lowercase) and the USDA food it means.

    Several names can share one food ("onion", "onions"), so the numbers are
    stored once, in foods. Spices have no food: they add almost nothing, so
    recipe totals skip them.
    """

    __tablename__ = "ingredients"

    name = db.Column(db.String(120), primary_key=True)
    fdc_id = db.Column(db.Integer, db.ForeignKey("foods.fdc_id"))
