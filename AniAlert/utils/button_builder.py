import discord
from typing import Tuple
from utils.embed_builder import build_add_anime_embed, build_remove_anime_embed
from db.database import cursor, conn


class CombinedAnimeButtonView(discord.ui.View):
  def __init__(self, anime: dict):
    super().__init__()
    self.anime = anime

  async def _get_user_and_guild_info(self, interaction: discord.Interaction) -> Tuple[str, str, str, str]:
    """Extract guild and user info from interaction."""
    return (
      str(interaction.guild.id),
      str(interaction.guild.name),
      str(interaction.user.id),
      str(interaction.user.name),
    )

  @discord.ui.button(label='Add to notify list', style=discord.ButtonStyle.blurple)
  async def add_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
    guild_id, guild_name, user_id, user_name = await self._get_user_and_guild_info(interaction)
    anime_name = self.anime.get('title', 'Unknown Title')
    unix_air_time = self.anime.get('airingAt_unix', 0)
    iso_air_time = self.anime.get('airingAt_iso', '1970-01-01T00:00:00')
    image = self.anime.get('image', '')
    next_episode = int(self.anime.get('episodes', 0)) + 1

    if unix_air_time == 0 or iso_air_time == '1970-01-01T00:00:00':
      await interaction.response.send_message(
        f"⚠️ **{anime_name}** has finished airing and has no more upcoming episodes.",
        ephemeral=True,
      )
      return

    query_params = (guild_id, guild_name, user_id, user_name, anime_name)

    cursor.execute(
      """
      SELECT 1 FROM anime_notify_list
      WHERE guild_id = ? AND guild_name = ? AND user_id = ? AND user_name = ? AND anime_name = ?
      """,
      query_params,
    )
    if cursor.fetchone():
      await interaction.response.send_message(
        f"⚠️ **{anime_name}** is already in your notify list.",
        ephemeral=True,
      )
      return

    cursor.execute(
      """
      INSERT INTO anime_notify_list (
        guild_id, guild_name, user_id, user_name,
        anime_name, episode, unix_air_time, iso_air_time, image
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
      """,
      (*query_params, next_episode, unix_air_time, iso_air_time, image),
    )
    conn.commit()

    embed = build_add_anime_embed(self.anime)
    await interaction.response.send_message(
      content=f"✅ **{anime_name}** added to your watchlist.",
      embed=embed,
      ephemeral=True,
    )

  @discord.ui.button(label='Remove from notify list', style=discord.ButtonStyle.red)
  async def remove_button(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
    guild_id, guild_name, user_id, user_name = await self._get_user_and_guild_info(interaction)
    anime_name = self.anime.get('title', 'Unknown Title')
    query_params = (guild_id, guild_name, user_id, user_name, anime_name)

    cursor.execute(
      """
      SELECT 1 FROM anime_notify_list
      WHERE guild_id = ? AND guild_name = ? AND user_id = ? AND user_name = ? AND anime_name = ?
      """,
      query_params,
    )
    if not cursor.fetchone():
      await interaction.response.send_message(
        f"⚠️ **{anime_name}** wasn't in your notify list.",
        ephemeral=True,
      )
      return

    cursor.execute(
      """
      DELETE FROM anime_notify_list
      WHERE guild_id = ? AND guild_name = ? AND user_id = ? AND user_name = ? AND anime_name = ?
      """,
      query_params,
    )
    conn.commit()

    embed = build_remove_anime_embed(self.anime)
    await interaction.response.send_message(
      content=f"✅ **{anime_name}** removed from your watchlist.",
      embed=embed,
      ephemeral=True,
    )

class GuessAnimeButton(discord.ui.Button):
  def __init__(self, label: str, correct_answer: str, row: int):
    super().__init__(label=label, style=discord.ButtonStyle.primary, row=row)
    self.correct_answer = correct_answer

  async def callback(self, interaction: discord.Interaction):
    if self.label == self.correct_answer:
      await interaction.response.send_message("✅ Correct!", ephemeral=True)
    else:
      await interaction.response.send_message(
        f"❌ Nope! The correct answer was: **{self.correct_answer}**",
        ephemeral=True
      )

    self.view.stop()
    for child in self.view.children:
      child.disabled = True
    await interaction.message.edit(view=self.view)

class GuessAnimeButtonView(discord.ui.View):
  def __init__(self, choices: list[str], correct_answer: str, timeout: int = 60):
    super().__init__(timeout=timeout)
    for index, choice in enumerate(choices):
      self.add_item(GuessAnimeButton(label=choice, correct_answer=correct_answer, row=index))

def anime_buttons_view(anime: dict) -> CombinedAnimeButtonView:
  return CombinedAnimeButtonView(anime)

def guess_anime_buttons_view(choices: list[str], correct_answer: str, timeout: int = 60) -> GuessAnimeButtonView:
  return GuessAnimeButtonView(choices, correct_answer, timeout)