import discord

def build_search_anime_embed(anime: dict) -> discord.Embed:
    embed = discord.Embed(
        title=f'🎬 {anime["title"]}',
        description=anime['synopsis'][:300] + '...',
        color=discord.Color.purple()
    )
    embed.add_field(name='📺 Type', value=anime['show_type'], inline=True)
    embed.add_field(name='⭐ Rating', value=str(anime['average_rating']), inline=True)
    embed.add_field(name='🎞️ Episodes', value=str(anime['episodes']), inline=True)
    embed.add_field(name='🗓️Airing', value=str(anime['airing']), inline=True)
    embed.add_field(name='Rank', value=str(anime['ranking']), inline=True)
    embed.add_field(name='Genres', value=str(anime['genres']), inline=True)
    embed.set_thumbnail(url=anime['image'])
    return embed
