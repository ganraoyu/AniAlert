import discord
from typing import Tuple
import json
from utils.embed_builder import build_add_anime_embed, build_remove_anime_embed
from db.database import cursor, conn

async def check_anime_exists(interaction, query_params, anime_name) -> bool:
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
    return True

  return False

def add_anime_table(query_params, episodes, unix_air_time, iso_air_time, image, episodes_list_json):
  cursor.execute(
    """
    INSERT INTO anime_notify_list (
      guild_id, guild_name, user_id, user_name,
      anime_name, episode, unix_air_time, iso_air_time, image, episodes_list
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (*query_params, episodes, unix_air_time, iso_air_time, image, episodes_list_json),
  )

def delete_anime_table(query_params):
  cursor.execute(
    """
    DELETE FROM anime_notify_list
    WHERE guild_id = ? AND guild_name = ? AND user_id = ? AND user_name = ? AND anime_name = ?
    """,
    query_params,
  ) 

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
    episodes = self.anime.get('episodes', 0) + 1
    episodes_list = self.anime.get('episodes_list', [])
    image = self.anime.get('image', '')

    query_params = (guild_id, guild_name, user_id, user_name, anime_name)
    await check_anime_exists(interaction, query_params, anime_name)

    episodes_list_json = json.dumps(episodes_list, indent=2, ensure_ascii=False)

    unix_air_time = self.anime.get('airingAt_unix', 0)
    iso_air_time = self.anime.get('airingAt_iso', '')
    
    add_anime_table(query_params, episodes, unix_air_time, iso_air_time, image, episodes_list_json)

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

    await check_anime_exists(interaction, query_params, anime_name)

    delete_anime_table(query_params)

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
    view: GuessAnimeButtonView = self.view

    if self.label == self.correct_answer:
      await interaction.response.send_message("✅ Correct!", ephemeral=True)
      view.stop()  # stop the view to disable buttons
    else:
      if view.guess_count < 1:
        await interaction.response.send_message("❌ Nope! Try again!", ephemeral=True)
        view.guess_count += 1
        return  # stop here, don't send more messages
      else:
        await interaction.response.send_message(
          f"❌ Nope! The correct answer was: **{self.correct_answer}**", ephemeral=True
        )
        view.stop()

    # Disable all buttons once game ends
    for child in view.children:
      child.disabled = True
    try:
      await interaction.message.edit(view=view)
    except discord.NotFound:
      pass

class GuessAnimeButtonView(discord.ui.View):
  def __init__(self, choices: list[str], correct_answer: str, timeout: int = 60):
    super().__init__(timeout=timeout)
    self.correct_answer = correct_answer
    self.guess_count = 0

    for index, choice in enumerate(choices):
      self.add_item(GuessAnimeButton(label=choice, correct_answer=correct_answer, row=index))

def anime_buttons_view(anime: dict) -> CombinedAnimeButtonView:
  return CombinedAnimeButtonView(anime)

def guess_anime_buttons_view(choices: list[str], correct_answer: str, timeout: int = 60) -> GuessAnimeButtonView:
  return GuessAnimeButtonView(choices, correct_answer, timeout)