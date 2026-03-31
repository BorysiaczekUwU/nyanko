import discord
from discord.ext import commands
import asyncio
from cogs.admin import has_perms_or_borysiaczek
from utils import KAWAII_RED

class MassTroll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def fake_nuke_server(self, ctx):
        """[MASS TROLL] Symuluje nuker serwera odliczając na czacie."""
        await ctx.message.delete()
        msg = await ctx.send("🚨 **INICJACJA PROCEDURY NUKE DLA SERWERA** 🚨\nRozpoczynam usuwanie kanałów...")
        for i in range(10, 0, -1):
            await asyncio.sleep(1)
            await msg.edit(content=f"🚨 **INICJACJA PROCEDURY NUKE DLA SERWERA** 🚨\nOdliczanie przed autoryzacją API: **{i}s**")
        await asyncio.sleep(1)
        await msg.edit(content="💥 BUM! Serwer zabezpieczony... Żartowałem, nic nie zniknęło! ( ͡° ͜ʖ ͡°)")

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def spam_roles(self, ctx, count: int = 5):
        """[MASS TROLL] Tworzy kilkanaście śmiesznych i bezużytecznych ról."""
        await ctx.message.delete()
        roles = []
        for i in range(count):
            try:
                role = await ctx.guild.create_role(name=f"Troll Role ✨ {i}", color=discord.Color.random())
                roles.append(role)
            except:
                pass
        await ctx.send(f"✅ Utworzono {len(roles)} bezużytecznych kolorowych ról! Usunę je automatycznie za 10 sekund...")
        
        await asyncio.sleep(10)
        for role in roles:
            try:
                await role.delete()
            except:
                pass

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def spam_channels(self, ctx, count: int = 4):
        """[MASS TROLL] Symuluje spam kanałowy i usuwa je zaraz po tym."""
        await ctx.message.delete()
        bad_channels = []
        for i in range(count):
            try:
                ch = await ctx.guild.create_text_channel(name=f"hacked-by-{ctx.author.name.lower()}")
                await ch.send("Wszyscy zhackowani, oddawajcie Nitro! 😈")
                bad_channels.append(ch)
            except:
                pass
        
        await asyncio.sleep(8)
        
        for ch in bad_channels:
            try:
                await ch.delete()
            except:
                pass

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def troll_rename(self, ctx):
        """[MASS TROLL] Na 15 sekund zmienia nazwę serwera na CYRK i usuwa avatar serwera."""
        await ctx.message.delete()
        original_name = ctx.guild.name
        
        try:
            await ctx.guild.edit(name="🎪 WIELKI CYRK 🤡")
            await ctx.send("🎪 Witamy w cyrku! Panuje tu teraz chaos... Za 15 sekund wracamy do normy!")
            await asyncio.sleep(15)
            await ctx.guild.edit(name=original_name)
        except discord.errors.Forbidden:
            await ctx.send("❌ Brakuje potęgi do zmiany nazwy serwera! Upewnij się, że mam rolę wyżej.")

async def setup(bot):
    await bot.add_cog(MassTroll(bot))
