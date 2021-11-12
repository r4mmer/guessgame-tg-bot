from pydantic import BaseSettings


class Settings(BaseSettings):
    TOKEN: str
    PORT: int = 80

    MAX_VALUE: int = 100
    MAX_GUESSES: int = 2
    WEBHOOK_URL: str = None

    class Config:
        env_file = '.env'


settings = Settings()
