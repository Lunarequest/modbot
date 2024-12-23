from datetime import datetime
from yaml import safe_load
from pathlib import Path
from typing import Any
from sys import exit
import hikari
import arc
import os
import re

MIN_LEN = 4
slur_list = []


class Slurs:
    slur_list: list[re.Pattern[Any]] = []  # noqa: RUF012

    def load_slurs(self):
        pathlist = Path("../slurs").glob("**/*.yaml")
        minlist = []
        for path in pathlist:
            with open(path) as file:
                yaml = safe_load(file.read())
                regex = yaml.get("regex")
                if regex:
                    minlist = [re.compile(string) for string in regex]
        self.slur_list = self.slur_list + minlist
        print(self.slur_list)

    def list(self):
        return self.slur_list


auto_mod = arc.GatewayPlugin("automod")
ANNOCEMENT_CHANNEL = os.environ.get("ANNOCEMENT_CHANNEL")
if not ANNOCEMENT_CHANNEL:
    print("MISSING REQUIRED ENV VAR ANNOCEMENT_CHANNEL")
    exit(1)
slurs_class = Slurs()
slurs_class.load_slurs()


async def spam(
    event: hikari.MessageCreateEvent,
    delete: bool,
    message: str,
    message_set: set,
) -> None:
    if (
        len(message.split())
        != len(message_set) & len(message.split()) - len(message_set)
        > MIN_LEN
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
            await auto_mod.client.rest.create_message(
                content=embed, channel=int(ANNOCEMENT_CHANNEL)
            )


async def slurs(event: hikari.MessageCreateEvent, message: str) -> bool:
    if message:
        print("checking for slurs")
        for regex in slurs_class.list():
            t = re.findall(regex, message)
            if t:
                embed = (
                    hikari.Embed(
                        title="Possible Spam",
                        description="You've been naughty",
                        colour=0x3B9DFF,
                        timestamp=datetime.now().astimezone(),
                    )
                    .set_thumbnail(Path("../assets/mommy.png"))
                    .add_field(
                        "You sent a naughty message",
                        message,
                        inline=True,
                    )
                )
                await event.message.author.send(embed)
                return True
    return False


@auto_mod.listen()
async def on_message(event: hikari.MessageCreateEvent) -> None:
    print(event)
    if event.is_human:
        channel = await auto_mod.client.rest.fetch_channel(event.message.channel_id)
        print(channel)
        message = event.message.content
        print(message)
        if channel and message:
            delete = await slurs(event, message)
            print(delete)
            if delete:
                await event.message.delete()
            old_messages = auto_mod.client.rest.fetch_messages(
                int(channel), before=event.message_id
            )
            print(old_messages)
            message_set = set(message.split(" "))
            await spam(event, delete, message, message_set)


@arc.loader
def loader(bot: arc.GatewayClient) -> None:
    bot.add_plugin(auto_mod)
