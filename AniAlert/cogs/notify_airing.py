
from discord.ext import commands, tasks

from services.anime_service import get_full_anime_info
from services.airing_checker import check_notify_list, check_if_aired

from utils.embed_builder import build_anime_airing_notification_embed

class NotifyAnimeAiredCog(commands.Cog):
  def __init__(self, bot, cursor, conn):
    self.bot = bot
    self.cursor = cursor
    self.conn = conn
    self.check_airing.start()

  @tasks.loop(minutes=1)
  async def check_airing(self):
    self.cursor.execute('SELECT DISTINCT user_id, guild_id FROM anime_notify_list')
    user_guild_pairs = self.cursor.fetchall()

    for user_id, guild_id in user_guild_pairs:
      await self._process_user_guild_pair(user_id, guild_id)

  async def _process_user_guild_pair(self, user_id, guild_id):
    anime_list = check_notify_list(user_id, guild_id, self.cursor)
    aired_list = check_if_aired(anime_list)  # List of (anime, episode) tuples

    if not aired_list:
      return

    guild = self.bot.get_guild(guild_id)
    if not guild:
      return

    channel = self._get_notification_channel(guild)
    if not channel:
      return

    for anime, episode in aired_list:
      await self._handle_anime_notification(anime, episode, user_id, channel)

  def _get_notification_channel(self, guild):
    return next(
      (ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages),
      None
    )

  async def _handle_anime_notification(self, anime, episode, user_id, channel):
    anime_id = anime['anime_id']
    anime_name = anime['anime_name']
    image_url = anime['image']

    new_data = get_full_anime_info(anime_name)

    if not new_data or not new_data[0].get('airingAt_unix'):
      await self._handle_final_episode(anime_id, anime_name, user_id, channel)
      return

    await self._send_airing_notification(anime_name, episode, user_id, image_url, channel)
    self._update_airing_time(anime_id, new_data[0])
    self.conn.commit()

  async def _handle_final_episode(self, anime_id, anime_name, user_id, channel):
    self.cursor.execute('DELETE FROM anime_notify_list WHERE id = ?', (anime_id,))
    await channel.send(
      content=(
        f"<@{user_id}> 🔔 **The final episode of _{anime_name}_ just aired!**\n"
        "It has now been removed from your notify list."
      )
    )

  async def _send_airing_notification(self, anime_name, episode, user_id, image_url, channel):
    embed = build_anime_airing_notification_embed(
      anime_name=anime_name,
      episode=episode,
      image_url=image_url,
      user_id=user_id
    )
    await channel.send(content=f"<@{user_id}>", embed=embed)

  def _update_airing_time(self, anime_id, anime_data):
    self.cursor.execute(
      'UPDATE anime_notify_list SET unix_air_time = ?, iso_air_time = ? WHERE id = ?',
      (
        anime_data['airingAt_unix'],
        anime_data.get('airingAt_iso'),
        anime_id
      )
    )
