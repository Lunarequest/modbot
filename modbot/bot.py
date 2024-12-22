import hikari
import sys
import arc
import os


def build_bot() -> hikari.GatewayBot:
    token = os.environ.get("BOT_TOKEN")
    if token:
        bot = hikari.GatewayBot(token)
        client = arc.GatewayClient(bot)

        os.chdir("modbot")
        client.load_extensions_from("./extensions")

        return bot
    else:
        print("the environment varible BOT_TOKEN was not defined")
        sys.exit(1)
