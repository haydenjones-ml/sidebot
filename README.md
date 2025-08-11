# SideBot

**Your side-betting ledger solution for all gambling shenanigans!**

Small side project so I could have an excuse to use the [Discord.py API](https://discordpy.readthedocs.io/en/latest/api.html)! I plan on hosting it soon for multiple servers, but if you want to use it in your own server then follow these instructions...

## Running Locally
- Make sure you have the necessary dependencies installed
    - [Discord.py](https://github.com/Rapptz/discord.py)
    - [TinyDB](https://tinydb.readthedocs.io/en/latest/getting-started.html)
- Generate a Discord developer project and OAuth token from the [Discord Developer Portal](https://discord.com/developers/docs/topics/oauth2)
- Clone this project, and create your "token_bank.json" file
- Fill file with Keys that match the ones listed on the top of "bot.py" and fill out their corresponding values
Template:
```
{
    "APP_ID" : <DISCORD_APP_ID_HERE>,
    "DISCORD_TOKEN" : <PRIVATE_OAUTH2_TOKEN_HERE>,
    "PUBLIC_KEY" : <PUBLIC_KEY_HERE>,
    "SERVER_ID" : <TARGET_SERVER_ID_HERE>
}
```
- Click run, and enjoy!
## Other notes
- If you want any other commands to be implemented, please feel free to contribute via pull requests!
- If you cannot write code, be sure to open up an [issue](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/creating-an-issue) with a description describing what you would like!
