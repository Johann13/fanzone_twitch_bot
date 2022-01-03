"""
This was only used to copy quotes from streamlabs.
Don't use this!

import asyncio
import random

from twitchAPI.twitch import Twitch
from twitchio.ext import commands
from twitchio.message import Message

from config.config_loader import FiZoneBotConfig
from google_sheet import GoogleSheet
# Used to copy quotes manually from streamlabs.
# This can take up to 20 minutes per 100 quotes.

class CopyStreamlabs(commands.Bot):
    current_index = 900
    start_index = 900
    amount = 35

    def __init__(self, config: FiZoneBotConfig):
        self.google_sheet = GoogleSheet()
        self.twitch = Twitch(
            config.twitch_config.client_id,
            config.twitch_config.secret
        )
        super().__init__(
            token=config.twitch_config.oauth,
            prefix='!',
            initial_channels=['fionn']
        )

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')

    async def event_message(self, message: Message):
        if message.author is not None:
            print(f'author: {message.author.name}')
        else:
            print(f'author: None')
        if message.channel is not None:
            print(f'channel: {message.channel.name}')
        else:
            print(f'channel: None')

        if message.author is not None:
            if message.author.name == 'streamlabs':
                if 'Quote #' in message.content:
                    print(f'message.content: {message.content}')
                    index = int(message.content.split('#')[1].split(' ')[0])
                    text = message.content.split('#')[1].split(' ', 1)[1].split('[')[0].rstrip()
                    contents = message.content.split('[')
                    game = contents[1].replace(']', '')
                    date = contents[2].replace(']', '')
                    self.google_sheet.quotes.update_cell(index, 1, index)
                    self.google_sheet.quotes.update_cell(index, 2, text)
                    self.google_sheet.quotes.update_cell(index, 3, game)
                    self.google_sheet.quotes.update_cell(index, 4, date)
                    context: commands.Context = await self.get_context(message)
                    r = random.randrange(0, 4)
                    s = 10 + r
                    await context.send(
                        f'Copied quote {index}. '
                        f'Waiting {s} seconds to copy the next quote.'
                    )
                    print(f'wait {s}s')
                    await asyncio.sleep(s)
                    await context.send(f'!quote {index + 1}')
                    self.current_index = index + 1
                pass
        # await self.handle_commands(message)

    @commands.command(name='sqc')
    async def start_quote_collection(self, ctx: commands.Context):
        try:
            print('start_quote_collection')
            index = int(ctx.message.content.replace('!sqc ', ''))
            self.start_index = index
            print(f'index: {index}')
            await ctx.send(f'!quote {index}')
        except Exception as e:
            print(e)
        pass

    @commands.command(name='close')
    async def close_bot(self, ctx: commands.Context):
        if ctx.message.author is not None:
            if ctx.message.author.is_mod or ctx.message.author.name.lower() == 'ostof':
                await ctx.send('stopping bot')
                await self.close()
            else:
                await ctx.reply('You are unauthorized to stopping the bot yogP')
        pass

    pass


if __name__ == '__main__':
    bot = CopyStreamlabs('oauth:ucgkm5guom8m4tu3nwmubwkjvddvop')
    bot.run()
"""
