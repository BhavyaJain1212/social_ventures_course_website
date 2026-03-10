"""
Image Service — Design concept image generation (pluggable backend).

Currently uses a mock image generator that creates styled placeholder
images using Pillow. The architecture supports swapping in real
image generation APIs.

---
FUTURE INTEGRATION POINTS:

1. OpenAI DALL-E:
    import openai
    openai.api_key = os.getenv("IMAGE_GEN_API_KEY")
    response = openai.Image.create(prompt=prompt, n=1, size="512x512")
    image_url = response["data"][0]["url"]

2. Stability AI (Stable Diffusion):
    import requests
    response = requests.post(
        "https://api.stability.ai/v1/generation/stable-diffusion-v1-5/text-to-image",
        headers={"Authorization": f"Bearer {api_key}"},
        json={"text_prompts": [{"text": prompt}], "cfg_scale": 7, ...}
    )

3. Hugging Face Inference:
    from huggingface_hub import InferenceClient
    client = InferenceClient("stabilityai/stable-diffusion-2", token=api_key)
    image = client.text_to_image(prompt)
---
"""

import os
import json
import base64
import hashlib
import urllib.error
import urllib.request
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Try to import Pillow for mock image generation
try:
    from PIL import Image, ImageDraw, ImageFont
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

# Directory to store generated concept images
GENERATED_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "static", "images", "generated"
)


def generate_concept_image(prompt, craft_type="", product_type=""):
    """
    Generate a concept image from a design prompt.

    Currently uses mock generation. Replace the body of this function
    with a real API call to enable AI image generation.

    Args:
        prompt (str): The design generation prompt.
        craft_type (str): For labeling the mock image.
        product_type (str): For labeling the mock image.

    Returns:
        str: Relative URL path to the generated image (for use in <img> tags).
    """
    provider = os.getenv(
        "IMAGE_GEN_PROVIDER",
        "openai_dalle" if os.getenv("OPENAI_API_KEY") else "mock",
    )

    if provider == "mock":
        return _generate_mock_image(prompt, craft_type, product_type)
    if provider == "openai_dalle":
        try:
            return _generate_openai_image(prompt)
        except Exception as exc:
            # Keep API resilient in local/dev environments.
            print(f"[image_service] OpenAI image generation failed: {exc}. Falling back to mock image.")
            return _generate_mock_image(prompt, craft_type, product_type)

    raise ValueError(f"Unknown image generation provider: {provider}")


