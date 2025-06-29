YEAR= 2025
SEASON = 'SUMMER'

import requests
import json

query = '''
query($page: Int, $perPage: Int, $seasonYear: Int, $season: MediaSeason, $type: MediaType) {
  Page(page: $page, perPage: $perPage) {
    media(
      seasonYear: $seasonYear,
      season: $season,
      type: $type,
      sort: [POPULARITY_DESC]
    ) {
      id
      title {
        romaji
        english
      }
      averageScore
      popularity
      rankings {
        rank
        type
        allTime
        context
        season
        year
      }
      season
      seasonYear
      description
      airingSchedule(notYetAired: true){
        nodes{
          airingAt
          timeUntilAiring
          episode
        }
      }
      coverImage{
        extraLarge
      }
    }
  }
}
'''

def get_seasonal_animes_anilist(page: int, perPage: int):
    variables = {
        'page': page,
        'perPage': perPage,
        'seasonYear': YEAR,    
        'season': SEASON,     
        'type': 'ANIME'
    }

    response = requests.post(
        'https://graphql.anilist.co',
        json={'query': query, 'variables': variables}
    )

    data =  response.json()
    anime_data = []

    for index, anime in enumerate(data['data']['Page']['media']):
        anilist_id = anime.get('id', -0)
        title_data = anime.get('title', {})
        title = title_data.get('english') or title_data.get('romaji') or 'Unknown Title'
        average_rating = anime.get('averageScore', 0)
        ranking = index + 1
        synopsis = anime.get('description', '')
        image = anime.get('coverImage', {}).get('extraLarge')

        # Anilsit does some weird shit when they webscrape idk
        words = ['<b>', '</b>', '<br>', '<i>', '</i>', '<i/>']
        
        for word in words:
            synopsis = synopsis.replace(word, "")
            
        anime_data.append({
            'anilist_id': anilist_id,
            'title': title,
            'average_rating': average_rating,
            'seasonal_ranking': ranking,
            'synopsis': synopsis,
            'image': image
        })
    
    return anime_data

# Example use
if __name__ == '__main__':
    result = get_seasonal_animes_anilist(1, 1)
    print(json.dumps(result, indent=2, ensure_ascii=False))
