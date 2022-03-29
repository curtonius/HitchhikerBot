import discord
import os
#import pynacl
#import dnspython
import server
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix="!")
TOKEN = os.getenv("DISCORD_TOKEN")

role_type_dictionary = {
    'React to this message with the notification roles you would like.\n🔴  Youtube Notifications\n🟣  Stream Notifications\n🟡  Announcement Notifications':
    {
        "🔴": 'Youtube Notifications',
        "🟣": 'Stream Notifications',
        "🟡": 'Announcement Notifications'
    },
    'React to this message with the gender roles you identify as.\n❤  He/Him\n🧡  She/Her\n💛  They/Them\n💚  He/They\n💙  She/They\n💜  Name Only\n🤍  Ask for Pronoun':
    {
        "❤": 'He/Him',
        "🧡": 'She/Her',
        "💛": 'They/Them',
        "💚": 'He/They',
        "💙": 'She/They',
        "💜": 'Name Only',
        "🤍": 'Ask for Pronoun'
    }
}


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return


@bot.event
async def on_raw_reaction_add(payload):
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


server.server()
bot.run(TOKEN)
