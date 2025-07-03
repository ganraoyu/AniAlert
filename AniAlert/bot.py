import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
  print(f"Logged in as {bot.user}!")
  try:
    await bot.load_extension("cogs.commands")
    print("Successfully loaded commands cog!") 
    
    print("Syncing application commands...")
    await bot.tree.sync()
    print("Application commands synced successfully!")
      
  except Exception as e:
    print(f"Failed to load commands cog: {e}")

@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandNotFound):
      await context.send("Command not found. Please check the command and try again.")
    else:
      await context.send(f"An error occurred: {error}")
      print(f"Error in command {context.command}: {error}")
        
bot.run(DISCORD_BOT_TOKEN)
