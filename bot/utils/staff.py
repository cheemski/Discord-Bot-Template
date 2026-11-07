import discord


def has_all_roles(member: discord.Member, requiredRoles) -> bool:
    return requiredRoles.issubset({r.id for r in member.roles})
