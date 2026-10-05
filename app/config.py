from pydantic_settings import BaseSettings


class Settings(BaseSettings):
  """應用程式設定與環境變數管理"""

  LINE_CHANNEL_SECRET: str = ""
  LINE_CHANNEL_ACCESS_TOKEN: str = ""
  GEMINI_API_KEY: str = ""
  PORT: int = 8000
  HOST: str = "0.0.0.0"

  class Config:
    env_file = ".env"
    env_file_encoding = "utf-8"
    extra = "ignore"


settings = Settings()
