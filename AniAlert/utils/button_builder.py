import discord
from utils.interaction_helper import get_user_and_guild_ids

class CombinedAnimeButtonView(discord.ui.View):
    def __init__(self, anime: dict):
        super().__init__()
        self.anime = anime

    @discord.ui.button(label="Add to notify list", style=discord.ButtonStyle.green)
    async def add_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id, _ = get_user_and_guild_ids(interaction)
        await interaction.response.send_message(
            f"✅ **{self.anime['title']}** added to your watchlist. (User ID: {user_id})",
            ephemeral=True
        )

    @discord.ui.button(label="Remove from notify list", style=discord.ButtonStyle.red)
    async def remove_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id, _ = get_user_and_guild_ids(interaction)
        await interaction.response.send_message(
            f"✅ **{self.anime['title']}** removed from your watchlist. (User ID: {user_id})",
            ephemeral=True
        )

def anime_buttons_view(anime: dict):
    buttons = CombinedAnimeButtonView(anime)
    return buttons
      
