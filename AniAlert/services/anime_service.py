import json

from AniAlert.providers import find_air_time
from AniAlert.providers import search_anime

def extract_airing_nodes(air_time):
  media = air_time.get('data', {}).get('Media') if air_time else None
  airing_schedule = media.get('airingSchedule') if media else None
  nodes = airing_schedule.get('nodes') if airing_schedule else None
  return nodes

def attach_episodes_info(anime, nodes, index):
  if isinstance(nodes, dict):
    nodes = [nodes]

  anime['upcoming_episodes'] = nodes
  anime['episodes'] = nodes[index]['episode'] - 1 if nodes else None
  return anime

def get_full_anime_info(name):
  anime_list = search_anime(name)

  for index, anime in enumerate(anime_list):
    title = anime.get('title') or name
    air_time = find_air_time(title)

    nodes = extract_airing_nodes(air_time)
    if not nodes:
      continue

    print(nodes)
    attach_episodes_info(anime, nodes, index)

  return anime_list

example = get_full_anime_info('one piece')
print(json.dumps(example, indent=2, ensure_ascii=False))
