from os import getenv

env_broker = getenv(
    "REDIS_URL",
    default="redis://redis:6379/0",
)

CELERY_BROKER_URL = env_broker
CELERY_ACCEPT_CONTENT = ['application/json']
# CELERY_RESULT_BACKEND = env_broker
CELERY_RESULT_BACKEND = 'test-db'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
