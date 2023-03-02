import sys
import hikari
import lightbulb
import os


def build_bot() -> lightbulb.BotApp:
    TOKEN = os.environ.get("BOT_TOKEN")
    GUILD = os.environ.get("GUILD")
    if GUILD and TOKEN:
        bot = lightbulb.BotApp(
            TOKEN,
            prefix="!",
            banner=None,
            intents=hikari.Intents.ALL,
            default_enabled_guilds=(int(GUILD)),
        )

        os.chdir("modbot")
        bot.load_extensions_from("./extensions", must_exist=True)

        return bot
    else:
        print("the environment varible BOT_TOKEN was not defined")
        sys.exit(1)
