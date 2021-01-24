import discord
from discord.ext import commands


class iCast(commands.Cog):
    client = discord.Client()

    voice_chan = None
    active_vc = None

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(pass_context=True)
    async def join(self, ctx):
        channel = ctx.author.voice.channel
        if channel:
            self.voice_chan = channel
            self.active_vc = await channel.connect()

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, arg):
        if self.active_vc:
            try:
                #TODO: add youtube binary stream for music
                await self.active_vc.play(discord.FFmpegPCMAudio(arg))
                # discord.FFmpegOpusAudio(arg)
            except discord.DiscordException as ex:
                await ctx.send(str(ex))
            #voice.play(discord.FFmpegPCMAudio(url), after=my_after)

