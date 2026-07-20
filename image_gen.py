from io import BytesIO
import requests
import base64
import random

from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID, OPENROUTER_API_KEY

def generate_image_cloudflare(prompt):
    """Generate image using Cloudflare AI (Free)"""
    try:
        print("🎨 Cloudflare: Generating image:", prompt)
        
        url = (
            f"https://api.cloudflare.com/client/v4/accounts/"
            f"{CLOUDFLARE_ACCOUNT_ID}/ai/run/"
            "@cf/black-forest-labs/flux-1-schnell"
        )
        
        headers = {
            "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            url,
            headers=headers,
            json={"prompt": prompt},
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            img_base64 = data["result"]["image"]
            image_bytes = base64.b64decode(img_base64)
            image = BytesIO(image_bytes)
            image.name = "image.jpg"
            image.seek(0)
            return image
        else:
            print(f"❌ Cloudflare Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Cloudflare Error: {e}")
    
    return None

def generate_image_fal(prompt):
    """Generate image using FAL AI (Free tier available)"""
    try:
        print("🎨 FAL: Generating image:", prompt)
        
        from config import FAL_KEY
        
        if not FAL_KEY:
            return None
            
        response = requests.post(
            "https://queue.fal.run/fal-ai/flux-pro",
            headers={"Authorization": f"Key {FAL_KEY}"},
            json={"prompt": prompt}
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            
            # Check if request is queued
            if "request_id" in data:
                request_id = data["request_id"]
                # Poll for result
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
                            image.name = "image.jpg"
                            image.seek(0)
                            return image
                    
                    import time
                    time.sleep(1)
            
            # Direct result
            if "image" in data:
                img_url = data["image"]["url"]
                img_response = requests.get(img_url)
                image = BytesIO(img_response.content)
                image.name = "image.jpg"
                image.seek(0)
                return image
                
    except Exception as e:
        print(f"❌ FAL Error: {e}")
    
    return None

def generate_image(prompt, use_fal=False):
    """Generate image using best available free service"""
    
    # Enhance prompt for better quality
    enhanced_prompt = enhance_prompt(prompt)
    print(f"📝 Enhanced prompt: {enhanced_prompt}")
    
    # Try FAL first if requested
    if use_fal:
        image = generate_image_fal(enhanced_prompt)
        if image:
            return image
    
    # Fallback to Cloudflare
    image = generate_image_cloudflare(enhanced_prompt)
    if image:
        return image
    
    # Try FAL as fallback
    if not use_fal:
        image = generate_image_fal(enhanced_prompt)
        if image:
            return image
    
    return None

def enhance_prompt(prompt):
    """Enhance prompt for better image generation"""
    
    quality_keywords = [
        "high quality, professional, detailed,",
        "masterpiece, 8k, sharp focus,",
        "cinematic lighting, beautiful composition,",
        "trending on artstation, award winning,"
    ]
    
    style_keywords = [
        "concept art",
        "digital painting",
        "illustration",
        "3D render",
        "photography"
    ]
    
    quality = random.choice(quality_keywords)
    style = random.choice(style_keywords)
    
    enhanced = f"{prompt}, {quality} {style}, aesthetic"
    return enhanced
