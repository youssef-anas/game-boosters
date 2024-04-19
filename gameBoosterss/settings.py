from dotenv import load_dotenv
import os
from pathlib import Path
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = os.getenv('DJANGO_DEBUG', 'False').lower() == 'true'
DEBUG = True

AUTH_USER_MODEL = 'accounts.BaseUser'
# CSRF_COOKIE_SECURE = False

ASGI_APPLICATION = 'gameBoosterss.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("localhost", 6379)],
#         },
#     },
# }

# Application definition
INSTALLED_APPS = [
    'daphne',
    'channels',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    
    # My Apps
    'booster.apps.BoosterConfig',
    'customer.apps.CustomerConfig',
    'dashboard.apps.DashboardConfig',
    'wildRift.apps.WildriftConfig',
    'valorant.apps.ValorantConfig',
    'pubg.apps.PubgConfig',
    'tft.apps.TftConfig',
    'hearthstone.apps.HearthstoneConfig',
    'WorldOfWarcraft.apps.WorldofwarcraftConfig',
    'leagueOfLegends.apps.LeagueoflegendsConfig',
    'rocketLeague.apps.RocketleagueConfig',
    'django_cleanup.apps.CleanupConfig',
    'accounts.apps.AccountsConfig',
    'mobileLegends.apps.MobilelegendsConfig',
    'honorOfKings.apps.HonorofkingsConfig',
    'dota2.apps.Dota2Config',
    'overwatch2.apps.Overwatch2Config',
    'csgo2.apps.Csgo2Config',
    'chat.apps.ChatConfig',
    
    # Games
    'games.apps.GamesConfig',

    # Others
    'paypal.standard.ipn',
    'corsheaders',
    'rest_framework',
    # 'django_q',
    # 'modeltranslation',
    # 'oauth2_provider',

    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.facebook',

    'social_django', 
    # 'django.contrib.sites',
    'whitenoise.runserver_nostatic'

]

SITE_ID = 1

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'gameBoosterss.middleware.ImageSizeLimitMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'gameBoosterss.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/"templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
            ],
        },
    },
]

WSGI_APPLICATION = 'gameBoosterss.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv('NAME'),
        "USER": os.getenv('USER'),
        "PASSWORD": os.getenv('PASSWORD'),
        "HOST": os.getenv('HOST'),
        "PORT": "5432",
    }
}



# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Directory where static files will be collected during deployment
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# STORAGES = {
#     'default': {
#         'BACKEND': "whitenoise.storage.CompressedManifestStaticFilesStorage",
#         # 'OPTIONS': {
#         #     'location': '/path/to/your/static/files',
#         # },
#     },
# }

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# MEDIA_URL = "media/"
MEDIA_URL = "https://storage.googleapis.com/mad-boost.appspot.com/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


# to send email via gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587  # For TLS
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'madboost.customer@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'wpmj llfn toax sfil'


# EMAIL_USE_SSL = False
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

AUTH_USER_MODEL = 'accounts.BaseUser'

ALLOWED_HOSTS = [
    '*'
    'https://www.madboost.gg',
    'localhost',
    '127.0.0.1',
    'www.madboost.gg',
    'madboost.gg',
    'gameboost-test-f25426e2eac4.herokuapp.com',
    'www.gameboost-test-f25426e2eac4.herokuapp.com'
    ]


PAYPAL_EMAIL='sb-blcbf28542348@business.example.com'
# PAYPAL_EMAIL='madboost.payment@gmail.com'
PAYPAL_TEST = True
PAYPAL_VERIFY_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
# SECURE_SSL_REDIRECT = True



Q_CLUSTER = {
    'name': 'gameBoosterss',
    'workers': 10,
    'recycle': 500,
    'timeout': 1960,
    'retry': 2000,
    'queue_limit': 50,
    'bulk': 10,
    'orm': 'default',
    'sync': False,
    'cleanup': 500, 
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#         'level': 'DEBUG',  # Set to 'DEBUG' for more detailed logs
#     },
#     'loggers': {
#         'django_q': {
#             'handlers': ['console'],
#             'level': 'DEBUG',  # Set to 'DEBUG' for more detailed logs
#             'propagate': True,
#         },
#     },
# }

OAUTH2_PROVIDER = {
    'SCOPES': {'read', 'write'},
    'CLIENT_ID': 'your-client-id',
    'CLIENT_SECRET': 'your-client-secret',
    'OAUTH2_SERVER_CLASS': 'oauth2_provider.oauth2.Server',
    'ALLOWED_REDIRECT_URI_SCHEMES': ['http', 'https'],
}


AUTHENTICATION_BACKENDS = [
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend',
    'accounts.backends.EmailOrUsernameModelBackend',
]

LOGIN_REDIRECT_URL = '/'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': '563095491808-r4dh48ijatksm45ndj2fphphesi2ppik.apps.googleusercontent.com',
            'secret': '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',
        }
    },
    'facebook': {
        'APP': {
            'client_id': '395531559777062',
            'secret': 'c20a1e8d9e7ecc668111c23da1528dee',
        }
    }
    
    #  'facebook': {
    #     'METHOD': 'oauth2',
    #     'SCOPE': ['email', 'public_profile', 'user_friends'],
    #     'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
    #     'INIT_PARAMS': {'cookie': True},
    #     'FIELDS': [
    #         'id',
    #         'email',
    #         'name',
    #         'first_name',
    #         'last_name',
    #         'verified',
    #         'locale',
    #         'timezone',
    #         'link',
    #         'gender',
    #         'updated_time',
    #     ],
    #     'EXCHANGE_TOKEN': True,
    #     'LOCALE_FUNC': lambda request: 'en_US',
    #     'VERIFIED_EMAIL': False,
    #     'VERSION': 'v12.0',
    #     'APP': {
    #         'client_id': '395531559777062',
    #         'secret': 'c20a1e8d9e7ecc668111c23da1528dee',
    #     }
    # }
}

import firebase_admin
from firebase_admin import credentials

# Initialize Firebase Admin SDK
cred = credentials.Certificate(os.path.join(BASE_DIR, 'fire-base.json'))
FIREBASE_STORAGE_BUCKET = "mad-boost.appspot.com"
firebase_admin.initialize_app(cred, {'storageBucket': FIREBASE_STORAGE_BUCKET})

# # Media files settings
# MEDIA_URL = 'media/'

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# DEFAULT_FILE_STORAGE = 'path.to.firebase.FirebaseStorage'
# DEFAULT_FILE_STORAGE = 'gameBoosterss.storage_backends.FirebaseStorage' 

# AUTHENTICATION_BACKENDS = [
#     'social_core.backends.facebook.FacebookOAuth2',
#     'django.contrib.auth.backends.ModelBackend',
# ]

# LOGIN_URL = 'account.login'
# LOGIN_REDIRECT_URL = "homepage.index"
# LOGOUT_URL = 'account.logout'
# LOGOUT_REDIRECT_URL = '/accounts/login/'
SOCIAL_AUTH_FACEBOOK_KEY = "395531559777062"
SOCIAL_AUTH_FACEBOOK_SECRET = "c20a1e8d9e7ecc668111c23da1528dee"
#for extra info
SOCIAL_AUTH_FACEBOOK_SCOPE = [
    'email',
]

# TODO remove comment after add ssl to site
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '563095491808-r4dh48ijatksm45ndj2fphphesi2ppik.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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',
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'profile',
    'email',
]