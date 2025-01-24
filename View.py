import disnake, os
from disnake.ext import commands
from disnake.ext.commands import CommandSyncFlags
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('token_bot')

client = commands.Bot(
    command_prefix=commands.when_mentioned_or("."),
    test_guilds=[673119818404200448],
    intents=disnake.Intents.all(),
    command_sync_flags=CommandSyncFlags(sync_commands_debug=True)
)

@client.command(name="reload")
async def r(ctx: disnake.Message, cog: str):
    if ctx.author.id != 399538331756658689:
        return
    
    cogs = ["view", "dump"]
    if cog not in cogs:
        await ctx.send(f"{cog} doesn't exist.")
        
    client.reload_extension(f"cogs.{cog}")

client.load_extensions("cogs")
client.run(token)