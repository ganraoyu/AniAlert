import discord
from typing import List, Tuple
from utils.formatted_time import iso_to_formatted_time

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
  time_until = str(anime.get('timeUntilAiring', 'N/A'))
  airing_at = str(anime.get('airingAt', 'N/A'))

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
    'time_until': time_until,
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
  embed.add_field(name='Next episode', value=str(int(vars['episodes']) + 1))
  embed.add_field(name='Next episode in', value=vars['time_until'], inline=True)
  embed.add_field(name='Airing at', value=vars['airing_at'], inline=True)

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

def build_anime_notify_list_embed(anime_name: str, iso_air_time: str, image: str) -> discord.Embed:
    formatted_time = iso_to_formatted_time(iso_air_time)

    embed = discord.Embed(
      title=f'🎬 {anime_name}',
      color=discord.Color.dark_blue()
    )
    embed.add_field(name='Next episode in', value=formatted_time, inline=True)
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


