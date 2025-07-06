import requests
import json
import datetime
from AniAlert.utils.time_converter import convert_unix


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

    for node in nodes:
      node['airingAt_unix'] = node['airingAt']
      node['airingAt_iso'] = datetime.datetime.utcfromtimestamp(node['airingAt_unix']).strftime("%Y-%m-%dT%H:%M:%S")
      node['time_until_airing'] = convert_unix(node['timeUntilAiring'])
    
    return data

if __name__ == '__main__':
  response = search_anime_anilist('One Piece')
  print(json.dumps(response, indent=2, ensure_ascii=False))
