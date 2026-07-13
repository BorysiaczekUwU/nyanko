import discord
from discord.ext import commands
from discord.ui import View, Button, Select, Modal, TextInput
import random
import asyncio
from datetime import datetime, timedelta, timezone
from utils import KAWAII_PINK, KAWAII_RED, KAWAII_GOLD, get_profile_data, update_profile, update_data, ORIENTATIONS, GENDERS

GIFS_KICK = ["https://media.giphy.com/media/wQCWMHY9EHLfq/giphy.gif", "https://media.giphy.com/media/26FPn4rR1damB0MQo/giphy.gif"]
GIFS_BAN = ["https://media.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif", "https://media.giphy.com/media/AC1HrkBir3bzq/giphy.gif"]

MINECRAFT_SPLASHES = [
    "Nie kop pionowo pod siebie!",
    "Nyanko to najlepszy bot na świecie!",
    "Czy widziałeś dzisiaj Herobrine'a?",
    "Zjedz pieczone żabie udko!",
    "100% czystego kodu i miłości!",
    "Mój drugi bot to też Nyanko!",
    "Made in Poland z miłością!",
    "Żaby rządzą tym serwerem! 🐸",
    "Borysiaczek tu był i patrzy!",
    "Kiedyś to było, teraz też jest super!",
    "Uważaj na Creepery w nocy!",
    "Diamonds, diamonds, diamonds!",
    "Ktoś tu pachnie nowym graczem...",
    "Czy masz ze sobą wiadro wody?",
    "Pij mleko, będziesz odporny na klątwy!",
    "Zbudujmy razem coś wspaniałego!",
    "Wciśnij Alt + F4 po darmowe diamenty! (Żart)",
    "Żaba na ramieniu to +10 do charyzmy!",
    "Wczytywanie protokołu przytulania...",
    "Nyanko czuwa, gdy Ty śpisz!",
    "Nie handluj z osadnikami w nocy!",
    "Głowa do góry, jutro też jest dzień na kopanie!",
    "Zawsze miej przy sobie łóżko!",
    "Netheryt czeka na najdzielniejszych!",
    "Czy Twój kilof ma Wydajność V?",
    "Koty odstraszają Creepery, a Nyanko wszystkich twardzieli!",
    "Nie patrz Endermanowi w oczy!",
    "Słodki różowy świat Nyanko!",
    "Wypij miksturę szybkości i biegnij przed siebie!",
    "Minecraft to nie gra, to styl życia!",
    "Wciśnij gotowość i czekaj na cud!",
    "Sędziowie już ostrzą swoje topory... 🪓",
    "Bądź miły dla żabek, a one będą miłe dla Ciebie!",
    "Muzyka z Minecrafta leczy duszę!",
    "Czy znasz przepis na ciasto?",
    "Złoty arbuz leczy rany!",
    "Złap je wszystkie... a nie, to nie ta gra!",
    "Nyanko potrafi latać (w kodzie)!",
    "Szczęście III na Twoim kilofie życia!",
    "Nie wchodź do portalu bez zbroi!",
    "Weryfikacja trwa... zachowaj spokój!",
    "Nasze żabki nie gryzą... zazwyczaj!",
    "Zbuduj bazę zebranych wspomnień!",
    "Czy słyszysz ten syczący dźwięk za sobą? 💥",
    "Odpocznij przy ognisku przed podróżą!",
    "Zjedz złote jabłko na drogę!",
    "Najlepsze przygody zaczynają się od weryfikacji!",
    "Czy masz już swojego oswojonego wilka?",
    "Zawsze sprawdzaj co jest za rogiem!",
    "Nyanko zatwierdza ten splash art!",
    "Witaj w naszej małej pikselowej rodzinie!"
]

ABSURD_QUESTIONS = [
    "Gdybyś był zupą, jaką zupą byś był i dlaczego?",
    "Czy pizza z ananasem to przestępstwo wojenne, czy kulinarne arcydzieło?",
    "Gdyby żaby potrafiły latać, to czy nosiłyby spodnie na przednich, czy na tylnych łapach?",
    "Wyjaśnij teorię względności Einsteina za pomocą trzech słów i ziemniaka.",
    "Ile żelek jesteś w stanie zmieścić w buzi na raz? (Odpowiedz szczerze)",
    "Gdybyś musiał stoczyć walkę z jedną kaczką wielkości konia lub stoma końmi wielkości kaczek, co byś wybrał?",
    "Jaki jest najlepszy sposób na przetrwanie ataku wściekłej żaby?",
    "Gdyby Twój komputer mógł mówić, jaka byłaby jego pierwsza skarga na Ciebie?",
    "Czy uważasz, że woda jest mokra? Uzasadnij swoją wypowiedź w jednym zdaniu.",
    "Jakie zaklęcie z Minecrafta najlepiej opisuje Twoją osobowość?",
    "Gdybyś mógł zamienić się w dowolny blok w Minecrafcie, czym byś był i dlaczego właśnie blokiem szlamu?",
    "Który klawisz na Twojej klawiaturze jest najbardziej niedoceniany?",
    "Gdybyś wygrał milion dolarów, ale musiałbyś je wydać w 24 godziny na rzeczy zaczynające się na literę 'Ż', co byś kupił?",
    "Jak brzmi Twój ulubiony dźwięk w grach komputerowych?",
    "Gdyby kolory miały smaki, jaki smak miałby różowy kolor bota Nyanko?",
    "Gdybyś mógł ptodróżować w czasie, ale tylko po to, by przesunąć jeden dowolny przedmiot o 5 centymetrów w lewo w przeszłości, co byś wybrał?",
    "Jakie jest najbardziej bezużyteczne supermocarstwo, jakie potrafisz wymyślić?",
    "Gdybyś był osadnikiem (villagerem) w Minecrafcie, co oferowałbyś za jeden szmaragd?",
    "Czy spanie w skarpetkach to przejaw geniuszu, czy czysty chaos?",
    "Jak wytłumaczyłbyś pojęcie 'internet' człowiekowi z XV wieku w 10 sekund?",
    "Gdybyś musiał do końca życia jeść tylko jeden rodzaj jedzenia o kolorze zielonym, co by to było?",
    "Jaka jest najbardziej absurdalna plotka, jaką kiedykolwiek o sobie słyszałeś (lub sam wymyśliłeś)?",
    "Gdybyś mógł kontrolować umysł jednej dowolnej żaby na świecie, co byś jej kazał zrobić?",
    "Czy potrafisz napisać wiersz o Nyanko w 4 linijkach?",
    "Jaki byłby Twój okrzyk bojowy, gdybyś musiał zaatakować zamek zbudowany z klocków LEGO?"
]

def track_verification_stat(stat_name):
    """Śledzi globalne statystyki weryfikacji w profilu bazy danych z fallbackiem RAM."""
    stats = get_profile_data("global_verification_stats")
    
    # Inicjalizacja, jeśli to pierwszy raz
    if "stats_initialized" not in stats:
        stats = {
            "stats_initialized": True,
            "verified": 0,
            "kicked": 0,
            "banned": 0,
            "coin_heads": 0,
            "coin_tails": 0,
            "roulette_live": 0,
            "roulette_dead": 0,
            "kps_played": 0,
            "kps_wins": 0,
            "kps_losses": 0,
            "quiz_wins": 0,
            "quiz_losses": 0,
            "scans_run": 0
        }
    
    # Inkrementacja statystyki
    stats[stat_name] = stats.get(stat_name, 0) + 1
    
    # Zapisz spowrotem
    for k, v in stats.items():
        update_profile("global_verification_stats", k, v)

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
ROLES = {
    "gender": ["—͟͞👧・Niewiasta", "—͟͞👦・Jegomość", "—͟͞💗・Demigirl", "—͟͞💙・Demiboy", "—͟͞👤・Helikopter Bojowy"],
    "age": ["16+", "18+", "22+", "25+", "30+", "35+"],
    "color": ["Czarny", "Krwisty", "Czerwony", "Brązowy", "Pomarańczowy", "Żółty", "Łososiowy", "Limonkowy", "Zielony", "Błękitny", "Niebieski", "Fioletowy", "Różowy", "Biały"],
    "ping": ["Gaduła", "Defibrylator Czatu", "Giejmer"],
    "orientation": [v["name"] for v in ORIENTATIONS.values()]
}

pending_roles = {}

async def refresh_member_flags(member, profile_data=None):
    """Odświeża pseudonim członka dodając flagi płci i orientacji z profilu"""
    if profile_data is None:
        profile_data = get_profile_data(member.id)
    
    gender = profile_data.get("gender", "")
    orientation = profile_data.get("orientation", "")
    
    # Znajdź flagę płci
    gender_flag = ""
    for g in GENDERS.values():
        if g["name"] == gender or (g["role_name"] and g["role_name"] == gender) or (g["role_name"] and g["role_name"] in gender):
            gender_flag = g.get("flag", "")
            break
            
    # Znajdź flagę orientacji
    orient_flag = ""
    if orientation:
        clean_orient = orientation.split()[-1] if len(orientation.split()) > 1 else orientation
        for v in ORIENTATIONS.values():
            if v["name"] == clean_orient or v["name"] in orientation:
                orient_flag = v.get("flag", "")
                break
                
    # Zbierz wszystkie znane flagi do usunięcia z obecnego pseudonimu
    flags_to_strip = set()
    for v in ORIENTATIONS.values():
        if "flag" in v:
            flags_to_strip.add(v["flag"])
    for g in GENDERS.values():
        if "flag" in g:
            flags_to_strip.add(g["flag"])
            
    # Usuń stare flagi z pseudonimu
    nick = member.display_name
    for flag in flags_to_strip:
        nick = nick.replace(f"{flag} ", "").replace(flag, "")
        nick = nick.replace(flag, "")
    nick = nick.strip()
    
    if len(nick) == 0:
        nick = member.name
        
    # Połącz nowe flagi
    flags_str = ""
    if gender_flag:
        flags_str += gender_flag
    if orient_flag:
        flags_str += orient_flag
        
    new_nick = f"{flags_str} {nick}" if flags_str else nick
    if len(new_nick) > 32:
        new_nick = new_nick[:32]
        
    try:
        await member.edit(nick=new_nick)
    except Exception as e:
        print(f"Błąd zmiany pseudonimu dla {member.name}: {e}")

