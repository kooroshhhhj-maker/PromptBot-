from io import BytesIO
import requests
import base64
import json

from PIL import Image, ImageEnhance, ImageFilter

from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID


# ============================================================
# Save uploaded image
# ============================================================

def save_user_image(user_id, image_bytes):
    """Save uploaded image."""
    path = f"user_{user_id}.png"

    with open(path, "wb") as f:
        f.write(image_bytes)

    return path


# ============================================================
# FLUX.2 KLEIN 4B — CLOUDFLARE IMAGE EDITOR
# ============================================================

def edit_image_with_ai(image_path, prompt):
    """
    Edit an image using Cloudflare Workers AI
    with FLUX.2 Klein 4B.

    Returns:
        BytesIO containing JPEG image
        or None if editing fails.
    """

    try:
        print("🎨 FLUX.2 Klein 4B Edit:", prompt)

        if not CLOUDFLARE_API_TOKEN:
            print("❌ CLOUDFLARE_API_TOKEN is missing")
            return None

        if not CLOUDFLARE_ACCOUNT_ID:
            print("❌ CLOUDFLARE_ACCOUNT_ID is missing")
            return None

        if not os_path_exists(image_path):
            print("❌ Image file does not exist:", image_path)
            return None

        url = (
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/"
            "@cf/black-forest-labs/flux-2-klein-4b"
        )

        # Open image
        with open(image_path, "rb") as f:
            image_bytes = f.read()

        print("📷 Input image:", len(image_bytes), "bytes")

        # Make sure the uploaded image has a normal image MIME type
        try:
            with Image.open(BytesIO(image_bytes)) as test_img:
                image_format = (test_img.format or "PNG").upper()
        except Exception as e:
            print("❌ Cannot read input image:", e)
            return None

        if image_format in ("JPG", "JPEG"):
            mime_type = "image/jpeg"
            filename = "input.jpg"
        elif image_format == "WEBP":
            mime_type = "image/webp"
            filename = "input.webp"
        else:
            mime_type = "image/png"
            filename = "input.png"

        # Keep the user's requested edit focused.
        final_prompt = (
            "Edit this image according to the user's request. "
            "Preserve everything that the user did not ask to change. "
            "Do not unnecessarily change the subject, composition, "
            "background, lighting, pose, or other details. "
            f"User request: {prompt}"
        )

        print("📝 Prompt:", final_prompt)

        # Cloudflare FLUX.2 Klein requires multipart/form-data.
        files = {
            "input_image_0": (
                filename,
                image_bytes,
                mime_type
            )
        }

        data = {
            "prompt": final_prompt
        }

        print("☁️ Sending to Cloudflare...")

        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"
            },
            files=files,
            data=data,
            timeout=180
        )

        print("☁️ Cloudflare HTTP:", response.status_code)

        if response.status_code != 200:
            print("❌ Cloudflare error:")
            print(response.text)
            return None

        # Cloudflare returns JSON containing Base64 image data.
        try:
            result = response.json()
        except Exception as e:
            print("❌ Invalid Cloudflare JSON:", e)
            print(response.text[:1000])
            return None

        if not result.get("success"):
            print("❌ Cloudflare returned success=false")
            print(result)
            return None

        result_data = result.get("result", {})

        if not isinstance(result_data, dict):
            print("❌ Unexpected result type:", type(result_data))
            return None

        image_base64 = result_data.get("image")

        if not image_base64:
            print("❌ Cloudflare did not return an image")
            print("Result keys:", list(result_data.keys()))
            return None

        print("🧩 Base64 image received:", len(image_base64), "characters")

        # Decode Base64 → real JPEG bytes
        try:
            # Some APIs may return a data URI.
            if "," in image_base64:
                image_base64 = image_base64.split(",", 1)[1]

            output_bytes = base64.b64decode(image_base64)
        except Exception as e:
            print("❌ Base64 decode error:", e)
            return None

        print("🖼️ Decoded output:", len(output_bytes), "bytes")

        # Validate that the returned data is actually an image.
        try:
            test_image = Image.open(BytesIO(output_bytes))
            test_image.load()

            print(
                "✅ Output image:",
                test_image.format,
                test_image.size,
                test_image.mode
            )

        except Exception as e:
            print("❌ Returned data is not a valid image:", e)
            return None

        # Return JPEG/PNG bytes in the format Telegram can send.
        output = BytesIO(output_bytes)
        output.name = "edited_image.jpg"
        output.seek(0)

        print("✅ FLUX.2 Klein edit successful")

        return output

    except requests.exceptions.Timeout:
        print("❌ FLUX timeout")
        return None

    except requests.exceptions.RequestException as e:
        print("❌ FLUX request error:", e)
        return None

    except Exception as e:
        print("❌ FLUX Edit Error:", repr(e))
        return None


