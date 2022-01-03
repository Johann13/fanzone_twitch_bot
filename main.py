from cogs.cog_manager_cog import CogManager
from config.config_loader import FiZoneBotConfig
from fizone_bot import FiZoneBot

if __name__ == '__main__':
    config = FiZoneBotConfig.from_file(
        bot_config_file_name='config/bot_config.json',
        twitch_config_file_name='config/twitch_config.json',
        quote_config_file_name='config/quote_config.json',
        raffle_config_file_name='config/raffle_config.json',
    )
    bot = FiZoneBot(
        config=config
    )
    bot.add_cog(
        CogManager(
            config=config,
            bot=bot
        )
    )
    bot.run()
    pass
