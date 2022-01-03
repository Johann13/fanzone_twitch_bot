from twitchio.ext import commands

from cogs.quote_cog import QuoteCog
from cogs.raffle_cog import RaffleCog
from config.config_loader import FiZoneBotConfig


class CogManager(commands.Cog):
    def __init__(self,
                 config: FiZoneBotConfig,
                 bot: commands.Bot):
        self.config = config
        self.bot = bot
        if config.bot_config.use_quote_bot:
            self.add_quote_cog()
        if config.bot_config.use_raffle_bot:
            self.add_raffle_cog()
        pass

    @commands.command(name='enable_quotes')
    async def _add_quote_cog(self, ctx: commands.Context):
        # !enable_quotes quotes_test quotes_fionn
        if not ctx.author.is_mod:
            return
        self.add_quote_cog()
        await ctx.send('Added Quote Module')
        pass

    @commands.command(name='enable_raffle')
    async def _add_raffle_cog(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            return
        self.add_raffle_cog()
        await ctx.send('Added Raffle Module')
        pass

    def add_quote_cog(self):
        self.bot.add_cog(QuoteCog(
            config=self.config.quote_config,
            twitch_config=self.config.twitch_config,
            bot_config=self.config.bot_config
        ))
        pass

    def add_raffle_cog(self):
        self.bot.add_cog(RaffleCog(
            config=self.config.raffle_config,
            bot_config=self.config.bot_config,
            twitch_config=self.config.twitch_config,
            bot=self.bot
        ))
        pass

    pass
