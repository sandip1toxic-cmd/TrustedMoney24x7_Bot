from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    OWNER_ID: int

    CHANNEL_USERNAME: str = "@Trusted_Money_India"
    CHANNEL_ID: str = ""

    SUPPORT_USERNAME: str = "@TM_24x7_SERVICE"

    DATABASE_URL: str = "sqlite+aiosqlite:///trusted_money.db"

    REQUIRE_CHANNEL_JOIN: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
