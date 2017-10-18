import discord
import math
import sys
import time
import asyncio
import random
from discord.ext import commands
import datetime
import json
import youtube_dl

async def get_pre(bot, message):
  with open('settings.json', 'r') as f:
    s = f.read()
    book = json.loads(s)
  prefix = book[str(message.guild.id)]['prefix']
  '''{}'''.format(prefix)
  return prefix

bot = commands.Bot(command_prefix=get_pre)

col = 0x38ffee
channels = bot.get_all_channels()

async def is_creator(ctx):
  person = ctx.author
  if person.id == 365938029640024064 or person.id == 199611371522883586:
    return True
  else:
    return False

async def is_owner(ctx):
  person = ctx.author
  if person.id == ctx.guild.owner.id or person.id == 365938029640024064 or person.id == 199611371522883586:
    return True
  else:
    return False

async def is_staff(ctx):
  with open('settings.json', 'r') as f:
    s = f.read()
    book = json.loads(s)
    one = str(ctx.author.id)
    if one in book[str(ctx.guild.id)]['staff']:
      return True
    else:
      return False

@bot.event
async def on_ready():
  print('''\
Hiya, my name is:

      ___           ___           ___           ___           ___                 
     /\  \         /\  \         /\__\         /\__\         /\__\          ___   
     \:\  \       /::\  \       /:/  /        /:/  /        /:/  /         /\  \  
      \:\  \     /:/\ \  \     /:/  /        /:/  /        /:/__/          \:\  \ 
      /::\  \   _\:\-\ \  \   /:/  /  ___   /:/  /  ___   /::\__\____      /::\__\\
     /:/\:\__\ /\ \:\ \ \__\ /:/__/  /\__\ /:/__/  /\__\ /:/\:::::\__\  __/:/\/__/
    /:/  \/__/ \:\ \:\ \/__/ \:\  \ /:/  / \:\  \ /:/  / \/_|:|~~|~    /\/:/  /   
   /:/  /       \:\ \:\__\    \:\  /:/  /   \:\  /:/  /     |:|  |     \::/__/    
   \/__/         \:\/:/  /     \:\/:/  /     \:\/:/  /      |:|  |      \:\__\    
                  \::/  /       \::/  /       \::/  /       |:|  |       \/__/    
                   \/__/         \/__/         \/__/         \|__|                ''')
  game = discord.Game(name='@Tsuuki prefix to get my prefix!')
  await bot.change_presence(game=game)

@bot.event
async def on_member_join(member):
  with open('settings.json', 'r') as f:
    s = f.read()
    book = json.loads(s)
  if book[str(member.guild.id)]['welcome']['enabled']:
    channel = member.guild.get_channel(int(book[str(member.guild.id)]['welcome']['channel']))
    try:
      await channel.send(book[str(member.guild.id)]['welcome']['message'].format(member.mention))
    except:
      await channel.send(book[str(member.guild.id)]['welcome']['message'])
  else:
    pass

@bot.event
async def on_guild_join(guild):
  with open('settings.json', 'r') as f:
    s = f.read()
    book = json.loads(s)
  with open('settings.json', 'w') as d:
    book[str(guild.id)] = {
      "welcome": {
			"enabled": False,
			"channel": "",
			"message": ""
		},
      'staff': [

      ],
      'tags': {

      },
      'assignable': [

      ],
      'prefix': ']'
    }
    m = json.dumps(book)
    d.write(m)
  await guild.owner.send('Thanks for adding me to your server ({})! Incase it wasn\'t you who added me, then someone with permissions did so. My prefix is `]`, but you can set it to whatever you want by doing `]setprefix <prefix>`. Enjoy!'.format(guild.name))

@bot.event
async def on_guild_remove(guild):
  with open('settings.json', 'r') as f:
    s = f.read()
    book = json.loads(s)
  with open('settings.json', 'w') as d:
    del book[str(guild.id)]
    m = json.dumps(book)
    d.write(m)
  await guild.owner.send('Sorry to see that I had to go p~p if you have any suggestions for the bot, let the creator know :point_right: **Sinon#5047**')

