from unittest.mock import patch
from AniAlert.providers.anilist.seasonal import get_seasonal_animes_anilist
from AniAlert.utils.time_converter import convert_unix

@patch('AniAlert.providers.anilist.seasonal.requests.post')
def test_get_dandadan_anime(mock_post):
  mock_post.return_value.json.return_value = {
    "data": {
      "Page": {
        "media": [
          {
            "id": 185660,
            "title": {
              "romaji": "Dandadan 2nd Season",
              "english": "DAN DA DAN Season 2"
            },
            "averageScore": 81,
            "popularity": 94978,
            "rankings": [],
            "season": "SUMMER",
            "seasonYear": 2025,
            "description": "The second season of <i>Dandadan</i>.<br><br> Okarun and Jiji have made a strange discovery.",
            "airingSchedule": {
              "nodes": [
                {
                  "airingAt": 1752161160,
                  "timeUntilAiring": 3600,
                  "episode": 2
                }
              ]
            },
            "coverImage": {
              "extraLarge": "https://s4.anilist.co/file/anilistcdn/media/anime/cover/large/bx185660-uB8RUMBGovGr.jpg"
            }
          }
        ]
      }
    }
  }

  result = get_seasonal_animes_anilist(1, 1)

  assert isinstance(result, list)
  assert len(result) == 1

  anime = result[0]
  assert anime['anilist_id'] == 185660
  assert anime['title'] == "DAN DA DAN Season 2"
  assert anime['average_rating'] == 81
  assert anime['seasonal_ranking'] == 1
  assert "<i>" not in anime['synopsis']
  assert "<br>" not in anime['synopsis']
  assert "Dandadan" in anime['synopsis']
  assert anime['image'].endswith(".jpg")
  assert anime['airingAt_unix'] == 1752161160
  assert anime['airingAt_iso'] == "2025-07-10T15:26:00"
  assert anime['episodes'] == 2
  assert anime['time_until_airing'] == convert_unix(3600)
