from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_NAME: str
    SECRET_KEY: str
    JWT_ALGORITHM: str
    CHECK_INTERVAL_MINUTES: int = 30

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"

    class Config:
        env_file = ".env"

settings = Settings()