#!/usr/bin/env python3

import discord
import os

BOT_TOKEN = os.environ['BOT_TOKEN']

HELP_TEXT = """SQUAWK!
`!parrot read` to read messages on this channel
Squawky wants a cookie!!!"""

channels = []
users = []


def users_to_text():
    users_as_text = ""
    for u in users:
        if users_as_text != "":
            users_as_text += " and "
        users_as_text += str(u.name) + "#" + str(u.discriminator) + " "

    return users_as_text


class MyClient(discord.Client):
    async def on_ready(self):
        print("I've logged in. Squawk!")

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith("!parrot"):
            message_content = message.content.split(" ")
            if len(message_content) == 1:
                await message.channel.send("SQUAWK")
            elif message_content[1] == "help":
                await self.show_help(message)
            elif message_content[1] == "read":
                await self.read_channel(message.channel)
                await message.channel.send("I've read messages from " + users_to_text())
            else:
                await message.channel.send("SQUAWK! I don't understand!")
                await self.show_help(message)

    async def show_help(self, message):
        await message.channel.send(HELP_TEXT)

    async def read_channel(self, channel):
        messages = await channel.history().flatten()
        for m in messages:
            if not m.author.bot:
                if m.author not in users:
                    users.append(m.author)
                if not m.content.startswith("!"):
                    print(str(m.author) + " wrote " + m.content)
        print(users)


client = MyClient()
client.run(BOT_TOKEN)


