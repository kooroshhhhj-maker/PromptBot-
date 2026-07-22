from io import BytesIO
import requests
import base64
import random
import time

from database import get_image_settings
from config import (
    CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID,
    HUGGING_FACE_API_KEY, DEEPAI_API_KEY, REPLICATE_API_TOKEN
)

# Hugging Face Models
HF_TEXT_TO_IMAGE_MODEL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2"
HF_SDXL_MODEL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl"

def generate_image_replicate(prompt):
    """Generate image using Replicate (Best Quality)"""
    try:
        print("🚀 Replicate: Generating image...", prompt[:50])
        
        if not REPLICATE_API_TOKEN:
            return None
        
        # Use Stable Diffusion 3 on Replicate
        import replicate

        output = replicate.run(
    "stability-ai/stable-diffusion-3:09faf2d46bbd2e38495dbe49b2d1fb65b11a42b88c924bfe47f47e4450849266",
    input={
        "prompt": f"{prompt}, style: realistic",
        "num_outputs": 1,
        "height": 1024,
        "width": 1024,
        "num_inference_steps": 50
    }
)
        
        if output and len(output) > 0:
            img_url = output[0]
            img_response = requests.get(img_url, timeout=30)
            image = BytesIO(img_response.content)
            image.name = "image.jpg"
            image.seek(0)
            return image
            
    except Exception as e:
        print(f"❌ Replicate Error: {e}")
    
    return None

def generate_image_deepai(prompt):
    """Generate image using DeepAI"""
    try:
        print("🎨 DeepAI: Generating image...", prompt[:50])
        
        if not DEEPAI_API_KEY:
            return None
        
        response = requests.post(
            "https://api.deepai.org/api/text2img",
            data={
                'text': prompt,
                'grid_size': 1,
                'num_inference_steps': 50
            },
            headers={
                'api-key': DEEPAI_API_KEY
            },
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            if 'output_url' in data:
                img_response = requests.get(data['output_url'], timeout=30)
                image = BytesIO(img_response.content)
                image.name = "image.jpg"
                image.seek(0)
                return image
        else:
            print(f"❌ DeepAI Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ DeepAI Error: {e}")
    
    return None

def generate_image_huggingface(prompt):
    """Generate image using Hugging Face"""
    try:
        print("🤗 Hugging Face: Generating image...", prompt[:50])
        
        if not HUGGING_FACE_API_KEY:
            return None
        
        headers = {"Authorization": f"Bearer {HUGGING_FACE_API_KEY}"}
        
        # Try SDXL first (better quality)
        payload = {
            "inputs": prompt,
            "parameters": {
                "num_inference_steps": 50,
                "guidance_scale": 7.5
            }
        }
        
        response = requests.post(
            HF_SDXL_MODEL,
            headers=headers,
            json=payload,
            timeout=120
        )
        
        if response.status_code == 200:
            image = BytesIO(response.content)
            image.name = "image.jpg"
            image.seek(0)
            return image
        else:
            # Fallback to Stable Diffusion 2
            response = requests.post(
                HF_TEXT_TO_IMAGE_MODEL,
                headers=headers,
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                image = BytesIO(response.content)
                image.name = "image.jpg"
                image.seek(0)
                return image
        
        print(f"❌ Hugging Face Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Hugging Face Error: {e}")
    
    return None

def generate_image_cloudflare(prompt):
    """Generate image using Cloudflare (Free tier)"""
    try:
        print("☁️ Cloudflare: Generating image...", prompt[:50])
        
        if not CLOUDFLARE_API_TOKEN or not CLOUDFLARE_ACCOUNT_ID:
            return None
        
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

def enhance_prompt(prompt):
    """Enhance prompt for better results"""
    
    quality_keywords = [
        "high quality, professional, detailed,",
        "masterpiece, 8k, sharp focus,",
        "cinematic lighting, beautiful composition,",
        "trending on artstation, award winning,",
        "ultra detailed, intricate, amazing,"
    ]
    
    style_keywords = [
        "concept art",
        "digital painting",
        "illustration",
        "3D render",
        "photography",
        "oil painting",
        "watercolor"
    ]
    
    quality = random.choice(quality_keywords)
    style = random.choice(style_keywords)
    
    enhanced = f"{prompt}, {quality} {style}, aesthetic, beautiful"
    return enhanced

def generate_image(prompt, engine="auto"):
    """Generate image using best available engine with fallback"""
    
    # Enhance prompt
    enhanced_prompt = enhance_prompt(prompt)
    print(f"📝 Enhanced: {enhanced_prompt}")
    
    # Order of preference
    engines = [
        ("replicate", generate_image_replicate),
        ("deepai", generate_image_deepai),
        ("huggingface", generate_image_huggingface),
        ("cloudflare", generate_image_cloudflare),
    ]
    
    if engine != "auto":
        for name, func in engines:
            if name == engine:
                result = func(enhanced_prompt)
                if result:
                    return result
    
    # Try all engines in order
    for name, func in engines:
        print(f"\n🔄 Trying {name}...")
        result = func(enhanced_prompt)
        if result:
            print(f"✅ Success with {name}!")
            return result
        time.sleep(1)  # Delay between attempts
    
    print("❌ All engines failed!")
    return None
