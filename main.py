import discord
import discord.ext
import asyncio
from Blackjack import blackJack
from discord.ext import commands

client = discord.Client()
player_names = []

bot = commands.Bot(command_prefix='$')
test = commands.Cog(command_prefix='.')


@bot.command()
async def test(ctx, arg):
    await ctx.send('You passed {}.' .format(arg))

@bot.command()
async def blackJack(ctx, arg):
    if arg == "":
        await ctx.send("Please enter $blackJack [your name]")
    elif len(player_names) == 0 and arg != "begin_game":
        player_names.append("House")
        player_names.append(str(arg))
        await ctx.send("Added player {}" .format(arg))
    elif arg == "begin_game":
        game = await blackJack(player_names)
        await game.draw_cards()
        #await game.draw_cards()
        #player_string = "test"
        #for n in game.players:
          #  player_string = player_string + n.player_name + " has value " + n.points + "\n"
       # with open('my_image.png', 'rb') as f:
        #await ctx.send(file=discord.File(.png'))
        await ctx.send("Please enter $blackJack [your name]")
    else:
        player_names.append(str(arg))
        await ctx.send("Added player {}".format(arg))

@test.Cog.listener()
async def blackJack(ctx, arg):
    if arg == "":
        await ctx.send("Please enter $blackJack [your name]")
    elif len(player_names) == 0 and arg != "begin_game":
        player_names.append("House")
        player_names.append(str(arg))
        await ctx.send("Added player {}".format(arg))
    elif arg == "begin_game":
        game = await blackJack(player_names)
        await game.draw_cards()
        # await game.draw_cards()
        # player_string = "test"
        # for n in game.players:
        #  player_string = player_string + n.player_name + " has value " + n.points + "\n"
        # with open('my_image.png', 'rb') as f:
        # await ctx.send(file=discord.File(.png'))
        await ctx.send("Please enter $blackJack [your name]")
    else:
        player_names.append(str(arg))
        await ctx.send("Added player {}".format(arg))


bot.run('NzUwMTU1MzA3Njk0Njg2MzE5.X02akg.0qfk0SeyOLTAuzckSymZGIvkq0s')