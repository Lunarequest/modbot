import sys
import hikari
import lightbulb
import os


def build_bot() -> lightbulb.BotApp:
    TOKEN = os.environ.get("BOT_TOKEN")
    if not os.environ.get("ANNOCEMENT_CHANNEL"):
        print("missing required env token ANNOCEMENT_CHANNEL")
        sys.exit(1)
    if TOKEN:
        bot = lightbulb.BotApp(
            TOKEN,
            prefix="!",
            banner=None,
            intents=hikari.Intents.ALL,
            default_enabled_guilds=(752062040075534397,),
        )

        bot.load_extensions_from("./modbot/extensions/", must_exist=True)

        return bot
    else:
        print("the environment varible BOT_TOKEN was not defined")
        sys.exit(1)
