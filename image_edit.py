from io import BytesIO
import requests
import base64
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import os

from config import OPENROUTER_API_KEY, FAL_KEY

def save_user_image(user_id, image_bytes):
    """Save uploaded image"""
    path = f"user_{user_id}.png"
    
    with open(path, "wb") as f:
        f.write(image_bytes)
    
    return path

def edit_image_with_ai(image_path, prompt):
    try:
        print(f"🎨 FAL Inpainting: {prompt}")
        
        if not FAL_KEY:
            return None
        
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        
        response = requests.post(
                "https://queue.fal.run/fal-ai/flux-kontext",
            headers={"Authorization": f"Key {FAL_KEY}"},
            json={
                "image_url": f"data:image/png;base64,{image_base64}",
                "prompt": f"Transform the image according to this instruction: {prompt}. Preserve the original identity, face, pose, lighting and background. Make the requested change clearly and realistically.",
                "enable_safety_checker": True
            },
            timeout=120
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            
            if "request_id" in data:
                request_id = data["request_id"]
                for _ in range(30):
                    result = requests.get(
                        f"https://queue.fal.run/requests/{request_id}/status",
                        headers={"Authorization": f"Key {FAL_KEY}"}
                    )
                    
                    if result.json().get("status") == "completed":
                        output = result.json().get("output", {})
                        if "image" in output:
                            img_url = output["image"]["url"]
                            img_response = requests.get(img_url)
                            image = BytesIO(img_response.content)
                            image.name = "edited_image.jpg"
                            image.seek(0)
                            return image
                    
                    import time
                    time.sleep(1)
            
            if "image" in data:
                img_url = data["image"]["url"]
                img_response = requests.get(img_url)
                image = BytesIO(img_response.content)
                image.name = "edited_image.jpg"
                image.seek(0)
                return image
                
    except Exception as e:
        print(f"❌ FAL Inpainting Error: {e}")
    
    return None

def edit_image_locally(image_path, prompt):
    """Edit image with local PIL (Brightness, Contrast, Filters)"""
    try:
        print(f"🎨 Local Edit: {prompt}")
        
        img = Image.open(image_path)
        
        # Parse prompt for filters
        prompt_lower = prompt.lower()
        
        # Brightness
        if "bright" in prompt_lower or "lighter" in prompt_lower:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.3)
        elif "dark" in prompt_lower or "darker" in prompt_lower:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.7)
        
        # Contrast
        if "contrast" in prompt_lower or "sharp" in prompt_lower:
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.3)
        
        # Saturation
        if "vivid" in prompt_lower or "saturated" in prompt_lower or "color" in prompt_lower:
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.4)
        elif "desaturate" in prompt_lower or "grayscale" in prompt_lower or "black and white" in prompt_lower:
            img = img.convert("L")
            img = img.convert("RGB")
        
        # Filters
        if "blur" in prompt_lower:
            img = img.filter(ImageFilter.GaussianBlur(radius=5))
        elif "sharpen" in prompt_lower or "detail" in prompt_lower:
            img = img.filter(ImageFilter.SHARPEN)
        elif "smooth" in prompt_lower:
            img = img.filter(ImageFilter.SMOOTH)
        elif "edge" in prompt_lower or "outline" in prompt_lower:
            img = img.filter(ImageFilter.FIND_EDGES)
        
        # Sepia/warm effect
        if "warm" in prompt_lower or "sepia" in prompt_lower or "vintage" in prompt_lower:
            img = apply_sepia(img)
        
        # Cool effect
        if "cool" in prompt_lower or "cold" in prompt_lower or "blue" in prompt_lower:
            img = apply_cool_tone(img)
        
        # Save and return
        output = BytesIO()
        img.save(output, format="JPEG", quality=95)
        output.name = "edited_image.jpg"
        output.seek(0)
        return output
        
    except Exception as e:
        print(f"❌ Local Edit Error: {e}")
    
    return None

def apply_sepia(img):
    """Apply sepia tone effect"""
    img = img.convert("RGB")
    pixels = img.load()
    
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            r, g, b = pixels[x, y]
            
            tr = int(0.393 * r + 0.769 * g + 0.189 * b)
            tg = int(0.349 * r + 0.686 * g + 0.168 * b)
            tb = int(0.272 * r + 0.534 * g + 0.131 * b)
            
            pixels[x, y] = (min(tr, 255), min(tg, 255), min(tb, 255))
    
    return img

def apply_cool_tone(img):
    """Apply cool/blue tone effect"""
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

def edit_image(image_path, prompt):
    """Edit image with AI or local filters"""
    
    # Try AI inpainting first
    result = edit_image_with_ai(image_path, prompt)
    if result:
        return result
    
    # Fallback to local editing
    result = edit_image_locally(image_path, prompt)
    if result:
        return result
    
    return None
