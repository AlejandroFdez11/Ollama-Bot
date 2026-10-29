import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ["TELEGRAM_TOKEN"]
ALLOWED_USER_ID = int(os.environ["ALLOWED_USER_ID"])
API_KEY = os.environ["API_KEY"]
API_URL = os.getenv("API_URL", "https://api.groq.com/openai/v1/chat/completions")
MODEL = os.getenv("MODEL", "llama-3.3-70b-versatile")