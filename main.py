from iCast import Bot21
from discord.ext import commands
import image_handler

image_handler.img_json_delete()

bot = commands.Bot(command_prefix='$')
bot.add_cog(Bot21(bot))

bot.run('Bot Token Goes Here')