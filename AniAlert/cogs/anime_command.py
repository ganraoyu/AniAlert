import discord
from discord.ext import commands
from discord import app_commands

from cogs.anime_select import pick_anime_view
from cogs.search_for_anime import search_anime_input

class add_anime_command(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  @app_commands.command(name="search_anime", description="Search for animes")
  async def search_anime_slash(self, interaction: discord.Interaction, query: str):
      await interaction.response.defer(ephemeral=True)

      await interaction.followup.send(f"Searching for anime: {query}", ephemeral=True)
  @app_commands.command(name="search_anime_modal", description="Open a modal to search for animes")
  async def search_anime_modal(self, interaction: discord.Interaction):
      modal = search_anime_input()
      await interaction.response.send_modal(modal)  

  @commands.command()
  async def pick_animes(self, context):
      view = pick_anime_view()
      await context.send("Please select animes:", view=view)
      
async def setup(bot):
  await bot.add_cog(add_anime_command(bot))
