import json
import requests

headers = {
  "Accept": "application/vnd.api+json",
  "Content-Type": "application/vnd.api+json",
  "User-Agent": "AniAlertBot/1.0 (https://github.com/ganraoyu/AniAlert)"
}

#%20 is a space. (Hardcoded)
response = requests.get(
  'https://kitsu.io/api/edge/anime?filter[text]=one%20piece',
  headers=headers
)

def search_kitsu_anime(query: str):
  if ' ' in query:
    new_query = query.replace(' ', '%20')
    print(new_query)
  else: 
    new_query = query

  response = requests.get(
  f'https://kitsu.io/api/edge/anime?filter[text]={new_query}&page[limit]=20',
  headers=headers
  )

  data = response.json()
  anime_data = []

  for anime in data['data']:
    attribute = anime['attributes']

    kitsu_id = anime.get('id', '-0')
    title = attribute.get('canonicalTitle', 'Unknown Title')
    show_type = attribute.get('showType', 'Unknown Type')
    average_rating = attribute.get('averageRating', 'N/A')
    ranking = attribute.get('ratingRank', 'N/A')
    synopsis = attribute.get('synopsis', 'No synopsis available')
    episodes = attribute.get('episodeCount', -0)
    length_per_episode = attribute.get('totalLength', -0)
    image = attribute.get('posterImage', {}).get('original', '')


    anime_data.append({
      'kitsu_id':  kitsu_id,
      'title': title,
      'show_type': show_type,
      'average_rating': average_rating,
      'ranking': ranking,
      'synopsis': synopsis,
      'episodes': episodes,
      'length_per_episode': length_per_episode,
      'image': image
    })

  return anime_data

if __name__ == '__main__':
  example = search_kitsu_anime('One piece')
  print(json.dumps(example, indent=4, ensure_ascii=False))