@bot.event
async def on_message(message):
  tsuuki = '<@368973799636336651>'
  if message.content == '<@368973799636336651> prefix':
    channel = message.channel
    with open('settings.json', 'r') as f:
      s = f.read()
      book = json.loads(s)
    await channel.send('The prefix for this server is: `{}`'.format(book[str(message.guild.id)]['prefix']))
  else:
    await bot.process_commands(message)

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, ytdl.extract_info, url)
        
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
'''
class gay:
    def __init__(self, bot):
      self.bot = bot

    @commands.command()
    async def vtimer(self, ctx, arg: int):
      """acts gay"""

      if ctx.voice_client is None:
        if ctx.author.voice.channel:
          await ctx.author.voice.channel.connect()
        else:
          return await ctx.send("Not connected to a voice channel.")
      
      if ctx.voice_client.is_playing():
        ctx.voice_client.stop()
      await ctx.send('Setting timer for {} minute(s)!'.format(arg))
      await asyncio.sleep(arg * 60 - 10)
      player = await YTDLSource.from_url('https://www.youtube.com/watch?v=0K_XUY4esNw', loop=self.bot.loop)
      ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
      
      await asyncio.sleep(10)
      await ctx.send('Finished! ({} minute(s))'.format(arg))
'''
'''-----------------------------------------------------------------------------------------------------------------'''
class Fun:
  '''Stuff to just fool around with.'''
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(help='Predicts whatever question you give it.', name="8ball")
  async def ball(self, ctx, *args):
    ques = ' '.join(args)
    answers = ['It is certain', 'It is decidedly so', 'Without a doubt', 'Yes definitely',
    'You may rely on it', 'As I see it, yes', 'Most likely', 'Outlook good', 'Yes', 'Signs point to yes',
      'Reply hazy try again', 'Ask again later', 'Better not tell you now', 'Cannot predict now',
      'Concentrate and ask again', 'Don\'t count on it' ,'My reply is no' ,'My sources say no' ,
      'Outlook not so good' ,'Very doubtful']
    ans = random.choice(answers)
    await ctx.channel.send(':8ball: | Question: {}\n:8ball: | Answer: {}'.format(ques, ans))

  @commands.command(help='Digital Coin Flip.', aliases=['cf'])
  async def coinflip(self, ctx):
    coin = random.randrange(1,3)
    if coin == 1:
      await ctx.send('You flipped tails!')
    else:
      await ctx.send('You flipped heads!')

  @commands.command(help='Googles something for you.')
  async def lmgtfy(self, ctx, *args):
    await ctx.send('http://lmgtfy.com/?q={}'.format('+'.join(args)))

  @commands.command()
  async def rps(self, ctx, arg):
    '''Makes the bot play rock/paper/scissors with you.'''
    if arg not in ['r', 'rock', 'p', 'paper', 's', 'scissors']:
      await ctx.channel.send('I don\'t think we use that to play rock paper scissors!')
    else:
      hand = random.randrange(1,4)
      if hand == 1:
        if arg in ['r', 'rock']:
          await ctx.channel.send(':scissors: | I chose scissors! You win.')
        elif arg in ['s', 'scissors']:
          await ctx.channel.send(':scissors: | I chose scissors! It\'s a tie game.')
        else:
          await ctx.channel.send(':scissors: | I chose scissors! I win.')
      elif hand == 2:
        if arg in ['s', 'scissors']:
          await ctx.channel.send(':newspaper: | I chose paper! You win.')
        elif arg in ['p', 'paper']:
          await ctx.channel.send(':newspaper: | I chose paper! It\'s a tie game.')
        else:
          await ctx.channel.send(':newspaper: | I chose paper! I win.')
      elif hand == 3:
        if arg in ['p', 'paper']:
          await ctx.channel.send(':metal: | I chose rock! You win.')
        elif arg in ['r', 'rock']:
          await ctx.channel.send(':metal: | I chose rock! It\'s a tie game.')
        else:
          await ctx.channel.send(':metal: | I chose rock! I win.')

  @commands.command()
  async def rr(self, ctx, *, args = None):
    '''Plays a game of russian roullette.'''
    if args == None:
      future = random.randrange(1,7)
      bullet = 0
      await ctx.send('You spin the cylinder of the revolver with 1 bullet in it...')
      await asyncio.sleep(1)
      await ctx.send('..you place the muzzle against your head and pull the trigger...')
      await asyncio.sleep(3)
      if future == 6 or bullet == 6:
        await ctx.send('...your brain gets splattered all over the wall.')
        bullet = 0
      else:
        await ctx.send('...you live to see another day.')
        bullet = bullet + 1
    else:
      rounds = int(args)
      if rounds >= 7 and rounds < 0:
        await ctx.send('That\'s not a valid number! Choose between 0 and 6')
      else:
        future = random.randrange(rounds,7)
        await ctx.send('You spin the cylinder of the revolver with {} bullet(s) in it...'.format(rounds))
        await asyncio.sleep(1)
        await ctx.send('..you place the muzzle against your head and pull the trigger...')
        await asyncio.sleep(3)
        if future <= rounds:
          await ctx.send('...your brain gets splattered all over the wall.')
        else:
          await ctx.send('...you live to see another day.')  
  
  @commands.command(help='Controls the tag.')
  async def tag(self, ctx, *args):
    if not args or args[0] == 'help':
      with open('settings.json', 'r') as f:
        s = f.read()
        book = json.loads(s)
      await ctx.send('```Tag Help\n\nAll tags will be lowercased, so trying to make two tags with the same name will just end up replacing the old one with the new one. Also, if you use a link that **isn\'t** an image, make sure to put something with it. For example, "]tag add a_video Hi There <video_link_here>". For an image, just do "]tag add an_image <link_here>"\n\n{0}tag <name>                       posts the message under that name.\n{0}tag [add|a] <name> <the message> Adds the tag specified.\n{0}tag [remove|r] <name>            Removes the tag specified (by the name, not message.)\n{0}tag help                         Shows this message.```'.format(book[str(ctx.guild.id)]['prefix']))
    elif args[0].lower() == 'add' or args[0].lower() == 'a':
      if await is_staff(ctx):
        with open('settings.json', 'r') as f:
          s = f.read()
          book = json.loads(s)
          with open('settings.json', 'w') as d:
            book[str(ctx.guild.id)]['tags'][args[1].lower()] = args[2:]
            m = json.dumps(book)
            d.write(m)
        await ctx.send('Successfully added **{0}** to the tag list!'.format(args[1]))
      else:
        await ctx.send('You do not have permissions to add tags! Sorry!')
    elif args[0].lower() == 'remove' or args[0].lower() == 'r':
      if await is_staff(ctx):
        with open('settings.json', 'r') as f:
          s = f.read()
          book = json.loads(s)
          with open('settings.json', 'w') as d:
            del book[str(ctx.guild.id)]['tags'][args[1].lower()]
            m = json.dumps(book)
            d.write(m)
        await ctx.send('Successfully removed **{0}** from the tag list!'.format(args[1]))
      else:
        await ctx.send('You do not have permissions to add tags! Sorry!')
    else:
      with open('settings.json', 'r') as f:
        s = f.read()
        book = json.loads(s)
        if args[0].lower() in book[str(ctx.guild.id)]['tags']:
          try:
            emb = discord.Embed(title='Tag: {}'.format(args[0].lower()), color=col)
            emb.set_image(url=book[str(ctx.guild.id)]['tags'][args[0].lower()][0])
            await ctx.send(embed=emb)
          except:
            await ctx.send(' '.join(book[str(ctx.guild.id)]['tags'][args[0].lower()]))
        else:
          await ctx.send('Sorry, could not find **{0}** in the tags! Use ``{1}tags`` to find my tag list!'.format(' '.join(args[0:]), book[str(ctx.guild.id)]['prefix']))

  @commands.command(help='Gives a list of tags.')
  async def tags(self, ctx):
    with open('settings.json') as f:
      s = f.read()
      book = json.loads(s)
      
      emb = discord.Embed(title='List of tags:', description='{}'.format(', '.join(list(book[str(ctx.guild.id)]['tags']))), color=col)
      await ctx.send(embed=emb)  
