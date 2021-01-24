from Cogs.iCast import iCast
from Cogs.Cog21 import Cog21
from discord.ext import commands
from Data_Handlers import image_handler

image_handler.img_json_delete()

# TODO: Create a Bot manager that adds cogs per Cog class
bot = commands.Bot(command_prefix='$')
bot.add_cog(iCast(bot))
#bot.add_cog(Cog21(bot))

bot.run('Add Bot Token Here')