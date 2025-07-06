import discord
from AniAlert.utils.embed_builder import build_anime_airing_notification_embed

def get_dummy_airing_data(**overrides):
    data = {
        'anime_name': "Attack on Titan",
        'episode': 12,
        'image_url': "http://example.com/image.jpg",
        'user_id': "123456789"
    }
    data.update(overrides)
    return data

def test_build_anime_airing_notification_embed():
    dummy = get_dummy_airing_data()
    embed = build_anime_airing_notification_embed(
        dummy['anime_name'],
        dummy['episode'],
        dummy['image_url'],
        dummy['user_id']
    )

    assert isinstance(embed, discord.Embed)
    assert embed.title == f"📢Episode {dummy['episode']} Aired: {dummy['anime_name']}"
    assert embed.description == f"<@{dummy['user_id']}> A new episode just dropped — go check it out!"
    assert embed.thumbnail.url == dummy['image_url']
    assert embed.footer.text == "AniAlert • Airing Notification"
