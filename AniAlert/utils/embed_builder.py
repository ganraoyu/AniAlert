import discord
from typing import List, Tuple
from utils.time_converter import convert_iso

def get_anime_variables(anime: dict):
  title = anime.get('title', 'Unknown Title')
  synopsis = anime.get('synopsis', 'No synopsis available.')
  show_type = str(anime.get('show_type', 'N/A'))
  rating = str(anime.get('average_rating', 'N/A'))
  episodes = str(anime.get('episodes', 'N/A'))
  airing = str(anime.get('airing', 'N/A'))
  ranking = str(anime.get('ranking', 'N/A'))
  genres = str(anime.get('genres', [])) or 'Unknown'
  image = anime.get('image')
  timeUntilAiring = str(anime.get('timeUntilAiring', 'N/A'))
  airing_at = str(anime.get('airingAt_iso', 'N/A'))

  return {
    'title': title,
    'synopsis': synopsis,
    'show_type': show_type,
    'rating': rating,
    'episodes': episodes,
    'airing': airing,
    'ranking': ranking,
    'genres': genres,
    'image': image,
    'timeUntilAiring': timeUntilAiring,
    'airing_at': airing_at
  }

def build_search_anime_embed(anime: dict) -> discord.Embed:
  vars = get_anime_variables(anime)

  embed = discord.Embed(
    title=f'🎬 {vars["title"]}',
    description=vars['synopsis'],
    color=discord.Color.purple()
  )
  embed.add_field(name='📺 Type', value=vars['show_type'], inline=True)
  embed.add_field(name='⭐ Rating', value=vars['rating'], inline=True)
  embed.add_field(name='🎞️ Episodes', value=vars['episodes'], inline=True)
  embed.add_field(name='🗓️ Airing', value=vars['airing'], inline=True)
  embed.add_field(name='🏆 Rank', value=vars['ranking'], inline=True)
  embed.add_field(name='🎭 Genres', value=vars['genres'], inline=True)

  if vars['image']:
    embed.set_thumbnail(url=vars['image'])

  return embed

def build_seasonal_anime_embed(anime: dict) -> discord.Embed:
  vars = get_anime_variables(anime)

  embed = discord.Embed(
    title=f'🎬 {vars["title"]}',
    description=vars['synopsis'],
    color=discord.Color.blue()
  )

  if vars['image']:
    embed.set_thumbnail(url=vars['image'])

  return embed

def build_add_anime_embed(anime: dict) -> discord.Embed:
  vars = get_anime_variables(anime)

  embed = discord.Embed(
    title=f'🎬 {vars["title"]}',
    color=discord.Color.green()
  )

  # Anilist only pulls current episodes, need a plus 1 to show the next airing episode
  embed.add_field(name=f"Episode {int(vars['episodes']) + 1} in", value=vars['timeUntilAiring'], inline=False)
  embed.add_field(name='Airing at', value=vars['airing_at'], inline=False)

  if vars['image']:
    embed.set_thumbnail(url=vars['image'])

  return embed

def build_remove_anime_embed(anime: dict) -> discord.Embed:
  vars = get_anime_variables(anime)

  embed = discord.Embed(
    title=f'❌ Removed: {vars["title"]}',
    color=discord.Color.red()
  )

  return embed

def build_anime_notify_list_embed(anime_name: str, id: int, episode: int, iso_air_time: str, image: str) -> discord.Embed:
    formatted_time = convert_iso(iso_air_time)  

    embed = discord.Embed(
      title=f'🎬 {anime_name} (ID: {id})',
      color=discord.Color.dark_blue()
    )
    
    # No plus 1 episode here. This is pulled straight from the data base.
    embed.add_field(name=f'Episode {episode} in', value=formatted_time, inline=False)
    embed.set_thumbnail(url=str(image))  

    return embed

def build_anime_airing_notification_embed(anime_name: str, image_url: str, user_id: str) -> discord.Embed:
    embed = discord.Embed(
        title=f'📢 New Episode Aired: {anime_name}',
        description=f'<@{user_id}> A new episode just dropped — go check it out!',
        color=discord.Color.dark_blue()
    )
    embed.set_thumbnail(url=image_url)
    embed.set_footer(text="AniAlert • Real-time Anime Notifications")

    return embed


