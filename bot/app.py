import discord

from config import Config as Config
from helpers.calendar import authenticate, create_event, delete_event, update_event

authenticate()

intents = discord.Intents.default()
intents.guild_scheduled_events = True

client = discord.Client(intents=intents)

async def send_notification(message:str):
    channel = await client.fetch_channel(Config.NOTIFICATION_CHANNEL)
    await channel.send(content=message)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(
        name='Events to update Google Calendar.',
        type=discord.ActivityType.watching,
        url='https://edinburghindiegamers.github.io/'
    ))

@client.event
async def on_scheduled_event_create(event):
    print(f'New event created: {event.name}. Populating Google Calendar.')

    if not event.end_time: event.end_time = event.start_time

    try:
        calendar_event = create_event(
            id=str(event.id),
            summary=event.name,
            location=event.location,
            description=event.description,
            start=event.start_time,
            end=event.end_time
        )

        await send_notification(f'Event `{event.name}` published to Google Calendar: {calendar_event.get('htmlLink')}')
    except Exception as error:
        await send_notification(f'Error when creating event: `{error}`.')

@client.event
async def on_scheduled_event_delete(event):
    print(f'Event deleted: {event.name}. Deleting from Google Calendar.')
    try:
        delete_event(id=str(event.id))
        await send_notification(f'Event `{event.name}` deleted from Google Calendar.')
    except Exception as error:
        await send_notification(f'Error when deleting event: `{error}`.')

@client.event
async def on_scheduled_event_update(before,after):
    print(f'Event updated: {after.name}. Updating Google Calendar.')
    try:
        if not after.end_time: after.end_time = after.start_time
        calendar_event = update_event(
            id=str(before.id),
            summary=after.name,
            location=after.location,
            description=after.description,
            start=after.start_time,
            end=after.end_time
        )
        await send_notification(f'Event `{calendar_event.get('summary')}` updated on Google Calendar.')
    except Exception as error:
        await send_notification(f'Error when updating event: `{error}`.')

if __name__ == '__main__': client.run(token=Config.BOT_TOKEN)