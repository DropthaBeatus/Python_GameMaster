from Bot21 import Bot21
from iCast import iCast
from discord.ext import commands
import image_handler

image_handler.img_json_delete()

# TODO: Create a Bot manager that adds cogs per Cog class
bot = commands.Bot(command_prefix='$')
bot.add_cog(iCast(bot))
#bot.add_cog(Bot21(bot))

bot.run('Add Bot Here')