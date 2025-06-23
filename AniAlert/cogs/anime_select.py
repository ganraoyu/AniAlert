import discord
from discord.ui import Select, View

class pick_anime_select(Select):
  def __init__(self):
    options = [
      discord.SelectOption(
        label='One Piece',
        value='One Piece',
        description='A long-running anime about pirates.',
        emoji='🏴‍☠️'
      ),
      discord.SelectOption(
        label='Naruto',
        value='Naruto',
        description='A story about ninjas and their adventures.',
        emoji='🥷'
      ),
      discord.SelectOption(
        label='Attack on Titan',
        value='Attack on Titan',
        description='A dark fantasy anime about humanity fighting against giant humanoid creatures.',
        emoji='🗡️'
      ),
      discord.SelectOption(
        label='My Hero Academia',
        value='My Hero Academia',
        description='A world where people have superpowers called Quirks.',
        emoji='🦸'
      ),
    ]

    super().__init__(placeholder='Pick an anime', min_values=1, max_values=len(options), options=options)

  async def callback(self, interaction: discord.Interaction):
    selected = ', '.join(self.values)
    await interaction.response.send_message(f"You picked: {selected}", ephemeral=True)

class pick_anime_view(View):
  def __init__(self):
    super().__init__()
    self.add_item(pick_anime_select())
