import discord
import sys
import os
from utils.embed_builder import build_add_anime_embed, build_remove_anime_embed

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from db.database import cursor, conn


class CombinedAnimeButtonView(discord.ui.View):
  def __init__(self, anime: dict):
    super().__init__()
    self.anime = anime

  async def _get_user_and_guild_info(self, interaction: discord.Interaction):
    return (
      str(interaction.guild.id),
      str(interaction.guild.name),
      str(interaction.user.id),
      str(interaction.user.name)
    )

  @discord.ui.button(label='Add to notify list', style=discord.ButtonStyle.blurple)
  async def add_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    guild_id, guild_name, user_id, user_name = await self._get_user_and_guild_info(interaction)
    anime_name = self.anime.get('title', 'Unknown Title')
    unix_air_time = self.anime.get('airingAt_unix', 0)
    iso_air_time = self.anime.get('airingAt_iso', '1970-01-01T00:00:00')
    image = self.anime.get('image', '')
    next_episode = int(self.anime.get('episodes', 0)) + 1

    if unix_air_time == 0 or iso_air_time == '1970-01-01T00:00:00':
      await interaction.response.send_message(
        f"⚠️ **{anime_name}** has finished airing and has no more upcoming episodes.",
        ephemeral=True
      )
      return

    cursor.execute(
      """
      SELECT 1 FROM anime_notify_list
      WHERE guild_id = ? AND guild_name = ? AND user_id = ? AND user_name = ? AND anime_name = ?
      """,
      (guild_id, guild_name, user_id, user_name, anime_name)
    )
    if cursor.fetchone():
      await interaction.response.send_message(
        f"⚠️ **{anime_name}** is already in your notify list.",
        ephemeral=True
      )
      return

    cursor.execute(
      """
      INSERT INTO anime_notify_list (
        guild_id, guild_name, user_id, user_name,
        anime_name, episode, unix_air_time, iso_air_time, image
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      """,
      (guild_id, guild_name, user_id, user_name,
       anime_name, next_episode, unix_air_time, iso_air_time, image)
    )
    conn.commit()

    embed = build_add_anime_embed(self.anime)
    await interaction.response.send_message(
      content=f"✅ **{anime_name}** added to your watchlist.",
      embed=embed,
      ephemeral=True
    )

  @discord.ui.button(label='Remove from notify list', style=discord.ButtonStyle.red)
  async def remove_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    guild_id, guild_name, user_id, user_name = await self._get_user_and_guild_info(interaction)
    anime_name = self.anime.get('title', 'Unknown Title')

    cursor.execute(
      """
      SELECT 1 FROM anime_notify_list
      WHERE guild_id = ? AND guild_name = ? AND user_id = ? AND user_name = ? AND anime_name = ?
      """,
      (guild_id, guild_name, user_id, user_name, anime_name)
    )
    if not cursor.fetchone():
      await interaction.response.send_message(
        f"⚠️ **{anime_name}** wasn't in your notify list.",
        ephemeral=True
      )
      return

    cursor.execute(
      """
      DELETE FROM anime_notify_list
      WHERE guild_id = ? AND guild_name = ? AND user_id = ? AND user_name = ? AND anime_name = ?
      """,
      (guild_id, guild_name, user_id, user_name, anime_name)
    )
    conn.commit()

    embed = build_remove_anime_embed(self.anime)
    await interaction.response.send_message(
      content=f"✅ **{anime_name}** removed from your watchlist.",
      embed=embed,
      ephemeral=True
    )

def anime_buttons_view(anime: dict):
  return CombinedAnimeButtonView(anime)
