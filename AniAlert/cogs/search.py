from typing import List, Optional

from discord.ext import commands
from discord import app_commands, Interaction

from services.anime_service import get_full_anime_info
from utils.embed_builder import build_search_anime_embed
from utils.embed_builder import build_remove_anime_embed
from utils.choices import get_choices
from utils.button_builder import anime_buttons_view

MEDIA_TYPE_CHOICES, STATUS_TYPE_CHOICES, POPULAR_GENRE_TAG_CHOICES, GENRE_TYPE_CHOICES, YEAR_CHOICES, SEASON_CHOICES = get_choices()


def _search_anime(name: str, results: int, media_type: Optional[app_commands.Choice[str]], status: Optional[app_commands.Choice[str]]) -> list:
  media_value = media_type.value if media_type else "all"
  status_value = status.value if status else "all"
  return get_full_anime_info(name, results, media_value, status_value)

async def _send_results(interaction: Interaction, animes: List[dict]):
  for anime in animes:
    embed = build_search_anime_embed(anime)
    buttons = anime_buttons_view(anime)
    await interaction.followup.send(embed=embed, view=buttons, ephemeral=True)

class AllAnimeSearchCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name='search_anime', description='Search for animes')
  @app_commands.describe(
    name="Anime name to search",
    results_shown="How many results to show",
    media_type="Type of media",
    status='Status of current anime'
  )
  @app_commands.choices(media_type=MEDIA_TYPE_CHOICES, status=STATUS_TYPE_CHOICES)
  async def search(
    self,
    interaction: Interaction,
    name: str,
    results_shown: int,
    media_type: Optional[app_commands.Choice[str]] = None,
    status: Optional[app_commands.Choice[str]] = None
  ):
    await interaction.response.defer(ephemeral=True)

    animes = _search_anime(name, results_shown, media_type, status)
    if not animes:
      await interaction.followup.send("⚠️ No anime found.", ephemeral=True)
      return

    await _send_results(interaction, animes)

