import discord
import os
import nacl
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
import music
# Discord is an asynchronous library -> things are done w/callbacks
# (Callback: a function that is called when something happens)
###############################################################################

cogs = [music]

# Connection to Discord
intents = discord.Intents.all()
client = commands.Bot(command_prefix='>', intents = intents)

async def main():
  async with client:
    for i in range(len(cogs)):
      await cogs[i].setup(client)
      await client.start(os.getenv('TOKEN'))
      
# Registering an event:
@client.event
async def on_ready():
    # On_ready event (Called when the bot is ready to be used):

    # Signifying the bot is ready
    print("{0.user} is now online!".format(client))
    return


# Play fanfare if a person that was not in any voice channel joins a vc
@client.event
async def on_voice_state_update(member, before, after):
    channel = after.channel  # Voice channel
    bot_connection = member.guild.voice_client  # Bot connection

    if not before.channel and channel:
        if not bot_connection:
            vc = await channel.connect()

        # CUE THE FANFARE~
        vc.play(discord.FFmpegOpusAudio('fanfare.mp3'))
        # Duration of the fanfare
        await asyncio.sleep(13)

        await member.guild.voice_client.disconnect()

    if not channel:
        if bot_connection:
            await member.guild.voice_client.disconnect()
        return

# General commands
@client.command()
async def hi(message):
    """Greetings."""
    await message.channel.send("HaIii~~")


@client.command()
async def hello(message):
    """Greetings."""
    await message.channel.send("HelL0!")


@commands.command()
async def morning(message):
    """Greetings."""
    await message.channel.send("Good Morning!")
    
load_dotenv()

asyncio.run(main())