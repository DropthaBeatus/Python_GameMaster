import discord.ext
from discord.ext import commands
from Blackjack import blackJack


#TODO: add JSON information for commands and explanation for rules
class Bot21(commands.Cog):
    client = discord.Client()

    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        self.game = None
        self.player_names = []
        self.started = False

    @commands.command()
    async def play21(self, ctx, arg=""):
        # TODO: if play21 is started twice will need to to wipe of previous game
        member = ctx.author
        player_names = []

        if self.game is None and len(player_names) < 1 and arg == "":
            self.player_names.append("House")
            self.player_names.append(member)
            await ctx.send("Okay... starting a good ol' game of Black Jack")

        elif arg == "start" and len(self.player_names) >= 2:
            print("test")
            self.game = blackJack(self.player_names)
            self.game.draw_cards()
            self.started = True
            for player in self.game.players:
                print(player.name)
                await self.send_images(player)
            await self.print_table(ctx)

        elif arg == "join" and len(self.player_names) <= 5:
            self.player_names.append(member)
            ctx.send("Adding Player... {}", member)

        elif arg == "show_hand":
            player = self.find_player(str(member))
            if player is not None:
                await self.print_hand(player)

        elif arg == "ace_up":
            for player in self.game.players:
                if player.name == str(member):
                    switched = player.switch_ace_up()
                    if switched:
                        await self.print_hand(player)
                    else:
                        await self.warn_msg(player, "You do not have any Aces")

        elif arg == "ace_down":
            for player in self.game.players:
                if player.name == str(member):
                    switched = player.switch_ace_down()
                    if switched:
                        await self.print_hand(player)
                    else:
                        await self.warn_msg(player, "You do not have any Aces")

        elif arg == "hit":
            # TODO: have enum for each player being ready
            # TODO: this is bad fix this later
            player = self.find_player(str(member))
            if player is not None and len(player.hand) < 5:
                self.game.draw_card(player.name)
                await self.print_hand(player)

        elif arg == "compare":
            await ctx.send(self.game.compare_cards())
            self.game.draw_cards()
            for player in self.game.players:
                await self.send_images(player)
            await self.print_table(ctx)


    @staticmethod
    async def print_hand(player):
        await player.name_client.send(player.return_count())
        await player.name_client.send(file=discord.File(player.file_name))

    async def send_images(self, player):
        if player.name != "House":
            await self.print_hand(player)

    def find_player(self, name):
        found = None
        for player in self.game.players:
            if player.name == name:
                found = player
        return found

    async def print_table(self, ctx):
        for player in self.game.players:
            await ctx.send(player.name)
            await ctx.send(file=discord.File(player.pub_file_name))

    @staticmethod
    async def warn_msg(player, warn):
        await player.name_client.send(warn)
