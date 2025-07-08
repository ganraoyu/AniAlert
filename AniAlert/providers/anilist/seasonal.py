YEAR = 2025
SEASON = 'SUMMER'

import requests
import json
import datetime
from AniAlert.utils.time_converter import convert_unix
from AniAlert.utils.common_genres_tags import get_common_genres_tags

query = '''
query(
  $page: Int,
  $perPage: Int,
  $seasonYear: Int,
  $season: MediaSeason,
  $type: MediaType,
  $genres: [String],
  $tags: [String]
) {
  Page(page: $page, perPage: $perPage) {
    media(
      seasonYear: $seasonYear,
      season: $season,
      type: $type,
      genre_in: $genres,
      tag_in: $tags,
      sort: [POPULARITY_DESC]
    ) {
      id
      title {
        romaji
        english
      }
      genres
      tags {
        name
      }
      averageScore
      popularity
      description
      coverImage {
        extraLarge
      }
      airingSchedule(notYetAired: true) {
        nodes {
          airingAt
          timeUntilAiring
          episode
        }
      }
    }
  }
}
'''

def get_seasonal_animes_anilist(page: int, per_page: int, genres: list[str]):
  common_genres, common_tags = get_common_genres_tags()

  filtered_genres = []
  filtered_tags = []

  for genre in genres:
    if genre in common_tags:
      filtered_tags.append(genre)
    else:
      filtered_genres.append(genre)

  variables = {
    'page': page,
    'perPage': per_page,
    'seasonYear': YEAR,
    'season': SEASON,
    'type': 'ANIME',
  }

  if filtered_genres:
    variables['genres'] = filtered_genres

  if filtered_tags:
    variables['tags'] = filtered_tags
  
  response = requests.post(
    'https://graphql.anilist.co',
    json={'query': query, 'variables': variables}
  )
  response.raise_for_status()
  data = response.json()

  anime_list = []

  for index, anime in enumerate(data.get('data', {}).get('Page', {}).get('media', [])):
    anilist_id = anime.get('id', -1)
    title_info = anime.get('title', {})
    title = title_info.get('english') or title_info.get('romaji') or 'Unknown Title'
    genres = anime.get('genres', [])
    tags = anime.get('tags', [])

    filtered_tag_names = [
      tag['name'] for tag in tags if tag.get('name') in common_tags
    ]

    genres = filtered_tag_names + genres
    average_score = anime.get('averageScore', 0)
    description = anime.get('description', '') or ''
    image_url = anime.get('coverImage', {}).get('extraLarge')

    airing_nodes = anime.get('airingSchedule', {}).get('nodes', [])
    first_airing = airing_nodes[0] if airing_nodes else {}
    airing_at_unix = first_airing.get('airingAt')
    airing_at_iso = None
    time_until_airing = convert_unix(first_airing.get('timeUntilAiring'))
    episodes = first_airing.get('episode')

    if airing_at_unix:
      airing_at_iso = datetime.datetime.utcfromtimestamp(airing_at_unix).strftime("%Y-%m-%dT%H:%M:%S")

    for html_tag in ['<b>', '</b>', '<br>', '<i>', '</i>', '<i/>']:
      description = description.replace(html_tag, '')

    anime_list.append({
      'anilist_id': anilist_id,
      'title': title,
      'genres': genres,
      'average_rating': average_score,
      'synopsis': description,
      'image': image_url,
      'airingAt_unix': airing_at_unix,
      'airingAt_iso': airing_at_iso,
      'time_until_airing': time_until_airing,
      'episodes': episodes
    })

  return anime_list

if __name__ == '__main__':
  result = get_seasonal_animes_anilist(1, 5, ['Isekai'])
  print(json.dumps(result, indent=2, ensure_ascii=False))
