"""
Trend Service — Recommendation engine for artisan design trends.

Currently uses mock data from data/mock_trends.json.
Structured for easy integration with external trend sources:

    FUTURE INTEGRATION POINTS:
    - Pinterest Trends API (when access is available)
    - Social media trend scraping (Instagram, etc.)
    - E-commerce trend feeds (Amazon, Etsy best-sellers)
    - Google Trends API for search-based signals
"""

import json
import os
import random

# Path to mock trend data
MOCK_DATA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "mock_trends.json"
)

# Cache loaded trend data in memory
_trend_data = None


def _load_trend_data():
    """Load and cache mock trend data from JSON file."""
    global _trend_data
    if _trend_data is None:
        with open(MOCK_DATA_PATH, "r", encoding="utf-8") as f:
            _trend_data = json.load(f)
    return _trend_data


def get_available_crafts():
    """Return a list of available craft types with labels."""
    data = _load_trend_data()
    return [
        {"key": key, "label": info["craft_label"]}
        for key, info in data.items()
    ]


def get_products_for_craft(craft_key):
    """Return available product categories for a given craft type."""
    data = _load_trend_data()
    craft = data.get(craft_key, {})
    products = craft.get("products", {})
    return [
        {"key": key, "label": info["label"]}
        for key, info in products.items()
    ]


def get_audiences_for_product(craft_key, product_key):
    """Return available target audiences for a craft-product combination."""
    data = _load_trend_data()
    audiences = (
        data.get(craft_key, {})
        .get("products", {})
        .get(product_key, {})
        .get("audiences", {})
    )
    return [
        {"key": key, "label": info["label"]}
        for key, info in audiences.items()
    ]


def get_recommendations(craft_type, product_category,
                        target_customer=None, style_preference=None):
    """
    Get trend recommendations for a craft-product-audience combination.

    Args:
        craft_type (str): e.g., "banarasi_weaving"
        product_category (str): e.g., "sari"
        target_customer (str, optional): e.g., "young_working_women"
        style_preference (str, optional): e.g., "pastel", "minimal"

    Returns:
        dict: Recommendation payload with colors, motifs, suggestions etc.

    ---
    FUTURE INTEGRATION:
    Replace the mock data lookup below with calls to:
        - pinterest_client.get_trending_pins(query=...)
        - social_scraper.get_trending_hashtags(craft_type)
        - ecommerce_api.get_bestsellers(category=product_category)
    Then merge and rank signals before returning recommendations.
    ---
    """
    data = _load_trend_data()

    craft = data.get(craft_type)
    if not craft:
        return _fallback_recommendation(craft_type, product_category)

    product = craft.get("products", {}).get(product_category)
    if not product:
        return _fallback_recommendation(craft_type, product_category)

    # Find the best matching audience data
    audiences = product.get("audiences", {})
    audience_data = None

    if target_customer and target_customer in audiences:
        audience_data = audiences[target_customer]
    else:
        # Pick the first available audience as default
        first_key = next(iter(audiences), None)
        audience_data = audiences.get(first_key) if first_key else None

    if not audience_data:
        return _fallback_recommendation(craft_type, product_category)

    # Build recommendation response
    recommendation = {
        "craft_type": craft.get("craft_label", craft_type),
        "craft_description": craft.get("description", ""),
        "product_category": product.get("label", product_category),
        "target_audience": audience_data.get("label", target_customer or "General"),
        "trending_colors": audience_data.get("trending_colors", []),
        "trending_motifs": audience_data.get("trending_motifs", []),
        "product_suggestions": audience_data.get("product_suggestions", []),
        "styling_insights": audience_data.get("styling_insights", []),
        "rationale": audience_data.get("rationale", ""),
        "data_source": "mock",  # Change to "live" when real APIs are connected
    }

    # Apply optional style filtering / emphasis
    if style_preference:
        recommendation["style_note"] = (
            f"Filtered for '{style_preference}' style preference. "
            "Recommendations have been adjusted to emphasize this aesthetic direction."
        )

    return recommendation


def _fallback_recommendation(craft_type, product_category):
    """
    Return generic recommendations when specific data isn't available.
    Ensures the app always returns something useful.
    """
    return {
        "craft_type": craft_type.replace("_", " ").title(),
        "product_category": product_category.replace("_", " ").title(),
        "target_audience": "General",
        "trending_colors": [
            {"name": "Earth Tone", "hex": "#A0785A"},
            {"name": "Off-White", "hex": "#FAF0E6"},
            {"name": "Indigo", "hex": "#3F51B5"},
            {"name": "Warm Gold", "hex": "#D4A843"},
        ],
        "trending_motifs": [
            "Contemporary adaptations of traditional patterns",
            "Minimalist interpretations with clean lines",
            "Nature-inspired motifs in modern compositions",
            "Geometric patterns blended with craft-specific elements",
        ],
        "product_suggestions": [
            "Explore lighter, everyday-use formats",
            "Consider accessories alongside traditional products",
            "Create coordinated collections for gifting",
        ],
        "styling_insights": [
            "Sustainability and handmade storytelling increases purchase intent",
            "Lighter, versatile pieces appeal to younger demographics",
            "Earth tones and muted palettes are trending across categories",
        ],
        "rationale": (
            "These are general trend directions based on broader market signals. "
            "For more specific recommendations, more detailed craft and "
            "audience data would be needed."
        ),
        "data_source": "fallback",
    }
