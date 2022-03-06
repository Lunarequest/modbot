__version__ = "0.1.0"
import os
import dotenv
from bot import build_bot

if os.path.exists(".env"):
    dotenv.load_dotenv()

if os.name != "nt":
    import uvloop

    uvloop.install()

if __name__ == "__main__":
    build_bot().run()
