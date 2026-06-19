from dotenv import load_dotenv
import os

load_dotenv()

TRAKT_CLIENT_ID = os.getenv("TRAKT_CLIENT_ID")
TRAKT_CLIENT_SECRET = os.getenv("TRAKT_CLIENT_SECRET")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

OMDB_API_KEY = os.getenv("OMDB_API_KEY")