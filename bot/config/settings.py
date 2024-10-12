from pydantic_settings import BaseSettings, SettingsConfigDict

logo = """

"""


class BaseBotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="allow")

    API_ID: int
    API_HASH: str

    SLEEP_BETWEEN_START: list[int] = [10, 20]
    SESSION_AC_DELAY: int = 10
    ERRORS_BEFORE_STOP: int = 5
    USE_PROXY_FROM_FILE: bool = False
    ADD_LOCAL_MACHINE_AS_IP: bool = False

    RANDOM_SLEEP_TIME: int = 8

    BOT_SLEEP_TIME: list[int] = [30000, 35000]

    LOGIN_CACHE_TTL: int = 3600
    REF_ID: str = '1092379081'
    auth_header: str = 'Init-Data'
    base_url: str = 'https://tonclayton.fun'
    bot_name: str = 'claytoncoinbot'
    bot_app: str = 'game'


class Settings(BaseBotSettings):
    SEND_TAPS: bool = True
    EXECUTE_TASKS: bool = True
    EXECUTE_GAMES: bool = True
    GAME: list[str] = ['clay', 'game', 'stack']


config = Settings()
