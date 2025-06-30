import discord
import sys
import os
from utils.interaction_helper import get_user_and_guild_ids
from utils.embed_builder import build_add_anime_embed

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from db.database import cursor, conn

class CombinedAnimeButtonView(discord.ui.View):
  def __init__(self, anime: dict):
    super().__init__()
    self.anime = anime

  @discord.ui.button(label="Add to notify list", style=discord.ButtonStyle.green)
  async def add_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    guild_id = str(interaction.guild.id)
    user_id = str(interaction.user.id)
    anime_name = self.anime['title']


    cursor.execute(
      "SELECT 1 FROM anime_notify_list WHERE guild_id = ? AND user_id = ? AND anime_name = ?",
      (guild_id, user_id, anime_name)
    )
    if cursor.fetchone():
      await interaction.response.send_message(
        f"⚠️ **{anime_name}** is already in your notify list.",
        ephemeral=True
      )
      return

    cursor.execute(
      "INSERT INTO anime_notify_list (guild_id, user_id, anime_name) VALUES (?, ?, ?)",
      (guild_id, user_id, anime_name)
    )

    embed = build_add_anime_embed(self.anime)
    conn.commit()

    await interaction.response.send_message(
      f"✅ **{anime_name}** added to your watchlist. (User ID: {user_id})",
      ephemeral=True
    )
    await interaction.followup.send(embed=embed, ephemeral=True)

  @discord.ui.button(label="Remove from notify list", style=discord.ButtonStyle.red)
  async def remove_button(self, interaction: discord.Interaction, button: discord.ui.Button):
    guild_id = str(interaction.guild.id)
    user_id = str(interaction.user.id)
    anime_name = self.anime['title']


    cursor.execute(
      "SELECT 1 FROM anime_notify_list WHERE guild_id = ? AND user_id = ? AND anime_name = ?",
      (guild_id, user_id, anime_name)
    )

    if not cursor.fetchone():
      await interaction.response.send_message(
        f"⚠️ **{anime_name}** wasn't in your notify list.",
        ephemeral=True
      )
      return

    cursor.execute(
      "DELETE FROM anime_notify_list WHERE guild_id = ? AND user_id = ? AND anime_name = ?",
      (guild_id, user_id, anime_name)
    )
    conn.commit()

    await interaction.response.send_message(
      f"✅ **{anime_name}** removed from your watchlist. (User ID: {user_id})",
      ephemeral=True
    )

def anime_buttons_view(anime: dict):
  return CombinedAnimeButtonView(anime)
