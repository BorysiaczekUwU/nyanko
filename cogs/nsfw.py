import discord
from discord.ext import commands
import aiohttp
import random
from utils import KAWAII_PINK, KAWAII_RED

class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def fetch_image(self, subreddit: str) -> str:
        url = f"https://meme-api.com/gimme/{subreddit}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get('url', None)
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
        return None

    @commands.group(invoke_without_command=True)
    async def porn(self, ctx):
        """Normalne zdjęcia 18+"""
        if not ctx.channel.is_nsfw():
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        subs = ["porn", "nsfw", "gonewild", "NSFW_GIF"]
        image = await self.fetch_image(random.choice(subs))
        
        if image:
            embed = discord.Embed(title="😏🔞", color=KAWAII_RED)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

    @commands.command()
    async def yuri(self, ctx):
        """Yuri (Dziewczyna x Dziewczyna) NSFW"""
        if not ctx.channel.is_nsfw():
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        subs = ["yuri", "wholesomeyuri", "nsfwyuri"]
        image = await self.fetch_image(random.choice(subs))
        
        if image:
            embed = discord.Embed(title="👩‍❤️‍💋‍👩 Yuri", color=KAWAII_PINK)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

    @commands.command()
    async def yaoi(self, ctx):
        """Yaoi (Chłopak x Chłopak) NSFW"""
        if not ctx.channel.is_nsfw():
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        subs = ["yaoi", "nsfwyaoi"]
        image = await self.fetch_image(random.choice(subs))
        
        if image:
            embed = discord.Embed(title="👨‍❤️‍💋‍👨 Yaoi", color=KAWAII_PINK)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

    @commands.command()
    async def femboy(self, ctx):
        """Femboy 18+"""
        if not ctx.channel.is_nsfw():
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        subs = ["femboyporn", "FemBoys", "TrapHentai"]
        image = await self.fetch_image(random.choice(subs))
        
        if image:
            embed = discord.Embed(title="🎀 Femboy", color=KAWAII_PINK)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

async def setup(bot):
    await bot.add_cog(NSFW(bot))
