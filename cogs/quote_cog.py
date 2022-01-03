import datetime
import random

import gspread
import pytz
from twitchAPI import Twitch
from twitchio.ext import commands

from cogs.google_sheet import QuoteSheet
from config.config_loader import QuoteConfig, TwitchConfig, BotConfig


class QuoteCog(commands.Cog):
    def __init__(self,
                 config: QuoteConfig,
                 twitch_config: TwitchConfig,
                 bot_config: BotConfig,
                 ):
        self.config = config
        self.bot_config = bot_config
        service_account: str = config.google_service_accounts
        spreadsheet: str = config.spreadsheet
        quotes_worksheet_name: str = config.quotes_worksheet_name
        sa = gspread.service_account(filename=service_account)
        sh = sa.open(spreadsheet)
        self.quote_sheet = QuoteSheet(sh.worksheet(quotes_worksheet_name))

        self.quotes_map: {str: any} = {
            v[0]: v for v in self.quote_sheet.get_all_quotes()
        }

        self.twitch = Twitch(twitch_config.client_id, twitch_config.secret)

    def _get_quote(self, index: str = None):
        if index is None:
            index = str(random.randint(1, len(self.quotes_map.keys())))
        if index in self.quotes_map:
            quote = self.quotes_map[index]
            return quote
        else:
            return None

    @commands.command()
    async def quote(self, ctx: commands.Context):
        message = ctx.message.content
        index = message.replace('!quote', '').replace('!quote ', '').replace(' ', '')
        print(f'index: [{index}]')
        if index == '':
            index = str(random.randint(1, len(self.quotes_map)))
        quote = self._get_quote(index)
        if quote is not None:
            quote_index, quote_text, quote_game, quote_date = quote
            await ctx.send(
                f'Quote #{quote_index} {quote_text.rstrip()} [{quote_game.rstrip()}] [{quote_date.rstrip()}]')
        else:
            await ctx.reply('Quote not found. Make sure to use the right syntax. !quote NUMBER')
            pass
        pass

    async def _quote(self, ctx: commands.Context):
        try:
            index = int(ctx.message.content.replace('!quote ', ''))
            print(f'index: {index}')
            quote = self.quote_sheet.get_quotes_by_index(index)
            if quote is not None:
                await ctx.send(quote)
            else:
                await ctx.send('Quote not found')
        except Exception as e:
            n = self.quote_sheet.last_quote_index()
            r = random.randint(1, n)
            quote = self.quote_sheet.get_quotes_by_index(r)
            if quote is not None:
                await ctx.send(quote)
            else:
                await ctx.send('Quote not found')
            print(e)
        pass

    @commands.command(name='addquote')
    async def add_quote(self, ctx: commands.Context):
        if not ctx.author.is_mod:
            await ctx.reply(f'Silly @{ctx.author.name} you are not allowed to add quotes')
            return

        quote_text = ctx.message.content.replace('!addquote ', '')
        streams = self.twitch.get_streams(
            user_login=[self.bot_config.channel]
        )['data']

        if len(streams) > 0:
            stream = streams[0]
            game_name = stream['game_name']
            date = datetime.datetime.now(tz=pytz.timezone('Europe/London'))
            date_str = date.strftime('%d/%m/%Y')
            quote = self.quote_sheet.add_quote(quote_text, game_name, date_str)
            self.quotes_map[quote[0]] = quote
            await ctx.send(f'@{ctx.author.name} added quote #{quote[0]} {quote_text}')
        else:
            await ctx.reply(f'@{ctx.author.name} could not add quote')
            print('channel not live')
        pass

    @commands.command(name='nquotes')
    async def number_of_quotes(self, ctx: commands.Context):
        n = len(self.quotes_map)
        await ctx.reply(f'There are {n} quotes')
        pass

    pass
