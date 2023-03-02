from datetime import datetime
from typing import Optional
import hikari
import os
import lightbulb

mod_plugin = lightbulb.Plugin("mod")
ANNOCEMENT_CHANNEL = os.environ.get("ANNOCEMENT_CHANNEL")
if not ANNOCEMENT_CHANNEL:
    print("MISSING REQUIRED ENV VAR ANNOCEMENT_CHANNEL")
    exit(1)
MODROLE = os.environ.get("MODROLE")
if not MODROLE:
    print("MISSING REQUIRED ENV VAR MODROLE")
    exit(1)


@mod_plugin.command
@lightbulb.add_checks(lightbulb.has_roles(int(MODROLE), mode=any))
@lightbulb.option(
    "target", "the member to get user info about.", hikari.User, required=False
)
@lightbulb.command("userinfo", "get information on a server member.")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def userinfo(ctx: lightbulb.Context) -> None:
    target: Optional[hikari.Member] = None
    guild = ctx.get_guild()
    if guild:
        if ctx.options.target:
            target = guild.get_member(ctx.user or ctx.options.target)

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
    reason = ""
    match ctx.options.reasons:
        case None:
            pass
        case _:
            reason = ctx.options.reasons
    try:
        await target.ban(reason=reason)
        await ctx.respond(f"user: {target.display_name} has been banned")
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
    target: hikari.Member = ctx.options.target
    reason = ""
    match ctx.options.reasons:
        case None:
            pass
        case _:
            reason = ctx.options.reasons
    try:
        await target.kick(reason=reason)
        await ctx.respond(f"user: {target.display_name} has been kicked")
    except Exception as e:
        await ctx.respond("an error occured while trying to kick the user")
        print(e)
    finally:
        return


@mod_plugin.listener(hikari.MemberCreateEvent)
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

    await mod_plugin.bot.rest.create_message(
        content=embed, channel=int(ANNOCEMENT_CHANNEL)
    )


@mod_plugin.command
@lightbulb.add_cooldown(10, 3, lightbulb.UserBucket)
@lightbulb.option(
    name="reason",
    description="the reasoning for channel lockdown",
    required=False,
)
@lightbulb.option(
    name="channel",
    description="the channel to lock",
    type=hikari.TextableGuildChannel,
    required=False,
)
@lightbulb.command(
    name="lock",
    description="Locks a channel",
    pass_options=True,
)
@lightbulb.implements(lightbulb.SlashCommand)
async def lock(
    ctx: lightbulb.Context, channel: hikari.TextableGuildChannel, reason: str
) -> None:
    """
    Allows mentioning of a channel or to use the id of one
    when using the channel option.
    If `reason` is not specified, it will be set to None.
    """
    guild = ctx.get_guild()
    guild_id = ctx.guild_id
    if guild and guild_id:
        _channel = guild.get_channel(channel.id if channel else ctx.channel_id)
        if _channel:
            await _channel.edit_overwrite(
                guild_id,
                target_type=hikari.PermissionOverwriteType.ROLE,
                deny=hikari.Permissions.SEND_MESSAGES,
                reason="Channel lockdown",
            )

            await ctx.respond(
                f"⚠️ {_channel.mention} has been locked by **{ctx.user}**.\n"
                f"**Reason**: {reason or 'None'}"
            )
        else:
            await ctx.respond(
                "❌ This channel has already been locked.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(mod_plugin)
