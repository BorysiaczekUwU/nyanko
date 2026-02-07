import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import random
from utils import get_level_data, update_level_data, load_levels, save_levels, KAWAII_PINK, KAWAII_GOLD

# KONFIGURACJA RÓL ZA LEVEL
# Klucz: Level, Wartość: Nazwa roli na Discordzie
# Upewnij się, że stworzyłeś te role na serwerze i bot ma rolę wyżej od nich!
LEVEL_ROLES = {
    1: "🌱 Nowicjusz",
    5: "🌸 Bywalec",
    10: "⭐ Elita",
    15: "👑 Legenda"
}

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_xp_loop.start()

    def xp_needed(self, level):
        return 100 * level

    async def add_xp(self, user, amount, channel=None):
        data = get_level_data(user.id)
        current_xp = data["xp"]
        current_lvl = data["level"]

        if current_lvl >= 15: return 

        new_xp = current_xp + amount
        needed = self.xp_needed(current_lvl)

        if new_xp >= needed:
            new_xp -= needed
            current_lvl += 1
            
            update_level_data(user.id, "level", current_lvl, "set")
            update_level_data(user.id, "xp", new_xp, "set")

            # --- SYSTEM RÓL ---
            if channel:
                # Sprawdź czy za ten level jest rola
                if current_lvl in LEVEL_ROLES:
                    new_role_name = LEVEL_ROLES[current_lvl]
                    role = discord.utils.get(user.guild.roles, name=new_role_name)
                    
                    if role:
                        try:
                            # Dodaj nową rolę
                            await user.add_roles(role)
                            
                            # Usuń stare role z leveli (opcjonalne, ale prosiłeś o to)
                            # Iterujemy po niższych levelach i zabieramy role jeśli user je ma
                            for lvl, r_name in LEVEL_ROLES.items():
                                if lvl < current_lvl:
                                    old_role = discord.utils.get(user.guild.roles, name=r_name)
                                    if old_role and old_role in user.roles:
                                        await user.remove_roles(old_role)
                                        
                            await channel.send(f"🆙 **LEVEL UP!** {user.mention} wbija **Level {current_lvl}** i otrzymuje rangę **{new_role_name}**! 🎉")
                        except discord.Forbidden:
                            await channel.send(f"🎉 **LEVEL UP!** {user.mention} wbija **Level {current_lvl}**! (Nie mogłam nadać roli - brak uprawnień 😿)")
                    else:
                        await channel.send(f"🎉 **LEVEL UP!** {user.mention} wbija **Level {current_lvl}**! (Rola {new_role_name} nie istnieje na serwerze)")
                else:
                    embed = discord.Embed(title="🎉 LEVEL UP! 🎉", description=f"Brawo **{user.mention}**! Awansowałeś na poziom **{current_lvl}**! ✨", color=KAWAII_GOLD)
                    await channel.send(embed=embed)
        else:
            update_level_data(user.id, "xp", new_xp, "set")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild: return
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

        if lvl >= 15:
            progress_bar = "MAX LEVEL 👑"
        else:
            percent = xp / needed
            blocks = int(percent * 10)
            progress_bar = "🟦" * blocks + "⬜" * (10 - blocks)

        embed = discord.Embed(title=f"📊 Poziom: {member.name}", color=KAWAII_PINK)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="⭐ Level", value=f"**{lvl}** / 15", inline=True)
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