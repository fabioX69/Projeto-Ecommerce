from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Projeto E-commerce"
    DB_URL: str = "mysql+mysqldb://root:root3333@localhost:3306/ecommerce"
    SECRET_KEY: str = "change_me_please_32_chars_min"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()
