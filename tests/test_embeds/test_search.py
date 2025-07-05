import pytest
import discord
from AniAlert.utils.embed_builder import build_search_anime_embed

def get_dummy_anime(**overrides):
  data = {
    'title': 'Naruto',
    'synopsis': 'Ninja adventure',
    'show_type': 'TV',
    'average_rating': 8.7,
    'episodes': 220,
    'airing': True,
    'ranking': 1,
    'genres': ['Action', 'Adventure'],
    'image': 'http://example.com/image.png',
  }
  data.update(overrides)
  return data

def test_search_anime_embed_all_fields_correct():
  dummy = get_dummy_anime()
  embed = build_search_anime_embed(dummy)

  assert isinstance(embed, discord.Embed)
  assert embed.title == '🎬 Naruto'
  assert embed.description == 'Ninja adventure'
  assert embed.color == discord.Color.purple()
  assert embed.thumbnail.url == dummy['image']
  assert embed.footer.text == "AniAlert • Search Results"

  field_map = {}
  for field in embed.fields:
    name = field.name
    value = field.value
    field_map[name] = value
  assert field_map['📺 Type'] == 'TV'
  assert field_map['⭐ Rating'] == '8.7'
  assert field_map['🎞️ Episodes'] == '220'
  assert field_map['🗓️ Airing'] == 'True'
  assert field_map['🏆 Rank'] == '1'
  assert field_map['🎭 Genres'] == "['Action', 'Adventure']"

test_data = [
  ('title', '🎬 Unknown Title', 'title'),
  ('synopsis', 'No synopsis available.', 'description'),
  ('show_type', 'N/A', '📺 Type'),
  ('average_rating', 'N/A', '⭐ Rating'),
  ('episodes', '0', '🎞️ Episodes'),
  ('airing', 'N/A', '🗓️ Airing'),
  ('ranking', 'N/A', '🏆 Rank'),
  ('genres', 'Unknown', '🎭 Genres'),
]

@pytest.mark.parametrize("missing_key, expected_value, expected_field_name", test_data)
def test_search_anime_embed_missing_values(missing_key, expected_value, expected_field_name):
  dummy = get_dummy_anime()
  dummy[missing_key] = None
  embed = build_search_anime_embed(dummy)

  if expected_field_name == 'title':
    assert embed.title == expected_value
  elif expected_field_name == 'description':
    assert embed.description == expected_value
  else:
    fields = {f.name: f.value for f in embed.fields}
    assert fields[expected_field_name] == expected_value

def test_search_anime_embed_missing_image():
  dummy = get_dummy_anime(image=None)
  embed = build_search_anime_embed(dummy)
  assert not embed.thumbnail.url  
