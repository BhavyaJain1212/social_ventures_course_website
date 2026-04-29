"""
Product Service — Mock artisan product catalog for the shop page.

This keeps marketplace browsing data separate from the trend metadata
used by the dashboard product dropdowns.
"""


MOCK_PRODUCTS = [
    {
        "id": "prod-indigo-stole",
        "name": "Handwoven Indigo Cotton Stole",
        "artisan_name": "Ramesh Kumar",
        "craft_type": "Banarasi Weaving",
        "region": "Varanasi, Uttar Pradesh",
        "price": 2800,
        "currency": "INR",
        "short_description": (
            "A lightweight handwoven stole with subtle zari edges and a soft "
            "indigo cotton drape for everyday layering."
        ),
        "image_url": "/static/images/generated/concept_1c6ed69ef905.png",
        "availability_status": "Preorder open",
        "estimated_delivery": "Ships in 3-4 weeks",
        "tags": ["handmade", "handwoven", "natural dyes", "cotton"],
    },
    {
        "id": "prod-terracotta-vase",
        "name": "Terracotta Studio Vase",
        "artisan_name": "Meera Prajapati",
        "craft_type": "Pottery",
        "region": "Khurja, Uttar Pradesh",
        "price": 1650,
        "currency": "INR",
        "short_description": (
            "A sculptural terracotta vase with a matte hand-finished surface, "
            "made for dried stems and quiet shelf styling."
        ),
        "image_url": "/static/images/generated/concept_ee568526781c.png",
        "availability_status": "Limited batch",
        "estimated_delivery": "Ships in 2-3 weeks",
        "tags": ["handmade", "ceramic", "small batch", "home decor"],
    },
    {
        "id": "prod-dhokra-figurine",
        "name": "Brass Dhokra Figurine",
        "artisan_name": "Anil Soren",
        "craft_type": "Dhokra Metal Craft",
        "region": "Bastar, Chhattisgarh",
        "price": 3400,
        "currency": "INR",
        "short_description": (
            "A lost-wax brass figurine with expressive linework, cast by hand "
            "using traditional Dhokra techniques."
        ),
        "image_url": "/static/images/generated/concept_49a19c1362b5.png",
        "availability_status": "Preorder open",
        "estimated_delivery": "Ships in 4-5 weeks",
        "tags": ["handmade", "brass", "heritage craft", "collectible"],
    },
    {
        "id": "prod-block-print-cushion",
        "name": "Natural Dye Block-Printed Cushion Cover",
        "artisan_name": "Farida Khan",
        "craft_type": "Block Printing",
        "region": "Bagru, Rajasthan",
        "price": 950,
        "currency": "INR",
        "short_description": (
            "A cotton cushion cover printed with carved wooden blocks and "
            "earthy natural dye tones."
        ),
        "image_url": "/static/images/generated/concept_498f90134f06.png",
        "availability_status": "Preorder open",
        "estimated_delivery": "Ships in 2 weeks",
        "tags": ["handmade", "block printed", "natural dyes", "cotton"],
    },
    {
        "id": "prod-bamboo-basket",
        "name": "Bamboo Utility Basket",
        "artisan_name": "Lalnunpuii",
        "craft_type": "Bamboo Weaving",
        "region": "Aizawl, Mizoram",
        "price": 1200,
        "currency": "INR",
        "short_description": (
            "A sturdy woven bamboo basket for storage, market runs, or "
            "textural home organization."
        ),
        "image_url": "/static/images/generated/concept_2ba3e33278a1.png",
        "availability_status": "Coming soon",
        "estimated_delivery": "Expected next month",
        "tags": ["handmade", "sustainable", "bamboo", "utility"],
    },
    {
        "id": "prod-blue-pottery-bowl",
        "name": "Blue Pottery Serving Bowl",
        "artisan_name": "Naseem Qureshi",
        "craft_type": "Blue Pottery",
        "region": "Jaipur, Rajasthan",
        "price": 2100,
        "currency": "INR",
        "short_description": (
            "A glazed serving bowl with floral blue pottery motifs, sized for "
            "snacks, salads, and festive table settings."
        ),
        "image_url": "/static/images/generated/concept_cfb144b0e477.png",
        "availability_status": "Limited batch",
        "estimated_delivery": "Ships in 3 weeks",
        "tags": ["handmade", "ceramic", "tableware", "glazed"],
    },
    {
        "id": "prod-leather-journal",
        "name": "Handcrafted Leather Journal",
        "artisan_name": "Saira Bano",
        "craft_type": "Leather Craft",
        "region": "Shantiniketan, West Bengal",
        "price": 1450,
        "currency": "INR",
        "short_description": (
            "A hand-stitched leather journal with recycled paper pages and a "
            "warm, naturally aging cover."
        ),
        "image_url": "/static/images/generated/concept_b77440a84e71.png",
        "availability_status": "Preorder open",
        "estimated_delivery": "Ships in 10-14 days",
        "tags": ["handmade", "leather", "recycled paper", "giftable"],
    },
    {
        "id": "prod-kilim-runner",
        "name": "Wool Kilim Table Runner",
        "artisan_name": "Tsering Dolma",
        "craft_type": "Kilim Weaving",
        "region": "Leh, Ladakh",
        "price": 3900,
        "currency": "INR",
        "short_description": (
            "A flatwoven wool runner with geometric kilim motifs, bringing "
            "warmth and pattern to dining tables and consoles."
        ),
        "image_url": "/static/images/generated/concept_1c6ed69ef905.png",
        "availability_status": "Preorder open",
        "estimated_delivery": "Ships in 5-6 weeks",
        "tags": ["handmade", "wool", "handwoven", "table linen"],
    },
]


def get_shop_products():
    """Return the mock shop catalog."""
    return MOCK_PRODUCTS


def get_shop_product_by_id(product_id):
    """Return one mock shop product by ID, or None."""
    return next(
        (product for product in MOCK_PRODUCTS if product["id"] == product_id),
        None,
    )
