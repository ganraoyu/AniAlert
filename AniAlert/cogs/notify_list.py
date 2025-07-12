from typing import List, Optional
import json
from discord.ext import commands
from discord import app_commands, Interaction

from utils.embed_builder import build_anime_notify_list_embed

from utils.interaction_helper import get_user_and_guild_ids

class CheckNotifyListCog(commands.Cog):
  def __init__(self, bot, cursor):
    self.bot = bot
    self.cursor = cursor

  @app_commands.command(name='list', description='Check notify list')
  @app_commands.describe(
    id='Choose the anime to view its notify list',
    full_list='Show all upcoming episodes instead of just the next one'
  )
  @app_commands.choices(
    full_list=[
      app_commands.Choice(name='True', value='True'),
      app_commands.Choice(name='False', value='False')
    ]
  )
  async def check_notify_list(
    self, 
    interaction: Interaction,
    id: Optional[int] = None,
    full_list: Optional[str] = 'False'
    ):
    await interaction.response.defer(ephemeral=True)
    user_id, guild_id = self._get_user_guild_ids(interaction)

    results = self._fetch_notify_list(user_id, guild_id)

    if not results:
      await interaction.followup.send(
        "⚠️ Your notify list is empty.", ephemeral=True
      )
      return

    embeds = self._create_notify_list_embeds(results, full_list)
    await interaction.followup.send(embeds=embeds, ephemeral=True)

  def _get_user_guild_ids(self, interaction: Interaction) -> tuple[int, int]:
    user_id, guild_id = get_user_and_guild_ids(interaction)
    return int(user_id), int(guild_id)

  def _fetch_notify_list(self, user_id: int, guild_id: int) -> List[tuple]:
    query = 'SELECT * FROM anime_notify_list WHERE user_id = ? AND guild_id = ?'
    self.cursor.execute(query, (user_id, guild_id))
    return self.cursor.fetchall()

  def _get_notify_list_embed(self, anime, full_list: str = 'False', ep: dict = None):
    id_ = anime[0]
    anime_name = anime[5]
    image = anime[9]

    if full_list == 'True' and ep is not None:
      episode = ep['episode']
      iso_air_time = ep['airingAt_iso']
    elif full_list == 'False':
      episode = anime[6]
      iso_air_time = anime[8]

    embed = build_anime_notify_list_embed(anime_name, id_, episode, iso_air_time, image)
    return embed

  def _create_notify_list_embeds(self, results: List[tuple], full_list: str = 'False'):
    embeds = []

    if full_list == 'False':
      for anime in results:
        embed = self._get_notify_list_embed(anime, full_list='False')
        embeds.append(embed)
    elif full_list == 'True':
      # Full list: iterate episodes inside each anime
      for anime in results:
        episodes_list = json.loads(anime[10])
        for ep in episodes_list:
          embed = self._get_notify_list_embed(anime, full_list, ep)
          embeds.append(embed)

    return embeds

