import os
from dotenv import load_dotenv
load_dotenv('.env')

class Config(object):
    """Basic app config"""
    APP_HOST = '0.0.0.0'
    CACHE_DIR = './.cache/'
    DISCORD_CACHE = f'{CACHE_DIR}discord.json'
    DEBUG = False
    TESTING = False
    SERVER_NAME = os.getenv('SERVER_NAME')
    GUILD_ID = os.getenv('GUILD_ID')
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    ORIGINS = ['https://edinburghindiegamers.com', 'https://edinburghindiegamers.github.io']

class Development(Config):
    SERVER_NAME = None
    DEBUG = True
    TESTING = True
    ORIGINS = ['http://127.0.0.1:8000']