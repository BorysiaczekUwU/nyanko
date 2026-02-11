import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import random
from utils import get_level_data, update_level_data, KAWAII_PINK, KAWAII_GOLD

# KONFIGURACJA RÓL ZA LEVEL
# Teraz automatycznie generujemy role w stylu "LVL 1", "LVL 2" ... "LVL 100"
# Upewnij się, że masz te role na serwerze, albo bot je stworzy (jeśli ma uprawnienia, ale tutaj zakładamy że są)
MAX_LEVEL = 100

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_xp_loop.start()
        # Cooldown: 1 użycie na 60 sekund per user
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 60.0, commands.BucketType.user)

    def xp_needed(self, level):
        # Wzór kwadratowy
        return 5 * (level ** 2) + 50 * level + 100

    async def add_xp(self, user, amount, channel=None):
        data = get_level_data(user.id)
        current_xp = data["xp"]
        current_lvl = data["level"]

        if current_lvl >= MAX_LEVEL: return

        current_xp += amount
        leveled_up = False

        # Pętla dla potencjalnego wielokrotnego awansu (np. duży bonus XP)
        while True:
            needed = self.xp_needed(current_lvl)
            if current_xp >= needed:
                current_xp -= needed
                current_lvl += 1
                leveled_up = True
                if current_lvl >= MAX_LEVEL:
                    current_xp = 0
                    break
            else:
                break
            
        # Zapisujemy zmiany
        update_level_data(user.id, "level", current_lvl, "set")
        update_level_data(user.id, "xp", current_xp, "set")

        if leveled_up and channel:
            embed = discord.Embed(title="🎉 LEVEL UP! 🎉", description=f"Brawo **{user.mention}**! Awansowałeś na poziom **{current_lvl}**! ✨", color=KAWAII_GOLD)

            new_role_name = f"LVL {current_lvl}"
            role = discord.utils.get(user.guild.roles, name=new_role_name)

            if role:
                try:
                    await user.add_roles(role)
                    embed.add_field(name="Nowa Ranga", value=f"**{new_role_name}**")

                    # Usuwamy poprzednią rangę
                    old_role_name = f"LVL {current_lvl - 1}"
                    old_role = discord.utils.get(user.guild.roles, name=old_role_name)
                    if old_role and old_role in user.roles:
                        await user.remove_roles(old_role)

                except discord.Forbidden:
                    embed.set_footer(text="Brak uprawnień do zarządzania rolami :(")

            # Wysyłamy z delete_after, żeby nie spamować kanału
            try:
                await channel.send(embed=embed, delete_after=60)
            except:
                pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild: return

        # Sprawdzamy cooldown XP
        bucket = self.cooldown.get_bucket(message)
        retry_after = bucket.update_rate_limit()
        if retry_after:
            return

        xp_amount = random.randint(10, 20)
        await self.add_xp(message.author, xp_amount, message.channel)

    @tasks.loop(minutes=5)
    async def voice_xp_loop(self):
        for guild in self.bot.guilds:
            for channel in guild.voice_channels:
                for member in channel.members:
                    if member.bot: continue
                    if member.voice.self_mute or member.voice.self_deaf: continue
                    text_channel = discord.utils.get(guild.text_channels, name="ogólny")
                    if text_channel: await self.add_xp(member, 30, text_channel)

    @voice_xp_loop.before_loop
    async def before_voice_loop(self):
        await self.bot.wait_until_ready()

    @commands.command(aliases=['lvl', 'rank'])
    async def poziom(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        data = get_level_data(member.id)
        lvl = data["level"]
        xp = data["xp"]
        rep = data["rep"]
        needed = self.xp_needed(lvl)

        if lvl >= MAX_LEVEL:
            progress_bar = "MAX LEVEL 👑"
        else:
            percent = xp / needed
            blocks = int(percent * 10)
            progress_bar = "🟦" * blocks + "⬜" * (10 - blocks)

        embed = discord.Embed(title=f"📊 Poziom: {member.name}", color=KAWAII_PINK)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="⭐ Level", value=f"**{lvl}** / {MAX_LEVEL}", inline=True)
        embed.add_field(name="✨ XP", value=f"{xp} / {needed}", inline=True)
        embed.add_field(name="❤️ Reputacja", value=f"**{rep}**", inline=True)
        embed.add_field(name="📈 Postęp", value=progress_bar, inline=False)
        
        await ctx.send(embed=embed)

    @commands.command()
    async def rep(self, ctx, member: discord.Member):
        if member == ctx.author: return await ctx.send("Nie sobie! (cJc)")
        user_data = get_level_data(ctx.author.id)
        now = datetime.now()
        
        if user_data["last_rep"]:
            last_rep = datetime.fromisoformat(user_data["last_rep"])
            if now - last_rep < timedelta(hours=24):
                return await ctx.send("⏳ Wróć jutro!")

        update_level_data(member.id, "rep", 1, "add")
        await self.add_xp(member, 50, ctx.channel)
        update_level_data(ctx.author.id, "last_rep", now.isoformat(), "set")

        embed = discord.Embed(title="❤️ REPUTACJA", description=f"**{ctx.author.name}** dał repa **{member.name}**! (+50 XP) ✨", color=KAWAII_PINK)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Levels(bot))