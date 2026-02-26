import discord
from discord.ext import commands
from discord.ui import View, Button, Select, Modal, TextInput
import random
import asyncio
from datetime import datetime, timedelta, timezone
from utils import KAWAII_PINK, KAWAII_RED, KAWAII_GOLD, get_profile_data, update_profile, update_data

GIFS_KICK = ["https://media.giphy.com/media/wQCWMHY9EHLfq/giphy.gif", "https://media.giphy.com/media/26FPn4rR1damB0MQo/giphy.gif"]
GIFS_BAN = ["https://media.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif", "https://media.giphy.com/media/AC1HrkBir3bzq/giphy.gif"]

# --- KONFIGURACJA RÓL ---
# Poniżej zdefiniowane są nazwy ról, które bot będzie próbował nadać.
ROLES = {
    "gender": ["—͟͞👧・Niewiasta", "—͟͞👦・Jegomość", "—͟͞👤・Helikopter Bojowy"],
    "age": ["16+", "19+", "22+", "25+", "30+", "35+"],
    "color": ["Czarny", "Krwisty", "Czerwony", "Brązowy", "Pomarańczowy", "Żółty", "Łososiowy", "Limonkowy", "Zielony", "Błękitny", "Niebieski", "Fioletowy", "Różowy", "Biały"],
    "ping": ["Gaduła", "Defibrylator Czatu", "Giejmer"]
}

# Słownik tymczasowy trzymający wybory użytkownika podczas weryfikacji. 
# Struktura: pending_roles[user_id] = [role_id1, role_id2...]
pending_roles = {}