'''-----------------------------------------------------------------------------------------------------------------'''
class Staff:
  '''Staff / Admin commands.'''
  def __init__(self, bot):
    self.bot = bot

  @commands.command(help='Shuts down the bot.', aliases=['sd'])
  @commands.check(is_creator)
  async def shutdown(self, ctx):
    await ctx.channel.send('Shutting down...')
    bot.logout()
    sys.exit()

  @commands.command(help='Kicks the player specified.')
  @commands.check(is_staff)
  async def kick(self, ctx, user: discord.Member):
    await user.kick()
    await ctx.send('Successfully kicked {0.name}.'.format(user))

  @commands.command(help='Bans the player specified.')
  @commands.check(is_staff)
  async def ban(self, ctx, user: discord.Member):
    await user.ban()
    await ctx.send('Successfully banned {0.name}.'.format(user))
  
  @commands.command(aliases=['w'], help='Controls the welcome message.')
  @commands.check(is_owner)
  async def welcome(self, ctx, *args):
    if not args or args[0] == 'help':
      with open('settings.json', 'r') as f:
        s = f.read()
        book = json.loads(s)
      await ctx.send('```Welcome Help\n\n{0}welcome enable               Enables the welcome message.\n{0}welcome disable              Disables the welcome message.\n{0}welcome test                 Creates a simulation of the author joining.\n{0}welcome set_channel #channel Sets the welcome channel.\n{0}welcome edit                 Edits the welcome message! Leave empty for nothing! If you put \'{{}}\' it will mention them.\n{0}welcome info                 Shows you what the welcome message is as well as the welcome channel.\n{0}welcome help                 Shows this message.```'.format(book[str(ctx.guild.id)]['prefix']))
    elif args[0] == 'test':
      with open('settings.json', 'r') as f:
        s = f.read()
        book = json.loads(s)
      try:
        await ctx.send(book[str(ctx.guild.id)]['welcome']['message'].format(ctx.author.mention))
      except:
        await ctx.send(book[str(ctx.guild.id)]['welcome']['message'])
    elif args[0] == 'set_channel':
      try:
        channel = discord.utils.get(ctx.guild.channels, mention=args[1])
      except:
        channel = None
      with open('settings.json', 'r') as f:
        s = f.read()
        book = json.loads(s)
      with open('settings.json', 'w') as d:
        if channel == None:
          book[str(ctx.guild.id)]['welcome']['channel'] = ''
          m = json.dumps(book)
          d.write(m)
          await ctx.send('Set the new welcome channel to None!')
        else:
          book[str(ctx.guild.id)]['welcome']['channel'] = str(channel.id)
          m = json.dumps(book)
          d.write(m)
          await ctx.send('Set the new welcome channel to {}!'.format(' '.join(args[1:])))
    elif args[0] == 'edit':
      with open('settings.json', 'r') as f:
        s = f.read()
        book = json.loads(s)
      with open('settings.json', 'w') as d:
        book[str(ctx.guild.id)]['welcome']['message'] = ' '.join(args[1:])
        m = json.dumps(book)
        d.write(m)
      await ctx.send('Set the new welcome message! Check what you set it do by doing ``{}welcome info``!'.format(book[str(ctx.guild.id)]['prefix']))
    elif args[0] == 'enable':
      with open('settings.json', 'r') as f:
        s = f.read()
        book = json.loads(s)
      with open('settings.json', 'w') as d:
        book[str(ctx.guild.id)]['welcome']['enabled'] = True
        m = json.dumps(book)
        d.write(m)
      await ctx.send('Successfully enabled the welcome message!')
    elif args[0] == 'disable':
      with open('settings.json', 'r') as f:
        s = f.read()
        book = json.loads(s)
      with open('settings.json', 'w') as d:
        book[str(ctx.guild.id)]['welcome']['enabled'] = False
        m = json.dumps(book)
        d.write(m)
      await ctx.send('Successfully disabled the welcome message!')
    elif args[0] == 'info':
      with open('settings.json', 'r') as f:
        s = f.read()
        book = json.loads(s)
      prop = book[str(ctx.guild.id)]['welcome']
      emb = discord.Embed(color=col)
      emb.add_field(name='Enabled', value=prop['enabled'], inline=False)
      if not prop['channel']:
        emb.add_field(name='Channel Set', value='None Set'.format(prop['channel']), inline=False)
      else:
        emb.add_field(name='Channel Set', value='<#{}>'.format(prop['channel']), inline=False)
      if not prop['message']:
        emb.add_field(name='Current Message', value='None Set', inline=False)
      else:
        emb.add_field(name='Current Message', value=prop['message'], inline=False)
      await ctx.send(embed=emb)

  @commands.command(aliases=['sp'], help='Sets a prefix to whatever you put next. (No Spaces)')
  @commands.check(is_owner)
  async def setprefix(self, ctx, prefix):
    with open('settings.json', 'r') as f:
      s = f.read()
      book = json.loads(s)
    with open('settings.json', 'w') as d:
      book[str(ctx.guild.id)]['prefix'] = prefix
      m = json.dumps(book)
      d.write(m)
    await ctx.send('Successfully set the prefix to `{}`!'.format(prefix))

  @commands.command(help='Adds the tagged player to the staff list.', aliases=['astaff'])
  @commands.check(is_owner)
  async def addstaff(self, ctx, user: discord.Member):
    with open('settings.json', 'r') as f:
      s = f.read()
      book = json.loads(s)
    with open('settings.json', 'w') as d:
      book[str(ctx.guild.id)]['staff'].append(str(user.id))
      m = json.dumps(book)
      d.write(m)
    await ctx.send('Successfully added {} to the staff list!'.format(user.mention))

  @commands.command(help='removes the tagged player to from staff list.', aliases=['rstaff'])
  @commands.check(is_owner)
  async def removestaff(self, ctx, user: discord.Member):
    with open('settings.json', 'r') as f:
      s = f.read()
      book = json.loads(s)
    with open('settings.json', 'w') as d:
      book[str(ctx.guild.id)]['staff'].remove(str(user.id))
      m = json.dumps(book)
      d.write(m)
    await ctx.send('Successfully removed {} from the staff list!'.format(user.mention))

  @commands.command(help='Purges the amount of messages given.')
  @commands.check(is_staff)
  async def purge(self, ctx, *, amount):
    if int(amount) >= 2501:
      await ctx.send('Sorry! Maximum purge amount is 2500!')
    else:
      await ctx.channel.purge(limit=int(amount))
      msg = await ctx.send('Successfully purged {} messages!'.format(str(amount)))
      await asyncio.sleep(3)
      await msg.delete()
