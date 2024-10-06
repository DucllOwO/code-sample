from pydantic_settings import BaseSettings


class Config(BaseSettings):
    DATABASE_URL_POSTGRES: str
    DATABASE_URL_MONGO: str

    BLOCKS_PER_TIME: int
    BLOCK_SLEEP_TIME: int
    RECORD_SLEEP_TIME: int
    RECORD_PER_TIME: int

    class Config:
        env_file = ".env"


settings = Config()
