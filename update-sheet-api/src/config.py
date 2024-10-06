from typing import Any
from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from src.constants import Environment


class Config(BaseSettings):

    ENVIRONMENT: Environment = Environment.LOCAL
    DATABASE_URL: str
    # REDIS_URL: str
    SITE_DOMAIN: str = "myapp.com"

    APP_SCRIPTS: str
    APP_ID: str

    EDU_BACKEND_URL: str = ""

    # SENTRY_DSN: str | None

    APP_VERSION: str = "1"

    class Config:
        env_file: str = ".env"
        extra: str = "allow"


settings = Config()

app_configs: dict[str, Any] = {"title": "App API"}
# if settings.ENVIRONMENT.is_deployed:
#     app_configs["root_path"] = f"/v{settings.APP_VERSION}"

# if not settings.ENVIRONMENT.is_debug:
#     app_configs["openapi_url"] = "/v1/asset"  # hide docs
