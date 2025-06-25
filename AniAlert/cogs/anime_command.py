import discord
from discord.ext import commands
from discord import app_commands
from providers import search_kitsu_anime

from cogs.anime_select import pick_anime_view
from cogs.search_for_anime import search_anime_input

from services.anime_service import get_full_anime_info

class add_anime_command(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name='search_anime', description='Search for animes')
  async def search_anime_slash(self, interaction: discord.Interaction, query: str):
    await interaction.response.defer(ephemeral=True)
    animes = get_full_anime_info(query)

    if not animes:
      await interaction.followup.send('❌ No results found.', ephemeral=True)
      return

    for anime in animes:
      embed = discord.Embed(
        title=f'🎬 {anime["title"]}',
        description=anime['synopsis'][:300] + '...',
        color=discord.Color.purple()
      )
      embed.add_field(name='📺 Type', value=anime['show_type'], inline=True)
      embed.add_field(name='⭐ Rating', value=str(anime['average_rating']), inline=True)
      embed.add_field(name='🎞️ Episodes', value=str(anime['episodes']), inline=True)
      embed.add_field(name='🗓️Airing', value=str(anime['airing']), inline=True)
      embed.add_field(name='MAL Rank', value=str(anime['ranking']), inline=True)
      # embed.add_field(name='Genres', value=str(anime['genres']), inline=True)
      embed.set_thumbnail(url=anime['image'])

      await interaction.followup.send(embed=embed, ephemeral=True)

  @app_commands.command(name='search_anime_modal', description='Open a modal to search for animes')
  async def search_anime_modal(self, interaction: discord.Interaction):
    modal = search_anime_input()
    await interaction.response.send_modal(modal)

  @commands.command()
  async def pick_animes(self, context):
    view = pick_anime_view()
    await context.send('Please select animes:', view=view)

async def setup(bot):
  await bot.add_cog(add_anime_command(bot))
