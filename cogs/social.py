import discord
from discord.ext import commands
import random
from utils import KAWAII_PINK, KAWAII_RED, KAWAII_GOLD, get_profile_data, update_profile

GIFS_HUG = [
    "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmRsaWN4N3h0eGV3eWdvZXowcHF1YTR6NmcxNW9nOTYyNzkwYXBwMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1JmGiBtqTuehfYxuy9/giphy.gif",
    "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmFmejR0Z201NTkxc3J2bjYzMDcwODNhZHJvcG5yeG13ZW53MjM4MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5sokLWDYub7efuAD1M/giphy.gif",
    "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExOG5mYW94NHMwZHk1OXg1MWY4enM4ajE1OXlidnF4OXh3cTBldWVjdCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PHZ7v9tfQu0o0/giphy.gif"
]
GIFS_KISS = [
    "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExOGgyc2xzeHF1anN2eGs1MXg5YzQ5eGx5Nnloa3h3YzV2dGMza2t2OCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/W1hd3uXRIbddu/giphy.gif",
    "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2hmZGc1ODJ4ZGYzaDltcDVqZDBsaWtueXZiNmJ5a2Y2a2Y1ZHcyZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/8AduCFP7qQ660NEKns/giphy.gif"
]
GIFS_SLAP = [
    "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZXV2aDU3a2VycnRjZGhocGRwdXNmcHN3NHJkNnZlNmszZGo4aDV6biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/mEtSQlxqBtWWA/giphy.gif",
    "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmtodWozZ3A0M2hpczN1ZDNhamowNjlvZGU4dXJiMHU1bHI2dzVzcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JXuGatu6v9pUA/giphy.gif"
]
GIFS_PAT = [
    "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWJ3YmkxMG5ycWVsdzJtaXNoNG8xbTRhdDUydmQzZTlyZm4xNmJvOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/t9igJ3odrXBixqXtgf/giphy.gif",
    "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExN2ZkeGJsc3VubXRqenQzYnAzMTJ1aGp0Zm5jajRnNmt6eHdudTkwayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/FH0EiKkU2vjPHZ5op1/giphy.gif"
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

    @commands.command()
    async def slub(self, ctx, member: discord.Member):
        """Weź ślub z wybraną osobą! 💍"""
        if member == ctx.author:
            await ctx.send("Nie możesz poślubić samego siebie! (cJc)")
            return

        user_profile = get_profile_data(ctx.author.id)
        target_profile = get_profile_data(member.id)

        if user_profile.get("partner"):
            await ctx.send("Jesteś już w związku! Najpierw weź rozwód. (qwq)")
            return

        if target_profile.get("partner"):
            await ctx.send(f"**{member.name}** jest już w związku! 💔")
            return

        # Pytanie o zgodę
        embed = discord.Embed(
            title="💍 Oświadczyny!",
            description=f"**{ctx.author.name}** oświadcza się **{member.name}**!\nCzy przyjmujesz oświadczyny? (napisz `tak` lub `nie`)",
            color=KAWAII_PINK
        )
        await ctx.send(member.mention, embed=embed)

        def check(m):
            return m.author == member and m.channel == ctx.channel and m.content.lower() in ["tak", "nie"]

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60)
            if msg.content.lower() == "tak":
                update_profile(ctx.author.id, "partner", member.id)
                update_profile(member.id, "partner", ctx.author.id)

                success_embed = discord.Embed(
                    title="💒 Nowe Małżeństwo!",
                    description=f"🎉 Gratulacje! **{ctx.author.name}** i **{member.name}** są teraz małżeństwem! 💍💖",
                    color=KAWAII_GOLD
                )
                await ctx.send(embed=success_embed)
            else:
                await ctx.send("💔 Oświadczyny odrzucone... (qwq)")
        except:
            await ctx.send("⌛ Czas minął... Oświadczyny anulowane.")

    @commands.command()
    async def rozwod(self, ctx):
        """Weź rozwód ze swoim partnerem 💔"""
        user_profile = get_profile_data(ctx.author.id)
        partner_id = user_profile.get("partner")

        if not partner_id:
            await ctx.send("Nie masz z kim brać rozwodu! (cJc)")
            return

        # Czyścimy oba profile
        update_profile(ctx.author.id, "partner", None)
        update_profile(partner_id, "partner", None)

        # Próbujemy zdobyć nazwę partnera
        try:
            partner = await self.bot.fetch_user(partner_id)
            name = partner.name
        except:
            name = "Nieznany"

        embed = discord.Embed(
            title="💔 Rozwód",
            description=f"Związek z **{name}** został zakończony... 🌧️",
            color=KAWAII_RED
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['h5'])
    async def highfive(self, ctx, member: discord.Member):
        """Przybij piątkę! 🙌"""
        embed = discord.Embed(description=f"**{ctx.author.name}** przybija piątkę **{member.name}**! 🙌", color=KAWAII_GOLD)
        embed.set_image(url="https://media.giphy.com/media/l1uk71T4mU6d6qM3Q/giphy.gif")
        await ctx.send(embed=embed)

    @commands.command()
    async def kill(self, ctx, member: discord.Member):
        """Wyeliminuj cel (RP) 🔪"""
        kills = [
            "rzuca w niego czołgiem!",
            "atakuje go poduszką!",
            "częstuje go zatrutym ciastkiem!",
            "wysyła go w kosmos bez skafandra!",
            "zrzuca na niego fortepian!"
        ]
        embed = discord.Embed(description=f"**{ctx.author.name}** {random.choice(kills)} **{member.name}** pada trupem! 💀", color=KAWAII_RED)
        await ctx.send(embed=embed)

    @commands.command()
    async def feed(self, ctx, member: discord.Member):
        """Nakarm kogoś 🍜"""
        embed = discord.Embed(description=f"**{ctx.author.name}** karmi **{member.name}**! Smacznego! 🍜", color=KAWAII_PINK)
        embed.set_image(url="https://media.giphy.com/media/xT39Dp00VAaF9Klc1M/giphy.gif")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Social(bot))
