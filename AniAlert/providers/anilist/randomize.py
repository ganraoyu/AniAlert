import requests, json, random
from AniAlert.utils.common_genres_tags import get_common_genres_tags
query = '''
query($page: Int, $genre_in: [String], $tag_in: [String], $media_type: [MediaFormat],) {
  Page(page: $page, perPage: 1) {
    media(
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

def get_random_anime(genres: list[str], media_type: str = 'all') -> dict:
  variables = {
    'page': random.randint(1, 300),
  }

  genres_array = []
  tags_array = []

  for genre in genres:
    if genre in common_genres:
      genres_array.append(genre)
    elif genre in common_tags:
      tags_array.append(genre)

  if genres_array:
    variables['genre_in'] = genres_array

  if tags_array:
    variables['tag_in'] = tags_array

  if media_type != 'all':
    variables['media_type'] = media_type

  response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables})
  result = response.json()

  media = result.get("data", {}).get("Page", {}).get("media", [])
  if not media:
    return {}

  anime = media[0]

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
    airing = 'N/A'

  flattened = {
    "title": anime["title"].get("english"),
    "image": anime["coverImage"].get("extraLarge"),
    "synopsis": synopsis,
    "episodes": anime.get("episodes"),
    "genres": ', '.join((list(tags) + list(genres))[:4]),
    "studios": ','.join(set(studios_array)),
    "show_type": anime['format'],
    "average_rating": anime['averageScore'],
    "airing": airing
  }

  return flattened

if __name__ == '__main__':
  anime = get_random_anime(['Action', 'Adventure'])
  print(json.dumps(anime, indent=2, ensure_ascii=False))
