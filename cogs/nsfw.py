import discord
from discord.ext import commands
import aiohttp
import random
from utils import KAWAII_PINK, KAWAII_RED

GIFS_NSFW_HUG = [
    "https://media.giphy.com/media/2UIcmK4pn7rYNLRboG/giphy.gif",
    "https://media.giphy.com/media/l2QDP39mURZH1Ble0/giphy.gif"
]
GIFS_NSFW_KISS = [
    "https://media.giphy.com/media/G3va31bE1KVhbclxXk/giphy.gif",
    "https://media.giphy.com/media/zkppEMFvRX5i2nZgK8/giphy.gif"
]
GIFS_SPANK = [
    "https://media.giphy.com/media/QscbSqUut7SFO/giphy.gif",
    "https://media.giphy.com/media/e8cf5858fc95acba2d627cbbfe7b26c2/giphy.gif"
]
GIFS_STRIP = [
    "https://media.giphy.com/media/l4pTfx2qLszoacZRS/giphy.gif",
    "https://media.giphy.com/media/3o7TKSxdQJIJiPcw0M/giphy.gif"
]

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

    @commands.command()
    async def hentai(self, ctx):
        """Hentai 18+"""
        if not ctx.channel.is_nsfw():
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        subs = ["hentai", "HENTAI_GIF", "rule34"]
        image = await self.fetch_image(random.choice(subs))
        
        if image:
            embed = discord.Embed(title="🔞 Hentai", color=KAWAII_RED)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

    @commands.command()
    async def boobs(self, ctx):
        """Piersi 18+"""
        if not ctx.channel.is_nsfw():
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        subs = ["boobs", "BustyPetite", "hugeboobs", "TittyDrop"]
        image = await self.fetch_image(random.choice(subs))
        
        if image:
            embed = discord.Embed(title="🍒 Piersi", color=KAWAII_RED)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

    @commands.command()
    async def ass(self, ctx):
        """Tyłeczki 18+"""
        if not ctx.channel.is_nsfw():
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        subs = ["ass", "pawg", "booty", "ThickThighs"]
        image = await self.fetch_image(random.choice(subs))
        
        if image:
            embed = discord.Embed(title="🍑 Tyłeczki", color=KAWAII_RED)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

    @commands.command()
    async def rule34(self, ctx):
        """Rule 34 zdjęcia 18+"""
        if not ctx.channel.is_nsfw():
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        subs = ["rule34", "Rule34LoL", "Overwatch_Porn"]
        image = await self.fetch_image(random.choice(subs))
        
        if image:
            embed = discord.Embed(title="🎨 Rule 34", color=KAWAII_RED)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

    @commands.command()
    async def nsfw_hug(self, ctx, member: discord.Member):
        """Gorące przytulenie obok osoby (NSFW)"""
        if not ctx.channel.is_nsfw():
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        if member == ctx.author:
            return await ctx.send("Nie możesz przytulić samego siebie w ten sposób! 😳")
            
        embed = discord.Embed(
            description=f"👩‍❤️‍💋‍👨 **{ctx.author.display_name}** namiętnie przytula **{member.display_name}**... oj robi się gorąco! 🔥",
            color=KAWAII_RED
        )
        embed.set_image(url=random.choice(GIFS_NSFW_HUG))
        await ctx.send(embed=embed)

    @commands.command()
    async def nsfw_kiss(self, ctx, member: discord.Member):
        """Gorący pocałunek (NSFW)"""
        if not ctx.channel.is_nsfw():
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
            
        if member == ctx.author:
            return await ctx.send("Brak Ci partnera? 🥺")

        embed = discord.Embed(
            description=f"💋 **{ctx.author.display_name}** namiętnie całuje **{member.display_name}**... 🔞",
            color=KAWAII_RED
        )
        embed.set_image(url=random.choice(GIFS_NSFW_KISS))
        await ctx.send(embed=embed)

    @commands.command()
    async def spank(self, ctx, member: discord.Member):
        """Daj komuś klapsa (NSFW)"""
        if not ctx.channel.is_nsfw():
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
            
        if member == ctx.author:
            return await ctx.send("To musi boleć... 😳")

        embed = discord.Embed(
            description=f"💥 **{ctx.author.display_name}** daje mocnego klapsa **{member.display_name}**! 🍑",
            color=KAWAII_RED
        )
        embed.set_image(url=random.choice(GIFS_SPANK))
        await ctx.send(embed=embed)

    @commands.command()
    async def strip(self, ctx, member: discord.Member = None):
        """Zdejmij z siebie (lub z kogoś) ubrania (NSFW)"""
        if not ctx.channel.is_nsfw():
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
            
        if member is None or member == ctx.author:
            desc = f"👚 **{ctx.author.display_name}** powoli zdejmuje z siebie ubrania... 🔥"
        else:
            desc = f"👙 **{ctx.author.display_name}** zaczyna rozbierać **{member.display_name}**... oj, robi się naprawdę gorąco! 😳"

        embed = discord.Embed(description=desc, color=KAWAII_RED)
        embed.set_image(url=random.choice(GIFS_STRIP))
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(NSFW(bot))
