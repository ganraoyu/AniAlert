import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from db.database import cursor, conn

from typing import Optional

from discord.ext import commands, tasks
from discord import app_commands, Interaction

from services.anime_service import get_full_anime_info
from services.anime_service import get_seasonal_anime_info
from services.airing_checker import check_notify_list, check_if_aired 

from utils.embed_builder import build_search_anime_embed
from utils.embed_builder import build_seasonal_anime_embed
from utils.embed_builder import build_anime_notify_list_embed
from utils.embed_builder import build_anime_airing_notification_embed
from utils.interaction_helper import get_user_and_guild_ids
from utils.button_builder import anime_buttons_view

from views.search_modal import SearchAnimeInput
from views.pick_anime_view import PickAnimeView

# Searches - Require user input
# Look ups - No user input, just returns data

class SeasonalAnimeLookUpCog(commands.Cog): 
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name='seasonal_anime', description='Look up currently airing seasonal anime')
  async def seasonal_anime_slash(self, interaction: Interaction, page: int, results_shown: int):
    await interaction.response.defer(ephemeral=True)
    
    animes = get_seasonal_anime_info(page, results_shown)

    if not animes:
      await interaction.followup.send('❌ No results found.', ephemeral=True)
      return

    for anime in animes:
      embed = build_seasonal_anime_embed(anime)
      buttons = anime_buttons_view(anime)

      await interaction.followup.send(embed=embed, view=buttons, ephemeral=True)

class AllAnimeSearchCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @app_commands.command(name='search_anime', description='Search for animes')
  @app_commands.describe(
    name="Anime name to search",
    results_shown="How many results to show",
    media_type="Type of media"
  )
  @app_commands.choices(
    media_type=[
      app_commands.Choice(name='All', value='all'),
      app_commands.Choice(name="TV", value="TV"),
      app_commands.Choice(name="Movie", value="movie"),
      app_commands.Choice(name="OVA", value="OVA"),
      app_commands.Choice(name="ONA", value="ONA"),
      app_commands.Choice(name="Special", value="special")
    ]
  )
  async def search_anime_slash(
    self,
    interaction: Interaction,
    name: str,
    results_shown: int,
    media_type: Optional[app_commands.Choice[str]] = None
  ):
    await interaction.response.defer(ephemeral=True)

    media_value = media_type.value if media_type else "all"
    animes = get_full_anime_info(name, results_shown, media_value)

    if not animes:
      await interaction.followup.send('❌ No results found.', ephemeral=True)
      return

    for anime in animes:
      embed = build_search_anime_embed(anime)
      buttons = anime_buttons_view(anime)

      await interaction.followup.send(embed=embed, view=buttons, ephemeral=True)

class CheckNotifyListCog(commands.Cog):
  def __init__(self, bot, cursor):
    self.bot = bot
    self.cursor = cursor

  @app_commands.command(name='list', description='Check notify list')
  async def check_notify_list(self, interaction: Interaction):
    user_id, guild_id = get_user_and_guild_ids(interaction)
    user_id, guild_id = int(user_id), int(guild_id)

    await interaction.response.defer(ephemeral=True)

    self.cursor.execute('SELECT * FROM anime_notify_list WHERE user_id = ? AND guild_id = ?', (user_id, guild_id))
    results = self.cursor.fetchall()

    embeds = []
    for anime in results:
      anime_name = anime[5]   
      episode = anime[6]          
      iso_air_time = anime[8]     
      image = anime[9]             

      embed = build_anime_notify_list_embed(anime_name, episode, iso_air_time, image)
      embeds.append(embed)

    await interaction.followup.send(embeds=embeds, ephemeral=True)

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
      anime_list = check_notify_list(user_id, guild_id, self.cursor)
      animes_with_episode_aired = check_if_aired(anime_list)

      if not animes_with_episode_aired:
        continue 

      guild = self.bot.get_guild(guild_id)
      if not guild:
        continue  

      channel = next(
        (ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages),
        None
      )
      if not channel:
        continue 
      
      for anime in animes_with_episode_aired:
        new_anime = get_full_anime_info(anime['anime_name'])

        anime_id = anime['anime_id']

        embed = build_anime_airing_notification_embed(
          anime_name=anime['anime_name'],
          image_url=anime['image'],
          user_id=anime['user_id']
        )
        await channel.send(content=f"<@{user_id}>", embed=embed)

        if new_anime and new_anime[0].get('airingAt_unix'):
          unix_air_time_value = new_anime[0]['airingAt_unix']
          iso_air_time_value = new_anime[0].get('airingAt_iso')

          self.cursor.execute(
              'UPDATE anime_notify_list SET unix_air_time = ?, iso_air_time = ? WHERE id = ?',
              (unix_air_time_value, iso_air_time_value, anime_id)
          )
        else:
          self.cursor.execute('SELECT * FROM anime_notify_list WHERE id = ?', (anime_id,))
          row = self.cursor.fetchone()

          if row:
            self.cursor.execute('DELETE FROM anime_notify_list WHERE id = ?', (anime_id,))
            
        self.conn.commit()      

class CharacterSearchCog(commands.Cog):
  pass

async def setup(bot):
  await bot.add_cog(SeasonalAnimeLookUpCog(bot))
  await bot.add_cog(AllAnimeSearchCog(bot))
  await bot.add_cog(CharacterSearchCog(bot))
  await bot.add_cog(CheckNotifyListCog(bot, cursor))
  await bot.add_cog(NotifyAnimeAiredCog(bot, cursor, conn))
