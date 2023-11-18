import discord
from discord import app_commands
from dotenv import load_dotenv
import os
import aiohttp
import random
import json

# Load environment variables
load_dotenv()

# Constants
MY_GUILD = discord.Object(id=int(os.getenv('GUILD_ID')))  # Use environment variable for guild ID
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT')  # Set your Reddit user agent in .env

class MyBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
client = MyBot(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

class RandMeme(discord.ui.View):  # Placeholder for RandPic class
    pass

async def reddit_pic_embed():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get('https://www.reddit.com/r/memes/hot.json?limit=10', 
                                   headers={'User-Agent': REDDIT_USER_AGENT}) as response:
                if response.status == 200:
                    json_data = await response.json()
                    posts = json_data['data']['children']
                    random_post = random.choice(posts)['data']
                    embed = discord.Embed(title=random_post['title'], color=0x3498db)
                    embed.set_image(url=random_post['url'])
                    embed.set_footer(text="👍 1 | 💬 1")
                    return embed
                else:
                    return discord.Embed(title="Error", description="Couldn't fetch memes from Reddit.", color=0xff0000)
        except Exception as e:
            print(f"Error fetching data from Reddit: {e}")
            return discord.Embed(title="Error", description="An error occurred while fetching data.", color=0xff0000)

@client.tree.command(name="reddit-meme", description="Hot Meme from Reddit")
async def random_pic(interaction: discord.Interaction):
    embed = await reddit_pic_embed()
    view = RandMeme()
    message = await interaction.response.send_message(embed=embed, view=view)

# Run the bot
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN:
    client.run(TOKEN)
else:
    print("Discord token not found. Check your .env file.")