
from discord.ext import commands
from discord import app_commands, Interaction

from utils.interaction_helper import get_user_and_guild_ids

class ClearNotifyListCog(commands.Cog):
  def __init__(self, bot, cursor, conn):
    self.bot = bot
    self.cursor = cursor
    self.conn = conn

  @app_commands.command(name='clear_list')
  async def clear(self, interaction: Interaction):
    await interaction.response.defer(ephemeral=True)

    user_id, guild_id = get_user_and_guild_ids(interaction)
    user_id, guild_id = int(user_id), int(guild_id)
    deleted_count = self._delete_notify_list(user_id, guild_id)

    if deleted_count == 0:
      await interaction.followup.send(
        "⚠️ Your notify list is empty.", ephemeral=True
      )
      return

    await interaction.followup.send(
      content=(
        "✅ **All your anime notifications have been successfully removed!**\n"
        "You will no longer receive alerts for any anime from your notify list."
      ),
      ephemeral=True
    )

  def _delete_notify_list(self, user_id: int, guild_id: int) -> int:
    query = 'DELETE FROM anime_notify_list WHERE guild_id = ? AND user_id = ?'
    self.cursor.execute(query, (guild_id, user_id))
    self.conn.commit()
    return self.cursor.rowcount