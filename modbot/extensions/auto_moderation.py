import os
import hikari
import lightbulb
from datetime import datetime
from pathlib import Path
from yaml import safe_load
from typing import List
import re

global SLUR_LIST
SLUR_LIST: List[str] = []


def load_slurs():
    pathlist = Path("./slurs").glob("**/*.yaml")
    minlist = []
    for path in pathlist:
        with open(path) as file:
            yaml = safe_load(file.read())
            regex = yaml.get("regex")
            if regex:
                for string in regex:
                    minlist.append(string)
    global SLUR_LIST
    SLUR_LIST = minlist
    print(SLUR_LIST)


auto_mod: lightbulb.Plugin = lightbulb.Plugin("mod")
ANNOCEMENT_CHANNEL = os.environ.get("ANNOCEMENT_CHANNEL")
if not ANNOCEMENT_CHANNEL:
    print("MISSING REQUIRED ENV VAR ANNOCEMENT_CHANNEL")
    exit(1)
load_slurs()


async def spam(
    event: hikari.MessageCreateEvent,
    delete: bool,
    message: str,
    message_set: set,
):
    if (
        len(message.split())
        != len(message_set) & len(message.split()) - len(message_set)
        > 4
    ):
        target = event.author
        embed = (
            hikari.Embed(
                title="Possible Spam",
                description=f"UserID: `{target.id}`",
                colour=0x3B9DFF,
                timestamp=datetime.now().astimezone(),
            )
            .set_thumbnail(target.avatar_url or target.default_avatar_url)
            .add_field(
                "Message Content:",
                message,
                inline=True,
            )
        )
        if not delete:
            await event.message.delete()
        if ANNOCEMENT_CHANNEL:
            await auto_mod.bot.rest.create_message(
                content=embed, channel=int(ANNOCEMENT_CHANNEL)
            )


async def slurs(event: hikari.MessageCreateEvent, message: str):
    if message:
        for regex in SLUR_LIST:
            t = re.findall(regex, message)
            if t:
                embed = (
                    hikari.Embed(
                        title="Possible Spam",
                        description="You've been naughty",
                        colour=0x3B9DFF,
                        timestamp=datetime.now().astimezone(),
                    )
                    .set_thumbnail(Path("./assets/mommy.png"))
                    .add_field(
                        "You sent a naughty message",
                        message,
                        inline=True,
                    )
                )
                await event.message.author.send(embed)
                return True
    return False


@auto_mod.listener(hikari.MessageCreateEvent)
async def on_message(event: hikari.MessageCreateEvent):
    if event.is_human:
        channel = await auto_mod.bot.rest.fetch_channel(
            event.message.channel_id
        )
        message = event.message.content
        if channel and message:
            delete = await slurs(event, message)
            if delete:
                await event.message.delete()
            old_messages = auto_mod.bot.rest.fetch_messages(
                int(channel), before=event.message_id
            )
            print(old_messages)
            message_set = set(message.split(" "))
            await spam(event, delete, message, message_set)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(auto_mod)
