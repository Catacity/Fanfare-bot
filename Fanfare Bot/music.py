import discord
from discord.ext import commands
import youtube_dl

# Music bot commands: 
# Reference: https://www.youtube.com/watch?v=jHZlvRr9KxM&ab_channel=MaxCodez

class music(commands.Cog):
  def __init__(self,client):
    self.client = client
    
  @commands.command()
  async def play(self,ctx,url):
    # Person not in vc
    if ctx.author.voice is None:
      await ctx.send("BuT yOu ArE Not iN a vOiCE cHAnNeL!!!")
      return
  
    # Person in vc
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
      await ctx.voice_client.move_to(voice_channel)
  
    # await play_music(ctx,url)
    await play_music(ctx,url)
  
  @commands.command()
  async def disconnect(self,ctx):
    """Disconnects the bot from your channel."""
    await ctx.voice_client.disconnect()
    
  @commands.command()
  async def resume(self,ctx):
    """Resume song"""
    await ctx.voice_client.resume()
    await ctx.send("Resumed.")
    
  @commands.command()
  async def pause(self,ctx):
    """Pause song"""
    await ctx.voice_client.pause()
    await ctx.send("Paused.")


async def setup(client):
  await client.add_cog(music(client))

async def play_music(ctx,url):
  ctx.voice_client.stop()
  
  FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  YDL_OPTIONS = {'format': "bestaudio"}
  vc = ctx.voice_client

  # Creating a stream to play the audio, then stream it directly into the vc
  with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    info = ydl.extract_info(url, download = False)
    url2 = info['formats'][0]['url']
    source = await discord.FFmpegOpusAudio.from_probe(url2,**FFMPEG_OPTIONS)
    vc.play(source)