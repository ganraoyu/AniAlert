from discord.ui import Modal, TextInput
from discord import Interaction

class SearchAnimeInput(Modal, title="Search for Anime"):
    anime_name = TextInput(label="Anime Name", required=True)

    async def on_submit(self, interaction: Interaction):
        await interaction.response.send_message(f"You searched for: {self.anime_name}", ephemeral=True)
