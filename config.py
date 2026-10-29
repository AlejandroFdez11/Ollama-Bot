import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ["TELEGRAM_TOKEN"]
ALLOWED_USER_ID = int(os.environ["ALLOWED_USER_ID"])
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")