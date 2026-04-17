import discord
from discord.ext import commands
from discord.ui import View, Button
from utils import (
    KAWAII_PINK, KAWAII_GOLD, KAWAII_RED, KAWAII_BLUE,
    get_profile_data, update_profile, get_level_data,
    get_clan_data, update_clan_data, clans_col, profiles_col
)
import random

CATEGORY_NAME = "╒════════╡Klan╞════════╕"

class ClanInviteView(View):
    def __init__(self, bot, clan_name, invitee):
        super().__init__(timeout=86400) # 24h
        self.bot = bot
        self.clan_name = clan_name
        self.invitee = invitee

    @discord.ui.button(label="Dołącz!", style=discord.ButtonStyle.success, emoji="✅")
    async def join_btn(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.invitee.id:
            return await interaction.response.send_message("❌ To zaproszenie nie jest dla Ciebie!", ephemeral=True)
            
        profile = get_profile_data(self.invitee.id)
        if profile.get('clan'):
            return await interaction.response.send_message("❌ Jesteś już w innym klanie! Opuść go najpierw (`!opusc_klan`).", ephemeral=True)
            
        clan = get_clan_data(self.clan_name)
        if not clan["owner_id"]:
            return await interaction.response.send_message("❌ Ten klan już nie istnieje.", ephemeral=True)
            
        update_clan_data(self.clan_name, "members", self.invitee.id, "push")
        update_profile(self.invitee.id, "clan", self.clan_name)
        
        guild = interaction.guild
        if guild:
            role = guild.get_role(clan["role_id"])
            if role:
                try: await self.invitee.add_roles(role)
                except: pass
                
        # Disable buttons
        for child in self.children: child.disabled = True
        await interaction.message.edit(view=self)
        
        await interaction.response.send_message(f"🎉 Dołączyłeś do klanu **{self.clan_name}**!", ephemeral=False)

class ClanApplicationView(View):
    def __init__(self, bot, author, clan_name):
        super().__init__(timeout=None)
        self.bot = bot
        self.author = author
        self.clan_name = clan_name

    @discord.ui.button(label="AKCEPTUJ", style=discord.ButtonStyle.success, emoji="✅")
    async def accept_btn(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator and interaction.user.name.lower() != "≽^borysiaczekuwu^≼":
             return await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
             
        guild = interaction.guild
        
        # Tworzenie Kategorii
        category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
        if not category:
            category = await guild.create_category(CATEGORY_NAME)
            
        # Tworzenie Roli
        role_name = f"Klan: {self.clan_name}"
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            role = await guild.create_role(name=role_name, color=discord.Color.random(), reason="Nowy klan")
            
        # Tworzenie Kanału
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            role: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }
        for r in guild.roles:
            if r.permissions.administrator:
                overwrites[r] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
                
        channel_name = self.clan_name.lower().replace(" ", "-")
        channel = discord.utils.get(guild.text_channels, name=channel_name)
        if not channel:
            channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
            
        # Przypisywanie
        update_profile(self.author.id, "clan", self.clan_name)
        update_clan_data(self.clan_name, "owner_id", self.author.id)
        update_clan_data(self.clan_name, "members", self.author.id, "push")
        update_clan_data(self.clan_name, "channel_id", channel.id)
        update_clan_data(self.clan_name, "role_id", role.id)
        
        try:
            member = await guild.fetch_member(self.author.id)
            if member: await member.add_roles(role)
        except: pass
        
        embed = discord.Embed(title="🛡️ Klan Zaakceptowany", description=f"Klan **{self.clan_name}** został poprawnie utworzony przez {interaction.user.mention}!", color=KAWAII_GOLD)
        for child in self.children: child.disabled = True
        await interaction.message.edit(embed=embed, view=self)
        try: await self.author.send(f"🎉 Twój wniosek o klan **{self.clan_name}** został zaakceptowany! Kanał: {channel.mention}")
        except: pass

    @discord.ui.button(label="ODRZUĆ", style=discord.ButtonStyle.danger, emoji="❌")
    async def reject_btn(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.administrator and interaction.user.name.lower() != "≽^borysiaczekuwu^≼":
             return await interaction.response.send_message("❌ Brak uprawnień!", ephemeral=True)
             
        embed = discord.Embed(title="🛡️ Wniosek Odrzucony", description=f"Wniosek o klan **{self.clan_name}** odrzucony przez {interaction.user.mention}.", color=KAWAII_RED)
        for child in self.children: child.disabled = True
        await interaction.message.edit(embed=embed, view=self)
        try: await self.author.send(f"❌ Twój wniosek o założenie klanu zaostał odrzucony.")
        except: pass

class Clans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    def xp_needed(self, level):
        return 10 * (level ** 2) + 100 * level + 200

    @commands.command()
    async def zaloz_klan(self, ctx, *, nazwa: str):
        """Wysyła prośbę o założenie własnego klanu."""
        if len(nazwa) > 20: return await ctx.send("❌ Nazwa klanu może mieć maksymalnie 20 znaków!")
        
        user_level = get_level_data(ctx.author.id)["level"]
        if user_level < 12:
            return await ctx.send(f"❌ Musisz posiadać co najmniej **12 poziom** aby założyć klan! (Masz {user_level} lvl)")
            
        profile = get_profile_data(ctx.author.id)
        if profile.get('clan'):
            return await ctx.send("❌ Jesteś już w klanie! Opuść go przed wzięciem odpowiedzialności za nowy (`!opusc_klan`).")
            
        # Check if already exists in DB
        existing = get_clan_data(nazwa)
        if existing["owner_id"] is not None:
            return await ctx.send("❌ Ten klan już istnieje!")

        embed = discord.Embed(
            title="📥 Nowy wniosek klanowy", 
            description=f"**Gracz:** {ctx.author.mention} (`{ctx.author.id}`)\n**Poziom:** {user_level}\n**Nazwa klanu:** `{nazwa}`", 
            color=KAWAII_BLUE
        )
        
        view = ClanApplicationView(self.bot, ctx.author, nazwa)
        
        # Wyszukaj lub stwórz kanał na logi/wnioski
        ch_name = "wnioski-klanowe"
        admin_channel = discord.utils.get(ctx.guild.text_channels, name=ch_name)
        if not admin_channel:
            overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False)}
            for r in ctx.guild.roles:
                if r.permissions.administrator: overwrites[r] = discord.PermissionOverwrite(view_channel=True)
            try:
                admin_channel = await ctx.guild.create_text_channel(ch_name, overwrites=overwrites)
            except:
                admin_channel = ctx.channel # Fallback on error
                
        await admin_channel.send(embed=embed, view=view)
        await ctx.send("✅ Twój wniosek został wysłany do Administracji! Poczekaj na decyzję.")

    @commands.command()
    async def zapros_do_klanu(self, ctx, member: discord.Member):
        """Zaprasza daną osobę do Twojego klanu."""
        if member.bot: return await ctx.send("❌ Nie możesz zaprosić bota!")
        profile = get_profile_data(ctx.author.id)
        clan_name = profile.get('clan')
        if not clan_name:
            return await ctx.send("❌ Nie jesteś w żadnym klanie!")
            
        clan = get_clan_data(clan_name)
        # Check if author is owner or just member (we allow members to invite)
        if ctx.author.id not in clan["members"]:
            return await ctx.send("❌ Błąd bazy. Nie jesteś na liście członków tego klanu.")
            
        if get_profile_data(member.id).get('clan'):
            return await ctx.send("❌ Ten użytkownik jest już w jakimś klanie!")
            
        embed = discord.Embed(
            title="✉️ Zaproszenie Klanowe", 
            description=f"{ctx.author.mention} zaprasza Cię do klanu **{clan_name}**!\nCzy chcesz dołączyć?", 
            color=KAWAII_PINK
        )
        view = ClanInviteView(self.bot, clan_name, member)
        await ctx.send(content=member.mention, embed=embed, view=view)

    @commands.command()
    async def opis_klanu(self, ctx, *, opis: str):
        """Ustawia nowy opis klanu (Tylko dowódca)."""
        profile = get_profile_data(ctx.author.id)
        clan_name = profile.get('clan')
        if not clan_name: return await ctx.send("❌ Nie jesteś w żadnym klanie!")
        
        clan = get_clan_data(clan_name)
        if clan["owner_id"] != ctx.author.id:
            return await ctx.send("❌ Tylko Dowódca klanu może zmienić jego opis!")
            
        if len(opis) > 300: return await ctx.send("❌ Opis może mieć najwyżej 300 znaków!")
        
        update_clan_data(clan_name, "description", opis)
        await ctx.send(f"✅ Opis klanu **{clan_name}** został zaktualizowany!")

    @commands.command()
    async def opusc_klan(self, ctx):
        """Opuszcza Twój obecny klan."""
        profile = get_profile_data(ctx.author.id)
        clan_name = profile.get('clan')
        if not clan_name: return await ctx.send("❌ Nie jesteś w żadnym klanie!")
        
        clan = get_clan_data(clan_name)
        if clan["owner_id"] == ctx.author.id:
            return await ctx.send("❌ Jesteś właścicielem klanu! Żeby klan usunąć skontaktuj się z administracją albo przekaż dowództwo (jeśli dodana opcja).")
            
        update_profile(ctx.author.id, "clan", None)
        update_clan_data(clan_name, "members", ctx.author.id, "pull")
        
        role = ctx.guild.get_role(clan["role_id"])
        if role:
            try: await ctx.author.remove_roles(role)
            except: pass
            
        await ctx.send(f"👋 Opuściłeś klan **{clan_name}**.")

    @commands.command()
    async def klan(self, ctx, *, nazwa_lub_osoba=None):
        """Wypisuje profil klanu."""
        clan_name = None
        
        if nazwa_lub_osoba is None:
            profile = get_profile_data(ctx.author.id)
            clan_name = profile.get('clan')
        else:
            try:
                converter = commands.MemberConverter()
                member = await converter.convert(ctx, nazwa_lub_osoba)
                clan_name = get_profile_data(member.id).get('clan')
            except:
                clan_name = nazwa_lub_osoba
                
        if not clan_name:
            return await ctx.send("❌ Nie znaleziono klanu!")
            
        clan = get_clan_data(clan_name)
        if not clan.get("owner_id"):
            return await ctx.send("❌ Taki klan nie istnieje.")
            
        try: owner = await self.bot.fetch_user(clan["owner_id"])
        except: owner = None
        
        lvl = clan["level"]
        xp = clan["xp"]
        needed = self.xp_needed(lvl)
        percent = min(xp / needed, 1.0)
        blocks = int(percent * 10)
        progress_bar = "🟦" * blocks + "⬜" * (10 - blocks)

        embed = discord.Embed(title=f"🛡️ Klan: {clan_name}", description=clan["description"], color=KAWAII_PINK)
        embed.add_field(name="👑 Dowódca", value=owner.name if owner else "Nieznany", inline=True)
        embed.add_field(name="👥 Członkowie", value=f"{len(clan['members'])} osób", inline=True)
        embed.add_field(name="⭐ Poziom", value=f"Lvl {lvl}", inline=True)
        embed.add_field(name="✨ XP Klanu", value=f"{xp} / {needed}\n{progress_bar}", inline=False)
        
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild: return
        
        profile = get_profile_data(message.author.id)
        clan_name = profile.get('clan')
        if not clan_name: return
        
        clan = get_clan_data(clan_name)
        if not clan.get("owner_id"): return # Zabezpieczenie
        
        # Oblicz XP
        base_xp = random.randint(5, 15)
        # Podwojone XP na kanale klanowym
        if message.channel.id == clan.get("channel_id"):
            base_xp *= 2
            
        current_xp = clan["xp"] + base_xp
        current_lvl = clan["level"]
        
        leveled_up = False
        while True:
            needed = self.xp_needed(current_lvl)
            if current_xp >= needed:
                current_xp -= needed
                current_lvl += 1
                leveled_up = True
            else:
                break
                
        update_clan_data(clan_name, "xp", current_xp)
        if leveled_up:
            update_clan_data(clan_name, "level", current_lvl)
            ch = self.bot.get_channel(clan["channel_id"])
            if ch:
                try: await ch.send(f"🎉 **Gratulacje!** Nasz klan wbił **{current_lvl} poziom**!")
                except: pass

    @commands.command()
    async def powiadom_klan(self, ctx, *, wiadomosc: str):
        """Wysyła ping do wszystkich członków klanu (Tylko dowódca/zarząd)."""
        profile = get_profile_data(ctx.author.id)
        clan_name = profile.get('clan')
        if not clan_name: return await ctx.send("❌ Nie jesteś w żadnym klanie!")
        clan = get_clan_data(clan_name)
        if clan["owner_id"] != ctx.author.id:
            return await ctx.send("❌ Tylko Dowódca może używać grupowego pingu!")
        role = ctx.guild.get_role(clan["role_id"])
        if role:
            await ctx.send(f"{role.mention}\n**Ogłoszenie od {ctx.author.name}:**\n{wiadomosc}")
        else:
            await ctx.send("❌ Nie znaleziono roli klanowej.")
            
    @commands.command()
    async def sklad_klanu(self, ctx):
        """Wyświetla listę członków klanu."""
        profile = get_profile_data(ctx.author.id)
        clan_name = profile.get('clan')
        if not clan_name: return await ctx.send("❌ Nie jesteś w żadnym klanie!")
        clan = get_clan_data(clan_name)
        
        opis = ""
        for member_id in clan["members"]:
            user = ctx.guild.get_member(member_id)
            if user:
                opis += f"• {user.mention} (Lvl: {get_level_data(user.id)['level']})\n"
            else:
                opis += f"• `{member_id}` (Brak na serwerze)\n"
                
        embed = discord.Embed(title=f"👥 Skład klanu: {clan_name}", description=opis, color=KAWAII_PINK)
        await ctx.send(embed=embed)

    @commands.command()
    async def usun_klan(self, ctx):
        """Usuwa klan (Tylko dowódca)."""
        profile = get_profile_data(ctx.author.id)
        clan_name = profile.get('clan')
        if not clan_name: return await ctx.send("❌ Nie jesteś w żadnym klanie!")
        clan = get_clan_data(clan_name)
        if clan["owner_id"] != ctx.author.id:
            return await ctx.send("❌ Tylko Dowódca może usunąć klan!")
            
        # 1. Usuwanie ze wszystkich profili
        for member_id in clan["members"]:
            update_profile(member_id, "clan", None)
            
        # 2. Usuwanie ról i kanału
        channel = ctx.guild.get_channel(clan["channel_id"])
        if channel:
            try: await channel.delete(reason="Usunięcie klanu")
            except: pass
            
        role = ctx.guild.get_role(clan["role_id"])
        if role:
            try: await role.delete(reason="Usunięcie klanu")
            except: pass
            
        # 3. Usunięcie z bazy
        from utils import delete_clan
        delete_clan(clan_name)
        
        embed = discord.Embed(title="💥 Klan usunięty", description=f"Klan **{clan_name}** został pomyślnie i bezpowrotnie usunięty.", color=KAWAII_RED)
        await ctx.send(embed=embed)

    @commands.command()
    async def wyrzuc_klan(self, ctx, member: discord.Member):
        """Wyrzuca członka z klanu (Tylko dowódca)."""
        profile = get_profile_data(ctx.author.id)
        clan_name = profile.get('clan')
        if not clan_name: return await ctx.send("❌ Nie jesteś w żadnym klanie!")
        clan = get_clan_data(clan_name)
        
        if clan["owner_id"] != ctx.author.id:
            return await ctx.send("❌ Tylko Dowódca może wyrzucać członków!")
            
        if member.id not in clan["members"]:
            return await ctx.send(f"❌ **{member.name}** nie jest w Twoim klanie!")
            
        if member.id == ctx.author.id:
            return await ctx.send("❌ Nie możesz wyrzucić samego siebie! Użyj `!usun_klan` lub podaj dowództwo innej osobie.")
            
        # Wyrzucenie
        update_profile(member.id, "clan", None)
        update_clan_data(clan_name, "members", member.id, "pull")
        role = ctx.guild.get_role(clan["role_id"])
        if role:
            try: await member.remove_roles(role)
            except: pass
            
        await ctx.send(f"👢 Wyrzucono **{member.name}** z klanu **{clan_name}**.")

    @commands.command(aliases=["wplywy", "top_klany", "zestawienie"])
    async def zestawienie_klanow(self, ctx):
        """Pokazuje procentowy udział klanów w całkowitym XP na serwerze (Top 10)."""
        from utils import get_all_clans
        clans = get_all_clans()
        if not clans:
            return await ctx.send("❌ Brak klanów na serwerze.")
            
        total_xp = sum(c.get("xp", 0) for c in clans)
        if total_xp == 0:
            return await ctx.send("❌ Żaden klan nie wygenerował jeszcze XP! Zacznijcie pisać.")
            
        sorted_clans = sorted(clans, key=lambda x: x.get("xp", 0), reverse=True)[:10]
        
        opis = ""
        emojis = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        for i, clan in enumerate(sorted_clans):
            xp = clan.get("xp", 0)
            percent = (xp / total_xp) * 100
            
            bar_len = 15
            filled = int((percent / 100) * bar_len)
            bar = "🟦" * filled + "⬜" * (bar_len - filled)
            
            opis += f"{emojis[i]} **{clan.get('name')}** - {percent:.1f}% ({xp} XP)\n{bar}\n\n"
            
        embed = discord.Embed(title="📊 Wpływy Klanów na Serwerze", description=opis, color=discord.Color.gold())
        embed.set_footer(text=f"Łączne zyski z czatu wszystkich klanów: {total_xp} XP")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Clans(bot))
