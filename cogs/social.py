import discord
from discord.ext import commands
import random
from utils import KAWAII_PINK, KAWAII_RED, KAWAII_GOLD

GIFS_HUG = [
    "https://media.giphy.com/media/ODy2AThnlxWxO/giphy.gif",
    "https://media.giphy.com/media/lrr9rHuoNOE0ZwcTE/giphy.gif",
    "https://media.giphy.com/media/PHZ7v9tfQu0o0/giphy.gif"
]
GIFS_KISS = [
    "https://media.giphy.com/media/FqBTvSNjNzeZG/giphy.gif",
    "https://media.giphy.com/media/nyGFcsP0kAobm/giphy.gif"
]
GIFS_SLAP = [
    "https://media.giphy.com/media/10Am8idu3qWomI/giphy.gif",
    "https://media.giphy.com/media/Lp5ideZTgwKmk/giphy.gif"
]
GIFS_PAT = [
    "https://media.giphy.com/media/5tmRHwTlHAA9WkVxTU/giphy.gif",
    "https://media.giphy.com/media/L2z7dnOduqE6Y/giphy.gif"
]

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def przytul(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"**{ctx.author.name}** przytula **{member.name}**! ⊂(・﹏・⊂)", color=KAWAII_PINK)
        embed.set_image(url=random.choice(GIFS_HUG))
        await ctx.send(embed=embed)

    @commands.command()
    async def pocaluj(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"**{ctx.author.name}** całuje **{member.name}**! Mwa! 💋", color=KAWAII_RED)
        embed.set_image(url=random.choice(GIFS_KISS))
        await ctx.send(embed=embed)

    @commands.command()
    async def policzek(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"**{ctx.author.name}** uderza **{member.name}**! Baka! 💢", color=0xFF4500)
        embed.set_image(url=random.choice(GIFS_SLAP))
        await ctx.send(embed=embed)

    @commands.command()
    async def pat(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"**{ctx.author.name}** głaszcze **{member.name}**! 🌸", color=KAWAII_GOLD)
        embed.set_image(url=random.choice(GIFS_PAT))
        await ctx.send(embed=embed)

    @commands.command()
    async def ship(self, ctx, member: discord.Member):
        procent = random.randint(0, 100)
        serca = "💖" * (procent // 10)
        msg = f"Miłość między **{ctx.author.name}** a **{member.name}** wynosi **{procent}%**!\n{serca}"
        if procent > 90: msg += "\nTo przeznaczenie! (♥ω♥*)"
        elif procent < 20: msg += "\nMoże zostańcie przyjaciółmi... (cJc)"
        await ctx.send(msg)

    @commands.command()
    async def kula(self, ctx, *, pytanie):
        odpowiedzi = ["Oczywiście! 💖", "Raczej nie... (qwq)", "To pewne! 🌟", "Nie licz na to >_<", "Spytaj później ✨"]
        await ctx.send(f"🔮 **Pytanie:** {pytanie}\n✨ **Odpowiedź:** {random.choice(odpowiedzi)}")

async def setup(bot):
    await bot.add_cog(Social(bot))