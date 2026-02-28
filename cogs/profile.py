import discord
from discord.ext import commands
import asyncio
from discord.ui import Modal, TextInput, View, Select
from utils import get_profile_data, update_profile, get_level_data, get_data, KAWAII_PINK, KAWAII_BLUE
from cogs.verification import RoleSelectView

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setbio(self, ctx):
        """Otwiera panel ustawiania profilu (Prywatnie)"""
        try:
            await ctx.message.delete()
        except:
            pass

        embed = discord.Embed(
            title="🎨 Kreator Profilu",
            description="Użyj menu poniżej, aby wybrać swoją płeć, wiek i notyfikacje serwerowe.\nMożesz też użyć przycisku Bio aby błyskawicznie edytować okienko informacyjne!",
            color=KAWAII_BLUE
        )
        embed.set_footer(text="Bot stworzony przez BorysiaczekUwU 💖")

        try:
            view = RoleSelectView(self.bot, ctx.author, is_setup=True)
            await ctx.author.send(embed=embed, view=view)
            # Opcjonalne potwierdzenie na kanale (znika po 5s)
            temp_msg = await ctx.send(f"{ctx.author.mention}, wysłałam Ci panel ustawień w wiadomości prywatnej! 📩")
            await asyncio.sleep(5)
            await temp_msg.delete()
        except discord.Forbidden:
            await ctx.send(f"❌ {ctx.author.mention}, nie mogę wysłać Ci wiadomości prywatnej! Odblokuj DM.")

    @commands.command()
    async def bio(self, ctx, member: discord.Member = None):
        """Wyświetla piękny profil użytkownika"""
        member = member or ctx.author
        
        # Pobieranie danych (Teraz z MongoDB przez utils)
        profile = get_profile_data(member.id)
        economy = get_data(member.id)
        level_data = get_level_data(member.id)
        
        roles = [r.mention for r in member.roles if r.name != "@everyone"]
        roles = roles[::-1][:5] 
        roles_str = " ".join(roles) if roles else "Brak ról"

        embed = discord.Embed(color=member.color if member.color != discord.Color.default() else KAWAII_PINK)
        
        embed.set_author(name=f"Profil użytkownika {member.name}", icon_url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

        embed.add_field(name="👤 O mnie", value=f"```\n{profile.get('bio', 'Pusto...')}\n```", inline=False)
        
        embed.add_field(name="⚧ Płeć", value=profile.get('gender', 'Nieznana'), inline=True)
        embed.add_field(name="🗣️ Zaimki", value=profile.get('pronouns', 'Nieznane'), inline=True)
        embed.add_field(name="📅 Wiek", value=profile.get('age', 'Nieznany'), inline=True)
        embed.add_field(name="🎂 Urodziny", value=profile.get('birthday', 'Nieznane'), inline=True)
        embed.add_field(name="💞 Status", value=profile.get('status', 'Nieznany'), inline=True)

        partner_id = profile.get('partner')
        partner_txt = "Brak"
        if partner_id:
             try:
                 p_user = await self.bot.fetch_user(partner_id)
                 partner_txt = f"{p_user.name} 💍"
             except:
                 partner_txt = "Nieznany"
        embed.add_field(name="💖 Partner", value=partner_txt, inline=True)

        stats = (
            f"⭐ **Level:** {level_data['level']}\n"
            f"✨ **XP:** {level_data['xp']}\n"
            f"❤️ **Reputacja:** {level_data['rep']}"
        )
        embed.add_field(name="📊 Statystyki", value=stats, inline=True)

        money_stats = (
            f"💰 **Portfel:** {economy['balance']}\n"
            f"📦 **Przedmioty:** {sum(economy.get('inventory', {}).values())}"
        )
        embed.add_field(name="💎 Ekonomia", value=money_stats, inline=True)
        
        # Podpis twórcy
        embed.set_footer(text=f"Stworzony przez BorysiaczekUwU 💖 • ID: {member.id}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Profile(bot))