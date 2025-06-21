import requests
import urllib3
import json
import random
import discord
from discord.ext import commands
#from colorama import init, Fore, Back, Style

urllib3.disable_warnings()
#init()

with open('data/config.json') as f:
    config = json.load(f)

LOG_CHANNEL = config['log_channel']
EMBED_COLOR = config['embed_color']
EMBED_IMAGE = config['embed_img']

class prepShippingRates():
    def __init__(self, link, zip, state):
        self.session = requests.Session()
        self.link = link
        self.zip = zip
        self.state = state
        self.site = f"{link.rpartition('com')[0]}com"

    def get_var(self):
        link = f"{self.link}.json"
        r = requests.get(link)
        link = r.json()
        vars = []
        for var in link['product']['variants']:
            vars.append(var['id'])
        v = random.choice(vars)
        return v
    
    def load_payment(self):
        payload = {
            "credit_card": {
                "number": "12344567",
                "name": "Test" + " " + "Tester",
                "month": "09",
                "year": "2027",
                "verification_value": "584"
            }
        }
        # positing info to payment portal
        payment = 'https://elb.deposit.shopifycs.com/sessions'

        pay = self.session.post(payment, json=payload, verify=False)

        #if pay.status_code == 200:
        #    print(f'Payment loaded! - {Fore.GREEN}SUCCESS{Style.RESET_ALL}')
        #else:
        #    print(f'Payment loaded error - {Fore.RED}ERROR{Style.RESET_ALL}')    

        payment_token = json.loads(pay.text)["id"]

    def add_to_cart(self):
        '''Given a session and variant ID, the product is added to cart and the
        response is returned.
        '''
        # Add the product to cart
        link = f"{self.site}/cart/add.js?quantity=1&id={self.get_var()}"

        response = self.session.get(link, verify=False)
        #if response.status_code == 200:
        #    print(f'ATC success! - {Fore.GREEN}SUCCESS{Style.RESET_ALL}')
        #else:
        #    print(f'ATC error - {Fore.RED}ERROR{Style.RESET_ALL}')
          
    def get_shipping(self):
        link = f"{self.site}/cart/shipping_rates.json?shipping_address[zip]={self.zip}&shipping_address[country]=us&shipping_address[province]={self.state}"

        response = self.session.get(link, verify=False)

        shipping_options = json.loads(response.text)

        ship_opt = shipping_options["shipping_rates"][0]["name"].replace(' ', "%20")
        ship_prc = shipping_options["shipping_rates"][0]["price"]

        shipping_option = "shopify-{}-{}".format(ship_opt,ship_prc)

        return shipping_option
    
    def final(self):
        self.load_payment()
        self.add_to_cart()
        final = self.get_shipping()
        return final


class shippingRates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sr(self, ctx, link, zip, state):
        siteLink = link
        zipCode = zip
        stateLiv = state
        sr = prepShippingRates(siteLink, zipCode, stateLiv)
        rate = sr.final()

        site = f"{siteLink.rpartition('com')[0]}com"

        embed=discord.Embed(title=f"Shipping Rate for {site} !", description=f'`{rate}`', color=EMBED_COLOR)
        embed.set_footer(text="Helper Bot", icon_url=EMBED_IMAGE)
        await ctx.send(embed=embed)

    @sr.error
    async def var_error(self, ctx, error):
        LOG_CHAN = self.bot.get_channel(LOG_CHANNEL)
        NAME = "shipping rates bot"
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color=EMBED_COLOR)
            embed.description = 'You are missing an argument!'
            await ctx.send(embed=embed)

        elif isinstance(error, KeyError):
            embed = discord.Embed(color=EMBED_COLOR)
            embed.description = 'Invalid state or zip code! Make sure you are using the abbreviation of your state!'
            await ctx.send(embed=embed)
            
        else:
            author = ctx.message.author
            error = error
            message_id = f"https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}"

            embed = discord.Embed(title=f"someone made an error while using {NAME}", color=EMBED_COLOR)
            embed.add_field(name="Author", value=f"{author}")
            embed.add_field(name="Error", value=f"`{error}`")
            embed.add_field(name="Message ID", value=f"{message_id}")

            await LOG_CHAN.send(f"<@123456789>", embed=embed)

def setup(bot):
    bot.add_cog(shippingRates(bot))