import hikari
import lightbulb
import os


def build_bot() -> lightbulb.BotApp:
    TOKEN = os.environ.get("BOT_TOKEN")
    bot = lightbulb.BotApp(
        TOKEN,
        prefix="!",
        banner=None,
        intents=hikari.Intents.ALL,
        default_enabled_guilds=(752062040075534397,)
    )

    bot.load_extensions_from("./modbot/extensions/", must_exist=True)

    return bot
