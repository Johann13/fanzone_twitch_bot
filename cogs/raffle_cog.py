import random

import twitchio
from twitchAPI import Twitch
from twitchio.ext import commands

from config.config_loader import RaffleConfig, TwitchConfig, BotConfig


class RaffleCog(commands.Cog):
    def __init__(self,
                 config: RaffleConfig,
                 bot_config: BotConfig,
                 twitch_config: TwitchConfig,
                 bot: commands.Bot):
        self.config = config
        self.bot_config = bot_config
        self.bot = bot
        self.bot.add_command(
            commands.Command(
                name=config.enter_raffle_command,
                func=self.enter_raffle
            )
        )
        self.raffle = []
        self.is_raffle = False
        self.twitch = Twitch(twitch_config.client_id, twitch_config.secret)

    @commands.command(name='startraffle')
    async def start_raffle(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            return
        if self.is_raffle:
            await ctx.send(f'@{ctx.author.name} there is already a raffle running')
            return
        self.is_raffle = True

        self.raffle = []
        await ctx.send(f'/me A raffle has started type !{self.config.enter_raffle_command} to enter')
        pass

    @commands.command(name='startchatterraffle')
    async def start_raffle(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            return
        if self.is_raffle:
            await ctx.send(f'@{ctx.author.name} there is already a raffle running')
            return
        channel: twitchio.Channel = self.bot.get_channel(self.bot_config.channel)
        if channel is not None:
            self.raffle = []
            chatters = channel.chatters
            if chatters is not None:
                for c in chatters:
                    if not c.is_mod:
                        self.raffle = [c.name.lower()]
            if len(self.raffle) > 0:
                await ctx.send(f'/me Everyone in chat was added to the raffle')
            else:
                await ctx.reply(f"@{ctx.author.name} an error occurred. No people in chat.")
        else:
            await ctx.reply(f"@{ctx.author.name} an error occurred. Channel not found.")
        pass

    @commands.command(name='stopraffle')
    async def stop_raffle(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            return

        if not self.is_raffle:
            await ctx.send(f'@{ctx.author.name} there is no raffle running')
            return

        self.is_raffle = False
        await ctx.send('/me The raffle has ended a winner will be drawn soon')
        pass

    @commands.command(name='drawraffle')
    async def draw_raffle(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            return
        if self.is_raffle:
            await ctx.send(f'@{ctx.author.name} you can not draw a winner. Close the raffle first.')
            return
        if len(self.raffle) <= 0:
            await ctx.send(f"There is no active raffle. Or no one entered")

        name = random.choice(self.raffle)
        self.raffle.remove(name)
        await ctx.send(f'@{name} has been drawn!')
        await ctx.send(f'/w  {name} you have been drawn! Write something in the chat!')
        pass

    # @commands.command(name='enter')
    async def enter_raffle(self, ctx: commands.Context):
        if not self.is_raffle:
            await ctx.send(f"/w {ctx.author.name} There is no active raffle.")
            return
        print(self.raffle)
        if ctx.author.name not in self.raffle:
            self.raffle.append(ctx.author.name)
            await ctx.send(f"/w {ctx.author.name} You have entered the raffle!")
        pass

    @commands.command(name='nraffle')
    async def n_raffle(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            return
        if len(self.raffle) <= 0:
            return
        await ctx.send(f"{len(self.raffle)} people have entered the raffle!")
        pass

    @commands.command(name='praffle')
    async def p_raffle(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            return
        if len(self.raffle) <= 0:
            return
        s = ''
        for e in self.raffle:
            s += f'{e} '
        s = s.rstrip()
        await ctx.send(f"These people entered the raffle: {s}!")
        pass

    pass
