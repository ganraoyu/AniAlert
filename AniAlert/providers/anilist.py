import requests

query = '''
query($search: String){
  Media(search: $search, type: ANIME){
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

def find_air_time(search):
  response = requests.post(
    'https://graphql.anilist.co',
    json={'query': query, 'variables': {'search': search}}
  )
  data = response.json()
  return data

example = find_air_time('One Piece Film: Strong World Episode 0')
print(example)