"""
First version of the bot.
Don't use this!

import asyncio
import datetime
import random

import pytz
import twitchio
from twitchAPI.twitch import Twitch
from twitchio.ext import commands

from config.config_loader import FiZoneBotConfig
from google_sheet import GoogleSheet

class Bot(commands.Bot):

    def __init__(self, config: FiZoneBotConfig):
        self.google_sheet = GoogleSheet()

        self.fionn_quotes: {str: any} = {
            v[0]: v for v in self.google_sheet.get_all_fionn_quotes()
        }

        self.raffle = []
        self.is_raffle = False

        self.channel = [config.channel]
        self.twitch = Twitch(config.client_id, config.secret)
        super().__init__(
            token=config.oauth,
            prefix='!',
            initial_channels=self.channel
        )

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        await asyncio.sleep(3)
        channel: twitchio.Channel = self.get_channel('ostof')
        if channel is not None:
            if channel.name == 'fionn':
                await channel.send('fionBot Bot ready! fionBot')
            elif channel.name == 'zoeyproasheck':
                await channel.send('MrDestructoid Bot ready! MrDestructoid')
            else:
                await channel.send('MrDestructoid Bot ready! MrDestructoid')
        else:
            print('channel is none')

    def _get_fionn_quote(self, index: str = None):
        if index is None:
            index = str(random.randint(1, len(self.fionn_quotes.keys())))
        if index in self.fionn_quotes:
            quote = self.fionn_quotes[index]
            return quote
        else:
            return None

    @commands.command()
    async def quote(self, ctx: commands.Context):
        index = ctx.message.content.replace('!quote ', '')
        if index == '':
            index = str(random.randint(1, len(self.fionn_quotes)))
        quote = self._get_fionn_quote(index)
        if quote is not None:
            quote_index, quote_text, quote_game, quote_date = quote
            await ctx.send(f'Quote #{quote_index}\n{quote_text}\n[{quote_game}] [{quote_date}]')
        else:
            await ctx.reply('Quote not found. Make sure to use the right syntax. !quote NUMBER')
            pass
        pass

    async def _quote(self, ctx: commands.Context):
        try:
            index = int(ctx.message.content.replace('!quote ', ''))
            print(f'index: {index}')
            quote = self.google_sheet.get_fionn_quotes_by_index(index)
            if quote is not None:
                await ctx.send(quote)
            else:
                await ctx.send('Quote not found')
        except Exception as e:
            n = self.google_sheet.get_number_of_fionn_quotes()
            r = random.randint(1, n)
            quote = self.google_sheet.get_fionn_quotes_by_index(r)
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
            user_login=['mousie']
        )['data']
        if len(streams) > 0:
            stream = streams[0]
            print(stream)
            game_name = stream['game_name']
            date = datetime.datetime.now(tz=pytz.timezone('Europe/London'))
            date_str = date.strftime('%d/%m/%Y')
            quote = self.google_sheet.add_fionn_quote(quote_text, game_name, date_str)
            print(quote)
            self.fionn_quotes[quote[0]] = quote
            await ctx.send(f'@{ctx.author.name} added quote #{quote[0]} {quote_text}')
        else:
            await ctx.reply(f'@{ctx.author.name} could not add quote')
            print('channel not live')

        pass

    @commands.command(name='nquotes')
    async def number_of_quotes(self, ctx: commands.Context):
        n = len(self.fionn_quotes)
        await ctx.reply(f'There are {n} quotes')
        pass

    @commands.command(name='startraffle')
    async def start_raffle(self, ctx: commands.Context):
        self.is_raffle = True
        if not ctx.author.is_mod:
            return
        self.raffle = []
        await ctx.send('/me A raffle has started type !enter to enter')
        pass

    @commands.command(name='stopraffle')
    async def stop_raffle(self, ctx: commands.Context):
        self.is_raffle = False
        if not ctx.author.is_mod:
            return
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

    @commands.command(name='enter')
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
        if not self.is_raffle:
            await ctx.send(f"There is no active raffle.")
            return
        await ctx.send(f"{len(self.raffle)} people have entered the raffle!")
        pass

    @commands.command(name='uptime')
    async def uptime(self, ctx: commands.Context):
        result: [twitchio.client.models.Stream] = \
            await self.fetch_streams(user_logins=[f'{ctx.channel.name}'])
        if len(result) > 0:
            stream: twitchio.client.models.Stream = result[0]
            tzname = pytz.timezone(stream.started_at.tzname())
            now = datetime.datetime.now(tz=tzname)
            diff = now - stream.started_at
            await ctx.send(f'@{ctx.author.name} We have been live for {str(datetime.timedelta(seconds=diff.seconds))}')
        pass

    @commands.command(name='close')
    async def close_bot(self, ctx: commands.Context):
        if ctx.message.author is not None:
            if ctx.message.author.name.lower() == 'ostof':
                await ctx.send('stopping bot')
                await self.close()
            else:
                await ctx.reply('You are unauthorized to stopping the bot yogP')
        pass

"""
