import os

class Settings:
    PROJECT_NAME: str = "ERP System"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:1234@localhost:5432/ERPDB",
    )
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://127.0.0.1:5173").rstrip("/")

settings = Settings()