# ============================================================
# Small helper
# ============================================================

def os_path_exists(path):
    """Avoid importing the entire os module just for this check."""
    try:
        with open(path, "rb"):
            return True
    except Exception:
        return False


# ============================================================
# LOCAL PIL FALLBACK
# ============================================================

def edit_image_locally(image_path, prompt):
    """Fallback image editing using local PIL filters."""

    try:
        print("🎨 Local Edit fallback:", prompt)

        img = Image.open(image_path).convert("RGB")

        prompt_lower = prompt.lower()

        # Brightness
        if "bright" in prompt_lower or "lighter" in prompt_lower:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.3)

        elif "dark" in prompt_lower or "darker" in prompt_lower:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.7)

        # Contrast
        if "contrast" in prompt_lower:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.3)

        # Sharpen
        if "sharp" in prompt_lower or "sharpen" in prompt_lower:
            img = img.filter(ImageFilter.SHARPEN)

        # Saturation
        if "vivid" in prompt_lower or "saturated" in prompt_lower:
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.4)

        # Grayscale
        if (
            "desaturate" in prompt_lower
            or "grayscale" in prompt_lower
            or "black and white" in prompt_lower
        ):
            img = img.convert("L").convert("RGB")

        # Blur
        if "blur" in prompt_lower:
            img = img.filter(ImageFilter.GaussianBlur(radius=5))

        # Smooth
        if "smooth" in prompt_lower:
            img = img.filter(ImageFilter.SMOOTH)

        # Edge
        if "edge" in prompt_lower or "outline" in prompt_lower:
            img = img.filter(ImageFilter.FIND_EDGES)

        # Warm / Sepia
        if (
            "warm" in prompt_lower
            or "sepia" in prompt_lower
            or "vintage" in prompt_lower
        ):
            img = apply_sepia(img)

        # Cool / Blue
        if "cool" in prompt_lower or "cold" in prompt_lower:
            img = apply_cool_tone(img)

        output = BytesIO()
        img.save(output, format="JPEG", quality=95)
        output.name = "edited_image.jpg"
        output.seek(0)

        print("✅ Local fallback successful")

        return output

    except Exception as e:
        print("❌ Local Edit Error:", repr(e))
        return None


# ============================================================
# SEPia
# ============================================================

def apply_sepia(img):
    """Apply sepia tone."""

    img = img.convert("RGB")
    pixels = img.load()

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b = pixels[x, y]

            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)

            pixels[x, y] = (
                min(tr, 255),
                min(tg, 255),
                min(tb, 255)
            )

    return img


# ============================================================
# COOL TONE
# ============================================================

def apply_cool_tone(img):
    """Apply cool blue tone."""

    img = img.convert("RGB")
    pixels = img.load()

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b = pixels[x, y]

            r = max(0, r - 30)
            g = min(255, g + 10)
            b = min(255, b + 50)

            pixels[x, y] = (r, g, b)

    return img


# ============================================================
# MAIN EDIT FUNCTION
# ============================================================

def edit_image(image_path, prompt):
    """
    Main image editing function.

    1. Try FLUX.2 Klein 4B.
    2. If AI fails, use local PIL fallback.
    """

    result = edit_image_with_ai(image_path, prompt)

    if result:
        return result

    print("⚠️ AI edit failed. Trying local fallback...")

    result = edit_image_locally(image_path, prompt)

    if result:
        return result

    print("❌ All image editing methods failed")

    return None
