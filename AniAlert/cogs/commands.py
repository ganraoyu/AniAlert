import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from db.database import cursor, conn

from .seasonal import SeasonalAnimeLookUpCog
from .search import AllAnimeSearchCog
from .remove import RemoveAnimeCog
from .notify_list import CheckNotifyListCog
from .notify_airing import NotifyAnimeAiredCog
from .clear_notify_list import ClearNotifyListCog
from .random import RandomAnimeCog

async def setup(bot):
  await bot.add_cog(SeasonalAnimeLookUpCog(bot))
  await bot.add_cog(AllAnimeSearchCog(bot))
  await bot.add_cog(CheckNotifyListCog(bot, cursor))
  await bot.add_cog(NotifyAnimeAiredCog(bot, cursor, conn))
  await bot.add_cog(RemoveAnimeCog(bot, cursor, conn))
  await bot.add_cog(ClearNotifyListCog(bot, cursor, conn))
  await bot.add_cog(RandomAnimeCog(bot))
