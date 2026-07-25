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
    """Generate image using Replicate FLUX Schnell"""
    try:
        print("🚀 Replicate API: Generating image...", prompt[:50])

        if not REPLICATE_API_TOKEN:
            return None

        headers = {
            "Authorization": f"Token {REPLICATE_API_TOKEN}",
            "Content-Type": "application/json"
        }

        data = {
            "version": "c846a69991daf4c0e5d016514849d14ee5b2e6846ce6b9d6f21369e564cfe51e",
            "input": {
                "prompt": prompt,
                "go_fast": True,
                "num_outputs": 1,
                "aspect_ratio": "1:1",
                "output_format": "jpg",
                "output_quality": 90
            }
        }

        response = requests.post(
            "https://api.replicate.com/v1/predictions",
            headers=headers,
            json=data,
            timeout=120
        )

        result = response.json()

        if response.status_code != 201:
            print("❌ Replicate Start Error:", result)
            return None

        prediction_url = result["urls"]["get"]

        # انتظار تا آماده شدن عکس
        for _ in range(60):
            time.sleep(2)

            check = requests.get(
                prediction_url,
                headers=headers,
                timeout=30
            ).json()

            if check.get("status") == "succeeded":
                img_url = check["output"][0]

                img_response = requests.get(
                    img_url,
                    timeout=60
                )

                image = BytesIO(img_response.content)
                image.name = "image.jpg"
                image.seek(0)

                return image

            if check.get("status") == "failed":
                print("❌ Replicate Failed:", check)
                return None

        print("❌ Replicate Timeout")
        return None

    except Exception as e:
        print("❌ Replicate Error:", e)
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

def generate_image(prompt, style="realistic", size="1024x1024", engine="auto"):
    """Generate image using best available engine with fallback"""
    
    # Enhance prompt
    # Convert size to width/height
    if size == "512x512":
        width, height = 512, 512
    elif size == "768x768":
        width, height = 768, 768
    elif size == "1024x1024":
        width, height = 1024, 1024
    elif size == "1536x1536":
        width, height = 1536, 1536
    elif size == "2048x2048":
        width, height = 2048, 2048
    else:
        width, height = 1024, 1024

    enhanced_prompt = enhance_prompt(prompt)
    print(f"📝 Enhanced: {enhanced_prompt}")
    
    # Order of preference
    engines = [
    ("cloudflare", generate_image_cloudflare),
    ("deepai", generate_image_deepai),
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

