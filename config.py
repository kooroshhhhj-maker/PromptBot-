import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# AI Models
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "meta-llama/llama-3-8b-instruct:free"

# Image Generation APIs
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
FAL_KEY = os.getenv("FAL_KEY")

# Image Generation - Hugging Face
HUGGING_FACE_API_KEY = os.getenv("HUGGING_FACE_API_KEY")

# Image Generation - DeepAI
DEEPAI_API_KEY = os.getenv("DEEPAI_API_KEY")

# Image Generation - Replicate
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

# Image Generation - Leonardo AI
LEONARDO_API_KEY = os.getenv("LEONARDO_API_KEY")

# Image Generation - Ideogram
IDEOGRAM_API_KEY = os.getenv("IDEOGRAM_API_KEY")

# Image Analysis - Google Vision
GOOGLE_VISION_API_KEY = os.getenv("GOOGLE_VISION_API_KEY")
GOOGLE_PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")

# Image Analysis - Clarifai
CLARIFAI_API_KEY = os.getenv("CLARIFAI_API_KEY")

# AWS Rekognition (optional)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Azure Computer Vision (optional)
AZURE_VISION_KEY = os.getenv("AZURE_VISION_KEY")
AZURE_VISION_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")

# Vision Models
HF_TOKEN = os.getenv("HF_TOKEN")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
