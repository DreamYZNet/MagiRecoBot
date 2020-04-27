import discord
from magi import parser

async def process_reaction_add(reaction, user, client):
    if reaction.message.author == client.user:
        if reaction.message.embeds:
            embed = reaction.message.embeds[0]
            data = parser.parse_girl_images(embed.url)
            image = data['images'][parser.symbols_to_stars[reaction.emoji]]
            embed.set_image(url=image)
            await reaction.message.edit(embed=embed)
            await reaction.remove(user)







