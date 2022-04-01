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
	"|3": "b",
	"/\\": "a",
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
	"¶":"p"
}
bad_word = {
	"[6b8][il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[t%+7][cç€©]h", #bitch
	"[6b8][il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[sz5$§]h",
	"[6b8][il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[t%+7]s*h*",
	"[f][uüûùúµaâäàåæáã@4][uüûùúµaâäàåæáã@4]*[qckç€©]", #fuck
	"[a@4^âäàåæáã][a@4^âäàåæáã]*[sz5$§][sz5$§][sz5$§]*", #ass
	"[sz5$§]h[il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[t%+7]", #shit
	"[6b8][a@4^âäàåæáã][a@4^âäàåæáã]*[sz5$§][sz5$§]*[t%+7][a@4^âäàåæáã][a@4^âäàåæáã]*rd", #bastard
	"r[e3êëèæ€][e3êëèæ€]*[t%+7][a@4^âäàåæáã][a@4^âäàåæáã]*rd", #r slur
	"[qcç€©k][uüûùúµ][uüûùúµ]*n[t%+7]", #cunt
	"d[il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[qcç€©k]", #dick
	"p[uüûùúµ][uüûùúµ]*[sz5$§][sz5$§]*[yÿ¥µŸý]", #pussy
	"v[a@4^âäàåæáã][a@4^âäàåæáã]*g", #vag
	"[6b8][o0ôöòó•Ø][o0ôöòó•Ø][o0ôöòó•Ø]*[6b8]", #boob
	"n[il1!|ïîìí¡¦][il1!|ïîìí¡¦]*gg*[e3êëèæ€aâäàåæáã@4^uüûùúµ]r?", #n slur
	"[t%+7][il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[t%+7]", #tit
	"[6b8][e3êëèæ€][e3êëèæ€]*[a@4^âäàåæáãe3êëèæ€]n[e3êëèæ€uüûùúµa@4^âäàåæáãr]r", #beaner
	"[6b8][il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[o0ôöòó•Ø][o0ôöòó•Ø]*wj[o0ôöòó•Ø][o0ôöòó•Ø]*[6b8]", #blowjob
	"[6b8][o0ôöòó•Ø][o0ôöòó•Ø]*n[e3êëèæ€uüûùúµa@4^aâäàåæáã]r", #boner
	"[6b8][uüûùúµ][t%+7][t%+7]", #butt
	"[cç€©k][il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[t%+7]", #clit
	"[cç€©k][o0ôöòó•Ø][o0ôöòó•Ø]*[cç€©kq]", #cock
	"[kcç€©g][o0ôöòó•Ø][o0ôöòó•Ø]*[o0ôöòó•Ø][o0ôöòó•Ø]*[t%+t]", #cooch
	"[kcç€©g][o0ôöòó•Ø][o0ôöòó•Ø]*[o0ôöòó•Ø][o0ôöòó•Ø]*[cç€©]h",
	"[kcç€©g][o0ôöòó•Ø][o0ôöòó•Ø]*[o0ôöòó•Ø][o0ôöòó•Ø]*[t%+t][cç€©]h",
	"[kcç€©g][o0ôöòó•Ø][o0ôöòó•Ø]*[o0ôöòó•Ø][o0ôöòó•Ø]*n", #c slur
	"[cç€©k][uüûùúµ]m", #cum
	"[cç€©k][uüûùúµ]n[il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[il1!|ïîìí¡¦][il1!|ïîìí¡¦]*?[il1!|ïîìí¡¦][il1!|ïîìí¡¦]*ng[uüûùúµ][sz5$§]", #cunnillingus
	"d[yÿ¥µŸýil1!|ïîìí¡¦]k[e3êëèæ€]", #d slur
	"d[o0ôöòó•Ø][o0ôöòó•Ø]*[o0ôöòó•Øuüûùúµ][cç€©]h", #douche
	"d[o0ôöòó•Ø][o0ôöòó•Ø]*[o0ôöòó•Øuüûùúµ][sz5$§]h", #douche
	"[f][a@4^âäàåæáã][a@4^âäàåæáã]*g", #f slur
	"g[a@4^âäàåæáã][a@4^âäàåæáã]*[ÿ¥µŸý]", #gay
	"h[a@4^âäàåæáã][a@4^âäàåæáã]*ndj[o0ôöòó•Ø][o0ôöòó•Ø]*[6b8]", #handjob
	"h[a@4^âäàåæáã][a@4^âäàåæáã]*rd[o0ôöòó•Ø][o0ôöòó•Ø]*n", #hardon
	"h[o0ôöòó•Ø]",#hoe
	"h[o0ôöòó•Ø][o0ôöòó•Ø]*m[o0ôöòó•Ø]", #homo
	"h[uüûùúµ]mp", #hump
	"[jg][il1!|ïîìí¡¦][il1!|ïîìí¡¦]*zz*", #jizz
	"[il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[e3êëèæ€][e3êëèæ€]*[sz5$§][6b8]", #lesbian
	"n[uüûùúµ][t%+7][sz5$§][a@4^âäàåæáã][a@4^âäàåæáã]*[cç€©kq]", #nutsack
	"p[il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[sz5$§][sz5$§]*", #piss
	"q[uüûùúµ][e3êëèæ€][e3êëèæ€]*[e3êëèæ€][e3êëèæ€]*f", #queef
	"[sz5$§][e3êëèæ€][e3êëèæ€]*x", #sex
	"q[uüûùúµ][e3êëèæ€][e3êëèæ€]*[e3êëèæ€a@4^âäàåæáã]r", #queer
	"r[il1!|ïîìí¡¦][il1!|ïîìí¡¦]*mj[o0ôöòó•Ø][o0ôöòó•Ø]*[6b8]", #rimjob
	"[sz5$§]h[il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[o0ôöòó•Ø][o0ôöòó•Ø]*ng", #schlong
	"[sz5$§][cç€©]h[il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[o0ôöòó•Ø][o0ôöòó•Ø]*ng",
	"[sz5$§][cç€©kq][a@4^âäàåæáã][a@4^âäàåæáã]*n[cç€©kq]", #skank
	"h[o0ôöòó•Ø][o0ôöòó•Ø]*r[e3êëèæ€][e3êëèæ€]*", #whore
	"[sz5$§][il1!|ïîìí¡¦][uüûùúµ][uüûùúµ]*[t%+7]", #slut
	"[t%+7][e3êëèæ€][e3êëèæ€]*[sz5$§][sz5$§]*[t%+7][il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[cç€©kq][il1!|ïîìí¡¦]*[e3êëèæ€]*", #testicles
	"[t%+7]w[a@4^âäàåæáã][a@4^âäàåæáã]*[t%+7]", #twat
	"v[a@4^âäàåæáã][a@4^âäàåæáã]*j[a@4^âäàåæáã][a@4^âäàåæáã]*[ÿ¥µŸý]j[a@4^âäàåæáã][a@4^âäàåæáã]*y",#vajayjay
	"w[a@4^âäàåæáã][a@4^âäàåæáã]*n[cç€©k]", #wank
	"w[e3êëèæ€][e3êëèæ€]*[t%+7][6b8][a@4^âäàåæáã][a@4^âäàåæáã]*[cç€©kq]", #wetback
	"pn[il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[sz5$§]", #penis
	"h[o0ôöòó•Ø][o0ôöòó•Ø]*[6b8][a4@^âäàåæáã][a4@^âäàåæáã]*g", #hobag
	"[cç€©<o0ôöòó•Ø6b8]=*[38bdo0ôöòó•Ø>]", #c==3
	"[sz5$§][uüûùúµ][cç€©kq] m[ÿ¥µŸý]", #suck my
	"w[e3êëèæ€][e3êëèæ€]*[e3êëèæ€][e3êëèæ€]*w[e3êëèæ€][e3êëèæ€]*[e3êëèæ€][e3êëèæ€]*", #weewee
	"p[o0ôöòó•Ø][o0ôöòó•Ø]*rn", #porn
	"[a@4^âäàåæáã][a@4^âäàåæáã]*n[uüûùúµ][sz5$§]", #anus
	"[a@4^âäàåæáã][a@4^âäàåæáã]*n[a@4^âäàåæáãuüûùúµ][il1!|ïîìí¡¦]", #anal
	"pr[il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[cç€©kq]", #prick
	"ph[a@4^âäàåæáã][a@4^âäàåæáã]*[il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[il1!|ïîìí¡¦][il1!|ïîìí¡¦]*[cç€©]" #phalic
}

