import pytest
import discord

from AniAlert.utils.embed_builder import build_seasonal_anime_embed

def get_dummy_data(**overrides):
  data = {
    'title': 'Solo Leveling',
    'synopsis': 'Leveling by yourself',
    'image': 'http://example.com/image.png'
  }
  data.update(overrides)
  return data 

def test_seasonal_anime_embed_all_fields_correct():
  dummy = get_dummy_data()
  embed = build_seasonal_anime_embed(dummy)

  assert isinstance(embed, discord.Embed)
  assert embed.title == '🎬 Solo Leveling'
  assert embed.description == 'Leveling by yourself'
  assert embed.thumbnail.url == 'http://example.com/image.png'

test_data = [
  ('title', '🎬 Unknown Title', 'title'),
  ('synopsis', 'No synopsis available.', 'description')
]

@pytest.mark.parametrize('missing_key, expected_value, expected_field_name', test_data)
def test_search_anime_embed_missing_values(missing_key, expected_value, expected_field_name):
  dummy = {
    'title': 'One Piece',
    'synopsis': 'Pirate adventure',
    'image': 'http://example.com/image.png',
  }
  dummy[missing_key] = None
  embed = build_seasonal_anime_embed(dummy)

  if expected_field_name == 'title':
    assert embed.title == expected_value
  elif expected_field_name == 'description':
    assert embed.description == expected_value