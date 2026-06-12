from os import environ


SESSION_CONFIGS = [
    dict(
        name='Pilot4UK',
        display_name="Pilot4UK",
        app_sequence=['Pilot4UK'],
        num_demo_participants=20,
    )
]


SESSION_CONFIG_DEFAULTS = dict(real_world_currency_per_point=1.00, participation_fee=0.00)
PARTICIPANT_FIELDS = ['task_rounds']
SESSION_FIELDS = []
LANGUAGE_CODE = 'en'
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True
ROOMS = []

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '3080418250966'

INSTALLED_APPS = ['otree']
