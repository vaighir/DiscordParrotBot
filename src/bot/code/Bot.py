#!/usr/bin/env python3

import discord
import os
import random

import mysql_helper
import learn_module
import generate_message

BOT_TOKEN = os.environ['BOT_TOKEN']

# List of nonsense expressions the bot says
RANDOM_PARROT_CHATTER = ["SQUAWK!!!", "Squawky wants a cookie!!!", "Squawky is a good bird!",
                         "Let's make discord great again!", "SQUAWK!", "Cookie!", "The cake is a lie!",
                         "I'm Squawky!", "I'm a star"]

# Text displayed when users ask for help
HELP_TEXT = """- `!parrot read` to read messages on this channel
- `!parrot learn <username>#<discriminator>` to analyse a user's messages
- `!parrot generate <username>#<discriminator>` to generate a user's messages
- `!parrot stats` to see users whose messages have been read and analysed
%s"""

MAX_MESSAGES = 20000

users = []
analysed_users = []


# Returns a nicely formatted string with all users whose messages have been read
def users_to_text(description="all"):
    users_as_text = ""

    if description == "all":
        for u in users:
            if users_as_text != "":
                users_as_text += " and "
            users_as_text += str(u.name) + "#" + str(u.discriminator) + " "

        if users_as_text == "":
            users_as_text = "no-one"

    elif description == "analysed":
        users_as_text = ', '.join(analysed_users)
        if len(analysed_users) == 0:
            users_as_text = "no-one"

    return users_as_text


def is_a_known_user(username):
    status = False

    name, discriminator = username.split("#")

    for u in users:
        if name == u.name and discriminator == u.discriminator:
            status = True

    return status


# Pick a random thing for the bot to say
def pick_random_chatter():
    return RANDOM_PARROT_CHATTER[random.randint(0, len(RANDOM_PARROT_CHATTER) - 1)]


class MyClient(discord.Client):
    # Log in
    async def on_ready(self):
        print("I've logged in. Squawk!")

    # React to messages
    async def on_message(self, message):
        # Ignore own messages
        if message.author == client.user:
            return

        if message.content.startswith("!parrot"):
            message_content = message.content.split(" ")

            # Respond with random chatter to message "!parrot"
            if len(message_content) == 1:
                await message.channel.send(pick_random_chatter())
                guild = message.channel.guild
                print(guild.text_channels)

            elif message_content[1] == "help":
                await self.show_help(message)

            elif message_content[1] == "read":
                count = await self.read_channel(message.channel)
                await message.channel.send("I've read " + str(count) + " messages from " + users_to_text())

            elif message_content[1] == "learn":
                if len(message_content) == 2:
                    await message.channel.send("You need to specify a user! SQUAWK")
                elif is_a_known_user(message_content[2]):
                    await self.learn(message.channel, message_content[2])
                else:
                    await message.channel.send("I don't know this user! SQUAWK")

            elif message_content[1] == "generate":
                if len(message_content) == 2:
                    await message.channel.send("You need to specify a user! SQUAWK")
                elif is_a_known_user(message_content[2]):
                    await self.generate(message.channel, message_content[2])
                else:
                    await message.channel.send("I don't know this user! SQUAWK")

            elif message_content[1] == "stats":

                await message.channel.send(
                    "I've read messages from " + users_to_text() + ". I've analysed " + users_to_text("analysed"))

            else:
                await message.channel.send("SQUAWK! I don't understand!")
                await self.show_help(message)

    # Display help message
    async def show_help(self, message):
        await message.channel.send(HELP_TEXT % pick_random_chatter())

    # Read and save messages from a channel
    async def read_channel(self, channel):
        await channel.send("Starting to read. It might take a while. I'm just a parrot. Squawk!")
        count = 0
        server = channel.guild
        all_channels = server.text_channels

        mysql_helper.delete_messages_from_server(server.name)

        for ch in all_channels:
            messages = await ch.history(limit=20000).flatten()
            for m in messages:
                if not m.author.bot:
                    if m.author not in users:
                        users.append(m.author)
                    if not m.content.startswith("!") and not m.content.startswith("$"):
                        count += 1
                        print(str(m.author) + " wrote " + m.content)
                        mysql_helper.write_message(str(m.author), m.content, channel.name, str(channel.guild))
            print(users)
        return count

    async def learn(self, channel, user):

        if user not in analysed_users:
            analysed_users.append(user)

        await channel.send("Learning " + user)

        server = channel.guild.name

        learn_module.main(user, server)

        await channel.send(user + " analysed")

    async def generate(self, channel, user):

        server = channel.guild.name

        new_message = generate_message.main(user, server)

        await channel.send(new_message)


client = MyClient(max_messages=MAX_MESSAGES)
client.run(BOT_TOKEN)