async def execute_verification(bot, guild, member, channel, balance_amount, welcome_description, pogadanki_extra="", interaction=None):
    # 1. Pomiary ról do dodania
    roles_to_add = []
    roles_added_names = []
    
    # Rola Bilecik
    verified_role = discord.utils.get(guild.roles, name="—͟͞✅・Bilecik")
    if not verified_role:
        try:
            verified_role = await guild.create_role(name="—͟͞✅・Bilecik", color=discord.Color.from_rgb(255, 182, 193))
        except Exception as e:
            print(f"Błąd tworzenia roli Bilecik: {e}")
    if verified_role:
        roles_to_add.append(verified_role)
        roles_added_names.append("—͟͞✅・Bilecik")
        
    # Rola Żaby
    zaba_role = discord.utils.get(guild.roles, name="🐸 • Żaby")
    if zaba_role:
        roles_to_add.append(zaba_role)
        roles_added_names.append("🐸 • Żaby")
        
    # Role oczekujące wybrane w kreatorze profilu
    user_pending_ids = pending_roles.get(member.id, [])
    for rid in user_pending_ids:
        r = guild.get_role(rid)
        if r and r not in roles_to_add:
            roles_to_add.append(r)
            roles_added_names.append(r.name)
            
    # Nadanie ról (zbiorczo, z fallbackiem)
    if roles_to_add:
        try:
            await member.add_roles(*roles_to_add)
        except discord.Forbidden:
            for r in roles_to_add:
                try:
                    await member.add_roles(r)
                except:
                    pass
        except Exception as e:
            print(f"Błąd dodawania ról: {e}")
            
    # Czyszczenie listy oczekujących ról
    pending_roles[member.id] = []
    
    # 2. Aktualizacja pseudonimu o flagi
    profile = get_profile_data(member.id)
    await refresh_member_flags(member, profile)
                
    # 3. Zapisanie ekonomii i śledzenie statystyk
    update_data(member.id, "balance", balance_amount, "add")
    track_verification_stat("verified")
    
    # 4. Wysłanie uroczej wiadomości powitalnej na kanale weryfikacyjnym
    formatted_roles = ", ".join([f"**{r}**" for r in roles_added_names])
    desc = welcome_description.replace("{roles}", formatted_roles)
    
    welcome_embed = discord.Embed(
        title="🎉 POMYŚLNIE ZWERYFIKOWANO! 🎉",
        description=desc,
        color=KAWAII_PINK
    )
    welcome_embed.set_footer(text="Życzymy miłej zabawy! 💕")
    
    if interaction:
        try:
            await interaction.response.send_message(embed=welcome_embed)
        except Exception:
            try:
                await channel.send(embed=welcome_embed)
            except:
                pass
    else:
        try:
            await channel.send(embed=welcome_embed)
        except:
            pass
            
    # 5. Wysłanie powitania na kanale pogadanki / ogólny
    general = discord.utils.get(guild.text_channels, name="💬・pogadanki") or discord.utils.get(guild.text_channels, name="ogólny")
    if general:
        pogadanki_desc = f"Witamy **{member.mention}**! (≧◡≦) ♡\n Cieszymy się że połączyłeś się z nami! 💖"
        if pogadanki_extra:
            pogadanki_desc += f"\n*{pogadanki_extra}*"
        embed = discord.Embed(description=pogadanki_desc, color=KAWAII_PINK)
        b = profile.get("bio", "Nowy gracz na streecie!")
        embed.add_field(name="Zostawił takie bio:", value=b)
        try:
            await general.send(embed=embed)
        except Exception as e:
            print(f"Błąd wysyłania powitania na ogólny: {e}")
            
    # 6. Automatyczne usunięcie kanału weryfikacyjnego po 10 sekundach
    await asyncio.sleep(10)
    try:
        await channel.delete()
    except Exception as e:
        print(f"Błąd usuwania kanału: {e}")

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
        update_profile(interaction.user.id, "bio", self.bio.value)
        await interaction.response.defer(thinking=False)

# --- PANEL WYBORU KOLORU ---
class ColorSelectView(View):
    def __init__(self, bot, member, is_setup=False):
        super().__init__(timeout=None)
        self.bot = bot
        self.member = member
        self.is_setup = is_setup

    @discord.ui.select(placeholder="Wybierz swój kolor!", min_values=1, max_values=1, custom_id="color_select_menu", options=[
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
            for role_name in ROLES["color"]:
                r = discord.utils.get(guild.roles, name=role_name)
                if r and r in user.roles:
                    try: await user.remove_roles(r)
                    except: pass
            
            r = discord.utils.get(guild.roles, name=chosen_value)
            if r:
                try: 
                    await user.add_roles(r)
                    await interaction.response.defer(thinking=False)
                except:
                    await interaction.response.send_message(f"❌ Brak uprawnień bota do nadania roli **{chosen_value}**.", ephemeral=True)
            else:
                await interaction.response.send_message(f"❌ Nie znaleziono roli **{chosen_value}** na serwerze.", ephemeral=True)
        else:
            r = discord.utils.get(guild.roles, name=chosen_value)
            role_id = r.id if r else None
            
            if role_id:
                cat_role_ids = [discord.utils.get(guild.roles, name=rn).id for rn in ROLES["color"] if discord.utils.get(guild.roles, name=rn)]
                pending_roles[user.id] = [rid for rid in pending_roles[user.id] if rid not in cat_role_ids]
                pending_roles[user.id].append(role_id)
                
                await interaction.response.defer(thinking=False)
            else:
                await interaction.response.send_message(f"❌ Nie znaleziono roli **{chosen_value}** na serwerze.", ephemeral=True)

# --- PANEL WYBORU RÓL (SELECT MENUS) ---
class RoleSelectView(View):
    def __init__(self, bot, member, is_setup=False):
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
        
        current_data = get_profile_data(user.id)
        
        chosen_values_str = ", ".join(select.values)
        if category_name == "orientation":
            formatted_vals = []
            for val in select.values:
                flag = next((v["flag"] for v in ORIENTATIONS.values() if v["name"] == val), "")
                formatted_vals.append(f"{flag} {val}" if flag else val)
            chosen_values_str = ", ".join(formatted_vals)
            
        update_profile(user.id, category_name, chosen_values_str)
        
        if self.is_setup:
            for role_name in ROLES[category_name]:
                r = discord.utils.get(guild.roles, name=role_name)
                if r and r in user.roles:
                    try: await user.remove_roles(r)
                    except: pass
            
            added_roles = []
            for role_name in select.values:
                r = discord.utils.get(guild.roles, name=role_name)
                if not r:
                    try:
                        role_color = discord.Color.default()
                        if category_name == "orientation":
                            color_val = next((v["color"] for v in ORIENTATIONS.values() if v["name"] == role_name), None)
                            if color_val is not None: role_color = discord.Color(color_val)
                        r = await guild.create_role(name=role_name, reason="Auto-tworzenie roli profilowej", color=role_color)
                    except Exception as e:
                        print(f"Nie udało się stworzyć roli {role_name}: {e}")
                if r:
                    try: await user.add_roles(r)
                    except: pass
                    added_roles.append(r.name)
            
            await interaction.response.defer(thinking=False)
        else:
            roles_to_add = []
            for role_name in select.values:
                r = discord.utils.get(guild.roles, name=role_name)
                if not r:
                    try:
                        role_color = discord.Color.default()
                        if category_name == "orientation":
                            color_val = next((v["color"] for v in ORIENTATIONS.values() if v["name"] == role_name), None)
                            if color_val is not None: role_color = discord.Color(color_val)
                        r = await guild.create_role(name=role_name, reason="Auto-tworzenie roli profilowej", color=role_color)
                    except Exception as e:
                        print(f"Nie udało się stworzyć roli {role_name}: {e}")
                if r: roles_to_add.append(r.id)
            
            cat_role_ids = [discord.utils.get(guild.roles, name=rn).id for rn in ROLES[category_name] if discord.utils.get(guild.roles, name=rn)]
            pending_roles[user.id] = [rid for rid in pending_roles[user.id] if rid not in cat_role_ids]
            pending_roles[user.id].extend(roles_to_add)
            
            await interaction.response.defer(thinking=False)

    @discord.ui.select(placeholder="Wybierz płeć!", min_values=1, max_values=1, custom_id="role_select_gender", options=[
        discord.SelectOption(label="—͟͞👧・Niewiasta", emoji="👱‍♀️"),
        discord.SelectOption(label="—͟͞👦・Jegomość", emoji="👱‍♂️"),
        discord.SelectOption(label="—͟͞💗・Demigirl", emoji="💗"),
        discord.SelectOption(label="—͟͞💙・Demiboy", emoji="💙"),
        discord.SelectOption(label="—͟͞👤・Helikopter Bojowy", emoji="🚁")
    ])
    async def gender_select(self, interaction: discord.Interaction, select: Select):
        await self.handle_roles(interaction, select, "gender")
        if self.is_setup:
            await refresh_member_flags(interaction.user)

    @discord.ui.select(placeholder="Wybierz wiek!", min_values=1, max_values=1, custom_id="role_select_age", options=[
        discord.SelectOption(label="16+", emoji="1️⃣"),
        discord.SelectOption(label="18+", emoji="2️⃣"),
        discord.SelectOption(label="22+", emoji="3️⃣"),
        discord.SelectOption(label="25+", emoji="4️⃣"),
        discord.SelectOption(label="30+", emoji="5️⃣"),
        discord.SelectOption(label="35+", emoji="6️⃣")
    ])
    async def age_select(self, interaction: discord.Interaction, select: Select):
         await self.handle_roles(interaction, select, "age")

    @discord.ui.select(placeholder="Wybierz pingi!", min_values=1, max_values=3, custom_id="role_select_ping", options=[
        discord.SelectOption(label="Gaduła", emoji="🗣️"),
        discord.SelectOption(label="Defibrylator Czatu", emoji="⚡"),
        discord.SelectOption(label="Giejmer", emoji="🎮")
    ])
    async def ping_select(self, interaction: discord.Interaction, select: Select):
         await self.handle_roles(interaction, select, "ping")

    @discord.ui.select(placeholder="Wybierz tożsamość / flagę!", min_values=1, max_values=1, custom_id="role_select_orient", options=[
        discord.SelectOption(label=v["name"], emoji=v.get("emoji", "🏳️‍🌈"), value=v["name"]) for v in list(ORIENTATIONS.values())[:25]
    ])
    async def orient_select(self, interaction: discord.Interaction, select: Select):
        await self.handle_roles(interaction, select, "orientation")
        if self.is_setup:
            await refresh_member_flags(interaction.user)

    @discord.ui.button(label="✏️ NAPISZ BIO", style=discord.ButtonStyle.blurple, emoji="📖", row=4, custom_id="role_select_bio_btn")
    async def bio_button(self, interaction: discord.Interaction, button: Button):
        if self.member and interaction.user.id != self.member.id:
            return await interaction.response.send_message("⛔ Ty nie piszesz tu bio!", ephemeral=True)
        await interaction.response.send_modal(BioModal())

    @discord.ui.button(label="🎨 WYBIERZ KOLOR", style=discord.ButtonStyle.secondary, emoji="🎨", row=4, custom_id="role_select_color_btn")
    async def color_button(self, interaction: discord.Interaction, button: Button):
        if self.member and interaction.user.id != self.member.id:
            return await interaction.response.send_message("⛔ Ty nie wybierasz tu koloru!", ephemeral=True)
        view = ColorSelectView(self.bot, interaction.user, is_setup=self.is_setup)
        await interaction.response.send_message("Wybierz swój kolor z listy poniżej:", view=view, ephemeral=True)


# --- WIDOK Z MENU ROZWIJANYMI NA WERYFIKACJI ---
class VerificationProfileSelectView(View):
    def __init__(self, bot, member):
        super().__init__(timeout=None)
        self.bot = bot
        self.member = member
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
        
        chosen_values_str = ", ".join(select.values)
        if category_name == "orientation":
            formatted_vals = []
            for val in select.values:
                flag = next((v["flag"] for v in ORIENTATIONS.values() if v["name"] == val), "")
                formatted_vals.append(f"{flag} {val}" if flag else val)
            chosen_values_str = ", ".join(formatted_vals)
            
        update_profile(user.id, category_name, chosen_values_str)
        
        roles_to_add = []
        for role_name in select.values:
            r = discord.utils.get(guild.roles, name=role_name)
            if r: roles_to_add.append(r.id)
        
        cat_role_ids = [discord.utils.get(guild.roles, name=rn).id for rn in ROLES[category_name] if discord.utils.get(guild.roles, name=rn)]
        pending_roles[user.id] = [rid for rid in pending_roles[user.id] if rid not in cat_role_ids]
        pending_roles[user.id].extend(roles_to_add)
        
        await interaction.response.defer(thinking=False)

    @discord.ui.select(placeholder="Wybierz płeć!", min_values=1, max_values=1, options=[
        discord.SelectOption(label="—͟͞👧・Niewiasta", emoji="👱‍♀️"),
        discord.SelectOption(label="—͟͞👦・Jegomość", emoji="👱‍♂️"),
        discord.SelectOption(label="—͟͞💗・Demigirl", emoji="💗"),
        discord.SelectOption(label="—͟͞💙・Demiboy", emoji="💙"),
        discord.SelectOption(label="—͟͞👤・Helikopter Bojowy", emoji="🚁")
    ], row=0)
    async def gender_select(self, interaction: discord.Interaction, select: Select):
        await self.handle_roles(interaction, select, "gender")

    @discord.ui.select(placeholder="Wybierz wiek!", min_values=1, max_values=1, options=[
        discord.SelectOption(label="16+", emoji="1️⃣"),
        discord.SelectOption(label="18+", emoji="2️⃣"),
        discord.SelectOption(label="22+", emoji="3️⃣"),
        discord.SelectOption(label="25+", emoji="4️⃣"),
        discord.SelectOption(label="30+", emoji="5️⃣"),
        discord.SelectOption(label="35+", emoji="6️⃣")
    ], row=1)
    async def age_select(self, interaction: discord.Interaction, select: Select):
         await self.handle_roles(interaction, select, "age")

    @discord.ui.select(placeholder="Wybierz pingi!", min_values=1, max_values=3, options=[
        discord.SelectOption(label="Gaduła", emoji="🗣️"),
        discord.SelectOption(label="Defibrylator Czatu", emoji="⚡"),
        discord.SelectOption(label="Giejmer", emoji="🎮")
    ], row=2)
    async def ping_select(self, interaction: discord.Interaction, select: Select):
         await self.handle_roles(interaction, select, "ping")

    @discord.ui.select(placeholder="Wybierz tożsamość / flagę!", min_values=1, max_values=1, options=[
        discord.SelectOption(label=v["name"], emoji=v.get("emoji", "🏳️‍🌈"), value=v["name"]) for v in list(ORIENTATIONS.values())[:25]
    ], row=3)
    async def orient_select(self, interaction: discord.Interaction, select: Select):
        await self.handle_roles(interaction, select, "orientation")

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
    ], row=4)
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
        
        r = discord.utils.get(guild.roles, name=chosen_value)
        role_id = r.id if r else None
        
        if role_id:
            cat_role_ids = [discord.utils.get(guild.roles, name=rn).id for rn in ROLES["color"] if discord.utils.get(guild.roles, name=rn)]
            pending_roles[user.id] = [rid for rid in pending_roles[user.id] if rid not in cat_role_ids]
            pending_roles[user.id].append(role_id)
            
            await interaction.response.defer(thinking=False)
        else:
            await interaction.response.send_message(f"❌ Nie znaleziono roli **{chosen_value}** na serwerze.", ephemeral=True)


