import pytest
import discord
from AniAlert.utils.embed_builder import build_remove_anime_embed

def get_dummy_data(**overide):
  data = {
    'title': 'Boruto',
  }
  
  data.update(overide)
  return data

def test_remove_anime_embed_all_fields_correct():
  dummy = get_dummy_data()
  embed = build_remove_anime_embed(dummy)

  assert embed.title == '❌ Removed: Boruto'
  assert embed.footer.text == 'AniAlert • Anime Removed'