import asyncio
import datetime

import pytz
import twitchio
from twitchAPI import Twitch
from twitchio.ext import commands

from config.config_loader import FiZoneBotConfig


class FiZoneBot(commands.Bot):
    def __init__(self, config: FiZoneBotConfig):
        self.config = config
        self.oauth_token = config.twitch_config.oauth
        self._channel = config.bot_config.channel
        self.twitch = Twitch(config.twitch_config.client_id, config.twitch_config.secret)
        super().__init__(
            token=config.twitch_config.oauth,
            prefix='!',
            initial_channels=[self._channel]
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

    @commands.command(name='uptime')
    async def uptime(self, ctx: commands.Context):
        streams = self.twitch.get_streams(
            user_login=[
                self._channel
            ]
        )['data']
        if len(streams) > 0:
            stream = streams[0]
            started_at = stream['started_at']
            tzname = pytz.timezone(started_at.tzname())
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

    pass