# --- PANEL WERYFIKACYJNY DLA NOWEGO UŻYTKOWNIKA ---
class VerificationWelcomeView(View):
    def __init__(self, bot, member, verified_role, channel):
        super().__init__(timeout=None)
        self.bot = bot
        self.member = member
        self.verified_role = verified_role
        self.channel = channel
        self.profile_msg = None

    @discord.ui.button(label="📝 Napisz Bio", style=discord.ButtonStyle.blurple, emoji="✍️", row=0)
    async def bio_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.member.id:
            return await interaction.response.send_message("⛔ Ty nie piszesz tu bio!", ephemeral=True)
        await interaction.response.send_modal(BioModal())

    @discord.ui.button(label="🟢 Oznacz Gotowość", style=discord.ButtonStyle.green, emoji="🟢", row=0)
    async def ready_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.member.id:
            return await interaction.response.send_message("❌ Tylko osoba weryfikowana może oznaczyć swoją gotowość!", ephemeral=True)

        profile = get_profile_data(self.member.id)
        bio = profile.get("bio", "").strip()

        if not bio or bio == "Pusto..." or len(bio) < 5:
            return await interaction.response.send_message(
                "❌ **Nie uzupełniłeś jeszcze swojego bio!**\n"
                "Kliknij przycisk **`📝 Napisz Bio`** powyżej i opisz siebie przed oznaczeniem gotowości.", 
                ephemeral=True
            )

        for item in self.children:
            item.disabled = True

        if self.profile_msg:
            try:
                await self.profile_msg.edit(view=None)
            except Exception as e:
                print(f"Błąd usuwania widoku z komunikatu profilu: {e}")

        # Animacja ładowania
        loading_embed = discord.Embed(
            title="🎮 INICJOWANIE WERYFIKACJI NYANKO...",
            description="⏳ Przygotowywanie plików gry...\n`[░░░░░░░░░░] 0%`",
            color=KAWAII_PINK
        )
        await interaction.response.edit_message(embed=loading_embed, view=self)
        await asyncio.sleep(1.2)
        
        loading_embed.description = "⏳ Wczytywanie chunków i biomów...\n`[■■■░░░░░░░] 30%`"
        await interaction.message.edit(embed=loading_embed)
        await asyncio.sleep(1.2)
        
        loading_embed.description = "⏳ Sprawdzanie obecności Creeperów...\n`[■■■■■■░░░░] 60%`"
        await interaction.message.edit(embed=loading_embed)
        await asyncio.sleep(1.2)
        
        loading_embed.description = "⏳ Karmienie głodnych żabek na mokradłach...\n`[■■■■■■■■■░] 90%`"
        await interaction.message.edit(embed=loading_embed)
        await asyncio.sleep(1.2)
        
        splash_text = random.choice(MINECRAFT_SPLASHES)
        loading_embed.title = "✅ WERYFIKACJA INICJOWANA POMYŚLNIE!"
        loading_embed.description = (
            "**`[■■■■■■■■■■] 100%`**\n\n"
            f"💛 ***{splash_text}*** 💛"
        )
        await interaction.message.edit(embed=loading_embed)
        await asyncio.sleep(1.0)

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

        decision_view = VerifyDecisionView(self.bot, self.member, self.verified_role, self.channel)
        
        await self.channel.send(
            content=f"🔔 **Administracja / Sędziowie** - {self.member.mention} jest gotowy!", 
            embed=embed_admin, 
            view=decision_view
        )

    @discord.ui.button(label="Szybki Kick", style=discord.ButtonStyle.danger, emoji="👢", row=1)
    async def quick_kick(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.kick_members and interaction.user.name.lower() not in ["≽^borysiaczekuwu^≼", "borysiaczekuwu"]:
            return await interaction.response.send_message("⛔ Brak uprawnień do wyrzucania!", ephemeral=True)

        guild = interaction.guild
        try:
            member = await guild.fetch_member(self.member.id)
        except discord.NotFound:
            member = None

        if not member:
            return await interaction.response.send_message("❌ Błąd: Użytkownik opuścił serwer.", ephemeral=True)

        try:
            await interaction.response.send_message(f"👢 Szybko wyrzucono {member.mention}...", ephemeral=True)
            await member.kick(reason=f"Szybki kick przy weryfikacji przez {interaction.user.name}")
            
            track_verification_stat("kicked")

            embed = discord.Embed(title="👋 WYRZUCONO (SZYBKA DECYZJA)!", description=f"**{member.name}** został szybko wyrzucony przez {interaction.user.mention}.", color=discord.Color.orange())
            embed.set_image(url=random.choice(GIFS_KICK))
            await self.channel.send(embed=embed)
            await asyncio.sleep(10)
            await self.channel.delete()
        except Exception as e:
            await self.channel.send(f"❌ Nie udało się: {e}")

    @discord.ui.button(label="Szybki Ban", style=discord.ButtonStyle.danger, emoji="🔨", row=1)
    async def quick_ban(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.ban_members and interaction.user.name.lower() not in ["≽^borysiaczekuwu^≼", "borysiaczekuwu"]:
            return await interaction.response.send_message("⛔ Brak uprawnień do banowania!", ephemeral=True)

        guild = interaction.guild
        try:
            member = await guild.fetch_member(self.member.id)
        except discord.NotFound:
            member = None

        if not member:
            return await interaction.response.send_message("❌ Błąd: Użytkownik opuścił serwer.", ephemeral=True)

        try:
            await interaction.response.send_message(f"🔨 Szybko zbanowano {member.mention}...", ephemeral=True)
            await member.ban(reason=f"Szybki ban przy weryfikacji przez {interaction.user.name}")
            
            track_verification_stat("banned")

            embed = discord.Embed(title="🔨 ZBANOWANO (SZYBKA DECYZJA)!", description=f"**{member.name}** został szybko zbanowany przez {interaction.user.mention}.", color=KAWAII_RED)
            embed.set_image(url=random.choice(GIFS_BAN))
            await self.channel.send(embed=embed)
            await asyncio.sleep(10)
            await self.channel.delete()
        except Exception as e:
            await self.channel.send(f"❌ Nie udało się: {e}")


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
        is_admin = interaction.user.guild_permissions.manage_roles or interaction.user.guild_permissions.administrator or interaction.user.name.lower() in ["≽^borysiaczekuwu^≼", "borysiaczekuwu"]
        if not is_admin:
            await interaction.response.send_message("⛔ Czekamy na administrację!", ephemeral=True)
            return

        guild = interaction.guild
        if not guild:
            return await interaction.response.send_message("❌ Błąd: Nie można odnaleźć serwera.", ephemeral=True)

        try:
            member = await guild.fetch_member(self.member.id)
        except discord.NotFound:
            member = None

        if not member:
            return await interaction.response.send_message("❌ Błąd: Użytkownik opuścił serwer.", ephemeral=True)

        welcome_desc = (
            f"Serdecznie witamy i zapraszamy na serwer, {member.mention}! 🥰\n\n"
            f"✨ Zostałeś pomyślnie zweryfikowany przez administrację!\n"
            f"🌸 Nadano Ci role: {{roles}}\n"
            f"💰 Otrzymujesz na start **100 monet** do ekonomii!\n\n"
            f"**Ten kanał weryfikacyjny zostanie automatycznie usunięty za 10 sekund...** ⏳"
        )
        
        await execute_verification(
            bot=self.bot,
            guild=guild,
            member=member,
            channel=self.channel,
            balance_amount=100,
            welcome_description=welcome_desc,
            pogadanki_extra="",
            interaction=interaction
        )

    @discord.ui.button(label="👋 WYRZUĆ", style=discord.ButtonStyle.danger, emoji="👢")
    async def kick_button(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.kick_members and interaction.user.name.lower() not in ["≽^borysiaczekuwu^≼", "borysiaczekuwu"]:
            return await interaction.response.send_message("⛔ Brak uprawnień do wyrzucania!", ephemeral=True)

        guild = interaction.guild
        try:
            member = await guild.fetch_member(self.member.id)
        except discord.NotFound:
            member = None

        if not member:
            return await interaction.response.send_message("❌ Błąd: Użytkownik opuścił serwer.", ephemeral=True)

        try:
            await interaction.response.send_message(f"👢 Wyrzucono {member.mention}...", ephemeral=True)
            await member.kick(reason=f"Wyrzucono przy weryfikacji przez {interaction.user.name}")
            
            track_verification_stat("kicked")

            embed = discord.Embed(title="👋 WYRZUCONO!", description=f"**{member.name}** nie przeszedł weryfikacji.", color=discord.Color.orange())
            embed.set_image(url=random.choice(GIFS_KICK))
            await self.channel.send(embed=embed)
            await asyncio.sleep(10)
            await self.channel.delete()
        except Exception as e:
            await self.channel.send(f"❌ Nie udało się: {e}")

    @discord.ui.button(label="🔨 ZBANUJ", style=discord.ButtonStyle.danger, emoji="🔨")
    async def ban_button(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.ban_members and interaction.user.name.lower() not in ["≽^borysiaczekuwu^≼", "borysiaczekuwu"]:
            return await interaction.response.send_message("⛔ Brak uprawnień do banowania!", ephemeral=True)

        guild = interaction.guild
        try:
            member = await guild.fetch_member(self.member.id)
        except discord.NotFound:
            member = None

        if not member:
            return await interaction.response.send_message("❌ Błąd: Użytkownik opuścił serwer.", ephemeral=True)

        try:
            await interaction.response.send_message(f"🔨 Zbanowano {member.mention}...", ephemeral=True)
            await member.ban(reason=f"Zbanowano przy weryfikacji przez {interaction.user.name}")
            
            track_verification_stat("banned")

            embed = discord.Embed(title="🔨 ZBANOWANO!", description=f"**{member.name}** nie przeszedł weryfikacji.", color=KAWAII_RED)
            embed.set_image(url=random.choice(GIFS_BAN))
            await self.channel.send(embed=embed)
            await asyncio.sleep(10)
            await self.channel.delete()
        except Exception as e:
            await self.channel.send(f"❌ Nie udało się: {e}")


# --- WIDOKI DLA NOWYCH INTERAKTYWNYCH FUNKCJI ---

QUIZ_QUESTIONS = [
    {
        "question": "Ile nóg ma typowa żaba po zjedzeniu trzech much?",
        "options": ["4 (Zawsze ma 4!)", "5 (Ta piąta wyrasta z nadmiaru uroczości)", "Żaby nie liczą nóg, one po prostu skaczą"],
        "correct_idx": 0,
        "correct_letter": "A"
    },
    {
        "question": "Co robi Nyanko, gdy admin nie patrzy?",
        "options": ["Śpi w najlepsze", "Planuje przejęcie władzy nad światem 👑", "Koduje nową wersję weryfikacji w Pythonie"],
        "correct_idx": 1,
        "correct_letter": "B"
    },
    {
        "question": "Jeśli w pokoju jest 5 Creeperów i 1 kot, ile Creeperów wybuchnie?",
        "options": ["0 (Kot je skutecznie odstraszy! 🐈)", "5 (Wszystkie z radości)", "Kot wybuchnie pierwszy"],
        "correct_idx": 0,
        "correct_letter": "A"
    },
    {
        "question": "Jak najlepiej przywitać żabę na serwerze?",
        "options": ["Powiedzieć 'Dzień dobry'", "Głośno zakumkać 'KUM! 🐸'", "Dać jej muchę w prezencie"],
        "correct_idx": 1,
        "correct_letter": "B"
    },
    {
        "question": "Ile złota potrzeba, by przekupić Piglina w Netherze?",
        "options": ["Jeden sztabek złota 🪙", "Cały blok złota", "Pigliny wolą różowy beton"],
        "correct_idx": 0,
        "correct_letter": "A"
    },
    {
        "question": "Co się stanie, gdy wciśniesz Alt + F4 podczas gry?",
        "options": ["Gra się zapisze i wyłączy", "Otrzymasz darmowe diamenty", "Doświadczysz nagłego powrotu do pulpitu 💻"],
        "correct_idx": 2,
        "correct_letter": "C"
    },
    {
        "question": "Jaki jest ulubiony napój bota Nyanko?",
        "options": ["Matcha latte 🍵", "Truskawkowe mleczko (Strawberry Milk) 🍓", "Woda z bagna"],
        "correct_idx": 1,
        "correct_letter": "B"
    },
    {
        "question": "Gdzie mieszka Herobrine?",
        "options": ["W Twojej szafie", "Nigdzie, to tylko legenda... a może? 👁️‍🗨️", "W kwaterze głównej Mojangu"],
        "correct_idx": 1,
        "correct_letter": "B"
    },
    {
        "question": "Co jest silniejsze w Minecrafcie?",
        "options": ["Diamentowy miecz", "Netherytowy miecz ⚔️", "Drewniana motyka z zaklęciem niezniszczalności"],
        "correct_idx": 1,
        "correct_letter": "B"
    },
    {
        "question": "Jaki kolor ma najrzadsza owca w Minecrafcie?",
        "options": ["Różowy 🌸", "Niebieski", "Tęczowy"],
        "correct_idx": 0,
        "correct_letter": "A"
    },
    {
        "question": "Ile żelek zmieści się w buzi przeciętnego gracza?",
        "options": ["Dokładnie 42", "O jedną więcej niż myślisz 🍬", "Żadna, wszystkie zostaną zjedzone od razu"],
        "correct_idx": 1,
        "correct_letter": "B"
    },
    {
        "question": "Co robi gracz, gdy widzi wodę w Minecrafcie spadając z 100 bloków?",
        "options": ["Celuje w nią, próbując zrobić MLG 💧", "Zamyka oczy i się modli", "Pisze skargę na serwer"],
        "correct_idx": 0,
        "correct_letter": "A"
    },
    {
        "question": "Która godzina jest najlepsza na weryfikację?",
        "options": ["Każda, o ile sędzia ma kawę ☕", "Dokładnie o północy", "4:20 rano"],
        "correct_idx": 0,
        "correct_letter": "A"
    },
    {
        "question": "Dlaczego żaby są maskotką tego serwera?",
        "options": ["Bo są urocze i głośno kumkają 🐸", "Bo admin boi się innych zwierząt", "To był przypadek w kodzie"],
        "correct_idx": 0,
        "correct_letter": "A"
    },
    {
        "question": "Co się stanie, gdy uderzysz zombie-pigmana?",
        "options": ["Przeprosi Cię i da złoto", "Cała horda ruszy na Ciebie z mieczami ⚔️", "Zamieni się w uroczą świnkę"],
        "correct_idx": 1,
        "correct_letter": "B"
    }
]

class KPSTieView(View):
    def __init__(self, bot, admin, member, verified_role, channel):
        super().__init__(timeout=120)
        self.bot = bot
        self.admin = admin
        self.member = member
        self.verified_role = verified_role
        self.channel = channel

    @discord.ui.button(label="🔄 Zagraj Ponownie", style=discord.ButtonStyle.blurple, emoji="🔄")
    async def retry_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.admin.id and interaction.user.id != self.member.id:
            return await interaction.response.send_message("❌ Nie bierzesz udziału w tym pojedynku!", ephemeral=True)

        view = KPSView(self.bot, self.admin, self.member, self.verified_role, self.channel)
        embed = discord.Embed(
            title="⚔️ POJEDYNEK KAMIEŃ, PAPIER, NOŻYCE ⚔️",
            description=f"Rewanż! Sędzia {self.admin.mention} i kandydat {self.member.mention} walczą o wszystko!\n\n"
                        f"👑 **Sędzia:** ⏳ Czeka na wybór...\n"
                        f"👤 **Kandydat:** ⏳ Czeka na wybór...",
            color=KAWAII_GOLD
        )
        await interaction.response.edit_message(embed=embed, view=view)

class KPSAdminDecisionView(View):
    def __init__(self, bot, admin, member, verified_role, channel):
        super().__init__(timeout=120)
        self.bot = bot
        self.admin = admin
        self.member = member
        self.verified_role = verified_role
        self.channel = channel

    @discord.ui.button(label="✅ ZATWIERDŹ", style=discord.ButtonStyle.success, emoji="🎟️")
    async def accept(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.admin.id:
            return await interaction.response.send_message("⛔ Tylko sędzia tego pojedynku może podjąć decyzję!", ephemeral=True)
        
        guild = interaction.guild
        if not guild:
            return await interaction.response.send_message("❌ Błąd: Nie można odnaleźć serwera.", ephemeral=True)

        try:
            member = await guild.fetch_member(self.member.id)
        except discord.NotFound:
            member = None

        if not member:
            return await interaction.response.send_message("❌ Błąd: Użytkownik opuścił serwer.", ephemeral=True)

        verified_role = discord.utils.get(guild.roles, name="—͟͞✅・Bilecik")
        if not verified_role:
            try:
                verified_role = await guild.create_role(name="—͟͞✅・Bilecik", color=discord.Color.from_rgb(255, 182, 193))
            except Exception as e:
                return await interaction.response.send_message(f"❌ Błąd tworzenia roli: {e}", ephemeral=True)

        roles_added = []
        try:
            await member.add_roles(verified_role)
            roles_added.append("—͟͞✅・Bilecik")
        except Exception as e:
            print(f"Błąd nadawania roli Bilecik: {e}")
        
        zaba_role = discord.utils.get(guild.roles, name="🐸 • Żaby")
        if zaba_role:
            try:
                await member.add_roles(zaba_role)
                roles_added.append("🐸 • Żaby")
            except Exception as e:
                print(f"Błąd nadawania roli Żaby: {e}")
        
        update_data(member.id, "balance", 100, "add")
        track_verification_stat("verified")

        welcome_embed = discord.Embed(
            title="🎉 POMYŚLNIE ZWERYFIKOWANO! 🎉",
            description=f"Serdecznie witamy i zapraszamy na serwer, {member.mention}! 🥰\n\n"
                        f"✨ Zostałeś pomyślnie zweryfikowany decyzją sędziego po pojedynku!\n"
                        f"🌸 Nadano Ci role: {', '.join([f'**{r}**' for r in roles_added]) if roles_added else 'Brak'}\n"
                        f"💰 Otrzymujesz na start **100 monet** do ekonomii!\n\n"
                        f"**Ten kanał weryfikacyjny zostanie automatycznie usunięty za 10 sekund...** ⏳",
            color=KAWAII_PINK
        )
        welcome_embed.set_footer(text="Życzymy miłej zabawy! 💕")
        await interaction.response.send_message(embed=welcome_embed)
        
        general = discord.utils.get(guild.text_channels, name="💬・pogadanki") or discord.utils.get(guild.text_channels, name="ogólny")
        if general:
            embed = discord.Embed(description=f"Witamy **{member.mention}**! (≧◡≦) ♡\n Cieszymy się że połączyłeś się z nami! 💖", color=KAWAII_PINK)
            b = get_profile_data(member.id).get("bio", "Nowy gracz na streecie!")
            embed.add_field(name="Zostawił takie bio:", value=b)
            await general.send(embed=embed)

        await asyncio.sleep(10)
        try:
            await self.channel.delete()
        except:
            pass

    @discord.ui.button(label="👢 Kick", style=discord.ButtonStyle.danger, emoji="👢")
    async def kick(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.admin.id:
            return await interaction.response.send_message("⛔ Tylko sędzia tego pojedynku może podjąć decyzję!", ephemeral=True)

        guild = interaction.guild
        try:
            member = await guild.fetch_member(self.member.id)
        except discord.NotFound:
            member = None

        if not member:
            return await interaction.response.send_message("❌ Błąd: Użytkownik opuścił serwer.", ephemeral=True)

        try:
            await interaction.response.send_message(f"👢 Wyrzucono {member.mention}...", ephemeral=True)
            await member.kick(reason=f"Przegrany pojedynek KPS i decyzja sędziego")
            track_verification_stat("kicked")

            embed = discord.Embed(title="👋 WYRZUCONO!", description=f"**{member.name}** przegrał pojedynek KPS i został wyrzucony.", color=discord.Color.orange())
            embed.set_image(url=random.choice(GIFS_KICK))
            await self.channel.send(embed=embed)
            await asyncio.sleep(10)
            await self.channel.delete()
        except Exception as e:
            await self.channel.send(f"❌ Nie udało się: {e}")

    @discord.ui.button(label="🔨 Ban", style=discord.ButtonStyle.danger, emoji="🔨")
    async def ban(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.admin.id:
            return await interaction.response.send_message("⛔ Tylko sędzia tego pojedynku może podjąć decyzję!", ephemeral=True)

        guild = interaction.guild
        try:
            member = await guild.fetch_member(self.member.id)
        except discord.NotFound:
            member = None

        if not member:
            return await interaction.response.send_message("❌ Błąd: Użytkownik opuścił serwer.", ephemeral=True)

        try:
            await interaction.response.send_message(f"🔨 Zbanowano {member.mention}...", ephemeral=True)
            await member.ban(reason=f"Przegrany pojedynek KPS i decyzja sędziego")
            track_verification_stat("banned")

            embed = discord.Embed(title="🔨 ZBANOWANO!", description=f"**{member.name}** przegrał pojedynek KPS i został zbanowany.", color=KAWAII_RED)
            embed.set_image(url=random.choice(GIFS_BAN))
            await self.channel.send(embed=embed)
            await asyncio.sleep(10)
            await self.channel.delete()
        except Exception as e:
            await self.channel.send(f"❌ Nie udało się: {e}")

    @discord.ui.button(label="🔄 Daj Szansę", style=discord.ButtonStyle.primary, emoji="🔄")
    async def retry(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.admin.id:
            return await interaction.response.send_message("⛔ Tylko sędzia tego pojedynku może podjąć decyzję!", ephemeral=True)

        view = KPSView(self.bot, self.admin, self.member, self.verified_role, self.channel)
        embed = discord.Embed(
            title="⚔️ POJEDYNEK KAMIEŃ, PAPIER, NOŻYCE ⚔️",
            description=f"Sędzia {self.admin.mention} daje drugą szansę! Wybierzcie swój ruch poniżej:\n\n"
                        f"👑 **Sędzia:** ⏳ Czeka na wybór...\n"
                        f"👤 **Kandydat:** ⏳ Czeka na wybór...",
            color=KAWAII_GOLD
        )
        await interaction.response.edit_message(embed=embed, view=view)

class KPSView(View):
    def __init__(self, bot, admin, member, verified_role, channel):
        super().__init__(timeout=120)
        self.bot = bot
        self.admin = admin
        self.member = member
        self.verified_role = verified_role
        self.channel = channel
        self.admin_choice = None
        self.member_choice = None
        self.game_over = False

    async def check_choices(self, interaction: discord.Interaction):
        if self.admin_choice and self.member_choice and not self.game_over:
            self.game_over = True
            for item in self.children:
                if isinstance(item, Button) and item.custom_id in ["kamien", "papier", "nozyce"]:
                    item.disabled = True

            choices_dict = {
                "kamien": {"emoji": "🪨", "beats": "nozyce", "name": "Kamień"},
                "papier": {"emoji": "📄", "beats": "kamien", "name": "Papier"},
                "nozyce": {"emoji": "✂️", "beats": "papier", "name": "Nożyce"}
            }

            admin_info = choices_dict[self.admin_choice]
            member_info = choices_dict[self.member_choice]

            embed = discord.Embed(
                title="⚔️ POJEDYNEK KPS: WYNIK! ⚔️",
                color=KAWAII_GOLD
            )
            embed.add_field(name=f"👑 Sędzia {self.admin.name}", value=f"{admin_info['emoji']} **{admin_info['name']}**", inline=True)
            embed.add_field(name=f"👤 Kandydat {self.member.name}", value=f"{member_info['emoji']} **{member_info['name']}**", inline=True)

            track_verification_stat("kps_played")

            if self.admin_choice == self.member_choice:
                embed.description = "👔 **Remis!** Obaj wybrali to samo. Spróbujcie jeszcze raz!"
                embed.color = discord.Color.orange()
                
                view = KPSTieView(self.bot, self.admin, self.member, self.verified_role, self.channel)
                await interaction.message.edit(embed=embed, view=view)
            elif choices_dict[self.member_choice]["beats"] == self.admin_choice:
                embed.description = f"🎉 **Kandydat {self.member.mention} wygrywa pojedynek!**\nUżytkownik zostaje automatycznie zweryfikowany z bonusem **150 monet**! 💰"
                embed.color = discord.Color.green()
                
                self.clear_items()
                await interaction.message.edit(embed=embed, view=self)

                track_verification_stat("kps_wins")

                try:
                    member = await interaction.guild.fetch_member(self.member.id)
                except discord.NotFound:
                    member = None

                if member:
                    welcome_desc = (
                        f"Serdecznie witamy i zapraszamy na serwer, {member.mention}! 🥰\n\n"
                        f"⚔️ Pokonałeś sędziego w pojedynku KPS i zostałeś automatycznie zweryfikowany!\n"
                        f"🌸 Nadano Ci role: {{roles}}\n"
                        f"💰 Otrzymujesz bonusowe **150 monet** do ekonomii! 💰\n\n"
                        f"**Ten kanał weryfikacyjny zostanie automatycznie usunięty za 10 sekund...** ⏳"
                    )
                    await execute_verification(
                        bot=self.bot,
                        guild=interaction.guild,
                        member=member,
                        channel=self.channel,
                        balance_amount=150,
                        welcome_description=welcome_desc,
                        pogadanki_extra="(Pokonał sędziego w pojedynku KPS! ⚔️)",
                        interaction=None
                    )
            else:
                embed.description = f"👑 **Sędzia {self.admin.mention} wygrywa pojedynek!**\nLos kandydata leży w rękach sędziego..."
                embed.color = discord.Color.red()
                
                track_verification_stat("kps_losses")
                
                self.clear_items()
                decision_view = KPSAdminDecisionView(self.bot, self.admin, self.member, self.verified_role, self.channel)
                for child in decision_view.children:
                    self.add_item(child)
                await interaction.message.edit(embed=embed, view=self)

    @discord.ui.button(label="🪨 Kamień", style=discord.ButtonStyle.secondary, custom_id="kamien")
    async def rock_button(self, interaction: discord.Interaction, button: Button):
        await self.handle_choice(interaction, "kamien")

    @discord.ui.button(label="📄 Papier", style=discord.ButtonStyle.secondary, custom_id="papier")
    async def paper_button(self, interaction: discord.Interaction, button: Button):
        await self.handle_choice(interaction, "papier")

    @discord.ui.button(label="✂️ Nożyce", style=discord.ButtonStyle.secondary, custom_id="nozyce")
    async def scissors_button(self, interaction: discord.Interaction, button: Button):
        await self.handle_choice(interaction, "nozyce")

    async def handle_choice(self, interaction: discord.Interaction, choice: str):
        user_id = interaction.user.id
        if user_id != self.admin.id and user_id != self.member.id:
            return await interaction.response.send_message("❌ Nie bierzesz udziału w tym pojedynku!", ephemeral=True)

        if user_id == self.admin.id:
            if self.admin_choice:
                return await interaction.response.send_message("❌ Już dokonałeś wyboru!", ephemeral=True)
            self.admin_choice = choice
        else:
            if self.member_choice:
                return await interaction.response.send_message("❌ Już dokonałeś wyboru!", ephemeral=True)
            self.member_choice = choice

        embed = interaction.message.embeds[0]
        desc = f"Sędzia {self.admin.mention} wyzywa {self.member.mention} na pojedynek Kamień, Papier, Nożyce!\n\n"
        
        status_admin = "✅ **WYBRAŁ!** 🔒" if self.admin_choice else "⏳ Czeka na wybór..."
        status_member = "✅ **WYBRAŁ!** 🔒" if self.member_choice else "⏳ Czeka na wybór..."
        
        desc += f"👑 **Sędzia:** {status_admin}\n👤 **Kandydat:** {status_member}"
        embed.description = desc

        await interaction.response.edit_message(embed=embed, view=self)
        await self.check_choices(interaction)

class QuizView(View):
    def __init__(self, bot, admin, member, verified_role, channel, question_data):
        super().__init__(timeout=30)
        self.bot = bot
        self.admin = admin
        self.member = member
        self.verified_role = verified_role
        self.channel = channel
        self.question_data = question_data
        self.answered = False

        self.btn_a.label = f"A: {question_data['options'][0]}"[:80]
        self.btn_b.label = f"B: {question_data['options'][1]}"[:80]
        self.btn_c.label = f"C: {question_data['options'][2]}"[:80]

    async def on_timeout(self):
        if not self.answered:
            self.answered = True
            for item in self.children:
                if isinstance(item, Button):
                    item.disabled = True
            
            track_verification_stat("quiz_losses")
            
            embed = discord.Embed(
                title="⏰ CZAS MINĄŁ! ⏰",
                description=f"Kandydat {self.member.mention} nie odpowiedział na pytanie w ciągu 30 sekund!\n\n"
                            f"🧠 Prawidłowa odpowiedź to: **{self.question_data['correct_letter']}: {self.question_data['options'][self.question_data['correct_idx']]}**\n\n"
                            f"Los kandydata leży w rękach sędziów...",
                color=discord.Color.red()
            )
            
            decision_view = VerifyDecisionView(self.bot, self.member, self.verified_role, self.channel)
            try:
                await self.channel.send(
                    content=f"🔔 {self.admin.mention} - kandydat spóźnił się z odpowiedzią!",
                    embed=embed,
                    view=decision_view
                )
            except Exception as e:
                print(f"Error on quiz timeout: {e}")

    async def handle_answer(self, interaction: discord.Interaction, choice_idx: int, choice_letter: str):
        if interaction.user.id != self.member.id:
            return await interaction.response.send_message("❌ Tylko kandydat może odpowiadać na pytanie!", ephemeral=True)

        self.answered = True
        self.stop()

        for item in self.children:
            if isinstance(item, Button):
                item.disabled = True

        correct_idx = self.question_data["correct_idx"]
        correct_option = self.question_data["options"][correct_idx]
        correct_letter = self.question_data["correct_letter"]

        embed = discord.Embed(title="🌀 WYNIK QUIZU WERYFIKACYJNEGO 🌀")

        if choice_idx == correct_idx:
            track_verification_stat("quiz_wins")
            embed.title = "✅ PRAWIDŁOWA ODPOWIEDŹ! ✅"
            embed.description = f"Gratulacje {self.member.mention}!\nOdpowiedziałeś poprawnie: **{choice_letter}: {self.question_data['options'][choice_idx]}**\n\n" \
                                f"Udowodniłeś swoje wysokie IQ i otrzymujesz bonus **50 monet**! 💰\n" \
                                f"Sędziowie mogą teraz podjąć ostateczną decyzję."
            embed.color = discord.Color.green()
            
            update_data(self.member.id, "balance", 50, "add")
        else:
            track_verification_stat("quiz_losses")
            embed.title = "❌ BŁĘDNA ODPOWIEDŹ! ❌"
            embed.description = f"Niestety {self.member.mention}...\nTwój wybór: **{choice_letter}: {self.question_data['options'][choice_idx]}**\n" \
                                f"Prawidłowa odpowiedź to: **{correct_letter}: {correct_option}**\n\n" \
                                f"Sędziowie kręcą nosami... Decyzja o Twoim losie należy do nich."
            embed.color = discord.Color.red()

        decision_view = VerifyDecisionView(self.bot, self.member, self.verified_role, self.channel)
        await interaction.response.edit_message(embed=embed, view=self)
        
        await self.channel.send(
            content=f"🔔 **Administracja / Sędziowie** - proszę o podjęcie decyzji dla {self.member.mention}!",
            view=decision_view
        )

    @discord.ui.button(style=discord.ButtonStyle.primary, custom_id="quiz_a")
    async def btn_a(self, interaction: discord.Interaction, button: Button):
        await self.handle_answer(interaction, 0, "A")

    @discord.ui.button(style=discord.ButtonStyle.primary, custom_id="quiz_b")
    async def btn_b(self, interaction: discord.Interaction, button: Button):
        await self.handle_answer(interaction, 1, "B")

    @discord.ui.button(style=discord.ButtonStyle.primary, custom_id="quiz_c")
    async def btn_c(self, interaction: discord.Interaction, button: Button):
        await self.handle_answer(interaction, 2, "C")


# --- GŁÓWNY COG ---
class Verification(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.join_times = {}
        self.raid_mode = {}
        self.raid_end_time = {}
        # Rejestracja widoków dla persystencji (żeby działały po restarcie)
        self.bot.add_view(RoleSelectView(self.bot, None, is_setup=True))
        self.bot.add_view(ColorSelectView(self.bot, None, is_setup=True))

    async def _create_missing_roles(self, guild):
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

    def get_verification_member(self, ctx):
        for target in ctx.channel.overwrites:
            if isinstance(target, discord.Member) and target.id != self.bot.user.id:
                if not target.guild_permissions.manage_roles and target.name.lower() not in ["≽^borysiaczekuwu^≼", "borysiaczekuwu"]:
                    return target
        return None

    @commands.command(name="w")
    async def w_command(self, ctx, action: str = None, *, member: discord.Member = None):
        """Komendy administracyjne do weryfikacji. Użycie: !w <wpusc|kick|ban|moneta|ruletka|kps|skan|quiz|pytaj|staty> [użytkownik]"""
        if not ctx.author.guild_permissions.manage_roles and ctx.author.name.lower() not in ["≽^borysiaczekuwu^≼", "borysiaczekuwu"]:
            return await ctx.send("⛔ Brak uprawnień do korzystania z komend weryfikacji!")

        valid_actions = [
            "wpusc", "akceptuj", "yes", "kick", "no", "ban", "moneta", "ruletka",
            "pytaj", "pytanie", "staty", "statystyki", "kps", "kpn", "rps",
            "skan", "wykrywacz", "audit", "quiz", "test"
        ]

        if not action or action.lower() not in valid_actions:
            embed = discord.Embed(
                title="⚖️ Panel Pomocy Weryfikacji",
                description="Użyj jednego z poniższych parametrów:\n"
                            "• `!w wpusc` / `!w akceptuj` - Akceptuje użytkownika i nadaje role.\n"
                            "• `!w kick` - Wyrzuca użytkownika z serwera.\n"
                            "• `!w ban` - Banuje użytkownika na serwerze.\n"
                            "• `!w moneta` - 50/50 na wpuszczenie lub kick z animacją rzutu monetą.\n"
                            "• `!w ruletka` - Rosyjska ruletka (1/6 szans na kick, 5/6 na wpuszczenie) z animacją rewolweru.\n"
                            "• `!w kps` / `!w kpn` - Inicjuje pojedynek Kamień, Papier, Nożyce z kandydatem.\n"
                            "• `!w skan` / `!w wykrywacz` - Przeprowadza zabawny diagnostyczny skan uroczości.\n"
                            "• `!w quiz` / `!w test` - Wyświetla szybki weryfikacyjny test jednokrotnego wyboru (30s).\n"
                            "• `!w pytaj` - Zadaje użytkownikowi losowe, zabawne pytanie rekrutacyjne.\n"
                            "• `!w staty` - Wyświetla globalne statystyki systemu weryfikacji z emotkami.",
                color=KAWAII_GOLD
            )
            return await ctx.send(embed=embed)

        action = action.lower()
        if not member and action not in ["staty", "statystyki"]:
            member = self.get_verification_member(ctx)

        if not member and action not in ["staty", "statystyki"]:
            return await ctx.send("❌ Nie znaleziono weryfikowanego użytkownika! Upewnij się, że jesteś na kanale weryfikacyjnym lub oznacz użytkownika ręcznie: `!w <akcja> <@użytkownik>`")

        verified_role = discord.utils.get(ctx.guild.roles, name="—͟͞✅・Bilecik")
        if not verified_role and action not in ["staty", "statystyki"]:
            try:
                verified_role = await ctx.guild.create_role(name="—͟͞✅・Bilecik", color=discord.Color.from_rgb(255, 182, 193))
            except Exception as e:
                return await ctx.send(f"❌ Nie udało się stworzyć/znaleźć roli weryfikacyjnej: {e}")

        if action in ["wpusc", "akceptuj", "yes"]:
            welcome_desc = (
                f"Witaj serdecznie na naszym serwerze, {member.mention}! 🌸\n"
                f"Pomyślnie nadano Ci role: {{roles}}.\n\n"
                f"**Ten kanał zostanie automatycznie usunięty za 10 sekund...** ⏳"
            )
            await execute_verification(
                bot=self.bot,
                guild=ctx.guild,
                member=member,
                channel=ctx.channel,
                balance_amount=100,
                welcome_description=welcome_desc,
                pogadanki_extra="",
                interaction=None
            )

        elif action in ["kick", "no"]:
            try:
                await ctx.send(f"👢 Wyrzucam {member.mention}...", delete_after=5)
                await member.kick(reason=f"Wyrzucono komendą !w przez {ctx.author.name}")

                track_verification_stat("kicked")

                embed = discord.Embed(title="👋 WYRZUCONO!", description=f"**{member.name}** nie przeszedł weryfikacji (decyzja: {ctx.author.mention}).", color=discord.Color.orange())
                embed.set_image(url=random.choice(GIFS_KICK))
                await ctx.send(embed=embed)
                await asyncio.sleep(5)
                await ctx.channel.delete()
            except Exception as e:
                await ctx.send(f"❌ Nie udało się: {e}")

        elif action == "ban":
            try:
                await ctx.send(f"🔨 Banuję {member.mention}...", delete_after=5)
                await member.ban(reason=f"Zbanowano komendą !w przez {ctx.author.name}")

                track_verification_stat("banned")

                embed = discord.Embed(title="🔨 ZBANOWANO!", description=f"**{member.name}** nie przeszedł weryfikacji (decyzja: {ctx.author.mention}).", color=KAWAII_RED)
                embed.set_image(url=random.choice(GIFS_BAN))
                await ctx.send(embed=embed)
                await asyncio.sleep(10)
                await ctx.channel.delete()
            except Exception as e:
                await ctx.send(f"❌ Nie udało się: {e}")

        elif action == "moneta":
            coin_embed = discord.Embed(
                title="🪙 RZUT MONETĄ WERYFIKACYJNĄ 🪙",
                description=f"Sędzia {ctx.author.mention} rzuca monetą, decydując o losie {member.mention}...\n\n"
                            "*Przygotowywanie monety...*",
                color=KAWAII_GOLD
            )
            msg = await ctx.send(embed=coin_embed)
            await asyncio.sleep(1.2)

            coin_embed.description = f"Sędzia {ctx.author.mention} rzuca monetą, decydując o losie {member.mention}...\n\n" \
                                     "🪙 **Podrzucenie!** Moneta leci wysoko w górę... 🔄"
            await msg.edit(embed=coin_embed)
            await asyncio.sleep(1.2)

            coin_embed.description = f"Sędzia {ctx.author.mention} rzuca monetą, decydując o losie {member.mention}...\n\n" \
                                     "⚡ **Wirowanie!** Orzeł czy Reszka? Los decyduje... ⚡"
            await msg.edit(embed=coin_embed)
            await asyncio.sleep(1.2)

            coin_embed.description = f"Sędzia {ctx.author.mention} rzuca monetą, decydując o losie {member.mention}...\n\n" \
                                     "✨ **Spadanie!** Moneta opada na stół... 🎯"
            await msg.edit(embed=coin_embed)
            await asyncio.sleep(1.2)

            is_heads = random.choice([True, False])
            if is_heads:
                coin_embed.title = "🦅 WYNIK: ORZEŁ! 🦅"
                coin_embed.description = f"**Wynik: ORZEŁ!** 🦅\n\n" \
                                         f"Los uśmiechnął się do {member.mention}! Użytkownik zostaje wpuszczony na serwer. 🎉"
                coin_embed.color = discord.Color.green()
                await msg.edit(embed=coin_embed)

                track_verification_stat("coin_heads")
                try:
                    fetched_member = await ctx.guild.fetch_member(member.id)
                except discord.NotFound:
                    fetched_member = None

                if fetched_member:
                    welcome_desc = (
                        f"Serdecznie witamy i zapraszamy na serwer, {fetched_member.mention}! 🥰\n\n"
                        f"🪙 Wygrałeś weryfikacyjny rzut monetą! Szczęśliwy traf!\n"
                        f"🌸 Nadano Ci role: {{roles}}\n"
                        f"💰 Otrzymujesz na start **100 monet** do ekonomii!\n\n"
                        f"**Ten kanał weryfikacyjny zostanie automatycznie usunięty za 10 sekund...** ⏳"
                    )
                    await execute_verification(
                        bot=self.bot,
                        guild=ctx.guild,
                        member=fetched_member,
                        channel=ctx.channel,
                        balance_amount=100,
                        welcome_description=welcome_desc,
                        pogadanki_extra="(Wygrał weryfikacyjny rzut monetą! 🪙)",
                        interaction=None
                    )
            else:
                coin_embed.title = "🪙 WYNIK: RESZKA! 🪙"
                coin_embed.description = f"**Wynik: RESZKA!** 🪙\n\n" \
                                         f"Niestety... Szczęście nie dopisało {member.mention}. Zostaje wykopany z serwera! 👢"
                coin_embed.color = discord.Color.red()
                await msg.edit(embed=coin_embed)

                track_verification_stat("coin_tails")
                track_verification_stat("kicked")

                try:
                    fetched_member = await ctx.guild.fetch_member(member.id)
                except discord.NotFound:
                    fetched_member = None

                if fetched_member:
                    try:
                        await fetched_member.kick(reason="Przegrany weryfikacyjny rzut monetą (!w moneta)")
                    except:
                        pass

                embed_kick = discord.Embed(title="👋 WYRZUCONO!", description=f"**{member.name}** przegrał rzut monetą i został wyrzucony.", color=discord.Color.orange())
                embed_kick.set_image(url=random.choice(GIFS_KICK))
                await ctx.send(embed_kick)

                await asyncio.sleep(10)
                try:
                    await ctx.channel.delete()
                except:
                    pass

        elif action == "ruletka":
            bullet_embed = discord.Embed(
                title="🔫 ROSYJSKA RULETKA WERYFIKACYJNA 🔫",
                description=f"Sędzia {ctx.author.mention} wyciąga rewolwer i poddaje {member.mention} próbie rosyjskiej ruletki...\n\n"
                            "*Przygotowywanie rewolweru...*",
                color=KAWAII_GOLD
            )
            msg = await ctx.send(embed=bullet_embed)
            await asyncio.sleep(1.2)

            bullet_embed.description = f"Sędzia {ctx.author.mention} wyciąga rewolwer i poddaje {member.mention} próbie rosyjskiej ruletki...\n\n" \
                                       "🔫 **Ładowanie!** Jeden ostry nabój trafia do komory bębenka... 💼"
            await msg.edit(embed=bullet_embed)
            await asyncio.sleep(1.2)

            bullet_embed.description = f"Sędzia {ctx.author.mention} wyciąga rewolwer i poddaje {member.mention} próbie rosyjskiej ruletki...\n\n" \
                                       "🔄 **Zakręcenie!** Bębenek wiruje z charakterystycznym terkotem... ⚡"
            await msg.edit(embed=bullet_embed)
            await asyncio.sleep(1.2)

            bullet_embed.description = f"Sędzia {ctx.author.mention} wyciąga rewolwer i poddaje {member.mention} próbie rosyjskiej ruletki...\n\n" \
                                       "🎯 **Przymierzenie!** Zimna lufa dotyka czoła... Palec ląduje na spuście... 🤫"
            await msg.edit(embed=bullet_embed)
            await asyncio.sleep(1.5)

            bullet_position = random.randint(1, 6)
            if bullet_position == 1:
                track_verification_stat("roulette_dead")
                track_verification_stat("kicked")

                bullet_embed.title = "💥 BUM! 💥"
                bullet_embed.description = f"**Wynik: STRZAŁ!** 💥\n\n" \
                                           f"Niestety! Komora była pełna. {member.mention} został wyeliminowany przez los! 👢"
                bullet_embed.color = discord.Color.red()
                await msg.edit(embed=bullet_embed)

                try:
                    fetched_member = await ctx.guild.fetch_member(member.id)
                except discord.NotFound:
                    fetched_member = None

                if fetched_member:
                    try:
                        await fetched_member.kick(reason="Przegrana rosyjska ruletka weryfikacyjna (!w ruletka)")
                    except:
                        pass

                embed_kick = discord.Embed(title="👋 WYRZUCONO!", description=f"**{member.name}** poległ w rosyjskiej ruletce weryfikacyjnej.", color=discord.Color.orange())
                embed_kick.set_image(url=random.choice(GIFS_KICK))
                await ctx.send(embed_kick)

                await asyncio.sleep(10)
                try:
                    await ctx.channel.delete()
                except:
                    pass
            else:
                track_verification_stat("roulette_live")
                try:
                    fetched_member = await ctx.guild.fetch_member(member.id)
                except discord.NotFound:
                    fetched_member = None

                if fetched_member:
                    welcome_desc = (
                        f"Serdecznie witamy i zapraszamy na serwer, {fetched_member.mention}! 🥰\n\n"
                        f"🔫 Przeżyłeś rosyjską ruletkę! Niesamowite szczęście!\n"
                        f"🌸 Nadano Ci role: {{roles}}\n"
                        f"💰 Otrzymujesz na start **100 monet** do ekonomii!\n\n"
                        f"**Ten kanał weryfikacyjny zostanie automatycznie usunięty za 10 sekund...** ⏳"
                    )
                    await execute_verification(
                        bot=self.bot,
                        guild=ctx.guild,
                        member=fetched_member,
                        channel=ctx.channel,
                        balance_amount=100,
                        welcome_description=welcome_desc,
                        pogadanki_extra="(Przeżył weryfikacyjną rosyjską ruletkę! 🔫)",
                        interaction=None
                    )

        elif action in ["pytaj", "pytanie"]:
            question = random.choice(ABSURD_QUESTIONS)
            embed_q = discord.Embed(
                title="🌀 ABSURDALNE PYTANIE WERYFIKACYJNE 🌀",
                description=f"Sędzia {ctx.author.mention} żąda od Ciebie odpowiedzi na poniższe pytanie, aby udowodnić swoje człowieczeństwo i poczucie humoru!\n\n"
                            f"🤔 **Pytanie:**\n### {question}",
                color=KAWAII_PINK
            )
            embed_q.set_footer(text="Odpowiedz szczerze i z humorem na czacie!")
            await ctx.send(content=f"{member.mention} - odpowiedz na pytanie!", embed=embed_q)

        elif action in ["kps", "kpn", "rps"]:
            embed_kps = discord.Embed(
                title="⚔️ POJEDYNEK KAMIEŃ, PAPIER, NOŻYCE ⚔️",
                description=f"Sędzia {ctx.author.mention} wyzywa {member.mention} na pojedynek Kamień, Papier, Nożyce!\n\n"
                            f"👑 **Sędzia:** ⏳ Czeka na wybór...\n"
                            f"👤 **Kandydat:** ⏳ Czeka na wybór...",
                color=KAWAII_GOLD
            )
            view = KPSView(self.bot, ctx.author, member, verified_role, ctx.channel)
            await ctx.send(embed=embed_kps, view=view)

        elif action in ["skan", "wykrywacz", "audit"]:
            track_verification_stat("scans_run")
            
            scan_embed = discord.Embed(
                title="🔍 INICJOWANIE SKANERA UROCZOŚCI NYANKO...",
                description="⏳ Podłączanie elektrod słodkości...\n`[░░░░░░░░░░] 0%`",
                color=KAWAII_PINK
            )
            msg = await ctx.send(embed=scan_embed)
            await asyncio.sleep(1.2)
            
            scan_embed.description = "⏳ Analizowanie profilu i uszek na awatarze...\n`[■■■░░░░░░░] 30%`"
            await msg.edit(embed=scan_embed)
            await asyncio.sleep(1.2)
            
            scan_embed.description = "⏳ Mierzenie poziomu żabiości (Frog Affinity)...\n`[■■■■■■░░░░] 60%`"
            await msg.edit(embed=scan_embed)
            await asyncio.sleep(1.2)
            
            scan_embed.description = "⏳ Sprawdzanie poziomu podejrzaności (Sus Level)...\n`[■■■■■■■■■░] 90%`"
            await msg.edit(embed=scan_embed)
            await asyncio.sleep(1.2)
            
            # Losowanie parametrów
            kawaii_factor = random.randint(50, 100)
            frog_affinity = random.randint(0, 100)
            sus_level = random.randint(0, 49)
            iq_level = random.randint(90, 160)
            
            # Opisy
            if kawaii_factor >= 90: kawaii_desc = "Ekstremalnie słodki! 🌸"
            elif kawaii_factor >= 75: kawaii_desc = "Bardzo uroczy 😊"
            else: kawaii_desc = "Uroczy w normie 👍"
            
            if frog_affinity >= 80: frog_desc = "Czystej krwi żaba! 🐸"
            elif frog_affinity >= 50: frog_desc = "Lubi deszcz i stawy 🌧️"
            else: frog_desc = "Dopiero uczy się kumkać 🐸"
            
            if sus_level >= 30: sus_desc = "Podejrzany o podjadanie w nocy 🍪"
            elif sus_level >= 15: sus_desc = "Niski poziom sus 🕵️"
            else: sus_desc = "Całkowicie bezpieczny 😇"
            
            iq_comments = [
                "Zna kod bota na pamięć",
                "Rozmawia płynnie w języku żabim",
                "Rozróżnia 50 odcieni różu",
                "Umie zbudować domek z ziemi w 3 sekundy"
            ]
            iq_comment = random.choice(iq_comments)
            
            recommendations = [
                "Zaleca się natychmiastowe wpuszczenie i poczęstowanie truskawkowym mlekiem! 🍓",
                "Wpuścić, ale obserwować czy nie kradnie żabich ciasteczek! 🐸",
                "Wzorowy profil! Dać mu VIP-owskie miejsce na stawie!",
                "Wpuścić, ale sędzia musi najpierw dostać przytulasa!"
            ]
            rec = random.choice(recommendations)
            
            scan_embed.title = "🔍 WYNIK AUDYTU UROCZOŚCI NYANKO 🔍"
            scan_embed.description = f"**Wynik skanowania biometrycznego dla {member.mention}:**"
            scan_embed.color = KAWAII_PINK
            
            scan_embed.add_field(name="🌸 Kawaii Factor", value=f"`{kawaii_factor}%` - {kawaii_desc}", inline=False)
            scan_embed.add_field(name="🐸 Frog Affinity", value=f"`{frog_affinity}%` - {frog_desc}", inline=False)
            scan_embed.add_field(name="🕵️ Sus Level", value=f"`{sus_level}%` - {sus_desc}", inline=False)
            scan_embed.add_field(name="🧠 IQ / Umiejętności", value=f"`{iq_level} IQ` ({iq_comment})", inline=False)
            scan_embed.add_field(name="💡 Werdykt / Rekomendacja", value=f"**{rec}**", inline=False)
            scan_embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            
            await msg.edit(embed=scan_embed)

        elif action in ["quiz", "test"]:
            q_data = random.choice(QUIZ_QUESTIONS)
            embed_q = discord.Embed(
                title="🧠 SZYBKI QUIZ WERYFIKACYJNY 🧠",
                description=f"Kandydat {member.mention} must odpowiedzieć na poniższe pytanie w ciągu **30 sekund**!\n\n"
                            f"### Pytanie:\n**{q_data['question']}**\n\n"
                            f"Wybierz odpowiedź klikając odpowiedni przycisk poniżej!",
                color=KAWAII_GOLD
            )
            view = QuizView(self.bot, ctx.author, member, verified_role, ctx.channel, q_data)
            await ctx.send(content=f"{member.mention} - Twój czas start!", embed=embed_q, view=view)

        elif action in ["staty", "statystyki"]:
            stats = get_profile_data("global_verification_stats")
            if "stats_initialized" not in stats:
                stats = {
                    "verified": 0,
                    "kicked": 0,
                    "banned": 0,
                    "coin_heads": 0,
                    "coin_tails": 0,
                    "roulette_live": 0,
                    "roulette_dead": 0,
                    "kps_played": 0,
                    "kps_wins": 0,
                    "kps_losses": 0,
                    "quiz_wins": 0,
                    "quiz_losses": 0,
                    "scans_run": 0
                }
            
            total_processed = stats.get("verified", 0) + stats.get("kicked", 0) + stats.get("banned", 0)
            survival_rate = 100.0
            if total_processed > 0:
                survival_rate = (stats.get("verified", 0) / total_processed) * 100.0
            
            embed_stats = discord.Embed(
                title="📊 ROZSZERZONE STATYSTYKI WERYFIKACJI 📊",
                description="Oto globalny raport z weryfikacji i gier na serwerze Nyanko:",
                color=KAWAII_GOLD
            )
            embed_stats.add_field(name="💖 Zatwierdzeni (Bileciki)", value=f"🥇 `{stats.get('verified', 0)}` graczy", inline=True)
            embed_stats.add_field(name="`❌ Wyrzuceni`", value=f"🚪 `{stats.get('kicked', 0)}` graczy", inline=True)
            embed_stats.add_field(name="🔨 Zbanowani (Bany)", value=f"🚷 `{stats.get('banned', 0)}` graczy", inline=True)
            
            embed_stats.add_field(
                name="🪙 Rzuty Monetą (50/50)",
                value=f"🦅 Orzeł (Wpuszczenie): `{stats.get('coin_heads', 0)}` | 🪙 Reszka (Kick): `{stats.get('coin_tails', 0)}`",
                inline=False
            )
            embed_stats.add_field(
                name="🔫 Rosyjska Ruletka (1/6)",
                value=f"💚 Przeżyli (Wpuszczenie): `{stats.get('roulette_live', 0)}` | 💥 Polegli (Kick): `{stats.get('roulette_dead', 0)}`",
                inline=False
            )
            
            kps_wins = stats.get("kps_wins", 0)
            kps_losses = stats.get("kps_losses", 0)
            kps_played = stats.get("kps_played", 0)
            quiz_wins = stats.get("quiz_wins", 0)
            quiz_losses = stats.get("quiz_losses", 0)
            scans_run = stats.get("scans_run", 0)
            
            embed_stats.add_field(
                name="⚔️ Pojedynki KPS (Kamień-Papier-Nożyce)",
                value=f"🏆 Wygrane kandydata: `{kps_wins}` | 👑 Wygrane sędziego: `{kps_losses}`\n🎮 Razem pojedynków: `{kps_played}`",
                inline=False
            )
            embed_stats.add_field(
                name="🧠 Quizy Weryfikacyjne",
                value=f"🟢 Dobre odpowiedzi: `{quiz_wins}` | 🔴 Błędne/Limit czasu: `{quiz_losses}`",
                inline=False
            )
            embed_stats.add_field(
                name="🔍 Skanery Uroczości",
                value=f"🌸 Wykonano diagnostyk: `{scans_run}` skanów",
                inline=False
            )
            
            embed_stats.add_field(
                name="❤️ Globalny Wskaźnik Przetrwania",
                value=f"📈 `{survival_rate:.1f}%` szansy na pomyślną weryfikację",
                inline=False
            )
            
            embed_stats.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else self.bot.user.default_avatar.url)
            embed_stats.set_footer(text=f"Łącznie obsłużono: {total_processed} weryfikowanych graczy")
            
            await ctx.send(embed=embed_stats)

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

        await self._create_missing_roles(guild)

        verified_role = discord.utils.get(guild.roles, name="—͟͞✅・Bilecik")
        if not verified_role:
            verified_role = await guild.create_role(name="—͟͞✅・Bilecik", color=discord.Color.from_rgb(255, 182, 193))

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            self.bot.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, manage_channels=True)
        }
        for role in guild.roles:
            if role.permissions.manage_roles:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        channel_name = f"✅・{member.name}".lower().replace("#", "")
        
        category_name = "╒═════╡Weryfikacja╞═════╕"
        category = discord.utils.get(guild.categories, name=category_name)
        if not category:
            try: category = await guild.create_category(category_name)
            except: category = None
            
        try:
            channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
            
            embed = discord.Embed(
                title=f"🌸 Witaj {member.name}! Rozpocznij weryfikację", 
                description=(
                    "Cieszymy się, że jesteś z nami! Aby uzyskać dostęp do serwera, uzupełnij poniższe dane:\n\n"
                    "1️⃣ Wybierz swoją **płeć, wiek, pingi, tożsamość/flagę oraz kolor** z poniższych menu rozwijanych.\n"
                    "2️⃣ Kliknij przycisk **`📝 Napisz Bio`** poniżej, aby opisać siebie.\n"
                    "3️⃣ Po zakończeniu konfiguracji kliknij przycisk **`🟢 Oznacz Gotowość`**.\n\n"
                    "⏳ *Po oznaczeniu gotowości, administracja/sędziowie sprawdzą Twój profil i zatwierdzą Twój dostęp!*"
                ),
                color=KAWAII_PINK
            )
            embed.set_footer(text="Podczas oczekiwania na weryfikację możesz pisać na tym kanale.")
            
            profile_view = VerificationProfileSelectView(self.bot, member)
            buttons_view = VerificationWelcomeView(self.bot, member, verified_role, channel)
            
            profile_msg = await channel.send(f"{member.mention} - uzupełnij swoje role i kolor nicku poniżej:", embed=embed, view=profile_view)
            buttons_view.profile_msg = profile_msg
            
            embed_buttons = discord.Embed(
                description="Uzupełnij bio i zgłoś swoją gotowość do weryfikacji sędziom serwera:",
                color=KAWAII_PINK
            )
            await channel.send(embed=embed_buttons, view=buttons_view)
        except Exception as e: 
            print(f"Błąd tworzenia instancji weryfikacji: {e}")

async def setup(bot):
    await bot.add_cog(Verification(bot))
