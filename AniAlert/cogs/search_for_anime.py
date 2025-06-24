import discord
from discord.ui import TextInput, Modal
from providers import search_anime
  
class search_anime_input(Modal):
  def __init__(self):
    super().__init__(title="Search for Anime")
    
    self.anime_input = TextInput(
      label="Search Anime",
      placeholder="Enter the name of the anime you want to search for...",
      style=discord.TextStyle.short,
      max_length=100,
      required=True
    )
    self.add_item(self.anime_input)
    
  async def on_submit(self, interaction: discord.Interaction):
    search_query = self.anime_input.value
    await interaction.response.send_message(f"Searching for anime: {search_query}", ephemeral=True)
