#!/usr/bin/env python3

import discord
import os

BOT_TOKEN = os.environ['BOT_TOKEN']


class MyClient(discord.Client):
    async def on_ready(self):
        print("I've logged in. Squawk!")

    async def on_message(self, message):
        if message.author == client.user:
            return

        if message.content.startswith("!parrot"):
            await message.channel.send("SQUAWK!")


client = MyClient()
client.run(BOT_TOKEN)
