import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from db.database import cursor, conn

from typing import Optional
from discord.ext import commands, tasks
from discord import app_commands, Interaction

from services.anime_service import get_full_anime_info
from services.anime_service import get_seasonal_anime_info
from services.anime_service import get_random_anime_suggestion
from services.airing_checker import check_notify_list, check_if_aired 

from utils.embed_builder import build_search_anime_embed
from utils.embed_builder import build_seasonal_anime_embed
from utils.embed_builder import build_anime_notify_list_embed
from utils.embed_builder import build_anime_airing_notification_embed
from utils.embed_builder import build_remove_anime_embed
from utils.embed_builder import build_random_anime_embed

from utils.interaction_helper import get_user_and_guild_ids
from utils.button_builder import anime_buttons_view

from views.search_modal import SearchAnimeInput
from views.pick_anime_view import PickAnimeView

class SeasonalAnimeLookUpCog(commands.Cog): 
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name='seasonal_anime', description='Look up currently airing seasonal anime')
  async def seasonal_anime(self, interaction: Interaction, page: int, results_shown: int):
    await interaction.response.defer(ephemeral=True)

    animes = self._fetch_seasonal_anime(page, results_shown)

    if not animes:
      await self._send_no_results(interaction)
      return

    await self._send_anime_embeds(interaction, animes)

  def _fetch_seasonal_anime(self, page: int, results_shown: int) -> list:
    return get_seasonal_anime_info(page, results_shown)

  async def _send_anime_embeds(self, interaction: Interaction, animes: list[dict]):
    for anime in animes:
      embed = build_seasonal_anime_embed(anime)
      buttons = anime_buttons_view(anime)
      await interaction.followup.send(embed=embed, view=buttons, ephemeral=True)

  async def _send_no_results(self, interaction: Interaction, message: str = "⚠️ No anime found."):
    await interaction.followup.send(message, ephemeral=True)

class AllAnimeSearchCog(commands.Cog):
  MEDIA_TYPE_CHOICES = [
    app_commands.Choice(name='All', value='all'),
    app_commands.Choice(name='TV', value='TV'),
    app_commands.Choice(name='Movie', value='movie'),
    app_commands.Choice(name='OVA', value='OVA'),
    app_commands.Choice(name='ONA', value='ONA'),
    app_commands.Choice(name='Special', value='special'),
  ]

  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name='search_anime', description='Search for animes')
  @app_commands.describe(
    name="Anime name to search",
    results_shown="How many results to show",
    media_type="Type of media"
  )
  @app_commands.choices(media_type=MEDIA_TYPE_CHOICES)
  async def search(
    self,
    interaction: Interaction,
    name: str,
    results_shown: int,
    media_type: Optional[app_commands.Choice[str]] = None
  ):
    await interaction.response.defer(ephemeral=True)

    animes = self._search_anime(name, results_shown, media_type)
    if not animes:
      await interaction.followup.send("⚠️ No anime found.", ephemeral=True)
      return

    await self._send_results(interaction, animes)

  def _search_anime(self, name: str, results: int, media_type: Optional[app_commands.Choice[str]]) -> list:
    media_value = media_type.value if media_type else "all"
    return get_full_anime_info(name, results, media_value)

  async def _send_results(self, interaction: Interaction, animes: list[dict]):
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

  def _fetch_notify_list(self, user_id: int, guild_id: int) -> list[tuple]:
    query = 'SELECT * FROM anime_notify_list WHERE user_id = ? AND guild_id = ?'
    self.cursor.execute(query, (user_id, guild_id))
    return self.cursor.fetchall()

  def _create_notify_list_embeds(self, results: list[tuple]):
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

class NotifyAnimeAiredCog(commands.Cog):
  def __init__(self, bot, cursor, conn):
    self.bot = bot
    self.cursor = cursor
    self.conn = conn
    self.check_airing.start()

  @tasks.loop(minutes=1)
  async def check_airing(self):
    self.cursor.execute('SELECT DISTINCT user_id, guild_id FROM anime_notify_list')
    user_guild_pairs = self.cursor.fetchall()

    for user_id, guild_id in user_guild_pairs:
      await self._process_user_guild_pair(user_id, guild_id)

  async def _process_user_guild_pair(self, user_id, guild_id):
    anime_list = check_notify_list(user_id, guild_id, self.cursor)
    animes_aired = check_if_aired(anime_list)
    if not animes_aired:
      return

    guild = self.bot.get_guild(guild_id)
    if not guild:
      return

    channel = self._get_notification_channel(guild)
    if not channel:
      return

    for anime in animes_aired:
      await self._handle_anime_notification(anime, user_id, channel)

  def _get_notification_channel(self, guild):
    return next(
      (ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages),
      None
    )

  async def _handle_anime_notification(self, anime, user_id, channel):
    anime_id = anime['anime_id']
    anime_name = anime['anime_name']
    image_url = anime['image']

    new_data = get_full_anime_info(anime_name)

    if not new_data or not new_data[0].get('airingAt_unix'):
      await self._handle_final_episode(anime_id, anime_name, user_id, channel)
      return

    await self._send_airing_notification(anime_name, user_id, image_url, channel)
    self._update_airing_time(anime_id, new_data[0])

    self.conn.commit()

  async def _handle_final_episode(self, anime_id, anime_name, user_id, channel):
    self.cursor.execute('DELETE FROM anime_notify_list WHERE id = ?', (anime_id,))
    await channel.send(
      content=(
        f"<@{user_id}> 🔔 **The final episode of _{anime_name}_ just aired!**\n"
        "It has now been removed from your notify list."
      )
    )

  async def _send_airing_notification(self, anime_name, user_id, image_url, channel):
    embed = build_anime_airing_notification_embed(
      anime_name=anime_name,
      image_url=image_url,
      user_id=user_id
    )
    await channel.send(content=f"<@{user_id}>", embed=embed)

  def _update_airing_time(self, anime_id, anime_data):
    self.cursor.execute(
      'UPDATE anime_notify_list SET unix_air_time = ?, iso_air_time = ? WHERE id = ?',
      (
        anime_data['airingAt_unix'],
        anime_data.get('airingAt_iso'),
        anime_id
      )
    )

