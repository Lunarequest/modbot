import arc
import os
import sys
import hikari
from typing import Any

MODROLE = os.environ.get("MODROLE")
if not MODROLE:
    print("MISSING REQUIRED ENV VAR MODROLE")
    sys.exit(1)


async def moduser(ctx: arc.Context[Any]) -> arc.HookResult:
    assert ctx.member

    if int(str(MODROLE)) in ctx.member.role_ids:
        await ctx.respond(
            "❌ This command is restricted. Only allowed roles are permitted to use\
this command.",
            flags=hikari.MessageFlag.EPHEMERAL,
        )
        return arc.HookResult(abort=True)

    return arc.HookResult()
