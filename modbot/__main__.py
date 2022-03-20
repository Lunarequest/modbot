__version__ = "0.1.0"
import os
import dotenv
from typing import TYPE_CHECKING

# stuff like this is a hack to make mypy work
# .bot trips up the regular python interpreter but its needed for mypy :/
if TYPE_CHECKING:
    from .bot import build_bot
else:
    from bot import build_bot

if os.path.exists(".env"):
    dotenv.load_dotenv()

if os.name != "nt":
    import uvloop

    uvloop.install()

if __name__ == "__main__":
    build_bot().run()
