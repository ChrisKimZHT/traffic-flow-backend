from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    bind_host: str = "0.0.0.0"
    bind_port: int = 8000

    database_user: str
    database_password: str
    database_host: str = "localhost"
    database_port: int = 3306
    database_name: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Config()
