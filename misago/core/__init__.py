from django.conf import settings
from django.core.checks import register, Critical

SUPPORTED_ENGINES = [
    'django.db.backends.postgresql',
    'django.db.backends.postgresql_psycopg2',
    'django.db.backends.mysql',
]


@register()
def check_db_engine(app_configs, **kwargs):
    errors = []

    try:
        if settings.DATABASES['default']['ENGINE'] not in SUPPORTED_ENGINES:
            raise ValueError()
    except (AttributeError, KeyError, ValueError):
        errors.append(Critical(
            msg='Misago requires PostgreSQL or MySQL database.',
            id='misago.001',
        ))

    return errors


default_app_config = 'misago.core.apps.MisagoCoreConfig'
