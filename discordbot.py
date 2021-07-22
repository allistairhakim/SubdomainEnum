import os
from discord.ext import commands

bot = commands.Bot(command_prefix='.')
# I am assuming that you have a test.py cog in a cogs folder

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

  else:
    print(f'Unable to load {filename[:-3]}')

bot.run('ODY3ODQ2NDkxNTYwODY5OTM4.YPnDBw.DHwdIQxtI8jTxUmv1AvpIoGhr6s')
