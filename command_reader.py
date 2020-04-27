
import shlex
import commands.command_list

previous_message = {}


async def process(message):
    # if message.content == ',':
    #     pass
    # el
    if message.content.startswith(','):
        # Backup for previous messages
        message_backup = message.content

        # Remove ,
        message.content = message.content[1:]

        # Split message command and the rest of the message
        split_message = message.content.split(' ', 1)
        command_name = split_message[0]
        message.content = split_message[1] if len(split_message) == 2 else ''

        # Split content into arguments
        args = shlex.split(message.content)

        if command_name == '':
            return
        if command_name in commands.command_list.command_list:
            command_obj = commands.command_list.command_list[command_name]
            if check(command_obj, message, args):
                await command_obj.execute(message, args)
                previous_message[message.author] = message_backup
            else:
                await message.channel.send("INCORRECT SYNTAX")


# Checks whether the argument count is proper by the commands requirements
def check (command_obj, message, args):
    if hasattr(command_obj, 'REQUIRED') and len(args) < command_obj.REQUIRED:
        return False
    elif hasattr(command_obj, 'TRAIL') and command_obj.TRAIL:
        return True
    elif hasattr(command_obj, 'OPTIONAL') and len(args) > command_obj.REQUIRED + command_obj.OPTIONAL:
        return False
    return True

