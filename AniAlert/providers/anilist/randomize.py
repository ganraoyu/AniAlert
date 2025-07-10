import requests, json, random
from AniAlert.utils.common_genres_tags import get_common_genres_tags
query = '''
query($page: Int, $genre_in: [String], $tag_in: [String], $media_type: [MediaFormat],) {
  Page(page: $page, perPage: 4) {
    media(
    type: ANIME,
    isAdult: false, 
    genre_in: $genre_in, 
    sort: [POPULARITY_DESC],
    tag_in: $tag_in,
    format_in: $media_type
    ) {
      title {
        romaji
        english
      }
      coverImage {
        extraLarge
      }
      description
      episodes
      genres
      tags {
        name
      }
      studios {
        nodes {
          isAnimationStudio
          name
        }
      }
      format
      averageScore
      status
    }
  }
}
'''

common_genres, common_tags = get_common_genres_tags()

def _filter_genre_and_tags(genres: list[str]):
    genres_array = []
    tags_array = []

    for genre in genres:
      if genre in common_genres:
        genres_array.append(genre)
      elif genre in common_tags:
        tags_array.append(genre)
    
    return genres_array, tags_array

def _build_variables(genres_array: list[str], tags_array: list[str], media_type: str):
  variables = {
    'page': random.randint(1, 300),
  }
  
  if genres_array:
    variables['genre_in'] = genres_array

  if tags_array:
    variables['tag_in'] = tags_array

  if media_type != 'all':
    variables['media_type'] = media_type

  return variables

def _extract_anime_details(anime: dict) -> dict:
  tags = []
  for tag in anime.get('tags', []):
      tags.append(tag.get('name'))

  studios_array = []
  for studio in anime.get('studios', {}).get('nodes', []): 
    if studio['isAnimationStudio'] == True:
      studios_array.append(studio.get('name', 'Unknown Studio'))

  synopsis = anime.get("description", "")
  for tag in ['<b>', '</b>', '<br>', '<i>', '</i>', '<i/>']:
      synopsis = synopsis.replace(tag, '')

  if anime['status'] == 'COMPLETED':
    airing = True
  elif anime['status'] == 'RELEASING':
    airing = False
  else: 
    airing = 'COMPLETED'

  return {
  'tags': tags,
  'studios': studios_array,
  'synopsis': synopsis,
  'airing': airing
  }

# This is only for the multiple choices in guess anime command.
def _remaining_animes(animes: dict) -> list[str]:
  remaining_anime_titles = []
  for i in range(1, 4):
    anime = animes[i]
    title = anime.get('title', {})
    title_str = title.get('english') or title.get('romaji') or 'Unknown Title'
    remaining_anime_titles.append(title_str)

  return remaining_anime_titles

def get_random_anime(genres: list[str], media_type: str = 'all') -> dict:
  genres_array, tags_array = _filter_genre_and_tags(genres)
  variables = _build_variables(genres_array, tags_array, media_type )

  response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables})
  result = response.json()

  media = result.get("data", {}).get("Page", {}).get("media", [])
  if not media:
    return {}

  anime = media[0]
  anime_details = _extract_anime_details(anime)
  remaining_anime_titles = _remaining_animes(media)

  title = anime["title"].get("english")
  image_url = anime["coverImage"].get("extraLarge")
  synopsis = anime_details['synopsis']
  episodes = anime.get("episodes")

  # Combine tags from anime details and input genres, take first 4
  combined_genres = list(anime_details['tags']) + list(genres)
  genres_str = ', '.join(combined_genres[:4])

  # Unique studios as comma-separated string
  studios_str = ', '.join(set(anime_details['studios']))

  show_type = anime['format']
  average_rating = anime['averageScore']
  airing_status = anime_details['airing']

  result = {
      "title": title,
      "image": image_url,
      "synopsis": synopsis,
      "episodes": episodes,
      "genres": genres_str,
      "studios": studios_str,
      "show_type": show_type,
      "average_rating": average_rating,
      "airing": airing_status,
      "remaining_anime_titles": remaining_anime_titles,
  }

  return result

if __name__ == '__main__':
  anime = get_random_anime(['Action', 'Adventure'])
  print(json.dumps(anime, indent=2, ensure_ascii=False))
