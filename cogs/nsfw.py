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

    def check_nsfw(self, ctx):
        if hasattr(ctx.channel, 'is_nsfw'):
            try:
                return ctx.channel.is_nsfw()
            except TypeError:
                return ctx.channel.is_nsfw
        return getattr(ctx.channel, 'nsfw', False)

    async def fetch_image(self, category_type="waifu") -> str:
        """
        Pomocnicza funkcja pobierająca obrazy NSFW.
        Domyślnie korzysta z api.waifu.pics, z zapasem na waifu.im.
        """
        urls = {
            "waifu": "https://api.waifu.pics/nsfw/waifu",
            "neko": "https://api.waifu.pics/nsfw/neko",
            "trap": "https://api.waifu.pics/nsfw/trap",
            "blowjob": "https://api.waifu.pics/nsfw/blowjob",
        }
        
        fallbacks = {
            "waifu": "https://api.waifu.im/search?included_tags=waifu&is_nsfw=true",
            "neko": "https://api.waifu.im/search?included_tags=hentai&is_nsfw=true",
            "trap": "https://api.waifu.im/search?included_tags=ero&is_nsfw=true",
            "blowjob": "https://api.waifu.im/search?included_tags=oral&is_nsfw=true",
        }
        
        target_url = urls.get(category_type, urls["waifu"])
        fallback_url = fallbacks.get(category_type, fallbacks["waifu"])
        
        try:
            timeout = aiohttp.ClientTimeout(total=5)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                headers = {'User-Agent': 'Mozilla/5.0'}
                # Proba glowna (waifu.pics)
                async with session.get(target_url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data and 'url' in data:
                            return data.get('url')
                
                # Zapas (waifu.im) - w przypadku blokady Cloudflare na IP serwera
                async with session.get(fallback_url, headers=headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        if data and 'images' in data and len(data['images']) > 0:
                            return data['images'][0].get('url')
                            
        except Exception as e:
            print(f"Error fetching from {target_url} or fallback: {e}")
        return None

    @commands.group(invoke_without_command=True)
    async def porn(self, ctx):
        """Normalne zdjęcia 18+"""
        if not self.check_nsfw(ctx):
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        image = await self.fetch_image("waifu")
        
        if image:
            embed = discord.Embed(title="😏🔞 PORN / Waifu", color=KAWAII_RED)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

    @commands.command()
    async def yuri(self, ctx):
        """Yuri (Dziewczyna x Dziewczyna) NSFW"""
        if not self.check_nsfw(ctx):
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        image = await self.fetch_image("waifu")
        
        if image:
            embed = discord.Embed(title="👩‍❤️‍💋‍👩 Yuri / Dziewczyny", color=KAWAII_PINK)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

    @commands.command()
    async def yaoi(self, ctx):
        """Yaoi (Chłopak x Chłopak) NSFW"""
        if not self.check_nsfw(ctx):
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        image = await self.fetch_image("trap")
        
        if image:
            embed = discord.Embed(title="👨‍❤️‍💋‍👨 Yaoi / Boys", color=KAWAII_PINK)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

    @commands.command()
    async def femboy(self, ctx):
        """Femboy / Trap 18+"""
        if not self.check_nsfw(ctx):
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        image = await self.fetch_image("trap")
        
        if image:
            embed = discord.Embed(title="🎀 Femboy / Trap", color=KAWAII_PINK)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

    @commands.command()
    async def hentai(self, ctx):
        """Hentai 18+"""
        if not self.check_nsfw(ctx):
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        image = await self.fetch_image(random.choice(["waifu", "neko"]))
        
        if image:
            embed = discord.Embed(title="🔞 Hentai / Neko / Waifu", color=KAWAII_RED)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

    @commands.command()
    async def boobs(self, ctx):
        """Piersi 18+"""
        if not self.check_nsfw(ctx):
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        image = await self.fetch_image("waifu")
        
        if image:
            embed = discord.Embed(title="🍒 Piersi", color=KAWAII_RED)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

    @commands.command()
    async def ass(self, ctx):
        """Tyłeczki 18+"""
        if not self.check_nsfw(ctx):
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        image = await self.fetch_image("waifu")
        
        if image:
            embed = discord.Embed(title="🍑 Tyłeczki", color=KAWAII_RED)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

    @commands.command()
    async def rule34(self, ctx):
        """Rule 34 zdjęcia 18+"""
        if not self.check_nsfw(ctx):
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        image = await self.fetch_image("waifu")
        
        if image:
            embed = discord.Embed(title="🔞 Rule 34", color=KAWAII_RED)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

    @commands.command()
    async def bj(self, ctx):
        """Zdjęcia BJ (Blowjob) 18+"""
        if not self.check_nsfw(ctx):
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        image = await self.fetch_image("blowjob")
        
        if image:
            embed = discord.Embed(title="💦 Blowjob", color=KAWAII_RED)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

    @commands.command()
    async def neko18(self, ctx):
        """Nekogirls (Kocie Dziewczyny) 18+"""
        if not self.check_nsfw(ctx):
            return await ctx.send("❌ Użyj tego na kanale NSFW! (Bonk!)")
        
        image = await self.fetch_image("neko")
        
        if image:
            embed = discord.Embed(title="🐱 Neko 18+", color=KAWAII_RED)
            embed.set_image(url=image)
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Nie udało mi się znaleźć odpowiedniego zdjęcia, spróbuj ponownie.")

    @commands.command()
    async def nsfw_hug(self, ctx, member: discord.Member):
        """Gorące przytulenie obok osoby (NSFW)"""
        if not self.check_nsfw(ctx):
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
        if not self.check_nsfw(ctx):
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
        if not self.check_nsfw(ctx):
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
        if not self.check_nsfw(ctx):
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
