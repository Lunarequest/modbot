import arc
import os
import sys
import hikari
from typing import Any

MODROLE = os.environ.get("MODROLE")
if not MODROLE:
    print("MISSING REQUIRED ENV VAR MODROLE")
    sys.exit(1)
MODROLE = int(MODROLE)


async def moduser(ctx: arc.Context[Any]) -> arc.HookResult:
    assert ctx.member
    print(ctx.member.role_ids)

    if MODROLE not in ctx.member.role_ids:
        await ctx.respond(
            "❌ This command is restricted. Only allowed roles are permitted to use this command.",  # noqa: E501
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return arc.HookResult(abort=True)

    return arc.HookResult()
