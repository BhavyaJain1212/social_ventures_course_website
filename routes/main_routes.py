"""
Main Routes — Page-serving routes for the Artisan Dashboard.

Handles:
    GET /           → Landing page
    GET /dashboard  → Artisan dashboard
    GET /shop       → Shop / preorder page
    GET /saved-concepts → Saved design concepts gallery
"""

from flask import Blueprint, render_template
from models.concept_model import get_all_concepts
from services.trend_service import get_available_crafts

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    """Render the landing / homepage."""
    return render_template("index.html")


@main_bp.route("/dashboard")
def dashboard():
    """
    Render the artisan dashboard with craft options and recent concepts.
    """
    crafts = get_available_crafts()
    recent_concepts = get_all_concepts()[:4]  # Show latest 4 on dashboard

    # Default artisan profile (in a full app, this would come from auth/session)
    artisan_profile = {
        "name": "Ramesh Kumar",
        "craft_type": "Banarasi Weaving",
        "region": "Varanasi, Uttar Pradesh",
        "materials": "Silk, Zari (gold/silver thread), Cotton blends",
        "experience": "Third-generation weaver, 22 years of experience",
    }

    return render_template(
        "dashboard.html",
        crafts=crafts,
        recent_concepts=recent_concepts,
        artisan=artisan_profile,
    )


@main_bp.route("/shop")
def shop():
    """Render the artisan product shop / preorder page."""
    return render_template("shop.html")


@main_bp.route("/saved-concepts")
def saved_concepts():
    """Render the full saved concepts gallery page."""
    concepts = get_all_concepts()
    return render_template("saved_concepts.html", concepts=concepts)
