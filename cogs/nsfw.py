import discord
from discord.ext import commands
import aiohttp
import random

KAWAII_PINK = discord.Color.from_rgb(255, 182, 193)
KAWAII_RED = discord.Color.from_rgb(255, 105, 180)

# Gifs
HUG = ["https://media.giphy.com/media/2UIcmK4pn7rYNLRboG/giphy.gif", "https://media.giphy.com/media/l2QDP39mURZH1Ble0/giphy.gif"]
KISS = ["https://media.giphy.com/media/G3va31bE1KVhbclxXk/giphy.gif", "https://media.giphy.com/media/zkppEMFvRX5i2nZgK8/giphy.gif"]
SPANK = ["https://media.giphy.com/media/QscbSqUut7SFO/giphy.gif", "https://media.giphy.com/media/e8cf5858fc95acba2d627cbbfe7b26c2/giphy.gif"]
STRIP = ["https://media.giphy.com/media/l4pTfx2qLszoacZRS/giphy.gif", "https://media.giphy.com/media/3o7TKSxdQJIJiPcw0M/giphy.gif"]

class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_nsfw(self, ctx):
        if hasattr(ctx.channel, "is_nsfw"):
            try:
                if callable(ctx.channel.is_nsfw):
                    return ctx.channel.is_nsfw()
                else:
                    return bool(ctx.channel.is_nsfw)
            except:
                pass
        if hasattr(ctx.channel, "nsfw"):
            return bool(ctx.channel.nsfw)
        return False

    async def get_image(self, type_str):
        urls = {
            "waifu": "https://api.waifu.pics/nsfw/waifu",
            "neko": "https://api.waifu.pics/nsfw/neko",
            "trap": "https://api.waifu.pics/nsfw/trap",
            "blowjob": "https://api.waifu.pics/nsfw/blowjob"
        }
        url = urls.get(type_str, urls["waifu"])
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=5) as r:
                    if r.status == 200:
                        data = await r.json()
                        return data.get("url")
        except:
            pass
        return None

    @commands.command()
    async def porn(self, ctx):
        if not self.is_nsfw(ctx): return await ctx.send("❌ To kanał SFW!")
        img = await self.get_image("waifu")
        if img:
            await ctx.send(embed=discord.Embed(title="🔞 PORN", color=KAWAII_RED).set_image(url=img))
        else:
            await ctx.send("❌ Błąd pobierania obrazka z API.")

    @commands.command()
    async def yuri(self, ctx):
        if not self.is_nsfw(ctx): return await ctx.send("❌ To kanał SFW!")
        img = await self.get_image("waifu")
        if img:
            await ctx.send(embed=discord.Embed(title="👩‍❤️‍💋‍👩 Yuri", color=KAWAII_PINK).set_image(url=img))
        else:
            await ctx.send("❌ Błąd pobierania obrazka.")

    @commands.command()
    async def yaoi(self, ctx):
        if not self.is_nsfw(ctx): return await ctx.send("❌ To kanał SFW!")
        img = await self.get_image("trap")
        if img:
            await ctx.send(embed=discord.Embed(title="👨‍❤️‍💋‍👨 Yaoi", color=KAWAII_PINK).set_image(url=img))
        else:
            await ctx.send("❌ Błąd pobierania obrazka.")

    @commands.command()
    async def femboy(self, ctx):
        if not self.is_nsfw(ctx): return await ctx.send("❌ To kanał SFW!")
        img = await self.get_image("trap")
        if img:
            await ctx.send(embed=discord.Embed(title="🎀 Femboy / Trap", color=KAWAII_PINK).set_image(url=img))
        else:
            await ctx.send("❌ Błąd pobierania obrazka.")

    @commands.command()
    async def hnt(self, ctx):
        if not self.is_nsfw(ctx): return await ctx.send("❌ To kanał SFW!")
        img = await self.get_image(random.choice(["waifu", "neko"]))
        if img:
            await ctx.send(embed=discord.Embed(title="🔞 Hentai", color=KAWAII_RED).set_image(url=img))
        else:
            await ctx.send("❌ Błąd pobierania obrazka.")

    @commands.command()
    async def boobs(self, ctx):
        if not self.is_nsfw(ctx): return await ctx.send("❌ To kanał SFW!")
        img = await self.get_image("waifu")
        if img:
            await ctx.send(embed=discord.Embed(title="🍒 Piersi", color=KAWAII_RED).set_image(url=img))
        else:
            await ctx.send("❌ Błąd pobierania obrazka.")

    @commands.command()
    async def ass(self, ctx):
        if not self.is_nsfw(ctx): return await ctx.send("❌ To kanał SFW!")
        img = await self.get_image("waifu")
        if img:
            await ctx.send(embed=discord.Embed(title="🍑 Tyłeczki", color=KAWAII_RED).set_image(url=img))
        else:
            await ctx.send("❌ Błąd pobierania obrazka.")

    @commands.command()
    async def rule34(self, ctx):
        if not self.is_nsfw(ctx): return await ctx.send("❌ To kanał SFW!")
        img = await self.get_image("waifu")
        if img:
            await ctx.send(embed=discord.Embed(title="🔞 Rule 34", color=KAWAII_RED).set_image(url=img))
        else:
            await ctx.send("❌ Błąd pobierania obrazka.")


    @commands.command()
    async def neko18(self, ctx):
        if not self.is_nsfw(ctx): return await ctx.send("❌ To kanał SFW!")
        img = await self.get_image("neko")
        if img:
            await ctx.send(embed=discord.Embed(title="🐱 Neko 18+", color=KAWAII_RED).set_image(url=img))
        else:
            await ctx.send("❌ Błąd pobierania obrazka.")

    @commands.command()
    async def nsfw_hug(self, ctx, member: discord.Member):
        if not self.is_nsfw(ctx): return await ctx.send("❌ To kanał SFW!")
        embed = discord.Embed(description=f"🔥 **{ctx.author.name}** przytula gorąco **{member.name}**!", color=KAWAII_RED)
        embed.set_image(url=random.choice(HUG))
        await ctx.send(embed=embed)

    @commands.command()
    async def nsfw_kiss(self, ctx, member: discord.Member):
        if not self.is_nsfw(ctx): return await ctx.send("❌ To kanał SFW!")
        embed = discord.Embed(description=f"💋 **{ctx.author.name}** całuje namiętnie **{member.name}**!", color=KAWAII_RED)
        embed.set_image(url=random.choice(KISS))
        await ctx.send(embed=embed)

    @commands.command()
    async def spank(self, ctx, member: discord.Member):
        if not self.is_nsfw(ctx): return await ctx.send("❌ To kanał SFW!")
        embed = discord.Embed(description=f"💥 **{ctx.author.name}** daje klapsa **{member.name}**!", color=KAWAII_RED)
        embed.set_image(url=random.choice(SPANK))
        await ctx.send(embed=embed)

    @commands.command()
    async def strip(self, ctx, member: discord.Member = None):
        if not self.is_nsfw(ctx): return await ctx.send("❌ To kanał SFW!")
        target = member.name if member else ctx.author.name
        embed = discord.Embed(description=f"👙 **{target}** zdejmuje ubrania...", color=KAWAII_RED)
        embed.set_image(url=random.choice(STRIP))
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(NSFW(bot))
