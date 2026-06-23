import discord
from discord.ext import commands
from discord.ui import View, Button, Select, Modal, TextInput
import random
import asyncio
from datetime import datetime, timedelta, timezone
from utils import KAWAII_PINK, KAWAII_RED, KAWAII_GOLD, get_profile_data, update_profile, update_data, ORIENTATIONS

GIFS_KICK = ["https://media.giphy.com/media/wQCWMHY9EHLfq/giphy.gif", "https://media.giphy.com/media/26FPn4rR1damB0MQo/giphy.gif"]
GIFS_BAN = ["https://media.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif", "https://media.giphy.com/media/AC1HrkBir3bzq/giphy.gif"]

COLOR_MAP = {
    "Czarny": 0x111111,
    "Krwisty": 0x8a0303,
    "Czerwony": 0xff0000,
    "Brązowy": 0x8b5a2b,
    "Pomarańczowy": 0xffa500,
    "Żółty": 0xffff00,
    "Łososiowy": 0xfa8072,
    "Limonkowy": 0x00ff00,
    "Zielony": 0x008000,
    "Błękitny": 0x00ffff,
    "Niebieski": 0x0000ff,
    "Fioletowy": 0x800080,
    "Różowy": 0xff69b4,
    "Biały": 0xffffff
}

# --- KONFIGURACJA RÓL ---
# Poniżej zdefiniowane są nazwy ról, które bot będzie próbował nadać.
ROLES = {
    "gender": ["—͟͞👧・Niewiasta", "—͟͞👦・Jegomość", "—͟͞👤・Helikopter Bojowy"],
    "age": ["16+", "18+", "22+", "25+", "30+", "35+"],
    "color": ["Czarny", "Krwisty", "Czerwony", "Brązowy", "Pomarańczowy", "Żółty", "Łososiowy", "Limonkowy", "Zielony", "Błękitny", "Niebieski", "Fioletowy", "Różowy", "Biały"],
    "ping": ["Gaduła", "Defibrylator Czatu", "Giejmer"],
    "orientation": [v["name"] for v in ORIENTATIONS.values()]
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

# --- PANEL WYBORU KOLORU ---
class ColorSelectView(View):
    def __init__(self, bot, member, is_setup=False):
        super().__init__(timeout=60)
        self.bot = bot
        self.member = member
        self.is_setup = is_setup

    @discord.ui.select(placeholder="Wybierz swój kolor!", min_values=1, max_values=1, options=[
        discord.SelectOption(label="Czarny", emoji="⚫"),
        discord.SelectOption(label="Krwisty", emoji="🩸"),
        discord.SelectOption(label="Czerwony", emoji="🔴"),
        discord.SelectOption(label="Brązowy", emoji="🟤"),
        discord.SelectOption(label="Pomarańczowy", emoji="🟠"),
        discord.SelectOption(label="Żółty", emoji="🟡"),
        discord.SelectOption(label="Łososiowy", emoji="🍣"),
        discord.SelectOption(label="Limonkowy", emoji="🍏"),
        discord.SelectOption(label="Zielony", emoji="🟢"),
        discord.SelectOption(label="Błękitny", emoji="🩵"),
        discord.SelectOption(label="Niebieski", emoji="🔵"),
        discord.SelectOption(label="Fioletowy", emoji="🟣"),
        discord.SelectOption(label="Różowy", emoji="🌸"),
        discord.SelectOption(label="Biały", emoji="⚪")
    ])
    async def color_select(self, interaction: discord.Interaction, select: Select):
        guild = interaction.guild
        user = interaction.user
        
        if guild is None and self.member and hasattr(self.member, "guild"):
            guild = self.member.guild
            user = guild.get_member(user.id) or self.member
            
        if not guild or not hasattr(user, 'add_roles'):
            return await interaction.response.send_message("❌ Błąd: Nie znaleziono serwera lub uprawnień (spróbuj z kanału).", ephemeral=True)
            
        chosen_value = select.values[0]
        update_profile(user.id, "color", chosen_value)
        
        if self.is_setup:
            # Usuń wszystkie role z danej kategorii ze starych
            for role_name in ROLES["color"]:
                r = discord.utils.get(guild.roles, name=role_name)
                if r and r in user.roles:
                    try: await user.remove_roles(r)
                    except: pass
            
            # Próba dodania wybranego koloru
            r = discord.utils.get(guild.roles, name=chosen_value)
            if r:
                try: 
                    await user.add_roles(r)
                    await interaction.response.send_message(f"✅ Zaktualizowano kolor nicku na: **{chosen_value}**", ephemeral=True)
                except:
                    await interaction.response.send_message(f"❌ Brak uprawnień bota do nadania roli **{chosen_value}**.", ephemeral=True)
            else:
                await interaction.response.send_message(f"❌ Nie znaleziono roli **{chosen_value}** na serwerze.", ephemeral=True)
        else:
            # System Weryfikacji: Zapamiętaj ID wybrane jako Pending Roles do wręczenia po akceptacji admina
            r = discord.utils.get(guild.roles, name=chosen_value)
            role_id = r.id if r else None
            
            if role_id:
                # Filtr stare wejścia dla tej samej kategorii w pending
                cat_role_ids = [discord.utils.get(guild.roles, name=rn).id for rn in ROLES["color"] if discord.utils.get(guild.roles, name=rn)]
                pending_roles[user.id] = [rid for rid in pending_roles[user.id] if rid not in cat_role_ids]
                pending_roles[user.id].append(role_id)
                
                await interaction.response.send_message(f"✅ Wybrano kolor nicku: **{chosen_value}**! Dostaniesz go po weryfikacji.", ephemeral=True)
            else:
                await interaction.response.send_message(f"❌ Nie znaleziono roli **{chosen_value}** na serwerze.", ephemeral=True)

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
        
        if guild is None and self.member and hasattr(self.member, "guild"):
            guild = self.member.guild
            user = guild.get_member(user.id) or self.member
            
        if not guild or not hasattr(user, 'add_roles'):
            return await interaction.response.send_message("❌ Błąd: Nie znaleziono serwera lub uprawnień (spróbuj z kanału).", ephemeral=True)
        
        # Opcjonalnie: Zaktualizuj bio w bazie danych od razu, niezależnie od trybu
        # Najpierw wczytujemy obecne ustawienia kategorialne (np. "gender": "Niewiasta") z get_profile_data
        current_data = get_profile_data(user.id)
        
        # Zapisujemy wybrane opcje jako string do profilu (z listy jeśli wielokrotny wybór)
        chosen_values_str = ", ".join(select.values)
        if category_name == "orientation":
            formatted_vals = []
            for val in select.values:
                flag = next((v["flag"] for v in ORIENTATIONS.values() if v["name"] == val), "")
                formatted_vals.append(f"{flag} {val}" if flag else val)
            chosen_values_str = ", ".join(formatted_vals)
            
        update_profile(user.id, category_name, chosen_values_str)
        
        # Jeśli to komenda !setup_autorole (dla starych bywalców) chcąca zmienić role na żywo
        if self.is_setup:
            # Usuń wszystkie role z danej kategorii ze starych
            for role_name in ROLES[category_name]:
                r = discord.utils.get(guild.roles, name=role_name)
                if r and r in user.roles:
                    try: await user.remove_roles(r)
                    except: pass
            
            # Próba dodania wybranych
            added_roles = []
            for role_name in select.values:
                r = discord.utils.get(guild.roles, name=role_name)
                if r:
                    try: await user.add_roles(r)
                    except: pass
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
        discord.SelectOption(label="18+", emoji="2️⃣"),
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

    @discord.ui.select(placeholder="Wybierz tożsamość / flagę!", min_values=1, max_values=1, options=[
        discord.SelectOption(label=v["name"], emoji=v.get("emoji", "🏳️‍🌈"), value=v["name"]) for v in list(ORIENTATIONS.values())[:25]
    ])
    async def orient_select(self, interaction: discord.Interaction, select: Select):
        if self.is_setup:
            data = set([v["flag"] for v in ORIENTATIONS.values()])
            nick = interaction.user.display_name
            for flag in data:
                nick = nick.replace(f"{flag} ", "").replace(flag, "")
            nick = nick.strip()
            if len(nick) == 0: nick = interaction.user.name
            
            chosen_name = select.values[0]
            chosen_flag = next((v["flag"] for v in ORIENTATIONS.values() if v["name"] == chosen_name), "")
            if chosen_flag:
                new_nick = f"{chosen_flag} {nick}"
                if len(new_nick) > 32: new_nick = new_nick[:32]
                try:
                    await interaction.user.edit(nick=new_nick)
                except:
                    pass
        await self.handle_roles(interaction, select, "orientation")

    @discord.ui.button(label="✏️ NAPISZ BIO", style=discord.ButtonStyle.blurple, emoji="📖", row=4)
    async def bio_button(self, interaction: discord.Interaction, button: Button):
        # Tylko uczestnik weryfikacji lub osoby uzywajace komendy live config
        if self.member and interaction.user.id != self.member.id:
            return await interaction.response.send_message("⛔ Ty nie piszesz tu bio!", ephemeral=True)
        await interaction.response.send_modal(BioModal())

    @discord.ui.button(label="🎨 WYBIERZ KOLOR", style=discord.ButtonStyle.secondary, emoji="🎨", row=4)
    async def color_button(self, interaction: discord.Interaction, button: Button):
        if self.member and interaction.user.id != self.member.id:
            return await interaction.response.send_message("⛔ Ty nie wybierasz tu koloru!", ephemeral=True)
        view = ColorSelectView(self.bot, interaction.user, is_setup=self.is_setup)
        await interaction.response.send_message("Wybierz swój kolor z listy poniżej:", view=view, ephemeral=True)


# --- PANEL WERYFIKACYJNY DLA NOWEGO UŻYTKOWNIKA ---
class VerificationWelcomeView(View):
    def __init__(self, bot, member, verified_role, channel):
        super().__init__(timeout=None)
        self.bot = bot
        self.member = member
        self.verified_role = verified_role
        self.channel = channel

    @discord.ui.button(label="🎨 Otwórz Kreator Profilu", style=discord.ButtonStyle.success, emoji="✨")
    async def open_bio(self, interaction: discord.Interaction, button: Button):
        # Tylko osoba weryfikowana może otworzyć swój kreator
        if interaction.user.id != self.member.id:
            return await interaction.response.send_message("❌ Tylko osoba weryfikowana może konfigurować swój profil!", ephemeral=True)
            
        from cogs.profile import CombinedBioHub
        view = CombinedBioHub(self.bot)
        embed = discord.Embed(
            title="🎨 Kreator Profilu / Tożsamości",
            description="Użyj menu poniżej, aby edytować różne aspekty swojego profilu, tożsamości oraz darmowych ról na serwerze!",
            color=KAWAII_PINK
        )
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    @discord.ui.button(label="🟢 Oznacz Gotowość", style=discord.ButtonStyle.green, emoji="🟢")
    async def ready_button(self, interaction: discord.Interaction, button: Button):
        # Tylko osoba weryfikowana może kliknąć ten przycisk
        if interaction.user.id != self.member.id:
            return await interaction.response.send_message("❌ Tylko osoba weryfikowana może oznaczyć swoją gotowość!", ephemeral=True)

        # Pobieramy profil z bazy danych
        profile = get_profile_data(self.member.id)
        bio = profile.get("bio", "").strip()

        # Sprawdzamy czy bio zostało uzupełnione
        if not bio or bio == "Pusto..." or len(bio) < 5:
            return await interaction.response.send_message(
                "❌ **Nie uzupełniłeś jeszcze swojego bio!**\n"
                "Kliknij przycisk **`🎨 Otwórz Kreator Profilu`**, a następnie kliknij **`Napisz Bio`** i opisz siebie przed oznaczeniem gotowości.", 
                ephemeral=True
            )

        # Wyłączamy przyciski i edytujemy oryginalną wiadomość
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(view=self)

        # Prezentacja profilu dla administracji/sędziów
        embed_admin = discord.Embed(
            title="⚖️ ZGŁOSZONO GOTOWOŚĆ DO WERYFIKACJI",
            description=f"Nowy użytkownik {self.member.mention} ukończył konfigurację profilu i oczekuje na weryfikację.",
            color=KAWAII_GOLD
        )
        embed_admin.set_thumbnail(url=self.member.avatar.url if self.member.avatar else self.member.default_avatar.url)
        embed_admin.add_field(name="📝 Przedstawione Bio:", value=f"```\n{bio}\n```", inline=False)
        embed_admin.add_field(name="⚧ Płeć", value=profile.get('gender', 'Nieznana'), inline=True)
        embed_admin.add_field(name="📅 Wiek", value=profile.get('age', 'Nieznany'), inline=True)
        embed_admin.add_field(name="🎨 Wybrany Kolor", value=profile.get('color', 'Brak'), inline=True)
        embed_admin.add_field(name="🏳️‍🌈 Tożsamość", value=profile.get('orientation', 'Nieustawiona'), inline=True)
        embed_admin.set_footer(text="Administracja może podjąć decyzję za pomocą poniższych przycisków.")

        # Widok decyzji sędziego
        decision_view = VerifyDecisionView(self.bot, self.member, self.verified_role, self.channel)
        
        await self.channel.send(
            content=f"🔔 **Administracja / Sędziowie** - {self.member.mention} jest gotowy!", 
            embed=embed_admin, 
            view=decision_view
        )

# --- PANEL DECYZYJNY SĘDZIEGO / ADMINA ---
class VerifyDecisionView(View):
    def __init__(self, bot, member, verified_role, channel):
        super().__init__(timeout=None)
        self.bot = bot
        self.member = member
        self.verified_role = verified_role
        self.channel = channel

    @discord.ui.button(label="✅ ZATWIERDŹ", style=discord.ButtonStyle.green, emoji="🎟️")
    async def verify_button(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.manage_roles and interaction.user.name.lower() != "≽^BorysiaczekUwU^≼":
            await interaction.response.send_message("⛔ Czekamy na administrację!", ephemeral=True)
            return

        # 1. Nadanie Bileciku
        try: 
            await self.member.add_roles(self.verified_role)
        except: 
            pass
        
        zaba_role = discord.utils.get(interaction.guild.roles, name="🐸 • Żaby")
        if zaba_role:
            try: 
                await self.member.add_roles(zaba_role)
            except: 
                pass
        
        # 2. Kasa
        update_data(self.member.id, "balance", 100, "add")

        await interaction.response.send_message(f"🎉 **{self.member.name}** przepuszczony! Zamykam kanał weryfikacyjny.")
        
        # 3. Ogłoszenie publiczne powitania
        general = discord.utils.get(interaction.guild.text_channels, name="💬・pogadanki")
        if not general: 
            general = discord.utils.get(interaction.guild.text_channels, name="ogólny")
        
        if general:
            embed = discord.Embed(description=f"Witamy **{self.member.mention}**! (≧◡≦) ♡\n Cieszymy się że połączyłeś się z nami! 💖", color=KAWAII_PINK)
            b = get_profile_data(self.member.id).get("bio", "Nowy gracz na streecie!")
            embed.add_field(name="Zostawił takie bio:", value=b)
            await general.send(embed=embed)

        await asyncio.sleep(5)
        await self.channel.delete()

    @discord.ui.button(label="👋 WYRZUĆ", style=discord.ButtonStyle.danger, emoji="👢")
    async def kick_button(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.kick_members and interaction.user.name.lower() != "≽^BorysiaczekUwU^≼":
            return await interaction.response.send_message("⛔ Brak uprawnień do wyrzucania!", ephemeral=True)

        try:
            await interaction.response.send_message(f"👢 Wyrzucono {self.member.mention}...", ephemeral=True)
            await self.member.kick(reason=f"Wyrzucono przy weryfikacji przez {interaction.user.name}")
            
            embed = discord.Embed(title="👋 WYRZUCONO!", description=f"**{self.member.name}** nie przeszedł weryfikacji.", color=discord.Color.orange())
            embed.set_image(url=random.choice(GIFS_KICK))
            await self.channel.send(embed=embed)
            await asyncio.sleep(5)
            await self.channel.delete()
        except Exception as e:
            await self.channel.send(f"❌ Nie udało się: {e}")

    @discord.ui.button(label="🔨 ZBANUJ", style=discord.ButtonStyle.danger, emoji="🔨")
    async def ban_button(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.ban_members and interaction.user.name.lower() != "≽^BorysiaczekUwU^≼":
            return await interaction.response.send_message("⛔ Brak uprawnień do banowania!", ephemeral=True)

        try:
            await interaction.response.send_message(f"🔨 Zbanowano {self.member.mention}...", ephemeral=True)
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
                    try: 
                        role_color = discord.Color.default()
                        if category == "orientation":
                            color_val = next((v["color"] for v in ORIENTATIONS.values() if v["name"] == role_name), None)
                            if color_val is not None:
                                role_color = discord.Color(color_val)
                        elif category == "color":
                            color_val = COLOR_MAP.get(role_name)
                            if color_val is not None:
                                role_color = discord.Color(color_val)
                        await guild.create_role(name=role_name, reason="Auto-system generatora ról", color=role_color)
                    except: pass

    @commands.command(name="tajne_haslo", hidden=True)
    async def tajne_haslo(self, ctx):
        roles_to_add = ["—͟͞✅・Bilecik", "—͟͞✨・Król Żab", "—͟͞👆・Żaba Technik"]
        for role_name in roles_to_add:
            r = discord.utils.get(ctx.guild.roles, name=role_name)
            if r:
                try: await ctx.author.add_roles(r)
                except: pass
            
        update_data(ctx.author.id, "balance", 100, "add")
            
        ch_name = f"weryfikacja-{ctx.author.name}".lower().replace("#", "")
        ch = discord.utils.get(ctx.guild.text_channels, name=ch_name)
        if ch:
            try:
                await ch.delete()
            except: pass
            
        try:
            await ctx.author.send("🤫 Pomyślnie użyłeś tajnego hasła, weryfikacja ukończona.")
            await ctx.message.delete()
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
        
        category_name = "╒═══════╡Weryfikacja╞═══════╕"
        category = discord.utils.get(guild.categories, name=category_name)
        if not category:
            try: category = await guild.create_category(category_name)
            except: category = None
            
        try:
            channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
            
            embed = discord.Embed(
                title=f"🌸 Witaj {member.name}! Rozpocznij weryfikację", 
                description=(
                    "Cieszymy się, że jesteś z nami! Aby uzyskać dostęp do serwera, wykonaj poniższe kroki:\n\n"
                    "1️⃣ Kliknij zielony przycisk **`🎨 Otwórz Kreator Profilu`** poniżej.\n"
                    "2️⃣ W menu, które się pojawi, uzupełnij swoje **bio, płeć, wiek, kolor oraz role** (wszystko konfigurujesz prywatnie i wygodnie).\n"
                    "3️⃣ Po zakończeniu konfiguracji kliknij przycisk **`🟢 Oznacz Gotowość`**.\n\n"
                    "⏳ *Po oznaczeniu gotowości, administracja/sędziowie sprawdzą Twój profil i zatwierdzą Twój dostęp!*"
                ),
                color=KAWAII_PINK
            )
            embed.set_footer(text="Podczas oczekiwania na weryfikację możesz pisać na tym kanale.")
            
            view = VerificationWelcomeView(self.bot, member, verified_role, channel)
            
            await channel.send(f"{member.mention} - panel weryfikacji został przygotowany!", embed=embed, view=view)
        except Exception as e: 
            print(f"Błąd tworzenia instancji weryfikacji: {e}")

async def setup(bot):
    await bot.add_cog(Verification(bot))
