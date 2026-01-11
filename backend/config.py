import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = os.getenv("OPENROUTER_API_URL", "UNUSED")

COUNCIL_MODELS = [
    "member1",
    "member2",
    "member3",
]

CHAIRMAN_MODEL = "chairman"

MODEL_ENDPOINTS = {
    "member1": {
        "url": "http://localhost:8002",
    },
    "member2": {
        "url": "http://localhost:8003",
    },
    "member3": {
        "url": "http://localhost:8004",
    },
    "chairman": {
        "url": "http://localhost:8005",
    },
}

DATA_DIR = "data/conversations"
