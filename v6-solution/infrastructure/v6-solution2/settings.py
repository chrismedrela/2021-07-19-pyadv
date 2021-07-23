from pydantic import BaseSettings


class Settings(BaseSettings):
    api_key: str

    class Config:
        secrets_dir = 'secrets/'  # use "/run/secrets" on docker

    # @classmethod
    # def getInstance(cls):
    #     if not hasattr(cls, 'settings'):
    #         cls.settings = Settings()
    #     return cls.settings

__settings = None

def get_settings() -> Settings:
    global __settings

    if __settings is None:
        __settings = Settings()

    return __settings
