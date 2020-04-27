from magi import parser
import discord

USAGE = None
DESCRIPTION = None
HELP = None

REQUIRED = 1
TRAIL = True


async def execute(message, args):
	girl_list = parser.find_girl(args, True)

	if len(girl_list) > 0:
		embed = discord.Embed()

		embed.colour = discord.Colour(value=0x000000)

		embed.title = 'Search Results:'

		value = ''
		for girl in girl_list:
			value += f'[{girl["name"]}]({girl["url"]})\n'

		embed.description = value

		message = await message.channel.send(embed=embed)
		# count = 0
		# for girl in girl_list:
		# 	count += 1
		# 	await message.add_reaction(parser.count_to_symbols[count])
	else:
		await message.channel.send('404: Girls not found.')