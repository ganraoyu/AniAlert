import discord
from discord.ext import commands, tasks
from discord import app_commands, Interaction

class GetChoices(commands.Cog):
  @staticmethod
  def choices():
    MEDIA_TYPE_CHOICES = [
      app_commands.Choice(name='All', value='all'),
      app_commands.Choice(name='TV', value='TV'),
      app_commands.Choice(name='Movie', value='MOVIE'),
      app_commands.Choice(name='OVA', value='OVA'),
      app_commands.Choice(name='ONA', value='ONA'),
      app_commands.Choice(name='Special', value='special'),
    ]

    STATUS_TYPE_CHOICES = [
      app_commands.Choice(name='All', value='all'),
      app_commands.Choice(name='Airing', value='airing'),
      app_commands.Choice(name='Completed', value='completed'),
    ]

    POPULAR_GENRE_TAG_CHOICES = [
        app_commands.Choice(name="Action", value="Action"),
        app_commands.Choice(name="Adventure", value="Adventure"),
        app_commands.Choice(name="Comedy", value="Comedy"),
        app_commands.Choice(name="Demons", value="Demons"),
        app_commands.Choice(name="Drama", value="Drama"),
        app_commands.Choice(name="Fantasy", value="Fantasy"),
        app_commands.Choice(name="Harem", value="Harem"),
        app_commands.Choice(name="Horror", value="Horror"),
        app_commands.Choice(name="Isekai", value="Isekai"),
        app_commands.Choice(name="Magic", value="Magic"),
        app_commands.Choice(name="Martial Arts", value="MartialArts"),
        app_commands.Choice(name="Mecha", value="Mecha"),
        app_commands.Choice(name="Mystery", value="Mystery"),
        app_commands.Choice(name="Psychological", value="Psychological"),
        app_commands.Choice(name="Romance", value="Romance"),
        app_commands.Choice(name="School", value="School"),
        app_commands.Choice(name="Sci-Fi", value="SciFi"),
        app_commands.Choice(name="Seinen", value="Seinen"),
        app_commands.Choice(name="Shounen", value="Shounen"),
        app_commands.Choice(name="Slice of Life", value="SliceOfLife"),
        app_commands.Choice(name="Sports", value="Sports"),
        app_commands.Choice(name="Supernatural", value="Supernatural"),
        app_commands.Choice(name="Thriller", value="Thriller"),
        app_commands.Choice(name="Tragedy", value="Tragedy"),
        app_commands.Choice(name="Vampire", value="Vampire"),
    ]
    
    GENRE_TYPE_CHOICES = [
        # Genre
        app_commands.Choice(name="Action", value="Action"),
        app_commands.Choice(name="Adventure", value="Adventure"),
        app_commands.Choice(name="Comedy", value="Comedy"),
        app_commands.Choice(name="Drama", value="Drama"),
        app_commands.Choice(name="Fantasy", value="Fantasy"),
        app_commands.Choice(name="Horror", value="Horror"),
        app_commands.Choice(name="Mystery", value="Mystery"),
        app_commands.Choice(name="Psychological", value="Psychological"),
        app_commands.Choice(name="Romance", value="Romance"),
        app_commands.Choice(name="Sci-Fi", value="SciFi"),
        app_commands.Choice(name="Slice of Life", value="SliceOfLife"),
        app_commands.Choice(name="Sports", value="Sports"),
        app_commands.Choice(name="Supernatural", value="Supernatural"),
        app_commands.Choice(name="Thriller", value="Thriller"),
        app_commands.Choice(name="Mecha", value="Mecha"),

        # Tags
        app_commands.Choice(name="Isekai", value="Isekai"),
        app_commands.Choice(name="Magic", value="Magic"),
        app_commands.Choice(name="Male Protagonist", value="MaleProtagonist"),
        app_commands.Choice(name="Female Protagonist", value="FemaleProtagonist"),
        app_commands.Choice(name="Reincarnation", value="Reincarnation"),
        app_commands.Choice(name="Demons", value="Demons"),
        app_commands.Choice(name="Dragons", value="Dragons"),
        app_commands.Choice(name="Gore", value="Gore"),
        app_commands.Choice(name="Martial Arts", value="MartialArts"),
        app_commands.Choice(name="School", value="School"),
        app_commands.Choice(name="Historical", value="Historical"),
        app_commands.Choice(name="Military", value="Military"),
        app_commands.Choice(name="Survival", value="Survival"),
        app_commands.Choice(name="Time Travel", value="TimeTravel"),
        app_commands.Choice(name="Virtual World", value="VirtualWorld"),
        app_commands.Choice(name="Game", value="Game"),
        app_commands.Choice(name="Harem", value="Harem"),
        app_commands.Choice(name="Parody", value="Parody"),
        app_commands.Choice(name="Coming of Age", value="ComingOfAge"),
        app_commands.Choice(name="Vampire", value="Vampire"),
    ]

    YEAR_CHOICES = [
        app_commands.Choice(name=str(year), value=year) for year in range(2000, 2025)
    ]

    SEASON_CHOICES = [
        app_commands.Choice(name="Winter", value="WINTER"),
        app_commands.Choice(name="Spring", value="SPRING"),
        app_commands.Choice(name="Summer", value="SUMMER"),
        app_commands.Choice(name="Fall", value="FALL"),
    ]

    return MEDIA_TYPE_CHOICES, STATUS_TYPE_CHOICES, POPULAR_GENRE_TAG_CHOICES, GENRE_TYPE_CHOICES, YEAR_CHOICES, SEASON_CHOICES

def get_choices():
  MEDIA_TYPE_CHOICES, STATUS_TYPE_CHOICES, POPULAR_GENRE_TAG_CHOICES, GENRE_TYPE_CHOICES, YEAR_CHOICES, SEASON_CHOICES = GetChoices.choices()
  return MEDIA_TYPE_CHOICES, STATUS_TYPE_CHOICES, POPULAR_GENRE_TAG_CHOICES, GENRE_TYPE_CHOICES, YEAR_CHOICES, SEASON_CHOICES
