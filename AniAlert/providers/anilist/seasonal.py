YEAR = 2025
SEASON = 'SUMMER'

from typing import List, Union
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
  $tags: [String],
  $media_type: [MediaFormat],
) {
  Page(page: $page, perPage: $perPage) {
    media(
      seasonYear: $seasonYear,
      season: $season,
      type: $type,
      genre_in: $genres,
      tag_in: $tags,
      sort: [POPULARITY_DESC]
      format_in: $media_type
    ) {
      id
      title {
        romaji
        english
      }
      format
      genres
      tags {
        name
      }
      averageScore
      meanScore
      popularity
      episodes
      description
      coverImage {
        extraLarge
      }
      startDate {
        year
        month
        day
      }
      endDate {
        year
        month
        day
      }
      status
      format
      studios {
        nodes {
          name
          isAnimationStudio
        }
      }
      rankings {
        rank
        type
        allTime
        context
        year
        season
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

def get_seasonal_animes_anilist(
    page: int, 
    per_page: int, 
    genres: str = 'all', 
    media_type: str = 'all', 
    year: int = YEAR, 
    season: str = SEASON 
    ):
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
    'seasonYear': year,
    'season': season,
    'type': 'ANIME',
  }
  
  if genres != 'all' and filtered_genres:
    variables['genres'] = filtered_genres

  if genres != 'all' and filtered_tags:
    variables['tags'] = filtered_tags

  if media_type != 'all':
    variables['media_type'] = media_type
  
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

    studios_array = []

    for studio in anime.get('studios', {}).get('nodes', []):
      if studio['isAnimationStudio'] == True:
        studios_array.append(studio.get('name', 'Unknown Studio'))
  
    show_type = anime.get('format')
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

    for html_tag in ['<b>', '</b>', '<br>', '<i>', '</i>', '<i/>', '\n']:
      description = description.replace(html_tag, '')

    anime_list.append({
      'anilist_id': anilist_id,
      'title': title,
      'studios':', '.join(set(studios_array)),
      'show_type': show_type,
      'genres': ', '.join(genres[:4]),
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
  result = get_seasonal_animes_anilist(1, 5, ["Drama"], ['TV'], 2024, "SPRING")
  print(json.dumps(result, indent=2, ensure_ascii=False))
