import os
from kombu import Queue

# TODO: depricated property
class BaseConfig:

    CELERY_BROKER_URL: str = os.environ.get(
        "CELERY_BROKER_URL", "redis://127.0.0.1:6379/0"
    )
    CELERY_RESULT_BACKEND: str = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0"
    )
    # CELERY_BEAT_SCHEDULE: dict = {
    #     # "task-schedule-work": {
    #     #     "task": "task_schedule_work",
    #     #     "schedule": 5.0,  # five seconds
    #     # }
    # }


class DevelopmentConfig(BaseConfig):

    POSTGRES_USER: str = os.environ.get(
        "POSTGRES_USER_DEV"
    )
    POSTGRES_PASSWORD: str = os.environ.get(
        "POSTGRES_PASSWORD_DEV"
    )
    DB_HOST: str = os.environ.get(
        "DB_HOST_DEV"
    )
    DB_PORT: str = os.environ.get(
        "DB_PORT_DEV"
    )
    POSTGRES_DB: str = os.environ.get(
        "POSTGRES_DB_DEV"
    )
    DATABASE_URL: str = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}'


class ProductionConfig(BaseConfig):
    POSTGRES_USER: str = os.environ.get(
        "POSTGRES_USER_PROD"
    )
    POSTGRES_PASSWORD: str = os.environ.get(
        "POSTGRES_PASSWORD_PROD"
    )
    DB_HOST: str = os.environ.get(
        "DB_HOST_PROD"
    )
    DB_PORT: str = os.environ.get(
        "DB_PORT_PROD"
    )
    POSTGRES_DB: str = os.environ.get(
        "POSTGRES_DB_PROD"
    )
    DATABASE_URL: str = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}'



class TestConfig(BaseConfig):
    DATABASE_URL: str = os.environ.get(
        "SQLITE_DATABASE_URL"
    )


def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "test": TestConfig,
    }

    config_name = os.environ.get("APP_CONFIG")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
