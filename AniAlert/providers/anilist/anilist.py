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
    }
  }
}
'''

def fetch_anilist_data(search):
  response = requests.post(
    'https://graphql.anilist.co',
    json={'query': query, 'variables': {'search': search}}
  )
  data = response.json()
  return data


if __name__ == '__main__':
  response = json.dumps(fetch_anilist_data('One Piece Film: Strong World Episode 0'), indent=2, ensure_ascii=False)
  print(response)