class ClearNotifyListCog(commands.Cog):
  def __init__(self, bot, cursor, conn):
    self.bot = bot
    self.cursor = cursor
    self.conn = conn

  @app_commands.command(name='clear_list')
  async def clear(self, interaction: Interaction):
    await interaction.response.defer(ephemeral=True)

    user_id, guild_id = get_user_and_guild_ids(interaction)
    user_id, guild_id = int(user_id), int(guild_id)
    deleted_count = self._delete_notify_list(user_id, guild_id)

    if deleted_count == 0:
      await interaction.followup.send(
        "⚠️ Your notify list is empty.", ephemeral=True
      )
      return

    await interaction.followup.send(
      content=(
        "✅ **All your anime notifications have been successfully removed!**\n"
        "You will no longer receive alerts for any anime from your notify list."
      ),
      ephemeral=True
    )

  def _delete_notify_list(self, user_id: int, guild_id: int) -> int:
    query = 'DELETE FROM anime_notify_list WHERE guild_id = ? AND user_id = ?'
    self.cursor.execute(query, (guild_id, user_id))
    self.conn.commit()
    return self.cursor.rowcount

class CharacterSearchCog(commands.Cog):
  pass

class RandomAnimeCog(commands.Cog):
  GENRES = [
    app_commands.Choice(name='Action', value='Action'),
    app_commands.Choice(name='Adventure', value='Adventure'),
    app_commands.Choice(name='Comedy', value='Comedy'),
    app_commands.Choice(name='Drama', value='Drama'),
    app_commands.Choice(name='Ecchi', value='Ecchi'),
    app_commands.Choice(name='Fantasy', value='Fantasy'),
    app_commands.Choice(name='Horror', value='Horror'),
    app_commands.Choice(name='Mahou Shoujo', value='Mahou Shoujo'),
    app_commands.Choice(name='Mecha', value='Mecha'),
    app_commands.Choice(name='Music', value='Music'),
    app_commands.Choice(name='Mystery', value='Mystery'),
    app_commands.Choice(name='Psychological', value='Psychological'),
    app_commands.Choice(name='Romance', value='Romance'),
    app_commands.Choice(name='Sci-Fi', value='Sci-Fi'),
    app_commands.Choice(name='Slice of Life', value='Slice of Life'),
    app_commands.Choice(name='Sports', value='Sports'),
    app_commands.Choice(name='Supernatural', value='Supernatural'),
    app_commands.Choice(name='Thriller', value='Thriller'),
    app_commands.Choice(name='Vampire', value='Vampire'),
  ]

  def __init__(self, bot):
    self.bot = bot
  
  @app_commands.command(name='random_anime_suggestion', description='Get a random anime ' \
  'based on genre')
  @app_commands.describe(genres='Enter genres separated by commas (e.g. Action,Adventure)')
  @app_commands.choices(genres=GENRES)
  async def random(self, interaction: Interaction, genres: str):
    await interaction.response.defer()

    genre_list = [g.strip() for g in genres.split(',') if g.strip()]

    anime = get_random_anime_suggestion(genre_list)

    embed = build_random_anime_embed(anime)

    await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot):
  await bot.add_cog(SeasonalAnimeLookUpCog(bot))
  await bot.add_cog(AllAnimeSearchCog(bot))
  await bot.add_cog(CharacterSearchCog(bot))
  await bot.add_cog(CheckNotifyListCog(bot, cursor))
  await bot.add_cog(NotifyAnimeAiredCog(bot, cursor, conn))
  await bot.add_cog(RemoveAnimeCog(bot, cursor, conn))
  await bot.add_cog(ClearNotifyListCog(bot, cursor, conn))
  await bot.add_cog(RandomAnimeCog(bot))
