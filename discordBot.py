import os
from pathlib import Path

import discord
from dotenv import load_dotenv

import apiCalls

dotenv_path = Path('secrets.env')
load_dotenv(dotenv_path=dotenv_path)
TOKEN = os.getenv('bot_token')

dotenv_path = Path('secrets.env')
load_dotenv(dotenv_path=dotenv_path)
riot_api_key = os.getenv("Riot_Api_Key")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

output = apiCalls.make_request(apiCalls.baseurl, apiCalls.accountById, riot_api_key)
print(apiCalls.parse_puid(output))


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('!'):
            content = message.content[1:]
            await message.channel.send(apiCalls.output.text)


client.run(TOKEN)
