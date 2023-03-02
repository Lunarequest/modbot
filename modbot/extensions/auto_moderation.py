import os
import hikari
import lightbulb
from datetime import datetime

auto_mod: lightbulb.Plugin = lightbulb.Plugin("mod")
ANNOCEMENT_CHANNEL = os.environ.get("ANNOCEMENT_CHANNEL")
if not ANNOCEMENT_CHANNEL:
    print("MISSING REQUIRED ENV VAR ANNOCEMENT_CHANNEL")
    exit(1)


async def spam(
    event: hikari.MessageCreateEvent, message: str, message_set: set
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
        if ANNOCEMENT_CHANNEL:
            await auto_mod.bot.rest.create_message(
                content=embed, channel=int(ANNOCEMENT_CHANNEL)
            )


@auto_mod.listener(hikari.MessageCreateEvent)
async def on_message(event: hikari.MessageCreateEvent):
    if event.is_human:
        channel = await auto_mod.bot.rest.fetch_channel(
            event.message.channel_id
        )
        if channel:
            old_messages = auto_mod.bot.rest.fetch_messages(
                int(channel), before=event.message_id
            )
            print(old_messages)
            message = event.message.content
            if message:
                message_set = set(message.split(" "))
                await spam(event, message, message_set)


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(auto_mod)
