import discord
import sys
import os
from datetime import datetime
from utils.interaction_helper import get_user_and_guild_ids
from utils.embed_builder import build_add_anime_embed, build_remove_anime_embed

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from db.database import cursor, conn

class CombinedAnimeButtonView(discord.ui.View):
  def __init__(self, anime: dict):
    super().__init__()
    self.anime = anime

  @discord.ui.button(label='Add to notify list', style=discord.ButtonStyle.blurple)
  async def add_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    guild_id = str(interaction.guild.id)
    guild_name = str(interaction.guild.name)
    user_id = str(interaction.user.id)
    user_name = str(interaction.user.name)
    anime_name = self.anime['title']
    unix_air_time = self.anime['airingAt_unix']
    iso_air_time = self.anime['airingAt_iso']

    cursor.execute(
      "SELECT 1 FROM anime_notify_list WHERE guild_id = ? AND guild_name = ? AND user_id = ? AND user_name = ? AND anime_name = ?",
      (guild_id, guild_name, user_id, user_name, anime_name)
    )

    if cursor.fetchone(): 
      await interaction.response.send_message(
        f"⚠️ **{anime_name}** is already in your notify list.",
        ephemeral=True
      )
      return

    cursor.execute(
      "INSERT INTO anime_notify_list (guild_id, guild_name, user_id, user_name, anime_name, unix_air_time, iso_air_time) VALUES (?, ?, ?, ?, ?, ?, ?)",
      (guild_id, guild_name, user_id, user_name, anime_name, unix_air_time, iso_air_time)
    )

    embed = build_add_anime_embed(self.anime)
    conn.commit()

    await interaction.response.send_message(
      content=f"✅ **{anime_name}** added to your watchlist. (User: {user_name})",
      embed=embed,
      ephemeral=True
    )

  @discord.ui.button(label='Remove from notify list', style=discord.ButtonStyle.red)
  async def remove_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    guild_id = str(interaction.guild.id)
    guild_name = str(interaction.guild.name)
    user_id = str(interaction.user.id)
    user_name = str(interaction.user.name)
    anime_name = self.anime['title']

    cursor.execute(
      "SELECT 1 FROM anime_notify_list WHERE guild_id = ? AND guild_name = ? AND user_id = ? AND user_name = ? AND anime_name = ?",
      (guild_id, guild_name, user_id, user_name, anime_name)
    )

    if not cursor.fetchone():
      await interaction.response.send_message(
        f"⚠️ **{anime_name}** wasn't in your notify list.",
        ephemeral=True
      )
      return

    cursor.execute(
      "DELETE FROM anime_notify_list WHERE guild_id = ? AND guild_name = ? AND user_id = ? AND user_name = ? AND anime_name = ?",
      (guild_id, guild_name, user_id, user_name, anime_name)
    )
    conn.commit()

    embed = build_remove_anime_embed(self.anime)

    await interaction.response.send_message(
      f"✅ **{anime_name}** removed from your watchlist. (User: {user_name})",
      embed=embed,
      ephemeral=True
    )

def anime_buttons_view(anime: dict):
  return CombinedAnimeButtonView(anime)
