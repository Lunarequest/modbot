from datetime import datetime
from checks import moduser
from sys import exit
import hikari
import arc
import os

mod_plugin = arc.GatewayPlugin("mod")
ANNOCEMENT_CHANNEL = os.environ.get("ANNOCEMENT_CHANNEL")
if not ANNOCEMENT_CHANNEL:
    print("MISSING REQUIRED ENV VAR ANNOCEMENT_CHANNEL")
    exit(1)


@mod_plugin.include
@arc.with_hook(moduser)
@arc.slash_command("userinfo", "get information on a server member.")
async def userinfo(
    ctx: arc.GatewayContext,
    user: arc.Option[hikari.Member, arc.MemberParams("user to get infomration about")],
) -> None:
    guild = ctx.get_guild()
    target = None
    if guild:
        target = guild.get_member(user)

    if not target:
        await ctx.respond("the requested user is not in the server")
        return

    created_at = int(target.created_at.timestamp())
    joined_at = 0
    if target.joined_at:
        joined_at = int(target.joined_at.timestamp())

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


@mod_plugin.include
@arc.with_hook(moduser)
@arc.slash_command("ban", "ban user with reason")
async def ban(
    ctx: arc.Context,
    user: arc.Option[hikari.Member, arc.MemberParams("User to ban")],
    reason: arc.Option[
        str, arc.StrParams("Reason why user is banned")
    ] = "User was banned",
) -> None:
    try:
        await user.ban(delete_message_seconds=604800, reason=reason)
        await ctx.respond(f"user: {user.display_name} has been banned")
    except Exception as e:
        await ctx.respond("an error occured while trying to ban the user")
        print(e)
    finally:
        return


@mod_plugin.include
@arc.with_hook(moduser)
@arc.slash_command("kick", "kick the user from a server.")
async def kick(
    ctx: arc.Context,
    target: arc.Option[hikari.Member, arc.MemberParams("User was kicked")],
    reason: arc.Option[
        str, arc.StrParams("Reason why user is banned")
    ] = "User was banned",
) -> None:
    try:
        await target.kick(reason=reason)
        await ctx.respond(f"user: {target.display_name} has been kicked")
    except Exception as e:
        await ctx.respond("an error occured while trying to kick the user")
        print(e)
    finally:
        return


@mod_plugin.listen()
async def member_join(event: hikari.MemberCreateEvent):
    target = event.member
    created_at = int(target.created_at.timestamp())
    joined_at = 0
    if target.joined_at:
        joined_at = int(target.joined_at.timestamp())
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

    await mod_plugin.client.rest.create_message(
        content=embed, channel=int(str(ANNOCEMENT_CHANNEL))
    )


@mod_plugin.include
@arc.slash_command("lockdown", "locks down channel")
async def lock(
    ctx: arc.Context,
    channel: arc.Option[
        hikari.TextableGuildChannel, arc.ChannelParams("the channel to lock")
    ],
    reason: arc.Option[str, arc.StrParams("the reasoning for channel lockdown")],
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


@mod_plugin.include
@arc.slash_command("unlock", "locks down channel")
async def unlock(
    ctx: arc.Context,
    channel: arc.Option[
        hikari.TextableGuildChannel, arc.ChannelParams("the channel to unlock")
    ],
) -> None:
    guild = ctx.get_guild()
    guild_id = ctx.guild_id
    if guild and guild_id:
        _channel = guild.get_channel(channel.id if channel else ctx.channel_id)
        if _channel:
            await _channel.remove_overwrite(_channel.permission_overwrites[_channel.id])

        else:
            await ctx.respond(
                "❌ This channel has already been locked.",
                flags=hikari.MessageFlag.EPHEMERAL,
            )


@arc.loader
def loader(client: arc.GatewayClient) -> None:
    client.add_plugin(mod_plugin)
