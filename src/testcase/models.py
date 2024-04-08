from typing import List, Optional

from pydantic import Field

from pydantic_settings import BaseSettings


class DjangoSettings(BaseSettings, env_prefix='django_'):
    debug: bool = Field(default=False)
    secret_key: str = Field(default='UNSECURE')
    allowed_hosts: List[str] = Field(default=['127.0.0.1'])


class DatabaseSettings(BaseSettings, env_prefix='database_'):
    engine: str = Field(default='sqlite')
    name: str = Field(default='db.sqlite3')
    host: Optional[str] = Field(default=None)
    port: Optional[int] = Field(default=None)
    user: Optional[str] = Field(default=None)
    user_password: Optional[str] = Field(default=None)


class RedisSettings(BaseSettings, env_prefix='redis_'):
    host: str = Field(default='localhost')
    port: int = Field(default=6379)


class AppSettings(BaseSettings):
    django: DjangoSettings = DjangoSettings()
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
