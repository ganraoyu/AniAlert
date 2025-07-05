import pytest
import discord
from AniAlert.utils.embed_builder import build_anime_notify_list_embed

# Everything is passed into the parameters from the database
def get_dummy_data(**override):
  title = override.get('title', 'Nana')

  database_data = {
    'id': 345,
    'episode': 21, # Current episode on the list that is being notified, not total amount.
    'iso_air_time': '2025-07-05T17:12:30Z',
    'image': 'http://example.com/image.png',
  }

  database_data.update(override)
  return title, database_data

def test_notify__list_anime_all_fields_correct():
  title, database = get_dummy_data()
  embed = build_anime_notify_list_embed(
      title,
      database['id'],
      database['episode'],
      database['iso_air_time'],
      database['image']
  )
  assert isinstance(embed, discord.Embed)
  assert embed.title == f"🎬 {title} (ID: {database['id']})"
  assert embed.footer.text == 'AniAlert • Notification List'
