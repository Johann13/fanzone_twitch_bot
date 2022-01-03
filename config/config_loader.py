import json


class QuoteConfig(object):

    def __init__(self, json_data: dict):
        self.spreadsheet = json_data['QUOTES_SPREADSHEET']
        self.quotes_worksheet_name = json_data['QUOTES_WORKSHEET']
        self.google_service_accounts = json_data['GOOGLE_SERVICE_ACCOUNT']

    @classmethod
    def from_file(cls, file_name: str):
        data = json.load(open(file_name))
        return cls(data)

    pass


class RaffleConfig(object):

    def __init__(self, json_data: dict):
        self.enter_raffle_command = json_data['ENTER_RAFFLE_COMMAND']

    @classmethod
    def from_file(cls, file_name: str):
        data = json.load(open(file_name))
        return cls(data)

    pass


class TwitchConfig(object):

    def __init__(self, json_data: dict):
        self.oauth = json_data['TWITCH_TMI_OAUTH']
        self.client_id = json_data['TWITCH_CLIENT_ID']
        self.secret = json_data['TWITCH_SECRET']

    @classmethod
    def from_file(cls, file_name: str):
        data = json.load(open(file_name))
        return cls(data)

    pass


class BotConfig(object):

    def __init__(self, json_data: dict):
        self.channel = json_data['CHANNEL']
        self.use_quote_bot = json_data['USE_QUOTE_MODULE']
        self.use_raffle_bot = json_data['USE_RAFFLE_MODULE']

    @classmethod
    def from_file(cls, file_name: str):
        data = json.load(open(file_name))
        return cls(data)

    pass


class FiZoneBotConfig(object):

    def __init__(self,
                 bot_config: BotConfig,
                 twitch_config: TwitchConfig,
                 quote_config: QuoteConfig,
                 raffle_config: RaffleConfig,
                 ):
        self.bot_config = bot_config
        self.twitch_config = twitch_config
        self.quote_config = quote_config
        self.raffle_config = raffle_config

    @classmethod
    def from_file(cls,
                  bot_config_file_name: str,
                  twitch_config_file_name: str,
                  quote_config_file_name: str,
                  raffle_config_file_name: str,
                  ):
        return cls(
            bot_config=BotConfig.from_file(bot_config_file_name),
            twitch_config=TwitchConfig.from_file(twitch_config_file_name),
            quote_config=QuoteConfig.from_file(quote_config_file_name),
            raffle_config=RaffleConfig.from_file(raffle_config_file_name),
        )

    pass
