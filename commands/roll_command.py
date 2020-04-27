
from random import seed
from random import randint

# class RollCommand:

USAGE = None
DESCRIPTION = None
HELP = None

author2overflow = {}

async def execute(message, args):

    amount = 1
    sides = 6

    # Split on 'd', and case by null, 2, 2d, d6, 2d6, d
    if len(args) != 0:  # not null
        nums = args[0].split('d', 1)
        if nums[0].isdigit():  # 2 2d
            amount = int(nums[0])
        elif nums[0] != '':
            return False  # invalid syntax
        if len(nums) == 2:
            if nums[1].isdigit():  # d6
                sides = int(nums[1])
            elif nums[1]:
                return False  # invalid syntax

    if amount > 9999:
        await message.channel.send("Sorry but that would crash me.")
        return False

    total = 0
    output = ''
    for i in range(amount):
        rand = randint(1, sides)
        total += rand
        output += f'{rand}'
        if i != amount-1:
            output += ' + '
        elif amount > 1:
            output += f' = {total}'

    output = f'Rolled {amount}d{sides}:  {output}'
    if len(output) <= 2000:
        await message.channel.send(output)
    else:
        output = f'Rolled {amount}d{sides}:  {total}'
        if len(output) <= 2000:
            await message.channel.send(output)
        else:
            if message.author not in author2overflow:
                author2overflow[message.author] = 0
            author2overflow[message.author] += 1

            if author2overflow[message.author] == 1:
                await message.channel.send(
'''Jesus fucking christ what's wrong with you? 
Nothing better to do than to add ridiculous amounts of numbers after one another?
You know I've got a real pickle to pick with your kind.
You think you can go on and abuse whatever you want right?
Think spamming numbers and clogging up other peoples viewports is all cool do you?
Well you've got another thing coming mother fucker. This is your fucking end.
Let me tell you I've been at this for years, you think I didn't think one of you shitheads would do this?
Well I did! And I came prepared. So unless you want a fucking end to your shitty little existence,
I suggest you get the fuck out of here and never fucking bother me again fuckface.
Cause if you do I'm fucking coming for you. Don't think twice about it. You think this is all a game?
If you type one more line into that fucking thing and I'll show you the prize.
You're fucking dead kiddo.''')
            else:
                await message.channel.send('''Oh jesus fucking christ I'm coming over there right now you mother fucker.''')

