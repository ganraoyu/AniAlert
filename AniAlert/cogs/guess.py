import discord
import random
from discord.ext import commands
from discord import app_commands, Interaction

from services.anime_service import get_random_anime_suggestion
from utils.embed_builder import build_guess_anime_embed
from utils.button_builder import guess_anime_buttons_view
from utils.choices import get_choices

MEDIA_TYPE_CHOICES, STATUS_TYPE_CHOICES, POPULAR_GENRE_TAG_CHOICES, GENRE_TYPE_CHOICES, YEAR_CHOICES, SEASON_CHOICES = get_choices()

async def _fetch_valid_anime(genre_list, interaction):
  max_tries = 5

  for _ in range(max_tries):
    anime = get_random_anime_suggestion(genre_list)
    if anime.get('title'):
      return anime
    else:
      await interaction.followup.send(
        content="No anime was found. Trying again...",
        ephemeral=True
      )

  return None

class GuessAnimeCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @app_commands.command(name='guess_anime', description='Guess what anime this is based off the image')
  @app_commands.describe(genres='Filter results by genres')
  @app_commands.choices(genres=POPULAR_GENRE_TAG_CHOICES)
  async def guess_anime(self, interaction: Interaction, genres: str = None):
    await interaction.response.defer(ephemeral=True)
    if genres:
      genre_list = [g.strip() for g in genres.split(',') if g.strip()]
    else:
      genre_list = 'all'

    anime = await _fetch_valid_anime(genre_list, interaction)

    if not anime:
      await interaction.followup.send(
        content="No valid anime found.",
        ephemeral=True
      )
      return

    embed = build_guess_anime_embed(anime)

    remaining_anime_titles_array = []
    main_title = anime.get('title', 'Unknown Title')[:80]

    # Limit title length to 80 characters
    for title in anime.get('remaining_anime_titles', []):
      remaining_anime_titles_array.append(title[:80])

    choices = [main_title] + remaining_anime_titles_array
    random.shuffle(choices)

    view = guess_anime_buttons_view(choices, anime['title'], timeout=60)
    await interaction.followup.send(embed=embed, view=view)
