__version__ = "0.1.0"
import os
import dotenv

# stuff like this is a hack to make python run it
# when python modbot is run and also poetry run start
if __name__ == "__main__":
    from bot import build_bot
else:
    from .bot import build_bot

if os.path.exists(".env"):
    dotenv.load_dotenv()

if os.name != "nt":
    import uvloop

    uvloop.install()


def start():
    bot = build_bot()
    bot.run()


if __name__ == "__main__":
    start()
