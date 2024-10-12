import json

from aiocache import Cache, cached
from pyrogram import Client

from bot.helper.decorators import error_handler, handle_request

from .base_api import BaseBotApi
from .models import UserData
from ..config.settings import config


class CryptoBotApi(BaseBotApi):
    def __init__(self, tg_client: Client):
        super().__init__(tg_client)

    @cached(ttl=config.LOGIN_CACHE_TTL, cache=Cache.MEMORY)
    @error_handler()
    @handle_request('/api/user/auth')
    async def login(self, *, response_json: dict) -> UserData:
        return UserData(**response_json)

    @error_handler()
    @handle_request('/api/tasks/super-tasks', method="GET")
    async def super_tasks(self, *, response_json: dict) -> dict:
        return response_json

    @error_handler()
    @handle_request('/api/tasks/partner-tasks', method="GET")
    async def partner_tasks(self, *, response_json: dict) -> dict:
        return response_json

    @error_handler()
    @handle_request('/a')
    async def daily_claim(self, *, response_json: dict) -> dict:
        return response_json

    @error_handler()
    @handle_request('/api/game/save-tile')
    async def save_tile(self, *, response_json: dict, request_data: dict) -> dict:
        return response_json

    @error_handler()
    async def start_game(self, game_name: str) -> dict:
        request = await self.http_client.post(config.base_url + f"/api/{game_name}/start-game", json={})
        return await request.json()

    @error_handler()
    @handle_request('/api/game/over')
    async def game_over(self, *, response_json: dict, request_data: dict) -> dict:
        return response_json

    @error_handler()
    async def update_game(self, *, response_json: dict) -> dict:
        return response_json

    @error_handler()
    async def end_game(self, game_name: str, request_data: dict) -> dict:
        request = await self.http_client.post(config.base_url + f"/api/{game_name}/end-game", json=request_data)
        return await request.json()

    @cached(ttl=2 * 60 * 60, cache=Cache.MEMORY)
    @error_handler()
    @handle_request(
        "https://raw.githubusercontent.com/testingstrategy/musk_daily/main/daily.json",
        method="GET",
        full_url=True,
    )
    async def get_helper(self, *, response_json: str) -> dict:
        return json.loads(response_json)
