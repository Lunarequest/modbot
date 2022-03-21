from datetime import datetime
from typing import Optional, TYPE_CHECKING
import hikari
import os
import lightbulb

mod_plugin = lightbulb.Plugin("mod")


@mod_plugin.listener(hikari.MemberChunkEvent)
async def member_join(event):
    target = event.member
    created_at: int = int(target.created_at.timestamp())
    joined_at: int = int(target.joined_at.timestamp())
    embed = (
        hikari.Embed(
            title=f"User Info - {target.display_name}",
            description=f"ID: `{target.id}`",
            colour=0x3B9DFF,
            timestamp=datetime.now().astimezone(),
        )
        .set_thumbnail(target.avatar_url or target.default_avatar_url)
        .add_field(
            "Bot?",
            str(target.is_bot),
            inline=True,
        )
        .add_field(
            "Created account on",
            f"<t:{created_at}:d>\n(<t:{created_at}:R>)",
            inline=True,
        )
        .add_field(
            "Joined server on",
            f"<t:{joined_at}:d>\n(<t:{joined_at}:R>)",
            inline=True,
        )
    )
    mod_plugin.bot.rest.create_message(
        content=embed, channel=int(os.environ.get("ANNOCEMENT_CHANNEL"))
    )


@mod_plugin.command
@lightbulb.add_checks(lightbulb.has_roles(774478728318681118, mode=any))
@lightbulb.option(
    "target", "the member to get user info about.", hikari.User, required=False
)
@lightbulb.command("userinfo", "get information on a server member.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def userinfo(ctx: lightbulb.Context) -> None:
    guild = ctx.get_guild()
    if guild:
        if ctx.options.target:
            if TYPE_CHECKING:
                target: Optional[hikari.Member] = guild.get_member(
                    ctx.options.target
                )
            else:
                target: Optional[hikari.Member] = guild.get_member(
                    ctx.user or ctx.options.target
                )

    if not target:
        await ctx.respond("the requested user is not in the server")
        return

    created_at: int = int(target.created_at.timestamp())
    joined_at: int = int(target.joined_at.timestamp())

    roles = (await target.fetch_roles())[1:]  # All but @everyone
    if target and ctx.member:
        embed = (
            hikari.Embed(
                title=f"User Info - {target.display_name}",
                description=f"ID: `{target.id}`",
                colour=0x3B9DFF,
                timestamp=datetime.now().astimezone(),
            )
            .set_footer(
                text=f"Requested by {ctx.member.display_name}",
                icon=ctx.member.avatar_url or ctx.member.default_avatar_url,
            )
            .set_thumbnail(target.avatar_url or target.default_avatar_url)
            .add_field(
                "Bot?",
                str(target.is_bot),
                inline=True,
            )
            .add_field(
                "Created account on",
                f"<t:{created_at}:d>\n(<t:{created_at}:R>)",
                inline=True,
            )
            .add_field(
                "Joined server on",
                f"<t:{joined_at}:d>\n(<t:{joined_at}:R>)",
                inline=True,
            )
            .add_field(
                "Roles",
                ", ".join(r.mention for r in roles),
                inline=False,
            )
        )
        await ctx.respond(embed)
    return


@mod_plugin.command
@lightbulb.add_checks(lightbulb.has_roles(774478728318681118, mode=any))
@lightbulb.option("target", "the member to ban.", hikari.Member, required=True)
@lightbulb.option("reason", "reason why user is banned", required=False)
@lightbulb.command("ban", "ban the user from a server.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ban(ctx: lightbulb.Context) -> None:
    target: hikari.Member = ctx.options.target
    reason: str = ctx.options.reason
    try:
        await target.ban(reason=reason)
        await ctx.respond(f"user: {target.username} has been banned")
    except Exception as e:
        await ctx.respond("an error occured while trying to ban the user")
        print(e)
    finally:
        return


@mod_plugin.command
@lightbulb.add_checks(lightbulb.has_roles(774478728318681118, mode=any))
@lightbulb.option("target", "the member to ban.", hikari.Member, required=True)
@lightbulb.option("reason", "reason why user is banned", required=False)
@lightbulb.command("kick", "kick the user from a server.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def kick(ctx: lightbulb.Context) -> None:
    target: hikari.Member = ctx.option.target
    reason: str = ctx.options.reason
    try:
        await target.kick(reason=reason)
        await ctx.respond(f"user: {target.username} has been kicked")
    except Exception as e:
        await ctx.respond("an error occured while trying to kick the user")
        print(e)
    finally:
        return


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(mod_plugin)
