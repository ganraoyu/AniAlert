from typing import List, Optional

from discord.ext import commands
from discord import app_commands, Interaction

from services.anime_service import get_seasonal_anime_info
from utils.embed_builder import build_seasonal_anime_embed
from utils.button_builder import anime_buttons_view
from utils.choices import get_choices

MEDIA_TYPE_CHOICES, STATUS_TYPE_CHOICES, POPULAR_GENRE_TAG_CHOICES, GENRE_TYPE_CHOICES, YEAR_CHOICES, SEASON_CHOICES = get_choices()

def _fetch_seasonal_anime(page: int, results_shown: int, genres: Optional[str], media_type: Optional[str], year: Optional[int], season: Optional[str]) -> list:
  genres_list = [genres] if genres else []
  media_value = media_type if media_type else "all"
  return get_seasonal_anime_info(page, results_shown, genres_list, media_value, year, season)

async def _send_anime_embeds(interaction: Interaction, animes: List[dict]):
  for anime in animes:
    embed = build_seasonal_anime_embed(anime)
    buttons = anime_buttons_view(anime)
    await interaction.followup.send(embed=embed, view=buttons, ephemeral=True)

async def _send_no_results(interaction: Interaction, message: str = "⚠️ No anime found."):
  await interaction.followup.send(message, ephemeral=True)

class SeasonalAnimeLookUpCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name='seasonal_anime', description='Look up currently airing seasonal anime')
  @app_commands.describe(
    page='Which Page to search',
    results_shown='How many results to show',
    genres='Filter results by genres',
    media_type="Type of media",
    year='Year of the season',
    season='Season of the year'
  )
  @app_commands.choices(genres=POPULAR_GENRE_TAG_CHOICES, media_type=MEDIA_TYPE_CHOICES, year=YEAR_CHOICES, season=SEASON_CHOICES)
  async def seasonal_anime(
    self, 
    interaction: Interaction, 
    page: int, 
    results_shown: int, 
    genres: Optional[app_commands.Choice[str]] = None, 
    media_type: Optional[app_commands.Choice[str]] = None,
    year: Optional[app_commands.Choice[int]] = None,
    season: Optional[app_commands.Choice[str]] = None
    ):
    await interaction.response.defer(ephemeral=True)

    animes = _fetch_seasonal_anime(
      page,
      results_shown,
      genres.value if genres else None,
      media_type.value if media_type else None,
      year.value if year else None,
      season.value if season else None
    )

    if not animes:
      await _send_no_results(interaction)
      return

    await _send_anime_embeds(interaction, animes)
