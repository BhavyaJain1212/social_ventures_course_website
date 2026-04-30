"""
Product Service — Mock artisan product catalog for the shop page.

This keeps marketplace browsing data separate from the trend metadata
used by the dashboard product dropdowns.
"""


MOCK_PRODUCTS = [
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
        "id": "prod-phulkari-laptop-bag",
        "name": "Phulkari Embroidered Laptop Bag",
        "artisan_name": "Gurpreet Kaur",
        "craft_type": "Phulkari Embroidery",
        "region": "Amritsar, Punjab",
        "price": 4200,
        "currency": "INR",
        "short_description": (
            "A structured laptop bag covered in vibrant Phulkari embroidery "
            "with fuchsia, gold, and orange threadwork on a tan leather frame."
        ),
        "image_url": "/static/images/phulkari-laptop-bag.jpeg",
        "availability_status": "Preorder open",
        "estimated_delivery": "Ships in 3-4 weeks",
        "tags": ["handmade", "embroidery", "phulkari", "laptop bag", "punjab"],
    },
    {
        "id": "prod-embroidered-shirt",
        "name": "Floral Embroidered Cotton Shirt",
        "artisan_name": "Priya Sharma",
        "craft_type": "Hand Embroidery",
        "region": "Lucknow, Uttar Pradesh",
        "price": 2600,
        "currency": "INR",
        "short_description": (
            "A breezy white cotton shirt with hand-embroidered floral vines "
            "in blue and pink running along the placket and cuffs."
        ),
        "image_url": "/static/images/embroidered-shirt.jpeg",
        "availability_status": "Preorder open",
        "estimated_delivery": "Ships in 2-3 weeks",
        "tags": ["handmade", "embroidery", "cotton", "wearable", "chikankari"],
    },
    {
        "id": "prod-khanda-tshirt",
        "name": "Khanda Embroidery Art T-Shirt",
        "artisan_name": "Harjinder Singh",
        "craft_type": "Embroidery Print",
        "region": "Amritsar, Punjab",
        "price": 1800,
        "currency": "INR",
        "short_description": (
            "A heritage black tee featuring an intricately embroidered Khanda "
            "motif with floral detailing in gold, red, and blue."
        ),
        "image_url": "/static/images/khanda-tshirt.jpeg",
        "availability_status": "Preorder open",
        "estimated_delivery": "Ships in 2 weeks",
        "tags": ["handmade", "embroidery", "wearable", "heritage", "punjab"],
    },
    {
        "id": "prod-crochet-sunflower-sling",
        "name": "Crochet Sunflower Sling Bag",
        "artisan_name": "Ananya Bose",
        "craft_type": "Crochet",
        "region": "Kolkata, West Bengal",
        "price": 1350,
        "currency": "INR",
        "short_description": (
            "A handcrocheted sling bag in cobalt blue with bold sunflower "
            "motifs — cheerful, compact, and entirely handmade."
        ),
        "image_url": "/static/images/crochet-sunflower-sling.jpeg",
        "availability_status": "Preorder open",
        "estimated_delivery": "Ships in 2-3 weeks",
        "tags": ["handmade", "crochet", "bag", "cotton", "colorful"],
    },
    {
        "id": "prod-crochet-granny-sling",
        "name": "Crochet Granny Square Sling Bag",
        "artisan_name": "Ananya Bose",
        "craft_type": "Crochet",
        "region": "Kolkata, West Bengal",
        "price": 1500,
        "currency": "INR",
        "short_description": (
            "A crescent-shaped crochet sling with granny square patchwork in "
            "slate, terracotta, teal, and mustard — roomy and adjustable."
        ),
        "image_url": "/static/images/crochet-granny-sling.jpeg",
        "availability_status": "Preorder open",
        "estimated_delivery": "Ships in 2-3 weeks",
        "tags": ["handmade", "crochet", "bag", "granny square", "boho"],
    },
    {
        "id": "prod-floral-laptop-bag",
        "name": "Wildflower Embroidered Laptop Bag",
        "artisan_name": "Ritu Verma",
        "craft_type": "Hand Embroidery",
        "region": "Delhi",
        "price": 3100,
        "currency": "INR",
        "short_description": (
            "A structured black canvas laptop bag with a delicate meadow of "
            "hand-embroidered wildflowers across the front panel."
        ),
        "image_url": "/static/images/floral-laptop-bag.jpeg",
        "availability_status": "Preorder open",
        "estimated_delivery": "Ships in 3 weeks",
        "tags": ["handmade", "embroidery", "laptop bag", "canvas", "floral"],
    },
    {
        "id": "prod-blue-pottery-vase-set",
        "name": "Blue Pottery Vase Collection",
        "artisan_name": "Naseem Qureshi",
        "craft_type": "Blue Pottery",
        "region": "Jaipur, Rajasthan",
        "price": 5800,
        "currency": "INR",
        "short_description": (
            "A curated set of five hand-thrown blue pottery vases with "
            "indigo floral motifs on a white glaze — perfect for shelf styling."
        ),
        "image_url": "/static/images/blue-pottery-vases.jpeg",
        "availability_status": "Preorder open",
        "estimated_delivery": "Ships in 4 weeks",
        "tags": ["handmade", "ceramic", "blue pottery", "home decor", "set"],
    },
    {
        "id": "prod-mushroom-mugs",
        "name": "Ceramic Mushroom Mug with Lid",
        "artisan_name": "Meera Prajapati",
        "craft_type": "Pottery",
        "region": "Khurja, Uttar Pradesh",
        "price": 1100,
        "currency": "INR",
        "short_description": (
            "A hand-sculpted ceramic mug shaped like a red-cap mushroom, "
            "complete with a matching lid — whimsical and functional."
        ),
        "image_url": "/static/images/mushroom-mugs.jpeg",
        "availability_status": "Preorder open",
        "estimated_delivery": "Ships in 2-3 weeks",
        "tags": ["handmade", "ceramic", "mug", "kitchenware", "quirky"],
    },
    {
        "id": "prod-bow-mug",
        "name": "Ceramic Bow Mug",
        "artisan_name": "Meera Prajapati",
        "craft_type": "Pottery",
        "region": "Khurja, Uttar Pradesh",
        "price": 950,
        "currency": "INR",
        "short_description": (
            "A hand-thrown cream ceramic mug with a sculpted pink bow and "
            "polka-dot texture — a charming addition to any morning ritual."
        ),
        "image_url": "/static/images/bow-mug.jpeg",
        "availability_status": "Preorder open",
        "estimated_delivery": "Ships in 2 weeks",
        "tags": ["handmade", "ceramic", "mug", "kitchenware", "gifting"],
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
