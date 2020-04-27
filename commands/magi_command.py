from magi import parser
import discord

USAGE = None
DESCRIPTION = None
HELP = None

REQUIRED = 1
TRAIL = True

elemental_to_color = {
	'Aqua': 0x83d4cd,
	'Forest': 0xfddc71,
	'Flame': 0xff6f6f,
	'Light': 0xff9eda,
	'Dark': 0x775e89,
	'DarkOrg': 0x473e59,
	'Void': 0xffffff,
	}

async def execute(message, args):

	data = parser.parse_girl(parser.find_girl(args, False))
	if data:
		embed = discord.Embed()

		try:
			embed.description = data['quotes'][0]
		except:
			pass

		try: embed.set_author(name=data['rarity'], icon_url=data['element_icon'])
		except: pass
		try: embed.colour = discord.Colour(value=elemental_to_color[data['element']])
		except: pass
		try: embed.set_image(url=list(data['images'].values())[0])
		except: pass

		embed.title = data['name']
		embed.url = data['url']
		try: embed.set_footer(text=embed.timestamp) # how does this work
		except: pass

		discs = ''
		for d in data['discs']:
			discs += d[0]
		embed.add_field(name='Discs:', value=discs)

		try: embed.add_field(name='Seiyuu', value=data['seiyuu'])
		except: pass

		try:
			embed.add_field(name='Max-Stats', value=f'HP: {data["stats"]["hp"]}  ATK: {data["stats"]["atk"]}  DEF: {data["stats"]["def"]}')
		except:
			print('exception')

		message = await message.channel.send(embed=embed)
		for image in data['images']:
			if image != 'Sprite':
				await message.add_reaction(parser.stars_to_symbols[image])
	else:
		await message.channel.send('404: Girl not found.')


reacts_to_images = {
	'1️⃣': '★',
	'2️⃣': '★★',
	'3️⃣': '★★★',
	'4️⃣': '★★★★',
	'5️⃣': '★★★★★',
	}