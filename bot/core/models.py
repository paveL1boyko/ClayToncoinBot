from pydantic import BaseModel, Field


class SessionData(BaseModel):
    user_agent: str = Field(validation_alias="User-Agent")
    proxy: str | None = None


class Reward(BaseModel):
    day: int
    tokens: float
    game_tries: int
    is_channel_required: bool
    is_og_badge_required: bool


class DailyReward(BaseModel):
    can_claim_today: bool
    current_day: int
    is_subscribed: bool
    reward: Reward
    subscription_needed: bool


class User(BaseModel):
    id_telegram: int
    username: str
    first_name: str
    last_name: str
    is_premium: bool
    start_param: str
    language_code: str
    allows_to_write_pm: bool
    start_time: str  # Можно использовать datetime, если нужно
    active_farm: bool
    tokens: float
    referral_code: str
    can_claim: bool
    storage: int
    multiplier: int
    consecutive_days: int
    partner: int
    daily_attempts: int
    last_attempt_reset: str  # Можно использовать datetime, если нужно
    level: int
    current_xp: int
    wallet: str | None
    avatar: str
    invite_count: int
    has_og_pass: bool


class UserData(BaseModel):
    dailyReward: DailyReward
    isNew: bool
    user: User
