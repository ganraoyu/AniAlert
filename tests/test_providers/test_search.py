import pytest
from unittest.mock import patch
import datetime

from AniAlert.providers.anilist.search import search_anime_anilist
from AniAlert.utils.time_converter import convert_unix

@patch('AniAlert.providers.anilist.search.requests.post')
def test_search_anime(mock_post):

  # FAKE DATA!!!! IN REAL LIFE COWBOY BEBOP IS NOTTTTTTTTTTTTT AIRING
  mock_response = mock_post.return_value
  mock_response.json.return_value = {
    "data": {
      "Media": {
        "genres": [
          "Action",
          "Adventure",
          "Drama",
          "Sci-Fi"
        ],
        "id": 1,
        "title": {  
          "romaji": "Cowboy Bebop",
          "english": "Cowboy Bebop"
        },
        "airingSchedule": {
          "nodes": [
            {
              "airingAt": 1751811360,
              "timeUntilAiring": 40126,
              "episode": 1135
            },
          ]
        },
        "averageScore": 86
      }
    }
  }

  result = search_anime_anilist('Cowboy Bebop')

  assert 'data' in result
  assert 'Media' in result['data']

  media = result['data']['Media']
  assert media['title']['romaji'] == 'Cowboy Bebop'
  assert media['title']['english'] == 'Cowboy Bebop'
  assert media['genres'] == ["Action","Adventure","Drama","Sci-Fi"]
  assert media['averageScore'] == 86
  
  nodes = media['airingSchedule']['nodes']
  for node in nodes:
    node['airingAt_unix'] = node['airingAt']
    node['time_until_airing'] = convert_unix(node['timeUntilAiring'])

    assert node['airingAt_unix'] == 1751811360
    assert node['airingAt_iso'] == datetime.datetime.utcfromtimestamp(1751811360).strftime("%Y-%m-%dT%H:%M:%S")
    assert node['time_until_airing'] == convert_unix(40126)
  