exceptions = {
	"fuch","fuco","fucus", 
	"assa", "asse", "assi", "asso", 
	"assu", "shittim","shittah","shitake","cant", 
	"benedick", "dickens","dicker",
	"medick","dickey", "dickie","duck",
	"dock","deck","[a-z,A-Z]d.k", "[a-z,A-Z]d.c", "doc",
	"d.c[a-bd-jl-z]","salvag","travag","vagabond","savag","vagra","vagar","selvag",
	"ravage","vagility","[a-z,A-Z]arse","titis","titive","titud","titut","antit","titch",
	"sanctit","titious","destit","tite","tition","constit","titying","tituency",
	"butter","button","scuttlebutt","rebutt","buttress","abutt", "heteroclite",
	"clitic","[a-z,A-Z]chode[a-z,A-Z]","cock[a-rt-z]","circum","docum","cumb","accum","cumulus","scum",
	"okeydoke","duke","goochie","[a-vx-z]ho","hospi","host","hous","horti","homog",
	"holo","hot","home","horr","hors","honey","honor","hodge","[a-z,A-Z]hump","humpback","whose",
	"whom","who\s","who\w","^who$","[a-z,A-Z]hole[a-z,A-Z]","^hole","\shole","unisex","sextup",
	"ho[a-df-z0-9]","[a-z,A-Z]t it","sextil","who$","horendous","racoon", "retardant"
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
		result = re.match(pattern, str)
		if result:
			matched = True
			match += 1
			print("Matched with: " + pattern)

	for pattern in exceptions:
		result = re.match(pattern, str)
		if result and matched == True:
			match -= 1
			print("Unmatched with: " + pattern)

	if matched == True and match != 0:
		channel = bot.get_channel(channels['bot-dev'])
		await channel.send(message.author.display_name + " posted in " + "Channel **" + message.channel.name + "**:\n" + message.content )
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
