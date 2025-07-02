from datetime import datetime

from discord import Interaction
from utils.interaction_helper import get_user_and_guild_ids
from utils.embed_builder import build_anime_airing_notification_embed

def check_notify_list(user_id: str, guild_id: str, cursor):
  cursor.execute('SELECT * FROM anime_notify_list WHERE guild_id = ? and user_id = ?', (guild_id, user_id))
  results = cursor.fetchall()

  anime_list = []

  for anime in results:
    anime_id = anime[0]
    user_id = anime[3]
    anime_name = anime[5]
    iso_air_time = anime[7]
    image = anime[8]

    anime_list.append({
    "anime_id": anime_id,
    "user_id": user_id,
    "anime_name": anime_name,
    "iso_air_time": iso_air_time,
    "image": image
    })

  return anime_list 

def check_if_aired(anime_list):
    current_time = datetime.now()  

    animes_with_episode_aired = []

    for anime in anime_list:
        air_time = datetime.fromisoformat(anime['iso_air_time'])
        
        if current_time >= air_time:
            animes_with_episode_aired.append(anime)

    return animes_with_episode_aired


def get_user_anime_status(interaction: Interaction, cursor):
  user_id, guild_id = get_user_and_guild_ids(interaction)
  anime_list = check_notify_list(user_id, guild_id, cursor)
  animes_with_episode_aired = check_if_aired(anime_list)

  return user_id, guild_id, anime_list, animes_with_episode_aired



