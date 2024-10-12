import asyncio
import random

import aiocache
from pyrogram import Client

from bot.config.headers import headers
from bot.config.logger import log
from bot.config.settings import config

from .api import CryptoBotApi
from .models import SessionData


class CryptoBot(CryptoBotApi):
    def __init__(self, tg_client: Client, additional_data: dict) -> None:
        super().__init__(tg_client)
        self.authorized = False
        self.sleep_time = config.BOT_SLEEP_TIME
        self.additional_data: SessionData = SessionData.model_validate(
            {k: v for d in additional_data for k, v in d.items()}
        )

    @aiocache.cached(ttl=config.LOGIN_CACHE_TTL)
    async def login_to_app(self, proxy: str | None) -> bool:
        tg_web_data = await self.get_tg_web_data(proxy=proxy)
        self.http_client.headers[config.auth_header] = tg_web_data
        self.user_data = await self.login()
        return True

    async def perform_game(self):
        while self.user_data.user.daily_attempts > 0:
            for game in config.GAME:
                await self.start_game(game)
                if 'clay' in game:
                    self.logger.info("Playing clay game sleep for 2 min before finish")
                    await asyncio.sleep(60 * 2)

                    await self.end_game(game, request_data={'score': random.randint(110, 130)})
                if 'stack' in game:
                    self.logger.info("Playing clay game sleep for 2 min before finish")
                    await asyncio.sleep(60 * 2)
                    await self.end_game(game, request_data={
                        {"score": random.randint(110, 130), "multiplier": random.randint(1, 3)}})
                if 'game' in game:
                    for i in range(1, 25):
                        await self.save_tile(request_data={"maxTile": 2 ** i})
                        await asyncio.sleep(random.randint(4, 6) + random.uniform(0, 1))
                    await self.game_over(request_data={"multiplier": random.randint(1, 4)})
                self.user_data.user.daily_attempts -= 1

    async def execute_tasks(self):
        pass

    async def run(self, proxy: str | None) -> None:
        async with await self.create_http_client(proxy=proxy, headers=headers):
            while True:
                if self.errors >= config.ERRORS_BEFORE_STOP:
                    self.logger.error("Bot stopped (too many errors)")
                    break
                try:
                    if await self.login_to_app(proxy):
                        self.super_task = await self.super_tasks()
                        self.partner_tasks =  await self.partner_tasks()

                    # if config.EXECUTE_TASKS:
                    #     await self.execute_tasks()
                    if config.EXECUTE_GAMES:
                        await self.perform_game()
                    sleep_time = random.randint(*config.BOT_SLEEP_TIME)
                    self.logger.info(f"🛌 Sleep time: {sleep_time // 60} minutes 🕒")
                    await asyncio.sleep(sleep_time)

                except RuntimeError as error:
                    raise error from error
                except Exception:
                    self.errors += 1
                    await self.login_to_app.cache.clear()
                    self.logger.exception("Unknown error")
                    await self.sleeper(additional_delay=self.errors * 8)


async def run_bot(tg_client: Client, proxy: str | None, additional_data: dict) -> None:
    try:
        await CryptoBot(tg_client=tg_client, additional_data=additional_data).run(proxy=proxy)
    except RuntimeError:
        log.bind(session_name=tg_client.name).exception("Session error")
