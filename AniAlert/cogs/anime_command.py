from discord.ext import commands
from discord import app_commands, Interaction
from services.anime_service import get_full_anime_info
from utils.embed_builder import build_search_anime_embed
from views.search_modal import SearchAnimeInput
from views.pick_anime_view import PickAnimeView

# Searches - Require user input
# Look ups - No user input, just returns data

class SeasonalAnimeLookUpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='search_seasonal_anime', description='Return currently airing seasonal anime')
    async def seasonal_anime_slash():
        pass

class AllAnimeSearchCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Slash command to search for animes
    @app_commands.command(name='search_anime', description='Search for animes')
    async def search_anime_slash(self, interaction: Interaction, query: str):
        await interaction.response.defer(ephemeral=True)
        animes = get_full_anime_info(query)

        if not animes:
            await interaction.followup.send('❌ No results found.', ephemeral=True)
            return

        for anime in animes:
            embed = build_search_anime_embed(anime)
            await interaction.followup.send(embed=embed, ephemeral=True)

    # Modal to search for animes
    @app_commands.command(name='search_anime_modal', description='Open a modal to search for animes')
    async def search_anime_modal(self, interaction: Interaction):
        modal = SearchAnimeInput()
        await interaction.response.send_modal(modal)

    # Command to search for animes using a modal
    @commands.command()
    async def pick_animes(self, ctx):
        view = PickAnimeView()
        await ctx.send('Please select animes:', view=view)


class CharacterSearchCog(commands.Cog):
    pass 

async def setup(bot):    
    await bot.add_vog(SeasonalAnimeLookUpCog(bot))

    await bot.add_cog(AllAnimeSearchCog(bot))
    await bot.add_cog(CharacterSearchCog(bot))
