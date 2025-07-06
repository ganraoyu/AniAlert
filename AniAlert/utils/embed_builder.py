import discord
from typing import List, Tuple
from .time_converter import convert_iso

def get_anime_variables(anime: dict):
  title = anime.get('title') or 'Unknown Title'
  synopsis = anime.get('synopsis') or 'No synopsis available.'
  show_type = str(anime.get('show_type') or 'N/A')
  rating = str(anime.get('average_rating') or 'N/A')
  episodes = str(anime.get('episodes') or 0)
  airing = str(anime.get('airing') or 'N/A')
  ranking = str(anime.get('ranking') or 'N/A')
  genres = str(anime.get('genres') or 'Unknown')
  image = anime.get('image')
  time_until_airing = str(anime.get('time_until_airing') or 'N/A')
  airingAt_iso = str(anime.get('airingAt_iso') or 'N/A')

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
    'time_until_airing': time_until_airing,
    'airingAt_iso': airingAt_iso
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

  embed.set_footer(text="AniAlert • Search Results")
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

  embed.set_footer(text="AniAlert • Seasonal Anime")
  return embed

def build_add_anime_embed(anime: dict) -> discord.Embed:
  vars = get_anime_variables(anime)

  embed = discord.Embed(
    title=f'🎬 {vars["title"]}',
    color=discord.Color.green()
  )

  embed.add_field(name=f"Episode {int(vars['episodes']) + 1} in", value=vars['time_until_airing'], inline=False)
  embed.add_field(name='Airing at', value=vars['airingAt_iso'], inline=False)

  if vars['image']:
    embed.set_thumbnail(url=vars['image'])

  embed.set_footer(text="AniAlert • Anime Added")
  return embed

def build_remove_anime_embed(anime: dict) -> discord.Embed:
  vars = get_anime_variables(anime)

  embed = discord.Embed(
    title=f'❌ Removed: {vars["title"]}',
    color=discord.Color.red()
  )

  embed.set_footer(text="AniAlert • Anime Removed")
  return embed

def build_anime_notify_list_embed(anime_name: str, id: int, episode: int, iso_air_time: str, image: str) -> discord.Embed:
  formatted_time = convert_iso(iso_air_time)  

  embed = discord.Embed(
    title=f'🎬 {anime_name} (ID: {id})',
    color=discord.Color.dark_blue()
  )
  
  embed.add_field(name=f'Episode {episode} in', value=formatted_time, inline=False)
  embed.set_thumbnail(url=str(image))  
  embed.set_footer(text="AniAlert • Notification List")
  return embed

def build_anime_airing_notification_embed(anime_name: str, image_url: str, user_id: str) -> discord.Embed:
  embed = discord.Embed(
    title=f'📢 New Episode Aired: {anime_name}',
    description=f'<@{user_id}> A new episode just dropped — go check it out!',
    color=discord.Color.dark_blue()
  )
  embed.set_thumbnail(url=image_url)
  embed.set_footer(text="AniAlert • Airing Notification")
  return embed

def build_random_anime_embed(anime: dict):
  vars = get_anime_variables(anime)
  
  embed = discord.Embed(
    title=f'🎲 Random Anime: {vars["title"]}',
    description=vars['synopsis'],
    color=discord.Color.random()
  )

  embed.add_field(name='🎞️ Episodes', value=vars['episodes'], inline=True)
  embed.add_field(name='🎭 Genres', value=vars['genres'], inline=True)

  if vars['image']:
    embed.set_thumbnail(url=vars['image'])

  embed.set_footer(text="AniAlert • Random Anime Generator")
  return embed