'''-----------------------------------------------------------------------------------------------------------------'''
class Info:
  '''Info commands to retrieve info from certain things.'''
  def __init__(self, bot):
    self.bot = bot

  @commands.command(aliases=['uinfo'], help='Info about the user mentioned.')
  async def userinfo(self, ctx, user: discord.Member = None):
    person = ctx.author if not user else user

    r = []
    for role in person.roles:
      r.append(role.name)
    emb = discord.Embed(color=col)
    emb.set_author(name=person, icon_url=person.avatar_url)
    emb.set_thumbnail(url=person.avatar_url)
    emb.add_field(name='Nickname', value=person.nick)
    emb.add_field(name='ID', value=person.id)
    emb.add_field(name='Status', value=person.status)
    emb.add_field(name='Playing', value=person.game)
    emb.add_field(name='Created At', value='{:%D @ %I:%M%p}'.format(person.created_at))
    emb.add_field(name='Joined At', value='{:%D @ %I:%M%p}'.format(person.joined_at))
    emb.add_field(name='Bot', value=person.bot, inline=False)
    emb.add_field(name='Roles [{}]'.format(len(person.roles)), value=', '.join(r))
    await ctx.send(embed=emb)

    
  @commands.command(help='Info about the bot.')
  async def info(self, ctx):
    with open('settings.json', 'r') as f:
      s = f.read()
      book = json.loads(s)
    emb = discord.Embed(color=col)
    emb.add_field(name='Creators', value='Sinon#5047', inline=False)
    emb.add_field(name='Created', value='{:%A, %B %dth %Y @ %I:%M%p}'.format(bot.user.created_at), inline=False)
    emb.add_field(name='About', value='This bot was created by **Sinon#5047** on a boring night, yeah that\'s basically it. If something isn\'t working, report it by using `{0}bug_report <the bug>`.'.format(book[str(ctx.guild.id)]['prefix']), inline=False)
    emb.add_field(name='Want to add me?', value='[**Click Here**](https://discordapp.com/oauth2/authorize/?permissions=2146958591&scope=bot&client_id=368973799636336651)', inline=True)
    emb.add_field(name='Need help?', value='[**Click Here**](https://discord.gg/xAFMPHX)', inline=True)
    emb.set_thumbnail(url=bot.user.avatar_url)
    
    await ctx.send(embed=emb)

  @commands.command(help='Gives info about the server.', aliases=['sinfo'])
  async def serverinfo(self, ctx):
    if len(ctx.guild.categories) == 1:
      c = '1 Category'
    else:
      c = '{} Categories'.format(len(ctx.guild.categories))
    
    with open('settings.json', 'r') as f:
        s = f.read()
        book = json.loads(s)
    
    d = len(ctx.guild.channels) - len(ctx.guild.categories)
    emb = discord.Embed(title='{}\'s Server Info'.format(ctx.guild.name), description='**ID:** {0}\n**Shard:** {1}'.format(ctx.guild.id, ctx.guild.shard_id),color=col)
    emb.set_thumbnail(url=ctx.guild.icon_url)
    emb.add_field(name='Member Count', value=len(ctx.guild.members), inline=True)
    emb.add_field(name='Channels [{}]'.format(d), value='{0} Text | {1} Voice'.format(len(ctx.guild.text_channels), len(ctx.guild.voice_channels)), inline=True)
    emb.add_field(name='Categories', value=c, inline=True)
    emb.add_field(name='Region', value=ctx.guild.region, inline=True)
    emb.add_field(name='Verification Level', value=ctx.guild.verification_level, inline=True)
    emb.add_field(name='Owner', value='{0}#{1} ({2})'.format(ctx.guild.owner.name, ctx.guild.owner.discriminator, ctx.guild.owner.id), inline=False)
    emb.add_field(name='Created On', value='{:%D @ %I:%M%p}'.format(ctx.guild.created_at), inline=False)
    emb.add_field(name='Roles [{}]'.format(len(ctx.guild.roles)), value='For a list of roles type ``{0}allroles``'.format(book[str(ctx.guild.id)]['prefix']), inline=False)
    emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    emb.set_footer(text='Command executed: {:%A, %B %Y at %I:%M%p}'.format(datetime.datetime.now()), icon_url=bot.user.avatar_url)
    await ctx.send(embed=emb)

  @commands.command(help='Shows all roles in the whole guild.')
  async def allroles(self, ctx):
    r = []
    for role in ctx.guild.roles:
      r.append(role.name)
    emb = discord.Embed(title='{} Roles'.format(len(ctx.guild.roles)), description=', '.join(r), color=col)
    await ctx.send(embed=emb)

  @commands.command(help='Gives the avatar of the user specified.')
  async def avatar(self, ctx, member: discord.Member = None):
      person = ctx.author if not member else member
      emb = discord.Embed(title='{0.name}\'s avatar:'.format(person), description='[**Avatar Link**]({0})'.format(person.avatar_url), color=col)
      emb.set_image(url=person.avatar_url)
      emb.set_footer(text='Command executed: {:%A, %B %Y at %I:%M%p}'.format(datetime.datetime.now()), icon_url=bot.user.avatar_url)
      emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
      await ctx.send(embed=emb)

  @commands.command(help='Allows you to report a bug for the bot creator to review. (If abused you will be put on a bug report ban list until further notice)', aliases=['br', 'bugreport'])
  async def bug_report(self, ctx, *args):
    report = args
    creator = bot.get_guild(369955504983638027).owner
    with open('no_more_reports.json', 'r') as f:
      s = f.read()
      book = json.loads(s)
    print(ctx.author)
    print(book)
    if str(ctx.author) in book:
      await ctx.send('Sorry! You\'ve been banned from sending bug reports until further notice.')
    else:
      await creator.send('Bug Report: {0}\n\nSent By: {1}#{2} ({3} | {4})'.format(' '.join(args), ctx.author.name, ctx.author.discriminator, ctx.guild.name, ctx.guild.id))
      await ctx.send('Successfully sent the bug report!')
