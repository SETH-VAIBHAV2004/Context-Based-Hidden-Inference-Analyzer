from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    api_host: str = "127.0.0.1"
    api_port: int = 8000
    api_cors_origins: str = "http://localhost:3000"
    log_conversation_text: bool = False
    request_body_limit_bytes: int = 65536
    circa_path: str = ""
    dataset_cache_dir: str = "data/cache"

    @property
    def cors_origin_list(self) -> list[str]:
        return [item.strip() for item in self.api_cors_origins.split(",") if item.strip()]


def get_settings() -> Settings:
    return Settings()
