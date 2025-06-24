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

def search_anime(query):
  if ' ' in query:
    new_query = query.replace(' ', '%20')
    print(new_query)
  else: 
    new_query = query

  response = requests.get(
  f'https://kitsu.io/api/edge/anime?filter[text]={new_query}',
  headers=headers
  )

  data = response.json()
  found_animes = []

  for anime in data['data']:
    title = anime['attributes']['canonicalTitle']
    found_animes.append(title)

  print(found_animes)
  
  return found_animes, data


searched_anime = search_anime('Cowboy bebop')