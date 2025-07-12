import json
from datetime import datetime
from AniAlert.providers.anilist.search import search_anime_anilist
from AniAlert.providers.anilist.seasonal import get_seasonal_animes_anilist
from AniAlert.providers.anilist.randomize import get_random_anime
from AniAlert.providers import search_kitsu_anime


def extract_airing_nodes(air_time: dict):
  media = air_time.get('data', {}).get('Media') if air_time else None
  airing_schedule = media.get('airingSchedule') if media else None
  nodes = airing_schedule.get('nodes') if airing_schedule else None
  return nodes


def extract_genres(anime: dict):
  media = anime.get('data', {}).get('Media') if anime else None
  genres = media.get('genres') if media else None
  return genres


# This is needed since Kitsu doesn't provide current airing anime episodes
def extract_episodes(anime: dict, nodes: dict, index: int) -> dict:
  if isinstance(nodes, dict):
    nodes = [nodes]

  anime['upcoming_episodes'] = nodes

  if nodes:
    episodes_val = anime.get('episodes')
    if (
      episodes_val is None
      or (isinstance(episodes_val, str) and episodes_val.lower() == 'none')
      or int(episodes_val) <= 0
    ):
      anime['episodes'] = nodes[index]['episode'] - 1

  return anime


def get_full_anime_info(name: str, results_shown: int = 1, media_type: str = 'all', status: str = 'all') -> list:
  results = search_kitsu_anime(name)
  anime_list = []

  for anime in results:
    if media_type != 'all' and anime.get('show_type') != media_type:
      continue  
    if status != 'all' and anime.get('status') != status:
      continue  
    anime_list.append(anime)

  anime_list = anime_list[:results_shown]

  for index, anime in enumerate(anime_list):
    title = anime.get('title') or name
    anilist_data = search_anime_anilist(title)

    if not anilist_data or not anilist_data.get('data'):
      anime['genres'] = 'Not Found'
      anime['airing'] = False
      anime['time_until_airing'] = None
      anime['airingAt_iso'] = None
      continue

    media = anilist_data.get('data', {}).get('Media')

    if media is None:
      anime['genres'] = 'Not Found'
      anime['airing'] = False
      anime['time_until_airing'] = None
      anime['airingAt_iso'] = None
      continue
      
    anime['status'] = media.get('status', 'Unknown').upper()

    nodes = extract_airing_nodes(anilist_data)
    genres = media.get('genres', [])
    anime['genres'] = ', '.join(genres) if genres else 'N/A'

    airing_time_stamps = media.get('airingSchedule', {}).get('nodes', [])

    if airing_time_stamps:
      next_ep = airing_time_stamps[0]
      anime['time_until_airing'] = next_ep.get('time_until_airing')  
      anime['airingAt_iso'] = next_ep.get('airingAt_iso')
      anime['airingAt_unix'] = next_ep.get('airingAt_unix')
    else:
      anime['time_until_airing'] = None
      anime['airingAt_iso'] = None
      anime['airingAt_unix'] = None

    extract_episodes(anime, nodes, index)

  return anime_list


def get_seasonal_anime_info(
    page: int, 
    results_shown: int, 
    genres: list[str] = 'all', 
    media_type: str = 'all', 
    year: int = 2025, 
    season: str = 'SUMMER'
    ) -> list:
  results = get_seasonal_animes_anilist(page, results_shown, genres, media_type, year, season)
  return results


def get_random_anime_suggestion(genres: list[str], media_type: str = 'all') -> list:
  results = get_random_anime(genres)
  return results


if __name__ == '__main__':
  example = get_full_anime_info('One Piece Film', 5, 'movie')
  print(json.dumps(example, indent=2, ensure_ascii=False))
