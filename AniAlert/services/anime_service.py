import json

from providers import search_by_title, search_kitsu_anime

def extract_airing_nodes(air_time):
  media = air_time.get('data', {}).get('Media') if air_time else None
  airing_schedule = media.get('airingSchedule') if media else None
  nodes = airing_schedule.get('nodes') if airing_schedule else None
  return nodes

def extract_genres(anime): 
   media = anime.get('data', {}).get('Media') if anime else None
   genres = media.get('genres') if media else None
   return genres

# This is needed since Kitsu does't provide episodes of current airing animes
def extract_episodes(anime, nodes, index):
    if isinstance(nodes, dict):
        nodes = [nodes]

    anime['upcoming_episodes'] = nodes

    if nodes:
        episodes_val = anime.get('episodes')
        if episodes_val is None or (isinstance(episodes_val, str) and episodes_val.lower() == 'none') or int(episodes_val) <= 0:
            anime['episodes'] = nodes[index]['episode'] - 1
    else:
        return

    return anime

def get_full_anime_info(name, results_shown, media_type):
    
    results = search_kitsu_anime(name)

    anime_list = results[:results_shown]

    for index, anime in enumerate(anime_list):
        title = anime.get('title') or name

        anilist_data = search_by_title(title)  

        if not anilist_data:
            anime['genres'] = 'Not Found'
            anime['airing'] = False
            continue

        nodes = extract_airing_nodes(anilist_data)

        genres = anilist_data.get('data', {}).get('Media', {}).get('genres', [])
        anime['genres'] = ', '.join(genres) if genres else 'N/A'

        anime['airing'] = bool(nodes)
        extract_episodes(anime, nodes, index)

        # Optional: add airing info like upcoming episodes

    return anime_list


if __name__ == '__main__':
  example = get_full_anime_info('one piece')  
  print(json.dumps(example, indent=2, ensure_ascii=False))

