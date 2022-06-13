import discord
import os
#import pynacl
#import dnspython
import server
from discord.ext import commands
from discord.utils import get
import re

bot = commands.Bot(command_prefix="!")
TOKEN = os.getenv("DISCORD_TOKEN")

replace = {
	"\\|3": "b",
	"/\\\\": "a",
	"ph": "f",
	"ck": "k",
	"zz": "s",
	"qw": "qu",
	"kw": "qu",
	"wh": "h",
	"uh": "a",
	"pe": "p",
	"p3": "p",
	"nn": "n",
	"🇦 ": "a",
	"🇧 ": "b",
	"🇨 ": "c",
	"🇩 ": "d",
	"🇪 ": "e",
	"🇫 ": "f",
	"🇬 ": "g",
	"🇭 ": "h",
	"🇮 ": "i",
	"🇯 ": "j",
	"🇰 ": "k",
	"🇱 ": "l",
	"🇲 ": "m",
	"🇳 ": "n",
	"🇴 ": "o",
	"🇵 ": "p",
	"🇶 ": "q",
	"🇷 ": "r",
	"🇸 ": "s",
	"🇹 ": "t",
	"🇺 ": "u",
	"🇻 ": "v",
	"🇼 ": "w",
	"🇽 ": "x",
	"🇾 ": "y",
	"🇿 ": "z",
	"¶":"p",
	"[@4^âäàåæáã]": "a",
	"[68]": "b",
	"[ç€©]": "c",
	"[3êëèæ€]": "e",
	"[l1!|ïîìí¡¦]": "i",
	"[0ôöòó•Ø]": "o",
	"[z5$§]":"s",
	"[%+7]":"t",
	"[üûùúµ]":"u",
	"[ÿ¥µŸý]": "y"
}

bad_word = {
	"re+ta+rd", #r slur
	"^n+i+g+[eau]r?", #n slur
	"[qck]o+o+n", #c slur
	"we+tba+[qck]", #wetback
	"be+[ae]n[euar]r", #beaner
	"chi+n[qck]", #chinese c slur
	"g[yi]psy", #g slur
	"tra+n+y", #t slur
	"she+ma+le", #shemale
	"d[yi]ke", #d slur
	"fa+g", #f slur
}

exceptions = {
	"retardant", "rac+oon","cocoon","tycoon","cooncan", "puccoon","coontie", "coonskin", "coonhound", "beanery", "beaneries", "pachinko", "chinkapin", "chinquapin", "chinch", "chincapin", "vandyke", "klondike","fagin","fage","[a-mo-zA-MO-Z]nig", "nig[a-fh-zA-FH-Z]"
}

role_type_dictionary = {
    'React to this message with the notification roles you would like.\n🔴  Youtube Notifications\n🟣  Stream Notifications\n🟡  Announcement Notifications':
    {
        "🔴": 'Youtube Notifications',
        "🟣": 'Stream Notifications',
        "🟡": 'Announcement Notifications'
    },
  
    'React to this message with the gender roles you identify as.\n❤️  He/Him\n🧡  She/Her\n💛  They/Them\n💚  He/They\n💙  She/They\n💜  Name Only\n🤍  Ask for Pronouns':
    {
        "❤️": 'He/Him',
        "🧡": 'She/Her',
        "💛": 'They/Them',
        "💚": 'He/They',
        "💙": 'She/They',
        "💜": 'Name Only',
        "🤍": 'Ask for Pronouns'
    },

    'React to this message with a ✅  to accept being pinged by anybody at any time (Non-Notification based pings)':
    {
        "✅": 'Accept Pings'
    }
}

channels = {
  "🔔-assign-roles": 951692177086488626,
  "bot-dev": 958468714846634004
}


@bot.event
async def on_ready():
		channel = bot.get_channel(channels['bot-dev'])
		await channel.send("Marvin the Robot Updated to V.2.0.4...SIGH")
		print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	str = message.content
	for replacer in replace.keys():
		str = str.replace(replacer, replace[replacer])
		
	matched = False
	match = 0
	
	for pattern in bad_word:
		result = re.search(pattern, str)
		if result:
			matched = True
			match += 1

	for pattern in exceptions:
		result = re.search(pattern, str)
		if result and matched == True:
			match -= 1

	if matched == True and match != 0:
		channel = bot.get_channel(channels['bot-dev'])
		await channel.send(message.author.display_name + " posted in " + "Channel **" + message.channel.name + "**:\n||" + message.content + "||" )
		await message.delete()

	await bot.process_commands(message)


@bot.event
async def on_raw_reaction_add(payload):
  if payload.channel_id != channels["🔔-assign-roles"]:
    return
    
  channel = bot.get_channel(payload.channel_id)
  message = await channel.fetch_message(payload.message_id)
  user = payload.member
  emoji_check = str(payload.emoji)

  if message.content in role_type_dictionary.keys():
      role = None
      role_dictionary = role_type_dictionary[message.content]
      if emoji_check in role_dictionary.keys():
          role = get(user.guild.roles, name=role_dictionary[emoji_check])
      else:
          await message.remove_reaction(emoji_check, user)

      if role != None:
          await user.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
  if payload.channel_id != channels["🔔-assign-roles"]:
    return
    
  channel = bot.get_channel(payload.channel_id)
  message = await channel.fetch_message(payload.message_id)
  guild = await bot.fetch_guild(payload.guild_id)
  user = await guild.fetch_member(payload.user_id)
  emoji_check = str(payload.emoji)

  if message.content in role_type_dictionary.keys():
      role = None
      role_dictionary = role_type_dictionary[message.content]
      if emoji_check in role_dictionary.keys():
          role = get(user.guild.roles, name=role_dictionary[emoji_check])

      if role != None:
          await user.remove_roles(role)

@bot.command()
async def get_channel_id(ctx):
  channel = bot.get_channel(channels['bot-dev'])
  await channel.send('Channel **' + ctx.channel.name + '** ID: ' + str(ctx.channel.id))
  await ctx.message.delete()

@bot.command()
async def send_depressing_message(ctx):
	channel = bot.get_channel(channels['bot-dev'])
	str = ctx.message.content
	str = str.replace("!send_depressing_message ","")
	await channel.send("Hmph.." + str + "... What do you know about " + str + "?")
	await ctx.message.delete()

@bot.command()
async def send_message(ctx):
	channel = bot.get_channel(channels['bot-dev'])
	str = ctx.message.content
	str = str.replace("!send_message ","")
	await channel.send(str)
	await ctx.message.delete()

@bot.command()
async def prime_reactions(ctx):
	if ctx.message.reference == None:
		return
		
	ref_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
	await ctx.message.delete()
	if ref_message.content in role_type_dictionary.keys():
		for emoji_check in role_type_dictionary[ref_message.content].keys():
			await ref_message.add_reaction(emoji_check)
  
server.server()
bot.run(TOKEN)
