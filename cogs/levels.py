import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import random
from utils import get_level_data, update_level_data, load_levels, save_levels, KAWAII_PINK, KAWAII_GOLD

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_xp_loop.start() # Uruchomienie naliczania XP za VC

    def xp_needed(self, level):
        """
        Oblicza ile XP potrzeba na NASTĘPNY poziom.
        Wzór: 100 * Level (np. na lvl 2 potrzeba 100 xp, na lvl 3 potrzeba 200 xp itd.)
        """
        return 100 * level

    async def add_xp(self, user, amount, channel=None):
        data = get_level_data(user.id)
        current_xp = data["xp"]
        current_lvl = data["level"]

        if current_lvl >= 15:
            return # Max level osiągnięty

        new_xp = current_xp + amount
        needed = self.xp_needed(current_lvl)

        # Sprawdzanie awansu (Level Up)
        if new_xp >= needed:
            new_xp -= needed # Zdejmujemy XP potrzebne na awans
            current_lvl += 1
            
            update_level_data(user.id, "level", current_lvl, "set")
            update_level_data(user.id, "xp", new_xp, "set")

            if channel:
                embed = discord.Embed(title="🎉 LEVEL UP! 🎉", description=f"Brawo **{user.mention}**! Awansowałeś na poziom **{current_lvl}**! ✨", color=KAWAII_GOLD)
                embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
                if current_lvl == 15:
                    embed.description += "\n👑 **OSIĄGNĄŁEŚ MAKSYMALNY POZIOM!** Jesteś legendą! 👑"
                await channel.send(embed=embed)
        else:
            update_level_data(user.id, "xp", new_xp, "set")

    # --- LISTENER: XP ZA WIADOMOŚCI ---
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild:
            return
        
        # Prosty system cooldownu (można dodać bardziej zaawansowany)
        # Dajemy losowo 10-20 XP za wiadomość
        xp_amount = random.randint(10, 20)
        await self.add_xp(message.author, xp_amount, message.channel)

    # --- TASK: XP ZA SIEDZENIE NA VC ---
    @tasks.loop(minutes=5)
    async def voice_xp_loop(self):
        # Ta pętla wykonuje się co 5 minut
        for guild in self.bot.guilds:
            for channel in guild.voice_channels:
                for member in channel.members:
                    if member.bot: continue
                    # Sprawdź czy nie jest wyciszony/zdeafowany (opcjonalne, tu dajemy za samą obecność)
                    # Dajemy 30 XP co 5 minut siedzenia
                    if member.voice.self_mute or member.voice.self_deaf:
                        continue # Nie dajemy XP jak ktoś jest wyciszony (anty-afk)
                    
                    # Hack: musimy znaleźć kanał tekstowy do wysłania info o level upie
                    text_channel = discord.utils.get(guild.text_channels, name="ogólny")
                    await self.add_xp(member, 30, text_channel)

    @voice_xp_loop.before_loop
    async def before_voice_loop(self):
        await self.bot.wait_until_ready()

    # --- KOMENDY ---

    @commands.command(aliases=['lvl', 'rank'])
    async def poziom(self, ctx, member: discord.Member = None):
        """Sprawdź swój poziom i XP"""
        member = member or ctx.author
        data = get_level_data(member.id)
        
        lvl = data["level"]
        xp = data["xp"]
        rep = data["rep"]
        needed = self.xp_needed(lvl)

        if lvl >= 15:
            progress_bar = "MAX LEVEL 👑"
            footer_text = "Jesteś mistrzem!"
        else:
            # Pasek postępu
            percent = xp / needed
            blocks = int(percent * 10)
            progress_bar = "🟦" * blocks + "⬜" * (10 - blocks)
            footer_text = f"Do następnego poziomu: {needed - xp} XP"

        embed = discord.Embed(title=f"📊 Karta Gracza: {member.name}", color=KAWAII_PINK)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="⭐ Poziom", value=f"**{lvl}** / 15", inline=True)
        embed.add_field(name="✨ XP", value=f"{xp} / {needed}", inline=True)
        embed.add_field(name="❤️ Reputacja", value=f"**{rep}** pkt", inline=True)
        embed.add_field(name="📈 Postęp", value=progress_bar, inline=False)
        embed.set_footer(text=footer_text)
        
        await ctx.send(embed=embed)

    @commands.command()
    async def rep(self, ctx, member: discord.Member):
        """Daj komuś punkt reputacji (XP) raz na 24h"""
        if member == ctx.author:
            await ctx.send("Nie możesz dać repa samemu sobie, głuptasku! (cJc)")
            return

        user_data = get_level_data(ctx.author.id)
        now = datetime.now()
        
        # Sprawdzanie cooldownu
        if user_data["last_rep"]:
            last_rep = datetime.fromisoformat(user_data["last_rep"])
            if now - last_rep < timedelta(hours=24):
                remaining = timedelta(hours=24) - (now - last_rep)
                hours, remainder = divmod(remaining.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                await ctx.send(f"⏳ Możesz dać repa dopiero za **{hours}h {minutes}m**! (o_O)")
                return

        # Dajemy Repa
        update_level_data(member.id, "rep", 1, "add")
        # Rep daje też sporo XP osobie obdarowanej!
        xp_bonus = 50
        await self.add_xp(member, xp_bonus, ctx.channel)
        
        # Zapisujemy czas
        update_level_data(ctx.author.id, "last_rep", now.isoformat(), "set")

        embed = discord.Embed(title="❤️ REPUTACJA", description=f"**{ctx.author.name}** podziękował użytkownikowi **{member.name}**!\nDodano +1 Rep i +{xp_bonus} XP! ✨", color=KAWAII_PINK)
        await ctx.send(embed=embed)

    @commands.command(aliases=['top'])
    async def leaderboard(self, ctx):
        """Ranking serwera"""
        raw_data = load_levels()
        # Sortowanie: najpierw level (malejąco), potem XP (malejąco)
        sorted_users = sorted(raw_data.items(), key=lambda x: (x[1]['level'], x[1]['xp']), reverse=True)
        
        desc = ""
        for i, (user_id, data) in enumerate(sorted_users[:10], start=1):
            # Próba pobrania nazwy użytkownika
            member = ctx.guild.get_member(int(user_id))
            name = member.name if member else f"Użytkownik {user_id}"
            
            medal = "👑" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            desc += f"{medal} **{name}** - Lvl {data['level']} (Rep: {data['rep']})\n"

        embed = discord.Embed(title="🏆 Ranking Serwera", description=desc, color=KAWAII_GOLD)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Levels(bot))