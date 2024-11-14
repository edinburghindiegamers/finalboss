from os import getenv

from dotenv import load_dotenv
load_dotenv('./.env')

class Config(object):
    BOT_TOKEN=getenv('BOT_TOKEN')
    GUILD_ID=getenv('GUILD_ID')
    NOTIFICATION_CHANNEL=getenv('NOTIFICATION_CHANNEL')