'''-----------------------------------------------------------------------------------------------------------------'''
class Emotes:
  '''Allows you to kiss, hug, etc.'''
  def __init__(self, bot):
    self.bot = bot

  @commands.command(help='Gives the lovely person a hug!', aliases=['hugs'])
  async def hug(self, ctx, member: discord.Member = None):
    await ctx.message.delete()
    person = ctx.author if not member else member
    with open('hugs.json', 'r') as f:
      s = f.read()
      book = json.loads(s)
    hug = random.randrange(1, len(book))

    if person == ctx.author:
      await ctx.send('{0} hugged themself ;-;\n{1}'.format(person.mention, book[0]))
    else:
      await ctx.send('{0} hugged {1} ~<3\n{2}'.format(ctx.author.mention, person.mention, book[hug]))

  @commands.command(help='Gives the lovely person a kiss!', aliases=['kisses'])
  async def kiss(self, ctx, member: discord.Member = None):
    await ctx.message.delete()
    person = ctx.author if not member else member
    with open('kisses.json', 'r') as f:
      s = f.read()
      book = json.loads(s)
    kiss = random.randrange(1, len(book))

    if person == ctx.author:
      await ctx.send('{0} tried to kiss themself ;-;\n{1}'.format(person.mention, book[0]))
    else:
      await ctx.send('{0} kissed {1} >/////<\n{2}'.format(ctx.author.mention, person.mention, book[kiss]))

  @commands.command(help='Gives the lovely person a good cuddle!', aliases=['cuddles'])
  async def cuddle(self, ctx, member: discord.Member = None):
    await ctx.message.delete()
    person = ctx.author if not member else member
    with open('cuddles.json', 'r') as f:
      s = f.read()
      book = json.loads(s)
    cuddle = random.randrange(1, len(book))

    if person == ctx.author:
      await ctx.send('{0} tried to cuddle themself ;-;\n{1}'.format(person.mention, book[0]))
    else:
      await ctx.send('{0} cuddled {1} :3\n{2}'.format(ctx.author.mention, person.mention, book[cuddle]))

  @commands.command(help='Gives the lovely person a pat!', aliases=['pats'])
  async def pat(self, ctx, member: discord.Member = None):
    await ctx.message.delete()
    person = ctx.author if not member else member
    with open('pats.json', 'r') as f:
      s = f.read()
      book = json.loads(s)
    pat = random.randrange(1, len(book))

    if person == ctx.author:
      await ctx.send('{0} tried to pat themself ;-;\n{1}'.format(person.mention, book[0]))
    else:
      await ctx.send('{0} patted {1} ~w~\n{2}'.format(ctx.author.mention, person.mention, book[pat]))
