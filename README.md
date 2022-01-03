# FiZone FanZone Twitch Bot

### A simple Twitch bot which anyone can run locally on their own computer!

## How to use

- Install Python 3.7
- Download and unpack this repository
- If you want to use the Quote functionality see the [Quote section](##quote-module-setup)
- Update all the [config files](#config)
- Run the python command python3 main.py

## Built in Commands

### Quotes

| Command         | Mod only | Description                                                                 |
|-----------------|----------|-----------------------------------------------------------------------------|
| !quote n        | false    | Returns the n-th quote. If no number is provided a random quote is returned |
| !addquote quote | true     | Adds a new quote                                                            |
| !nquotes        | false    | Returns the number of quotes                                                |

### Raffle

| Command      | Mod only | Description                                                                           |
|--------------|----------|---------------------------------------------------------------------------------------|
| !startraffle | true     | Starts a new raffle                                                                   |
| !startchatterraffle | true     | Starts a new raffle but automaticly adds everyone in chat to the raffle (except mods) |
| !stopraffle  | true     | Ends a raffle                                                                         |
| !drawraffle  | true     | Picks a random chatter who entered the raffle                                         |
| !enter       | false    | Enters the chatter to the raffle                                                      |

## Config

The bot needs a few configuration files which need to be in the *config* folder.

### General Bot Config

The file should be called *bot_config.json*

| Attribute         | Type     | Description                                      |
|-------------------|----------|--------------------------------------------------|
| CHANNEL           | string   | The name of the channel where the bot should run |
| USE_QUOTE_MODULE  | boolean  | Whether or not the quote module should be used   |
| USE_RAFFLE_MODULE | boolean  | Whether or not the raffle module should be used|

```json
{
  "CHANNEL": "CHANNEL NAME",
  "USE_QUOTE_MODULE": true,
  "USE_RAFFLE_MODULE": true
}
```

---

### Twitch Config

The file should be called *twitch_config.json*

| Attribute         | Type     | Description                          |
|-------------------|----------|--------------------------------------|
| TWITCH_CLIENT_ID | string   | The client id to use the twitch api  |
| TWITCH_SECRET  | string  | The app secret to use the twitch api |
| TWITCH_TMI_OAUTH | string  | OAuth Token of the bots account      |

```json
{
  "TWITCH_CLIENT_ID": "CLIENT_ID",
  "TWITCH_SECRET": "SECRET",
  "TWITCH_TMI_OAUTH": "OAUTH_TOKEN"
}
```

### Quote Config

The file should be called *quote_config.json*

| Attribute         | Type     | Description                                                                                   |
|-------------------|----------|-----------------------------------------------------------------------------------------------|
| QUOTES_SPREADSHEET | string   | Name of the spreadsheet where the quotes are saved                                            |
| QUOTES_WORKSHEET  | string  | Name of the table where the quotes are saved                                                  |
| GOOGLE_SERVICE_ACCOUNT | string  | Path to the google_service_account.json file which is used to write to the google spreadsheet |

```json
{
  "QUOTES_SPREADSHEET": "quotes_test",
  "QUOTES_WORKSHEET": "quotes_fionn",
  "GOOGLE_SERVICE_ACCOUNT": "google_service_account.json"
}
```

### Raffle Config

The file should be called *raffle_config.json*

| Attribute         | Type   | Description                                          |
|-------------------|--------|------------------------------------------------------|
| ENTER_RAFFLE_COMMAND | string | Name of the command people can use to enter a raffle |

```json
{
  "ENTER_RAFFLE_COMMAND": "join"
}
```

## Twitch setup

To get the necessary Twitch credentials you need to do the following:

- Go to https://dev.twitch.tv/
- Top right, click on *Your Console*
- Click on *Applications*
- Register a new Application
- Give it a name
- Enter https://localhost as the OAuth Redirect URLs (we don't need this but need to enter something)
- Select Chat Bot as the category
- Click on *Manage*
- Copy the *Client-ID*
- Click on *New Secret* and copy it (DO NOT SHARE THIS WITH ANYONE)
- The Client-ID and Secret are used for the [Twitch Config](#twitch-config)

For the oauth-token:

- Make sure you are signed in with the account that you want to use as your bot. This can also be you personal twitch
  account.
- Go to https://twitchapps.com/tmi/
- Connect using you twitch account
- Copy the oauth-token (DO NOT SHARE THIS WITH ANYONE)

## Quote Module Setup

The Quote functionality uses Google Sheets to store them. For the bot to be able to read and write the sheet you need to
do a bit of setup.

- Go to https://console.cloud.google.com/home/dashboard (Login with your google account)
- Select/Create a project
- On the top, search for *Google Drive API* and activate it
- On the top, search for *Google Sheets API* and activate it
- Go to https://console.cloud.google.com/apis/credentials
- On the bottom right, click on **manage service accounts**
- On the top, click on **create new service account**
- Give it a name und click on done
- Now you should see the service account
- Click on the three dots on the right
- Click on **manage keys**
- Click on **add key**
- Click on **create new key**
- Make sure **JSON** is selected and click on **Create**
- A file should be downloaded (DO NOT SHARE THIS WITH ANYONE)
- Rename it to something like *google_service_account.json* and put it into the config folder
- Go back to https://console.cloud.google.com/iam-admin/serviceaccounts
- Copy the email which should look something like this *service-account@PROJECTNAME.iam.gserviceaccount.com*
- Go to https://docs.google.com/spreadsheets/
- Create a spreadsheet and give it a name like *Twitch Quotes*
- Create a table and name it something like *Quotes*
- These names are used in [the *quotes_config.json* file](###quote-config)

## Future plans

### More modules

- Social

### Functionality

- Scheduled commands
- Custom commands
- Actual Modding functionality?

### Quotes

- Remove quotes
- Edit quotes

### Other

- Custom commands
