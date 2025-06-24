import json

from AniAlert.providers import find_air_time
from AniAlert.providers import search_anime

def get_full_anime_info(name):
    anime_list = search_anime(name)  # likely a list
    air_time = find_air_time(name)

    nodes = air_time['data']['Media']['airingSchedule']['nodes']

    if isinstance(nodes, dict):
        nodes = [nodes]

    # If search_anime returns a single dict instead of list, wrap it in a list
    if not isinstance(anime_list, list):
        anime_list = [anime_list]

    # For each anime, attach upcoming episodes and compute episodes count
    for anime_info in anime_list:
        anime_info['upcoming_episodes'] = nodes

        # Kitsu doesn't have current airing anime episodes, must get from Anilist
        anime_info['episodes'] = nodes[0]['episode'] - 1 if nodes else None

    # Current code gets the episode of searched anime. Next: run all the titles from Kitsu into Anilist to see if other ones have episodes.
    return anime_list


example = get_full_anime_info('one piece')
print(json.dumps(example, indent=4, ensure_ascii=False))
