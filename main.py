
# add invalid syntax exception

import discord
import command_reader
import activity_reader
import globals

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_reaction_add(reaction, user):
    if user != client.user:
        await activity_reader.process_reaction_add(reaction, user, client)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await command_reader.process(message)

client.run('private_number')


# class MyClient(discord.Client):
#     async def on_ready(self):
#         print('Logged on as {0}!'.format(self.user))
# client = MyClient()