import requests 
from dotenv import load_dotenv
import os

load_dotenv()

client_id = os.getenv('CLIENT_ID')

headers = {
    'X-MAL-CLIENT-ID': client_id,
}

def search_anime(query, limit):
  response = requests.get(
    f'https://api.myanimelist.net/v2/anime?q={query}&limit={limit}',
    headers=headers
  )

  data = response.json()
  found_animes = []

  for anime in data['data']:
   title = anime['node']['title']
   found_animes.append(title)

  return found_animes, data

my_animes = search_anime('Bleach', 10)
print(my_animes)
