import requests
import json
from datetime import datetime

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

def break_down_time(unix_time):
  
  days = unix_time // 86400
  hours = (unix_time % 86400) // 3600
  minutes = (unix_time % 3600) // 60
  seconds = unix_time % 60

  time = f'{days}d {hours}h {minutes}m {seconds}s'

  return time

def search_anime_anilist(search):
    response = requests.post(
        'https://graphql.anilist.co',
        json={'query': query, 'variables': {'search': search}}
    )
    data = response.json()

    nodes = data['data']['Media']['airingSchedule']['nodes']

    for episode in nodes:
        episode['airingAt'] = datetime.utcfromtimestamp(episode['airingAt']).isoformat()
        episode['timeUntilAiring'] = break_down_time(episode['timeUntilAiring'])

    return data

if __name__ == '__main__':
    response = search_anime_anilist('DAndadon season 2"')
    print(json.dumps(response, indent=2, ensure_ascii=False))