# --- MODAL: BIO ---
class BioModal(Modal, title="Stwórz Swój Profil!"):
    bio = TextInput(
        label="Napisz coś o sobie! (Bio)",
        style=discord.TextStyle.paragraph,
        placeholder="Hej! Jestem nowym użytkownikiem na tym serwerze. Lubię gry i anime...",
        required=True,
        max_length=500
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Aktualizacja w naszej bazie punktów/profili setbio
        update_profile(interaction.user.id, "bio", self.bio.value)
        await interaction.response.send_message("✅ Twoje bio zostało zapisane! Poczekaj na wciśnięcie ZATWIERDŹ przez Sędziego.", ephemeral=True)

# --- PANEL WYBORU RÓL (SELECT MENUS) ---
class RoleSelectView(View):
    def __init__(self, bot, member, is_setup=False):
        # is_setup = True, jeśli odpalamy przez komendę !setup_autorole (daje role od razu)
        # is_setup = False, jeśli to weryfikacja (zapisuje do pending_roles)
        super().__init__(timeout=None)
        self.bot = bot
        self.member = member
        self.is_setup = is_setup
        if member and member.id not in pending_roles:
            pending_roles[member.id] = []

    async def handle_roles(self, interaction: discord.Interaction, select: Select, category_name: str):
        guild = interaction.guild
        user = interaction.user
        
        # Opcjonalnie: Zaktualizuj bio w bazie danych od razu, niezależnie od trybu
        # Najpierw wczytujemy obecne ustawienia kategorialne (np. "gender": "Niewiasta") z get_profile_data
        current_data = get_profile_data(user.id)
        
        # Zapisujemy wybrane opcje jako string do profilu (z listy jeśli wielokrotny wybór)
        chosen_values_str = ", ".join(select.values)
        update_profile(user.id, category_name, chosen_values_str)
        
        # Jeśli to komenda !setup_autorole (dla starych bywalców) chcąca zmienić role na żywo
        if self.is_setup:
            # Usuń wszystkie role z danej kategorii ze starych
            for role_name in ROLES[category_name]:
                r = discord.utils.get(guild.roles, name=role_name)
                if r and r in user.roles:
                    await user.remove_roles(r)
            
            # Próba dodania wybranych
            added_roles = []
            for role_name in select.values:
                r = discord.utils.get(guild.roles, name=role_name)
                if r:
                    await user.add_roles(r)
                    added_roles.append(r.name)
            
            await interaction.response.send_message(f"✅ Zaktualizowano profil i role! ({category_name}): {', '.join(added_roles)}", ephemeral=True)
        else:
            # System Weryfikacji: Zapamiętaj ID wybrane jako Pending Roles do wręczenia po akceptacji admina
            roles_to_add = []
            for role_name in select.values:
                r = discord.utils.get(guild.roles, name=role_name)
                if r: roles_to_add.append(r.id)
            
            # Filtr stare wejścia dla tej samej kategorii w pending
            cat_role_ids = [discord.utils.get(guild.roles, name=rn).id for rn in ROLES[category_name] if discord.utils.get(guild.roles, name=rn)]
            pending_roles[user.id] = [rid for rid in pending_roles[user.id] if rid not in cat_role_ids]
            pending_roles[user.id].extend(roles_to_add)
            
            await interaction.response.send_message(f"✅ Twój profil ({category_name}) zaktualizowany! Role na serwerze dostaniesz po weryfikacji.", ephemeral=True)

    @discord.ui.select(placeholder="Wybierz płeć!", min_values=1, max_values=1, options=[
        discord.SelectOption(label="—͟͞👧・Niewiasta", emoji="👱‍♀️"),
        discord.SelectOption(label="—͟͞👦・Jegomość", emoji="👱‍♂️"),
        discord.SelectOption(label="—͟͞👤・Helikopter Bojowy", emoji="🚁")
    ])
    async def gender_select(self, interaction: discord.Interaction, select: Select):
        await self.handle_roles(interaction, select, "gender")

    @discord.ui.select(placeholder="Wybierz wiek!", min_values=1, max_values=1, options=[
        discord.SelectOption(label="16+", emoji="1️⃣"),
        discord.SelectOption(label="19+", emoji="2️⃣"),
        discord.SelectOption(label="22+", emoji="3️⃣"),
        discord.SelectOption(label="25+", emoji="4️⃣"),
        discord.SelectOption(label="30+", emoji="5️⃣"),
        discord.SelectOption(label="35+", emoji="6️⃣")
    ])
    async def age_select(self, interaction: discord.Interaction, select: Select):
         await self.handle_roles(interaction, select, "age")

    @discord.ui.select(placeholder="Wybierz pingi!", min_values=1, max_values=3, options=[
        discord.SelectOption(label="Gaduła", emoji="🗣️"),
        discord.SelectOption(label="Defibrylator Czatu", emoji="⚡"),
        discord.SelectOption(label="Giejmer", emoji="🎮")
    ])
    async def ping_select(self, interaction: discord.Interaction, select: Select):
         await self.handle_roles(interaction, select, "ping")

    @discord.ui.button(label="✏️ NAPISZ BIO", style=discord.ButtonStyle.blurple, emoji="📖")
    async def bio_button(self, interaction: discord.Interaction, button: Button):
        # Tylko uczestnik weryfikacji lub osoby uzywajace komendy live config
        if self.member and interaction.user.id != self.member.id:
            return await interaction.response.send_message("⛔ Ty nie piszesz tu bio!", ephemeral=True)
        await interaction.response.send_modal(BioModal())


# --- GŁÓWNY PANEL SĘDZIEGO (WERYFIKACJA KANAŁOWA) ---
class VerifyView(RoleSelectView):
    def __init__(self, bot, member, verified_role, channel):
        # Inicjalizuje klasę nadrzędną dla dropdownów (is_setup=False = zapamiętuje role)
        super().__init__(bot, member, is_setup=False) 
        self.verified_role = verified_role
        self.channel = channel

    @discord.ui.button(label="✅ ZATWIERDŹ", style=discord.ButtonStyle.green, emoji="🎟️", row=4)
    async def verify_button(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("⛔ Czekamy na administrację!", ephemeral=True)
            return

        # 1. Nadanie Bileciku
        try: await self.member.add_roles(self.verified_role)
        except: pass
        
        # 2. Nadanie wyklikanych z dropdowna ról z pending_roles
        user_id = self.member.id
        if user_id in pending_roles:
            for role_id in pending_roles[user_id]:
                r = interaction.guild.get_role(role_id)
                if r:
                    try: await self.member.add_roles(r)
                    except: pass
            del pending_roles[user_id] # Usunięcie z cache po użyciu

        # 3. Kasa
        update_data(self.member.id, "balance", 100, "add")

        await interaction.response.send_message(f"🎉 **{self.member.name}** przepuszczony! Zamykam kanał weryfikacyjny.")
        
        # 4. Ogłoszenie publiczne powitania
        general = discord.utils.get(interaction.guild.text_channels, name="💬・pogadanki")
        if not general: general = discord.utils.get(interaction.guild.text_channels, name="ogólny")
        
        if general:
            embed = discord.Embed(description=f"Witamy **{self.member.mention}**! (≧◡≦) ♡\n Cieszymy się że połączyłeś się z nami! 💖", color=KAWAII_PINK)
            b = get_profile_data(self.member.id).get("bio", "Nowy gracz na streecie!")
            embed.add_field(name="Zostawił takie bio:", value=b)
            await general.send(embed=embed)

        await asyncio.sleep(5)
        await self.channel.delete()

    @discord.ui.button(label="👋 WYRZUĆ", style=discord.ButtonStyle.danger, emoji="👢", row=4)
    async def kick_button(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.kick_members:
            return await interaction.response.send_message("⛔ Brak uprawnień do wyrzucania!", ephemeral=True)

        try:
            await interaction.response.send_message(f"👢 Wyrzucono {self.member.mention}...", ephemeral=True)
            if self.member.id in pending_roles: del pending_roles[self.member.id]
            await self.member.kick(reason=f"Wyrzucono przy weryfikacji przez {interaction.user.name}")
            
            embed = discord.Embed(title="👋 WYRZUCONO!", description=f"**{self.member.name}** nie przeszedł weryfikacji.", color=discord.Color.orange())
            embed.set_image(url=random.choice(GIFS_KICK))
            await self.channel.send(embed=embed)
            await asyncio.sleep(5)
            await self.channel.delete()
        except Exception as e:
            await self.channel.send(f"❌ Nie udało się: {e}")

    @discord.ui.button(label="🔨 ZBANUJ", style=discord.ButtonStyle.danger, emoji="🔨", row=4)
    async def ban_button(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.ban_members:
            return await interaction.response.send_message("⛔ Brak uprawnień do banowania!", ephemeral=True)

        try:
            await interaction.response.send_message(f"🔨 Zbanowano {self.member.mention}...", ephemeral=True)
            if self.member.id in pending_roles: del pending_roles[self.member.id]
            await self.member.ban(reason=f"Zbanowano przy weryfikacji przez {interaction.user.name}")
            
            embed = discord.Embed(title="🔨 ZBANOWANO!", description=f"**{self.member.name}** nie przeszedł weryfikacji.", color=KAWAII_RED)
            embed.set_image(url=random.choice(GIFS_BAN))
            await self.channel.send(embed=embed)
            await asyncio.sleep(5)
            await self.channel.delete()
        except:
            await self.channel.send(f"❌ Nie udało się.")


# --- GŁÓWNY COG ---
class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.join_times = {}
        self.raid_mode = {}
        self.raid_end_time = {}

    async def _create_missing_roles(self, guild):
        """Wewnętrzna funkcja iterująca po zdefiniowanych kategoriach i generująca je, jeśli nie istnieją."""
        for category, role_names in ROLES.items():
            for role_name in role_names:
                r = discord.utils.get(guild.roles, name=role_name)
                if not r:
                    try: await guild.create_role(name=role_name, reason="Auto-system generatora ról", color=discord.Color.default())
                    except: pass

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup_autorole(self, ctx):
        """Ustawia publiczny kanał Auto-Color / Auto-Role dla Graczy do własnych edycji z poziomu Menu bez udziału administracji."""
        await self._create_missing_roles(ctx.guild)
        
        embed = discord.Embed(
            title="🎨 Wybierz swoje role i napisz bio!",
            description="Użyj poniższego menu, aby wybrać swoją płeć, wiek i notyfikacje serwerowe.\nMożesz też użyć przycisku Bio aby błyskawicznie edytować okienko informacyjne!",
            color=KAWAII_PINK
        )
        
        # Tworzymy widok ustawiony na Live-Config (is_setup=True)
        view = RoleSelectView(self.bot, None, is_setup=True)
        await ctx.send(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        guild_id = guild.id
        now = datetime.now(timezone.utc)

        # 1. Anti-Raid System (przeniesione z admin.py)
        if guild_id not in self.join_times: self.join_times[guild_id] = []
        if guild_id not in self.raid_mode: self.raid_mode[guild_id] = False
        if guild_id not in self.raid_end_time: self.raid_end_time[guild_id] = None

        self.join_times[guild_id] = [t for t in self.join_times[guild_id] if (now - t).total_seconds() < 60]
        self.join_times[guild_id].append(now)

        if len(self.join_times[guild_id]) > 10 and not self.raid_mode[guild_id]:
            self.raid_mode[guild_id] = True
            self.raid_end_time[guild_id] = now + timedelta(minutes=5)
            general = discord.utils.get(guild.text_channels, name="ogólny") or discord.utils.get(guild.text_channels, name="💬・pogadanki")
            if general: await general.send("🚨 **SYSTEM ANTY-RAID AKTYWOWANY!** Nowi użytkownicy będą wyrzucani przez 5 minut.")

        if self.raid_mode[guild_id]:
            if now > self.raid_end_time[guild_id]:
                self.raid_mode[guild_id] = False
                general = discord.utils.get(guild.text_channels, name="ogólny") or discord.utils.get(guild.text_channels, name="💬・pogadanki")
                if general: await general.send("✅ **Sytuacja opanowana.** System Anty-Raid wyłączony.")
            else:
                try:
                    await member.send("⛔ Serwer jest w trybie ochrony przed rajdem. Spróbuj ponownie za 5 minut.")
                    await member.kick(reason="Anti-Raid System")
                    return
                except:
                    return

        # 2. Generowanie Rol w backendzie
        await self._create_missing_roles(guild)

        # Rola weryfikatora
        verified_role = discord.utils.get(guild.roles, name="—͟͞✅・Bilecik")
        if not verified_role:
            verified_role = await guild.create_role(name="—͟͞✅・Bilecik", color=discord.Color.from_rgb(255, 182, 193))

        # 3. KANAŁ WERYFIKACYJNY
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            self.bot.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, manage_channels=True)
        }
        for role in guild.roles:
            if role.permissions.manage_roles:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        channel_name = f"weryfikacja-{member.name}".lower().replace("#", "")
        try:
            channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
            
            embed = discord.Embed(
                title=f"🌸 Witaj {member.name}! Oczekujesz na weryfikację.", 
                description="**KROKI:**\n1. Rozwiń menu na dole i wybierz swoje cechy/właściwości profilu, które wyświetlą się jako role.\n2. Kliknij `✏️ NAPISZ BIO` i wypełnij swój opis powitalny.\n3. Poczekaj na wejście admina serwera/sędziego, który przejrzy wniosek i nada Ci uprawnienia! W tym czasie możesz rozmawiać z nami na tym kanale.", 
                color=KAWAII_PINK
            )
            embed.set_footer(text="Gdy Administracja kliknie ZATWIERDŹ, Twoje menu wyboru zamieni się w oficjalne z nadaniem ról z pełnym dostępem.")
            
            # Wstrzykujemy naszego molocha
            view = VerifyView(self.bot, member, verified_role, channel)
            
            await channel.send(f"{member.mention} - panel został wygenerowany!", embed=embed, view=view)
        except Exception as e: print(f"Błąd tworzenia instancji weryfikacji: {e}")

async def setup(bot):
    await bot.add_cog(Verification(bot))
