import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from db.database import cursor

from typing import Optional

from discord.ext import commands
from discord import app_commands, Interaction

from services.anime_service import get_full_anime_info
from services.anime_service import get_seasonal_anime_info

from utils.embed_builder import build_search_anime_embed
from utils.embed_builder import build_seasonal_anime_embed
from utils.embed_builder import build_anime_notify_list_embed
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
    await interaction.response.send_message("Look up Seasonal Anime (Popularity).", ephemeral=True)

    animes = get_seasonal_anime_info(page, results_shown)

    if not animes:
      await interaction.followup.send('❌ No results found.', ephemeral=True)
      return
    
    for anime in animes:
      embed = build_seasonal_anime_embed(anime)
      await interaction.followup.send(embed=embed, ephemeral=True)

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

    for anime in results:
      anime_name = anime[5]
      iso_air_time = anime[7]
      image = anime[8]
      print(image)
      
      embed = build_anime_notify_list_embed(anime_name, iso_air_time, image)

      await interaction.followup.send(embed=embed, ephemeral=True)
      
class CharacterSearchCog(commands.Cog):
  pass

async def setup(bot):
  await bot.add_cog(SeasonalAnimeLookUpCog(bot))
  await bot.add_cog(AllAnimeSearchCog(bot))
  await bot.add_cog(CharacterSearchCog(bot))
  await bot.add_cog(CheckNotifyListCog(bot, cursor))
