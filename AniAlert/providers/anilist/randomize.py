import requests, json, random

query = '''
query($page: Int, $genre_in: [String]) {
  Page(page: $page, perPage: 1) {
    media(isAdult: false, genre_in: $genre_in, sort: [POPULARITY_DESC]) {
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
    }
  }
}
'''

def get_random_anime(genres: list[str]) -> dict:
  variables = {
    'page': random.randint(1, 300),
    'genre_in': genres
  }
  response = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': variables})
  result = response.json()

  media = result.get("data", {}).get("Page", {}).get("media", [])
  if not media:
    return {}

  anime = media[0]
  
  flattened = {
    "title": anime["title"].get("english"),
    "image": anime["coverImage"].get("extraLarge"),
    "synopsis": anime.get("description"),
    "episodes": anime.get("episodes"),
    "genres": anime.get("genres")
  }

  return flattened

if __name__ == '__main__':
  anime = get_random_anime(['Action', 'Adventure'])
  print(json.dumps(anime, indent=2, ensure_ascii=False))
