from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str
    MONGODB_URI: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
