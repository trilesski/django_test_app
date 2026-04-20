import environ
from dj_database_url import parse as db_url

class Env:
    def __init__(self, environment: str):
        self.env = environment.lower()
        self.is_prod = self.env.startswith('prod')
        self.is_stage = self.env.startswith('stage')
        self.is_dev = self.env == 'dev'
        self.is_test = self.env == 'test'

    def __str__(self):
        return self.env

    def __repr__(self):
        return self.env

@environ.config(prefix='')
class AppConfig:
    debug = environ.bool_var(default=False)
    env = environ.var(name='ENVIRONMENT', converter=Env)
    postgresql = environ.var(name='POSTGRESQL_URL', converter=lambda x: db_url(x))
    redis_url = environ.var(name='REDIS_CACHE_URL')

    django_print_sql = environ.bool_var(default=False)


conf = environ.to_config(AppConfig)
