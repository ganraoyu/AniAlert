from discord.ext import commands
from discord import app_commands, Interaction
from utils.embed_builder import build_remove_anime_embed

class RemoveAnimeCog(commands.Cog):

  def __init__(self, bot, cursor, conn):
    self.bot = bot
    self.cursor = cursor
    self.conn = conn

  def _fetch_notify_list(self, id: int):
    self.cursor.execute('SELECT * FROM anime_notify_list WHERE id = ?', (id,))
    return self.cursor.fetchone()

  @app_commands.command(name='remove_anime', description='Remove animes from notify list')
  @app_commands.describe(id='Enter anime ID to remove')
  async def remove_anime(self, interaction: Interaction, id: int):
    await interaction.response.defer(ephemeral=True)

    result = self._fetch_notify_list(id)

    if result:
      anime_dict = {
        'id': result[0],
        'guild_id': result[1],
        'guild_name': result[2],
        'user_id': result[3],
        'user_name': result[4],
        'title': result[5],
        'episode': result[6],
        'unix_air_time': result[7],
        'iso_air_time': result[8],
        'image': result[9]
      }

      embed = build_remove_anime_embed(anime_dict)
      self.cursor.execute('DELETE FROM anime_notify_list WHERE id = ?', (id,))
      await interaction.followup.send(embed=embed, ephemeral=True)
    else:
      await interaction.followup.send(
        f"⚠️ No anime found with ID `{id}`.",
        ephemeral=True
      )

    self.conn.commit()