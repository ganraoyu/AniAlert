import discord

def get_user_and_guild_ids(interaction: discord.Interaction) -> tuple[int, int | None]:
  user_id = interaction.user.id
  guild_id = interaction.guild.id
  

  return user_id, guild_id