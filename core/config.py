# -*- coding: utf-8 -*-
import os

from pydantic_settings import BaseSettings


class Config(BaseSettings):
    ENV: str = "local"
    DEBUG: bool = True
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    WRITER_DB_URL: str = "postgresql+asyncpg://tesfa:admin@localhost/taskdb"
    READER_DB_URL: str = "postgresql+asyncpg://tesfa:admin@localhost/taskdb"
    JWT_SECRET_KEY: str = "fastapi"
    JWT_ALGORITHM: str = "HS256"
    CELERY_BROKER_URL: str = "amqp://user:bitnami@localhost:5672/"
    CELERY_BACKEND_URL: str = "redis://:password123@localhost:6379/0"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379


class DevelopmentConfig(Config):
    WRITER_DB_URL: str = "postgresql+asyncpg://tesfa:admin@db:5432/taskdb"
    READER_DB_URL: str = "postgresql+asyncpg://tesfa:admin@db:5432/taskdb"
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379


class LocalConfig(Config):
    WRITER_DB_URL: str = "postgresql+asyncpg://tesfa:admin@localhost/taskdb"
    READER_DB_URL: str = "postgresql+asyncpg://tesfa:admin@localhost/taskdb"


class ProductionConfig(Config):
    DEBUG: bool = False
    WRITER_DB_URL: str = "postgresql+asyncpg://tesfa:admin@db:5432/taskdb"
    READER_DB_URL: str = "postgresql+asyncpg://tesfa:admin@db:5432/taskdb"


def get_config():
    env = os.getenv("ENV", "local")
    config_type = {
        "dev": DevelopmentConfig(),
        "local": LocalConfig(),
        "prod": ProductionConfig(),
    }
    return config_type[env]


config: Config = get_config()
