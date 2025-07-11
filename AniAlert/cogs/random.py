from discord.ext import commands
from discord import app_commands, Interaction
from services.anime_service import get_random_anime_suggestion

from utils.embed_builder import build_random_anime_embed
from utils.choices import get_choices

MEDIA_TYPE_CHOICES, STATUS_TYPE_CHOICES, POPULAR_GENRE_TAG_CHOICES, GENRE_TYPE_CHOICES, YEAR_CHOICES, SEASON_CHOICES = get_choices()

class RandomAnimeCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name='random_anime_suggestion', description='Get a random anime based on genre')
  @app_commands.describe(genres='Filter by genres', media_type="Type of media",)
  @app_commands.choices(genres=POPULAR_GENRE_TAG_CHOICES,  media_type=MEDIA_TYPE_CHOICES)
  async def random(
    self, 
    interaction: Interaction,
    genres: str = None, 
    media_type: str = None
    ):
    await interaction.response.defer()
    
    if genres:
      genre_list = [g.strip() for g in genres.split(',') if g.strip()]
    else:
      genre_list = 'all'
      
    anime = get_random_anime_suggestion(genre_list, media_type)

    embed = build_random_anime_embed(anime)

    await interaction.followup.send(embed=embed, ephemeral=True)