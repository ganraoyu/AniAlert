from typing import List, Optional

from discord.ext import commands
from discord import app_commands, Interaction

from services.anime_service import get_full_anime_info
from utils.embed_builder import build_search_anime_embed
from utils.embed_builder import build_remove_anime_embed
from utils.choices import get_choices
from utils.button_builder import anime_buttons_view

MEDIA_TYPE_CHOICES, STATUS_TYPE_CHOICES, POPULAR_GENRE_TAG_CHOICES, GENRE_TYPE_CHOICES = get_choices()

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

    animes = self._search_anime(name, results_shown, media_type, status)
    if not animes:
      await interaction.followup.send("⚠️ No anime found.", ephemeral=True)
      return

    await self._send_results(interaction, animes)

  def _search_anime(self, name: str, results: int, media_type: Optional[app_commands.Choice[str]], status: Optional[app_commands.Choice[str]]) -> list:
    media_value = media_type.value if media_type else "all"
    status_value = status.value if status else "all"
    return get_full_anime_info(name, results, media_value, status_value)

  async def _send_results(self, interaction: Interaction, animes: List[dict]):
    for anime in animes:
      embed = build_search_anime_embed(anime)
      buttons = anime_buttons_view(anime)
      await interaction.followup.send(embed=embed, view=buttons, ephemeral=True)

class RemoveAnimeCog(commands.Cog):

  def __init__(self, bot, cursor, conn):
    self.bot = bot
    self.cursor = cursor
    self.conn = conn

  def _fetch_notify_list(self, id: int):
    self.cursor.execute('SELECT * FROM anime_notify_list WHERE id = ?', (id,))
    return self.cursor.fetchone()

  @app_commands.command(name='remove_anime', description='Remove animes from notify list')
  @app_commands.describe(id='Enter anime ID to remove')
  async def remove_anime(self, interaction: Interaction, id: int):
    await interaction.response.defer(ephemeral=True)

    result = self._fetch_notify_list(id)

    if result:
      anime_dict = {
        'id': result[0],
        'guild_id': result[1],
        'guild_name': result[2],
        'user_id': result[3],
        'user_name': result[4],
        'title': result[5],
        'episode': result[6],
        'unix_air_time': result[7],
        'iso_air_time': result[8],
        'image': result[9]
      }

      embed = build_remove_anime_embed(anime_dict)
      self.cursor.execute('DELETE FROM anime_notify_list WHERE id = ?', (id,))
      await interaction.followup.send(embed=embed, ephemeral=True)
    else:
      await interaction.followup.send(
        f"⚠️ No anime found with ID `{id}`.",
        ephemeral=True
      )

    self.conn.commit()
