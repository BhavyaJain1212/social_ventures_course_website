"""
API Routes — JSON API endpoints for the Artisan Dashboard.

Handles:
    POST /api/recommend-trends   → Get trend recommendations
    POST /api/generate-design    → Generate a design concept
    GET  /api/concepts           → List all saved concepts
    DELETE /api/concepts/<id>    → Delete a saved concept
    PUT  /api/profile            → Update artisan profile (stretch)
    GET  /api/crafts             → Get available craft types
    GET  /api/products/<craft>   → Get products for a craft
    GET  /api/audiences/<craft>/<product> → Get audiences
"""

from flask import Blueprint, request, jsonify
from services.trend_service import (
    get_recommendations,
    get_available_crafts,
    get_products_for_craft,
    get_audiences_for_product,
)
from services.prompt_service import (
    build_design_prompt,
    generate_concept_summary,
    generate_concept_title,
)
from services.image_service import generate_concept_image
from models.concept_model import (
    create_concept,
    get_all_concepts,
    get_concept_by_id,
    delete_concept,
)

api_bp = Blueprint("api", __name__, url_prefix="/api")


# ─── Trend Recommendations ───────────────────────────────────────────────────

@api_bp.route("/recommend-trends", methods=["POST"])
def recommend_trends():
    """
    Get trend recommendations for a craft-product combination.

    Expected JSON body:
    {
        "craft_type": "banarasi_weaving",
        "product_category": "sari",
        "target_customer": "young_working_women",   // optional
        "style_preference": "pastel"                 // optional
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    craft_type = data.get("craft_type", "")
    product_category = data.get("product_category", "")

    if not craft_type or not product_category:
        return jsonify({
            "error": "Both 'craft_type' and 'product_category' are required."
        }), 400

    target_customer = data.get("target_customer", "")
    style_preference = data.get("style_preference", "")

    recommendations = get_recommendations(
        craft_type=craft_type,
        product_category=product_category,
        target_customer=target_customer,
        style_preference=style_preference,
    )

    return jsonify({
        "success": True,
        "recommendations": recommendations,
    })


# ─── Design Concept Generation ───────────────────────────────────────────────

@api_bp.route("/generate-design", methods=["POST"])
def generate_design():
    """
    Generate a design concept with prompt, summary, and image.

    Expected JSON body:
    {
        "craft_type": "Banarasi weaving",
        "product_type": "stole",
        "style": "contemporary",
        "color_palette": "pastel rose, muted gold, ivory",
        "motif_direction": "floral zari motifs",
        "target_audience": "young urban professionals"
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    craft_type = data.get("craft_type", "")
    product_type = data.get("product_type", "")

    if not craft_type or not product_type:
        return jsonify({
            "error": "Both 'craft_type' and 'product_type' are required."
        }), 400

    style = data.get("style", "contemporary")
    color_palette = data.get("color_palette", "")
    motif_direction = data.get("motif_direction", "")
    target_audience = data.get("target_audience", "")

    # 1. Build the design prompt
    prompt = build_design_prompt(
        craft_type=craft_type,
        product_type=product_type,
        style=style,
        color_palette=color_palette,
        motif_direction=motif_direction,
        target_audience=target_audience,
    )

    # 2. Generate concept summary
    summary = generate_concept_summary(
        craft_type=craft_type,
        product_type=product_type,
        style=style,
        color_palette=color_palette,
        motif_direction=motif_direction,
        target_audience=target_audience,
    )

    # 3. Generate concept title
    title = generate_concept_title(craft_type, product_type, style)

    # 4. Generate concept image
    # Use the key version of craft_type for image service
    craft_key = craft_type.lower().replace(" ", "_")
    product_key = product_type.lower().replace(" ", "_")
    image_url = generate_concept_image(prompt, craft_key, product_key)

    # 5. Save to database
    concept_data = {
        "title": title,
        "craft_type": craft_type,
        "product_type": product_type,
        "target_audience": target_audience,
        "style": style,
        "color_palette": color_palette,
        "motif_direction": motif_direction,
        "prompt_text": prompt,
        "image_url": image_url,
        "summary": summary,
    }
    concept_id = create_concept(concept_data)

    return jsonify({
        "success": True,
        "concept": {
            "id": concept_id,
            "title": title,
            "prompt": prompt,
            "summary": summary,
            "image_url": image_url,
            "craft_type": craft_type,
            "product_type": product_type,
            "style": style,
        },
    })


# ─── Saved Concepts CRUD ─────────────────────────────────────────────────────

@api_bp.route("/concepts", methods=["GET"])
def list_concepts():
    """Return all saved concepts as JSON."""
    concepts = get_all_concepts()
    return jsonify({"success": True, "concepts": concepts})


@api_bp.route("/concepts/<int:concept_id>", methods=["DELETE"])
def remove_concept(concept_id):
    """Delete a saved concept by ID."""
    deleted = delete_concept(concept_id)
    if deleted:
        return jsonify({"success": True, "message": "Concept deleted."})
    return jsonify({"error": "Concept not found."}), 404


# ─── Craft Metadata Endpoints ────────────────────────────────────────────────

@api_bp.route("/crafts", methods=["GET"])
def list_crafts():
    """Return available craft types."""
    crafts = get_available_crafts()
    return jsonify({"success": True, "crafts": crafts})


@api_bp.route("/products/<craft_key>", methods=["GET"])
def list_products(craft_key):
    """Return product categories for a craft type."""
    products = get_products_for_craft(craft_key)
    return jsonify({"success": True, "products": products})


@api_bp.route("/audiences/<craft_key>/<product_key>", methods=["GET"])
def list_audiences(craft_key, product_key):
    """Return target audiences for a craft-product combination."""
    audiences = get_audiences_for_product(craft_key, product_key)
    return jsonify({"success": True, "audiences": audiences})


# ─── Profile (Stretch Feature) ───────────────────────────────────────────────

@api_bp.route("/profile", methods=["PUT"])
def update_profile():
    """
    Update artisan profile. (Stretch feature — stores in session for MVP.)

    In a full app this would update a database record.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    # For MVP, just echo back the updated profile
    # In production, save to a users table
    return jsonify({
        "success": True,
        "message": "Profile updated successfully.",
        "profile": data,
    })
