from asyncio import run
from datetime import datetime, timedelta
import json
import os

from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix

from config import Config as Config
from helpers.discord import DiscordEvents

os.makedirs(Config.CACHE_DIR, exist_ok=True)

discord_events = DiscordEvents(discord_token=Config.BOT_TOKEN)

app = Flask(__name__)
app.config.from_object(Config())
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto= 1, x_host= 1)
cors = CORS(app=app, resources={
    '/api/get_guild_events/': {
        'origins': Config.ORIGINS
    }
})

@app.route('/api/get_guild_events/')
def _get_guild_events():
    now = datetime.now()
    if os.path.isfile(Config.DISCORD_CACHE):
        with open(Config.DISCORD_CACHE,'r') as file:
            cache = json.loads(file.read())
            if datetime.fromisoformat(cache['timestamp']) > now - timedelta(hours=24):
                return jsonify(cache['data']), 200
    events = run(discord_events.list_guild_events(guild_id=Config.GUILD_ID))
    with open(Config.DISCORD_CACHE, 'w') as file:
        file.write(json.dumps({
            'timestamp': now.isoformat(),
            'data': events
        }))
    return jsonify(events), 200

@app.route('/api/receive/')
def _receive():
    pass

if __name__ == '__main__': app.run(debug=Config.DEBUG)