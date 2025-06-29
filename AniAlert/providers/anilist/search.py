import requests
import json

query = '''
query($search: String){
  Media(search: $search, type: ANIME){
    genres,
    id,
    title{
      romaji,
      english
    },
    airingSchedule(notYetAired: true){
      nodes{
        airingAt,
        timeUntilAiring,
        episode
      }
    },
    averageScore,
    rankings {
      rank
      type
      allTime
      context
      season
      year
    }
  }
}
'''

def search_anime_anilist(search):
    response = requests.post(
        'https://graphql.anilist.co',
        json={'query': query, 'variables': {'search': search}}
    )
    data = response.json()
    return data

if __name__ == '__main__':
    response = search_anime_anilist('Solo Leveling: How to Get Stronger"')
    print(json.dumps(response, indent=2, ensure_ascii=False))
