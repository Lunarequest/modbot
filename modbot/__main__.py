__version__ = "0.1.0"
from bot import build_bot
import asyncio
import dotenv
import os


if os.path.exists(".env"):
    dotenv.load_dotenv()

if os.name != "nt":
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def start():
    bot = build_bot()
    bot.run()


if __name__ == "__main__":
    start()
