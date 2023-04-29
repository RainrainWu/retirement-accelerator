from sys import intern

from pydantic import BaseSettings, Field, PositiveInt, SecretStr, StrictStr
from retirement_accelerator.helper import Singleton


class ManagerConfig(BaseSettings, Singleton):
    class Config:
        env_file = ".env"

    EODHD_API_ENDPOINT: StrictStr = intern(
        "https://eodhistoricaldata.com/api/fundamentals"
    )
    EODHD_API_KEY: SecretStr = Field(env="EODHD_API_KEY")

    CACHED_FILE_TIMESTAMP_FORMAT: StrictStr = intern("%m/%d/%Y, %H:%M:%S")
    CACHED_FILE_EXPIRATION_HOURS: PositiveInt = Field(
        env="CACHED_FILE_EXPIRATION_HOURS", default=168
    )
