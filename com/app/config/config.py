import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)

            # Groq LLM
            cls._instance.GROQ_API_KEY = os.getenv("GROQ_API_KEY")
            cls._instance.GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

            # PostgreSQL
            cls._instance.DB_HOST = os.getenv("DB_HOST", "localhost")
            cls._instance.DB_PORT = os.getenv("DB_PORT", "5432")
            cls._instance.DB_NAME = os.getenv("DB_NAME", "stayease")
            cls._instance.DB_USER = os.getenv("DB_USER", "postgres")
            cls._instance.DB_PASSWORD = os.getenv("DB_PASSWORD", "")
            cls._instance.DATABASE_URL = (
                f"postgresql://{cls._instance.DB_USER}:"
                f"{cls._instance.DB_PASSWORD}@"
                f"{cls._instance.DB_HOST}:"
                f"{cls._instance.DB_PORT}/"
                f"{cls._instance.DB_NAME}"
            )

            # App
            cls._instance.APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
            cls._instance.APP_PORT = int(os.getenv("APP_PORT", "8000"))
            cls._instance.DEBUG = os.getenv("DEBUG", "false").lower() == "true"

        return cls._instance