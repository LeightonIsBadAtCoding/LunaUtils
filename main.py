import discord
from discord.ext import commands
from webserver import keep_alive
import os
from discord.shard import AutoShardedClient
from asyncio import sleep
import json
keywords = ["retarded", "retard"]

client = commands.Bot(command_prefix = 'l!')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="OnlyFans"))
    print('Bot online.')

@client.event
async def on_message(message):
    message.content = message.content.lower()
    for word in keywords:
        if word in message.content:
            await message.delete()
            await message.channel.send("Woah there, you're not allowed to say that word here.", delete_after=3)
            break

@client.command()
async def ping(ctx):
    embed=discord.Embed(description=f"**Current Ping:**\n`{round(client.latency * 1000)}ms`", color=0x8151e2)
    await ctx.send(embed=embed)

@client.command()
@commands.has_role("Moderation Perms")
async def purge(ctx, amount=5):
    embed=discord.Embed(title="**SUCCESS**",description=f":white_check_mark: Purged {amount} total messages.", color=0x8151e2)
    await ctx.channel.purge(limit=amount)
    await ctx.send(embed=embed, delete_after=3)

@client.command()
@commands.has_role("Moderation Perms")
async def kick(ctx, member : discord.Member,*,reason = "No reason was provided."):
    embed3=discord.Embed(description=f"❌ Can't kick yourself.", color=0xff3939)
    if member == ctx.author:
            await ctx.send(embed=embed3)
            return
    embed=discord.Embed(description=f"You were kicked from the Luna Networks Discord Server.\nReason: {reason}", color=0xff3939)
    embed2=discord.Embed(title="**SUCCESS**",description=f":white_check_mark: Kicked {member.mention} for {reason}", color=0x8151e2)
    await ctx.send(embed=embed2, delete_after=3)
    await member.send(embed=embed)
    await member.kick(reason=reason)

@client.command()
@commands.has_role("Moderation Perms")
async def ban(ctx, member : discord.Member,*,reason = "No reason provided."):
    embed3=discord.Embed(description=f"❌ Can't ban yourself.", color=0xff3939)
    if member == ctx.author:
            await ctx.send(embed=embed3)
            return
    embed=discord.Embed(description=f"You were banned from the Luna Networks Discord Server\nReason: {reason}", color=0xff5f5f)
    embed2=discord.Embed(title="**SUCCESS**",description=f":white_check_mark: Banned {member.mention} for {reason}", color=0x8151e2)
    await ctx.send(embed=embed2, delete_after=3)
    await member.send(embed=embed, delete_after=3)
    await member.ban(reason=reason)

@client.command()
@commands.has_role("Moderation Perms")
async def mute(ctx, member: discord.Member, *, reason='No reason specified'):
    embed3=discord.Embed(description=f"❌ Can't mute yourself.", color=0xff3939)
    if member == ctx.author:
            await ctx.send(embed=embed3)
            return

    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, add_reactions=False)
    embed=discord.Embed(description=f"You were muted in the Luna Networks Discord Server\nReason: {reason}", color=0xff3939)
    embed2=discord.Embed(description=f":white_check_mark: Muted {member.mention} for {reason}", color=0x8151e2)        
    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(embed=embed2, delete_after=3)
    await member.send(embed=embed)

@client.command()
@commands.has_role("Moderation Perms")
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="muted")

    embed=discord.Embed(description=f"You were unmuted the Luna Networks Discord Server", color=0xff3939)
    embed2=discord.Embed(description=f":white_check_mark: Unmuted {member.mention}", color=0x8151e2)        
    await member.remove_roles(mutedRole)
    await ctx.send(embed=embed2, delete_after=3)
    await member.send(embed=embed)

keep_alive()
TOKEN = os.environ.get("DISCORD_BOT_SECRET")
client.run(TOKEN)