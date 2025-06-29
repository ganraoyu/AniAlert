import requests
import json
YEAR=2024
SEASON='SUMMER'

query = '''
query ($page: Int, $seasonYear: Int, $season: MediaSeason, $type: MediaType) {
  Page(page: $page, perPage: 2) {
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
    }
  }
}
'''

def get_seasonal_animes_anilist(page: int):
    variables = {
        'page': page,
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
        title = anime.get('title', {}).get('english', 'romaji')
        average_rating = anime.get('averageScore', 0)
        ranking = index + 1
        synopsis = anime.get('description', '')

        anime_data.append({
            'anilist_id': anilist_id,
            'title': title,
            'average_rating': average_rating,
            'seasonal_ranking': ranking,
            'synopsis': synopsis
        })
    
    return anime_data

# Example use
if __name__ == '__main__':
    result = get_seasonal_animes_anilist  (1)
    print(json.dumps(result, indent=2, ensure_ascii=False))
