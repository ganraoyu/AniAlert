import discord
from discord.ext import commands, tasks
from discord import app_commands, Interaction

class GetChoices(commands.Cog):
  @staticmethod
  def choices():
    MEDIA_TYPE_CHOICES = [
      app_commands.Choice(name='All', value='all'),
      app_commands.Choice(name='TV', value='TV'),
      app_commands.Choice(name='Movie', value='movie'),
      app_commands.Choice(name='OVA', value='OVA'),
      app_commands.Choice(name='ONA', value='ONA'),
      app_commands.Choice(name='Special', value='special'),
    ]

    STATUS_TYPE_CHOICES = [
      app_commands.Choice(name='All', value='all'),
      app_commands.Choice(name='Airing', value='airing'),
      app_commands.Choice(name='Completed', value='completed'),
    ]

    return MEDIA_TYPE_CHOICES, STATUS_TYPE_CHOICES
  
def get_choices():
  MEDIA_TYPE_CHOICES, STATUS_TYPE_CHOICES = GetChoices.choices()
  return  MEDIA_TYPE_CHOICES, STATUS_TYPE_CHOICES

