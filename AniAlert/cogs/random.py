from discord.ext import commands
from discord import app_commands, Interaction
from services.anime_service import get_random_anime_suggestion

from utils.embed_builder import build_random_anime_embed

class RandomAnimeCog(commands.Cog):

  GENRES = [
    app_commands.Choice(name='Action', value='Action'),
    app_commands.Choice(name='Adventure', value='Adventure'),
    app_commands.Choice(name='Comedy', value='Comedy'),
    app_commands.Choice(name='Drama', value='Drama'),
    app_commands.Choice(name='Ecchi', value='Ecchi'),
    app_commands.Choice(name='Fantasy', value='Fantasy'),
    app_commands.Choice(name='Horror', value='Horror'),
    app_commands.Choice(name='Mahou Shoujo', value='Mahou Shoujo'),
    app_commands.Choice(name='Mecha', value='Mecha'),
    app_commands.Choice(name='Music', value='Music'),
    app_commands.Choice(name='Mystery', value='Mystery'),
    app_commands.Choice(name='Psychological', value='Psychological'),
    app_commands.Choice(name='Romance', value='Romance'),
    app_commands.Choice(name='Sci-Fi', value='Sci-Fi'),
    app_commands.Choice(name='Slice of Life', value='Slice of Life'),
    app_commands.Choice(name='Sports', value='Sports'),
    app_commands.Choice(name='Supernatural', value='Supernatural'),
    app_commands.Choice(name='Thriller', value='Thriller'),
    app_commands.Choice(name='Vampire', value='Vampire'),
  ]

  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name='random_anime_suggestion', description='Get a random anime based on genre')
  @app_commands.describe(genres='Enter genres separated by commas (e.g. Action,Adventure)')
  async def random(self, interaction: Interaction, genres: str):
    await interaction.response.defer()

    genre_list = [g.strip() for g in genres.split(',') if g.strip()]

    anime = get_random_anime_suggestion(genre_list)

    embed = build_random_anime_embed(anime)

    await interaction.followup.send(embed=embed, ephemeral=True)