from typing import List

from discord.ext import commands
from discord import app_commands, Interaction

from utils.embed_builder import build_anime_notify_list_embed


from utils.interaction_helper import get_user_and_guild_ids

class CheckNotifyListCog(commands.Cog):

  def __init__(self, bot, cursor):
    self.bot = bot
    self.cursor = cursor

  @app_commands.command(name='list', description='Check notify list')
  async def check_notify_list(self, interaction: Interaction):
    await interaction.response.defer(ephemeral=True)
    user_id, guild_id = self._get_user_guild_ids(interaction)

    results = self._fetch_notify_list(user_id, guild_id)

    if not results:
      await interaction.followup.send(
        "⚠️ Your notify list is empty.", ephemeral=True
      )
      return

    embeds = self._create_notify_list_embeds(results)
    await interaction.followup.send(embeds=embeds, ephemeral=True)

  def _get_user_guild_ids(self, interaction: Interaction) -> tuple[int, int]:
    user_id, guild_id = get_user_and_guild_ids(interaction)
    return int(user_id), int(guild_id)

  def _fetch_notify_list(self, user_id: int, guild_id: int) -> List[tuple]:
    query = 'SELECT * FROM anime_notify_list WHERE user_id = ? AND guild_id = ?'
    self.cursor.execute(query, (user_id, guild_id))
    return self.cursor.fetchall()

  def _create_notify_list_embeds(self, results: List[tuple]):
    embeds = []
    for anime in results:
      id = anime[0]
      anime_name = anime[5]
      episode = anime[6]
      iso_air_time = anime[8]
      image = anime[9]
      embed = build_anime_notify_list_embed(anime_name, id, episode, iso_air_time, image)
      embeds.append(embed)
    return embeds