'''-----------------------------------------------------------------------------------------------------------------'''
class Roles:
  '''Controls self assignable roles!'''
  def __init__(self, bot):
    self.bot = bot

  @commands.command(help='Adds a role to you if the role is assignable.', aliases=['arole'])
  async def addrole(self, ctx, *, role):
    role = discord.utils.get(ctx.guild.roles, name=role)
    green = 0x29d82c
    red = 0xbc2e21
    with open('settings.json', 'r') as f:
      s = f.read()
      book = json.loads(s)
    if role.name not in book[str(ctx.guild.id)]['assignable']:
      emb = discord.Embed(description='**{}** is not allowed for self roles.'.format(role.name), color=red)
      await ctx.send(embed=emb)
    else:
      await ctx.author.add_roles(role)
      emb = discord.Embed(description='Successfully gave you the **{}** role!'.format(role.name), color=green)
      await ctx.send(embed=emb)

  @commands.command(help='Removes a role from you if the role is assignable.', aliases=['rrole'])
  async def removerole(self, ctx, *, role):
    role = discord.utils.get(ctx.guild.roles, name=role)
    green = 0x29d82c
    red = 0xbc2e21
    with open('settings.json', 'r') as f:
      s = f.read()
      book = json.loads(s)
    if role.name not in book[str(ctx.guild.id)]['assignable']:
      emb = discord.Embed(description='**{}** is not removable.'.format(role.name), color=red)
      await ctx.send(embed=emb)
    else:
      await ctx.author.remove_roles(role)
      emb = discord.Embed(description='Successfully removed the **{}** role!'.format(role.name), color=green)
      await ctx.send(embed=emb)

  @commands.command(help='Adds a role to the assignable list.', aliases=['assign'])
  @commands.check(is_staff)
  async def assignable(self, ctx, *role):
    words = ' '.join(role)
    with open('settings.json', 'r') as f:
      s = f.read()
      book = json.loads(s)
    with open('settings.json', 'w') as d:
      book[str(ctx.guild.id)]['assignable'].append(words)
      m = json.dumps(book)
      d.write(m)
    await ctx.send('Successfully added **{}** to the assignable list!'.format(words))
  
  @commands.command(help='Removes a role to from assignable list.', aliases=['unassign'])
  @commands.check(is_staff)
  async def unassignable(self, ctx, *role):
    words = ' '.join(role)
    with open('settings.json', 'r') as f:
      s = f.read()
      book = json.loads(s)
    with open('settings.json', 'w') as d:
      book[str(ctx.guild.id)]['assignable'].remove(words)
      m = json.dumps(book)
      d.write(m)
    await ctx.send('Successfully removed **{}** from the assignable list!'.format(words))

  @commands.command(help='Shows what roles you can assign yourself.')
  async def roles(self, ctx):
    with open('settings.json', 'r') as f:
      s = f.read()
      book = json.loads(s)
    emb = discord.Embed(title='{} Assignable Roles'.format(len(book[str(ctx.guild.id)]['assignable'])), description=', '.join(book[str(ctx.guild.id)]['assignable']), color=col)
    await ctx.send(embed=emb)
    



