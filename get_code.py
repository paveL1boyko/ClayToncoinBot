import asyncio

from pydantic_settings import BaseSettings, SettingsConfigDict
from pyrogram import Client


class BaseBotSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="allow")

    API_ID: int
    API_HASH: str


settings = BaseBotSettings()

app = Client("russ", api_id=settings.API_ID, api_hash=settings.API_HASH, workdir="sessions/")

target_first_name = "Telegram"


async def main():
    async with app:
        target_chat = None
        async for dialog in app.get_dialogs():
            if dialog.chat.first_name == target_first_name:
                target_chat = dialog.chat
                break

        if target_chat:
            async for i in app.get_chat_history(chat_id=target_chat.id, limit=1):
                print(f"Последнее сообщение в чате '{i.text}")
                break
        else:
            print(f"Чат с именем '{target_first_name}' не найден.")


asyncio.run(main())
