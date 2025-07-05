import discord
from AniAlert.utils.embed_builder import build_random_anime_embed

def get_dummy_anime(**overrides):
    data = {
        'title': 'Mob Psycho 100',
        'synopsis': 'A boy with psychic powers tries to live a normal life.',
        'episodes': '25',
        'genres': 'Action, Supernatural',
        'image': 'http://example.com/mob.png'
    }
    data.update(overrides)
    return data


def test_build_random_anime_embed():
    anime = get_dummy_anime()
    embed = build_random_anime_embed(anime)

    assert isinstance(embed, discord.Embed)
    assert embed.title == f"🎲 Random Anime: {anime['title']}"
    assert embed.description == anime['synopsis']
    assert embed.fields[0].name == '🎞️ Episodes'
    assert embed.fields[0].value == anime['episodes']
    assert embed.fields[1].name == '🎭 Genres'
    assert embed.fields[1].value == anime['genres']
    assert embed.thumbnail.url == anime['image']
    assert embed.footer.text == "AniAlert • Random Anime Generator"