'''
class Music:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        
        await channel.connect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        if ctx.voice_client is None:
            if ctx.author.voice.channel:
                await ctx.author.voice.channel.connect()
            else:
                return await ctx.send("Not connected to a voice channel.")

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)
        
        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def yt(self, ctx, *, url):
        """Streams from a url (almost anything youtube_dl supports)"""

        if ctx.voice_client is None:
            if ctx.author.voice.channel:
                await ctx.author.voice.channel.connect()
            else:
                return await ctx.send("Not connected to a voice channel.")

        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        player = await YTDLSource.from_url(url, loop=self.bot.loop)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
        
        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume
        await ctx.send("Changed volume to {}%".format(volume))


    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()
'''
@bot.command(help='Adds the ban to the bug report.')
@commands.check(is_creator)
async def ban_bugger(ctx, user):
  with open('no_more_reports.json', 'r') as f:
    s = f.read()
    book = json.loads(s)
  with open('no_more_reports.json', 'w') as d:
    book.append(user)
    m = json.dumps(book)
    d.write(m)
  await ctx.send('Successfully added {} to the banned bug submitter list!'.format(user))

@bot.command(help='Removes the ban from bug report.')
@commands.check(is_creator)
async def unban_bugger(ctx, user):
  with open('no_more_reports.json', 'r') as f:
    s = f.read()
    book = json.loads(s)
  with open('no_more_reports.json', 'w') as d:
    book.remove(user)
    m = json.dumps(book)
    d.write(m)
  await ctx.send('Successfully removed {} from the banned bug submitter list!'.format(user))

bot.add_cog(Fun(bot))
bot.add_cog(Info(bot))
bot.add_cog(Staff(bot))
bot.add_cog(Emotes(bot))
bot.add_cog(Roles(bot))
bot.run('MzY4OTczNzk5NjM2MzM2NjUx.DMRxhQ.s3m6OOV8HjgY2EKGdp0kN0sMOc8')