import discord.ext
import image_handler
from discord.ext import commands
from Blackjack import blackJack



class Bot21(commands.Cog):
    client = discord.Client()


    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.game = None
        self.player_names = []

    @commands.command()
    async def play21(self, ctx, arg=""):
        member = ctx.author
        player_names = []
        print(arg)
        if self.game is None and len(player_names) < 1 and arg == "":
            self.player_names.append("House")
            self.player_names.append(member)
            await ctx.send("Okay... starting a good ol' game of Black Jack")
        elif arg == "join" and len(self.player_names) <= 5:
            self.player_names.append(member)
        elif arg == "showhand":
            player = self.find_player(str(member))
            if player is not None:
                await self.print_hand(player)
        elif arg == "start" and len(self.player_names) >= 2:
            self.add_game("play_blackjack")
            self.game.draw_cards()
            for player in self.game.players:
                await self.send_images(player)
        elif arg == "up_ace":
            player = self.find_player(str(member))
            if player is not None and player.switch_ace_up() == True:
                await self.print_hand(player)
            elif player is not None and player.switch_ace_up() == False:
                self.warn_msg("You do not have any Aces")
        elif arg == "up_down":
            player = self.find_player(str(member))
            if player is not None and player.switch_ace_down()==True:
                await self.print_hand(player)
            elif player is not None and player.switch_ace_down()==False:
                self.warn_msg("You do not have any Aces")
        elif arg == "hit":
            #TODO: have enum for each player being ready
            #TODO: this is bad fix this later
            player = self.find_player(str(member))
            if player is not None and len(player.hand) < 5:
                self.game.draw_card(player.name)
                await self.print_hand(player)
        elif arg == "compare":
            ctx.send(self.game.compare_cards())

    def add_game(self, game):
        if game == "play_blackjack":
            self.game = blackJack(self.player_names)

    async def print_hand(self, player):
        await player.name_client.send(player.return_count())
        await player.name_client.send(file=player.discord_img)

    async def send_images(self, player):
        if player.name != "House":
            await self.print_hand(player)

    def find_player(self, name):
        found = ""
        for player in self.game.players:
            if player.name == name:
                found = player
        return found

    async def warn_msg(self, player, warn):
        await player.name_client.send(warn)

bot = commands.Bot(command_prefix='$')
bot.add_cog(Bot21(bot))

bot.run('NzUwMTU1MzA3Njk0Njg2MzE5.X02akg.0qfk0SeyOLTAuzckSymZGIvkq0s')


