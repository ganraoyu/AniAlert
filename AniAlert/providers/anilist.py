import requests

query = '''
query ($search: String) {
  Media(search: $search, type: ANIME) {
    id
    title {
      romaji
      english
    }
    airingSchedule(notYetAired: true) {
      nodes {
        episode
        airingAt
      }
    }
  }
}
'''

variables = {
    'search': 'Mushoku Tensei'  
}

response = requests.post(
    'https://graphql.anilist.co',
    json={'query': query, 'variables': variables}
)

data = response.json()
print(data)