def _generate_openai_image(prompt):
    """
    Generate an image with OpenAI Images API and save it locally.

    Required env vars:
        OPENAI_API_KEY

    Optional env vars:
        IMAGE_GEN_MODEL      (default: gpt-image-1)
        IMAGE_GEN_SIZE       (default: 1024x1024)
        IMAGE_GEN_QUALITY    (optional)
        IMAGE_GEN_STYLE      (optional)
        OPENAI_IMAGES_ENDPOINT (default: https://api.openai.com/v1/images/generations)
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    endpoint = os.getenv(
        "OPENAI_IMAGES_ENDPOINT", "https://api.openai.com/v1/images/generations"
    )
    model = os.getenv("IMAGE_GEN_MODEL", "gpt-image-1")
    size = os.getenv("IMAGE_GEN_SIZE", "1024x1024")
    quality = os.getenv("IMAGE_GEN_QUALITY", "").strip()
    style = os.getenv("IMAGE_GEN_STYLE", "").strip()

    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "n": 1,
    }
    if quality:
        payload["quality"] = quality
    if style:
        payload["style"] = style

    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        err_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"OpenAI API error ({exc.code}): {err_body[:300]}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach OpenAI API: {exc.reason}") from exc

    response_data = json.loads(body)
    image_data = (response_data.get("data") or [{}])[0]
    if not image_data:
        raise RuntimeError("OpenAI API returned no image data.")

    os.makedirs(GENERATED_DIR, exist_ok=True)
    prompt_hash = hashlib.md5(
        f"{prompt}{datetime.now().isoformat()}".encode("utf-8")
    ).hexdigest()[:12]
    filename = f"concept_{prompt_hash}.png"
    filepath = os.path.join(GENERATED_DIR, filename)

    b64_image = image_data.get("b64_json")
    image_url = image_data.get("url")

    if b64_image:
        image_bytes = base64.b64decode(b64_image)
        with open(filepath, "wb") as file_handle:
            file_handle.write(image_bytes)
    elif image_url:
        with urllib.request.urlopen(image_url, timeout=120) as image_resp:
            image_bytes = image_resp.read()
        with open(filepath, "wb") as file_handle:
            file_handle.write(image_bytes)
    else:
        raise RuntimeError("OpenAI response did not include 'b64_json' or 'url'.")

    return f"/static/images/generated/{filename}"


def _generate_mock_image(prompt, craft_type="", product_type=""):
    """
    Create a styled placeholder image using Pillow.

    Generates a visually appealing placeholder with craft-specific
    colors and text overlay showing the concept details.
    """
    os.makedirs(GENERATED_DIR, exist_ok=True)

    # Create a unique filename from the prompt
    prompt_hash = hashlib.md5(
        f"{prompt}{datetime.now().isoformat()}".encode()
    ).hexdigest()[:12]
    filename = f"concept_{prompt_hash}.png"
    filepath = os.path.join(GENERATED_DIR, filename)

    if PILLOW_AVAILABLE:
        _create_pillow_placeholder(filepath, craft_type, product_type, prompt)
    else:
        _create_simple_placeholder(filepath)

    return f"/static/images/generated/{filename}"


def _create_pillow_placeholder(filepath, craft_type, product_type, prompt):
    """Create a visually styled placeholder image using Pillow."""
    width, height = 512, 512

    # Craft-specific background colors (warm, artisan-friendly palette)
    color_map = {
        "banarasi_weaving": [(200, 170, 120), (180, 140, 100)],
        "madhubani_art":    [(180, 120, 100), (160, 100, 80)],
        "block_printing":   [(120, 140, 160), (100, 120, 140)],
    }
    colors = color_map.get(craft_type, [(160, 140, 130), (140, 120, 110)])
    bg_top, bg_bottom = colors

    # Create gradient background
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)

    for y in range(height):
        ratio = y / height
        r = int(bg_top[0] + (bg_bottom[0] - bg_top[0]) * ratio)
        g = int(bg_top[1] + (bg_bottom[1] - bg_top[1]) * ratio)
        b = int(bg_top[2] + (bg_bottom[2] - bg_top[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Draw decorative border
    border_color = (255, 248, 240, 180)
    draw.rectangle([20, 20, width - 20, height - 20], outline=(255, 248, 240), width=2)
    draw.rectangle([30, 30, width - 30, height - 30], outline=(255, 248, 240), width=1)

    # Draw decorative corner elements
    corner_size = 40
    for x, y in [(35, 35), (width - 35 - corner_size, 35),
                 (35, height - 35 - corner_size),
                 (width - 35 - corner_size, height - 35 - corner_size)]:
        draw.rectangle([x, y, x + corner_size, y + corner_size],
                       outline=(255, 248, 240), width=1)
        draw.line([(x, y), (x + corner_size, y + corner_size)],
                  fill=(255, 248, 240), width=1)

    # Draw central diamond decorative element
    cx, cy = width // 2, height // 2 - 30
    diamond_size = 60
    draw.polygon([
        (cx, cy - diamond_size),
        (cx + diamond_size, cy),
        (cx, cy + diamond_size),
        (cx - diamond_size, cy)
    ], outline=(255, 248, 240), width=2)

    # Add text labels
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11)
    except (IOError, OSError):
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    text_color = (255, 248, 240)

    # Title
    title = "✦ Design Concept ✦"
    bbox = draw.textbbox((0, 0), title, font=font_large)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, 60), title, fill=text_color, font=font_large)

    # Craft type
    craft_label = craft_type.replace("_", " ").title() if craft_type else "Artisan Craft"
    bbox = draw.textbbox((0, 0), craft_label, font=font_medium)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, 90), craft_label, fill=text_color, font=font_medium)

    # Product type
    product_label = product_type.replace("_", " ").title() if product_type else "Product"
    bbox = draw.textbbox((0, 0), product_label, font=font_medium)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, 115), product_label, fill=text_color, font=font_medium)

    # Mock AI notice
    notice = "[ AI-Generated Concept Preview ]"
    bbox = draw.textbbox((0, 0), notice, font=font_small)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, height // 2 + 50), notice, fill=text_color, font=font_small)

    # Prompt preview (truncated)
    prompt_preview = prompt[:80] + "..." if len(prompt) > 80 else prompt
    # Word wrap
    words = prompt_preview.split()
    lines = []
    current_line = ""
    for word in words:
        test = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font_small)
        if bbox[2] - bbox[0] > width - 80:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test
    if current_line:
        lines.append(current_line)

    y_offset = height // 2 + 80
    for line in lines[:3]:
        bbox = draw.textbbox((0, 0), line, font=font_small)
        tw = bbox[2] - bbox[0]
        draw.text(((width - tw) // 2, y_offset), line, fill=text_color, font=font_small)
        y_offset += 18

    # Footer
    footer = "Connect real image API for actual generation"
    bbox = draw.textbbox((0, 0), footer, font=font_small)
    tw = bbox[2] - bbox[0]
    draw.text(((width - tw) // 2, height - 50), footer, fill=(255, 248, 240), font=font_small)

    img.save(filepath, "PNG")


def _create_simple_placeholder(filepath):
    """Fallback: create a tiny valid PNG without Pillow."""
    # Minimal 1x1 white PNG
    import struct
    import zlib

    def create_png(width, height, color=(200, 180, 160)):
        raw_data = b""
        for _ in range(height):
            raw_data += b"\x00" + bytes(color) * width
        compressed = zlib.compress(raw_data)

        png = b"\x89PNG\r\n\x1a\n"
        # IHDR
        ihdr_data = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
        ihdr_crc = zlib.crc32(b"IHDR" + ihdr_data) & 0xFFFFFFFF
        png += struct.pack(">I", 13) + b"IHDR" + ihdr_data + struct.pack(">I", ihdr_crc)
        # IDAT
        idat_crc = zlib.crc32(b"IDAT" + compressed) & 0xFFFFFFFF
        png += struct.pack(">I", len(compressed)) + b"IDAT" + compressed + struct.pack(">I", idat_crc)
        # IEND
        iend_crc = zlib.crc32(b"IEND") & 0xFFFFFFFF
        png += struct.pack(">I", 0) + b"IEND" + struct.pack(">I", iend_crc)
        return png

    with open(filepath, "wb") as f:
        f.write(create_png(256, 256))
