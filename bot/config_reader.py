from typing import Optional

from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    bot_token: SecretStr
    admin_chat_id: int
    remove_sent_confirmation: bool
    webhook_domain: Optional[str]
    webhook_path: Optional[str]
    app_host: Optional[str] = "0.0.0.0"
    app_port: Optional[int] = 9000
    custom_bot_api: Optional[str]

    class Config:
        env_prefix = ""
        case_sensitive = False


config = Settings()
