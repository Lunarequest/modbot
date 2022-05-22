import os
import hikari
import lightbulb
from datetime import datetime

auto_mod: lightbulb.Plugin = lightbulb.Plugin("mod")

async def spam(event: hikari.MessageCreateEvent , message: str, message_set: set):
    if (
            len(message.split())
            != len(message_set) & len(message.split()) - len(message_set)
            > 4
        ):
            target = event.author
            embed = (
                hikari.Embed(
                    title=f"Possible Spam",
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
            await auto_mod.bot.rest.create_message(
                content=embed, channel=int(os.environ.get("ANNOCEMENT_CHANNEL"))
            )


@auto_mod.listener(hikari.MessageCreateEvent)
async def on_message(event: hikari.MessageCreateEvent):
    if event.is_human:
        guild: hikari.Snowflake = event.message.guild_id
        guild.get
        message = event.message.content
        message_set = set(message.split(" "))
        await spam(event, message, message_set)



def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(auto_mod)
