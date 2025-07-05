import pytest
import discord
from AniAlert.utils.embed_builder import build_add_anime_embed

def get_dummy_data(**override):
  data = {
    'title': 'Mushoku Tensei',
    'episodes': 12,
    'image': 'http://example.com/image.png',
    'time_until_airing': '20h 38m 45s',               
    'airingAt_iso': '2025-07-06T14:16:00',        
  }
  data.update(override)
  return data

def test_add_anime_embed_all_fields_correct():
  dummy = get_dummy_data()
  embed = build_add_anime_embed(dummy)

  assert isinstance(embed, discord.Embed)
  assert embed.title == '🎬 Mushoku Tensei'
  assert embed.thumbnail.url == dummy['image']
  assert embed.footer.text == "AniAlert • Anime Added"

  field_map = {f.name: f.value for f in embed.fields}
  assert field_map[f"Episode {dummy['episodes'] + 1} in"] == dummy['time_until_airing']
  assert field_map["Airing at"] == dummy['airingAt_iso']

test_data = [
  ('title', '🎬 Unknown Title', 'title'),
  ('episodes', 'N/A', 'Episode 1 in'),          
  ('time_until_airing', 'N/A', 'Episode 1 in'), 
  ('airingAt_iso', 'N/A', 'Airing at'),         
  ('image', None, 'thumbnail'),                    
]

@pytest.mark.parametrize('missing_key, expected_value, expected_field_name', test_data)
def test_add_anime_embed_missing_values(missing_key, expected_value, expected_field_name):
    dummy = get_dummy_data()
    dummy[missing_key] = None

    if missing_key == 'episodes':
        dummy['episodes'] = 0      
        dummy['time_until_airing'] = 'N/A'
    elif missing_key == 'time_until_airing':
        dummy['episodes'] = 0       
        dummy['time_until_airing'] = 'N/A'
    elif missing_key == 'airingAt_iso':
        dummy['airingAt_iso'] = 'N/A'

    embed = build_add_anime_embed(dummy)

    if expected_field_name == 'title':
        assert embed.title == expected_value
    elif expected_field_name == 'thumbnail':
        assert embed.thumbnail.url is None 
    else:
        fields = {f.name: f.value for f in embed.fields}
        assert fields[expected_field_name] == expected_value
