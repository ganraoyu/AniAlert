import requests
import json
from datetime import datetime
from utils.time_converter import convert_unix


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


    nodes = data['data']['Media']['airingSchedule']['nodes']

    for episode in nodes:
        episode['airingAt_unix'] = episode['airingAt']
        episode['airingAt'] = datetime.utcfromtimestamp(episode['airingAt']).isoformat()
        episode['time_until_airing'] = convert_unix(episode['timeUntilAiring'])

    return data

if __name__ == '__main__':
    response = search_anime_anilist('One Piece')
    print(json.dumps(response, indent=2, ensure_ascii=False))
