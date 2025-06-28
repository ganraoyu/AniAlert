import requests
import json

query = '''
query($page:Int, $seasonYear: Int, $season: MediaSeason, $type: MediaType){
   Page(page: $page, perPage: 50) {
    media(seasonYear: $seasonYear, season: $season, type: $type) {
      id,
      title {
        romaji
        english
      }
      season
      seasonYear
    }
  }
}
'''

def get_seasonal_data(page, seasonYear, season, type_):
  variables = {
    'page': page,
    'seasonYear': seasonYear,
    'season': season,
    'type': type_
  }


  response = requests.post(
    'https://graphql.anilist.co',
    json={'query': query, 'variables': variables}
  )
  
  return response.json()

if __name__ == '__main__':
  page = 1
  while True:
    response = get_seasonal_data(page, 2024, 'SUMMER', 'ANIME')
    media = response['data']['Page']['media']

    if not media:  
      break

    print(json.dumps(response, indent=2, ensure_ascii=False))
    page += 1





