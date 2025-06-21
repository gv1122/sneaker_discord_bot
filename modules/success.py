import asyncio
import discord
import json
import datetime
import tweepy
import requests
from discord.ext import commands

with open("./data/config.json") as f:
    config = json.load(f)

LOG_CHANNEL = config['log_channel']
EMBED_COLOR = config['embed_color']
EMBED_IMAGE = config['embed_img']
CONSUMER_KEY = config["twitter_consumer_key"]
CONSUMER_SECRET = config["twitter_secret_key"]
ACCESS_KEY = config["twitter_access_key"]
ACCESS_SECRET = config["twitter_access_secret"]


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

class TwitterSuccess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        
        try:
            if message.channel.id == 498489199289434132:
                author = str(message.author).split('#')[0]
                image_url = message.attachments[0].url
                tweet_text = ('Success by ' + author + " in @StrikeAccess")
                filename = './img/success.jpg'
                r = requests.get(image_url)
                if r.status_code == 200:
                    with open(filename, 'wb') as image:
                        for img in r:
                            image.write(img)
                    post_tweet = api.update_with_media(filename, status=tweet_text)
                    embed = discord.Embed(title=f"Successfully posted your success!", description=f"Success by <@{message.author.id}> \n You can find your tweet [here](https://twitter.com/Strike_Success/status/{str(post_tweet.id)}) \n React with 🗑️ to delete the post", color=EMBED_COLOR)
                    embed.set_footer(text='Helper Bot Success', icon_url=EMBED_IMAGE)
                    n = await message.channel.send(embed=embed)
                    await n.add_reaction("🗑️")
                    deleted = discord.Embed(title=f"Success Deleted!", description=f"<@{message.author.id}> your tweet has been successfully deleted \n If you think it was an error please open a ticket", color=EMBED_COLOR)
                    deleted.set_footer(text='Helper Bot Success', icon_url=EMBED_IMAGE)
                    def check(reaction, user):
                        return user == message.author and str(reaction.emoji) == '🗑️' and reaction.message.id == n.id
                    try:
                        reaction, user = await self.bot.wait_for('reaction_add', timeout=300, check=check)
                    except asyncio.TimeoutError:
                        pass
                    else:
                        api.destroy_status(str(post_tweet.id))
                        await n.edit(embed=deleted)
                        await message.delete()
        except IndexError:
            pass
        
def setup(bot):
    bot.add_cog(TwitterSuccess(bot))