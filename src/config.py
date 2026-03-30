from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL : str
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRES : int
    REFRESH_TOKEN_EXPIRES : int
    
    REDIS_URL : str = "redis://localhost:7998/0"

    DOMAIN : str
    PORT : int

    MAIL_USERNAME : str
    MAIL_PASSWORD : str
    MAIL_FROM : str
    MAIL_PORT : int
    MAIL_SERVER : str
    MAIL_FROM_NAME : str
    MAIL_SSL_TLS : bool
    MAIL_STARTTLS : bool
    USE_CREDENTIALS : bool

    model_config = SettingsConfigDict(
        env_file='src/.env',
        extra="ignore"
    )

Config = Settings()

broker_url = Config.REDIS_URL
result_backend = Config.REDIS_URL