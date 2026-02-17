from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.OPENAI_API_KEY: str | None = os.getenv("OPENAI_API_KEY")

        if not self.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY no está definido en el entorno")


settings = Settings()
