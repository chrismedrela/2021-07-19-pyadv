from pydantic import BaseSettings


class Settings(BaseSettings):
    api_key: str

    class Config:
        secrets_dir = 'secrets/'  # use "/run/secrets" on docker

__settings = None

def get_settings() -> Settings:
    global __settings

    if __settings is None:
        __settings = Settings()

    return __settings
