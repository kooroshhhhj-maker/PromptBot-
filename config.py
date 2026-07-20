import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
FAL_KEY = os.getenv("FAL_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")
CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
HF_API_TOKEN = os.getenv("HF_API_TOKEN")

MODEL = "tencent/hy3:free"

