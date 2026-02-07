import discord
from discord.ext import commands
from discord.ui import Button, View
import asyncio
import random
import json
import os
import re
from datetime import datetime, timedelta

# --- IMPORT SERWERA WWW (DLA RENDER) ---
from keep_alive import keep_alive

# --- KONFIGURACJA INTENCJI ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# --- KONFIGURACJA BOTA ---
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# --- KOLORY I GIFY (KAWAII STYLE) ---
KAWAII_PINK = 0xFF69B4
KAWAII_RED = 0xFF0000
KAWAII_GOLD = 0xFFD700
KAWAII_BLUE = 0x87CEEB
KAWAII_PURPLE = 0x9B59B6

# Listy GIFów
GIFS_BAN = [
    "https://media.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif",
    "https://media.giphy.com/media/AC1HrkBir3bzq/giphy.gif",
    "https://media.giphy.com/media/qPD4yGsrc0pdm/giphy.gif",
    "https://media.giphy.com/media/H99r2epvbWWFVX0rJv/giphy.gif"
]

GIFS_KICK = [
    "https://media.giphy.com/media/wQCWMHY9EHLfq/giphy.gif",
    "https://media.giphy.com/media/26FPn4rR1damB0MQo/giphy.gif",
    "https://media.giphy.com/media/l3V0j3ytFyGHqiV7W/giphy.gif"
]

GIFS_MUTE = [
    "https://media.giphy.com/media/hfBvLPfHXRLO1gYgJv/giphy.gif",
    "https://media.giphy.com/media/liW10vuLjuUA8/giphy.gif"
]

GIFS_NUKE = [
    "https://media.giphy.com/media/OE6FE4GZF78nm/giphy.gif",
    "https://media.giphy.com/media/HhTXt43pk1I1W/giphy.gif"
]

GIFS_HUG = [
    "https://media.giphy.com/media/ODy2AThnlxWxO/giphy.gif",
    "https://media.giphy.com/media/lrr9rHuoNOE0ZwcTE/giphy.gif",
    "https://media.giphy.com/media/PHZ7v9tfQu0o0/giphy.gif",
    "https://media.giphy.com/media/GMFUrC8E8aWoo/giphy.gif"
]

GIFS_KISS = [
    "https://media.giphy.com/media/FqBTvSNjNzeZG/giphy.gif",
    "https://media.giphy.com/media/nyGFcsP0kAobm/giphy.gif",
    "https://media.giphy.com/media/bm2O3nXTcKJeU/giphy.gif"
]

GIFS_SLAP = [
    "https://media.giphy.com/media/10Am8idu3qWomI/giphy.gif",
    "https://media.giphy.com/media/Lp5ideZTgwKmk/giphy.gif",
    "https://media.giphy.com/media/Zau0yrl17uzdK/giphy.gif"
]

GIFS_PAT = [
    "https://media.giphy.com/media/5tmRHwTlHAA9WkVxTU/giphy.gif",
    "https://media.giphy.com/media/L2z7dnOduqE6Y/giphy.gif",
    "https://media.giphy.com/media/ye7OTQgkwLIPI/giphy.gif"
]

# --- SYSTEM EKONOMII I EKWIPUNKU ---
ECONOMY_FILE = "economy.json"

def load_economy():
    if not os.path.exists(ECONOMY_FILE):
        return {}
    with open(ECONOMY_FILE, "r") as f:
        return json.load(f)

def save_economy(data):
    with open(ECONOMY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_data(user_id):
    data = load_economy()
    str_id = str(user_id)
    if str_id not in data:
        data[str_id] = {"balance": 0, "last_daily": None, "inventory": {}}
    return data[str_id]

def update_data(user_id, key, value, mode="set"):
    data = load_economy()
    str_id = str(user_id)
    if str_id not in data:
        data[str_id] = {"balance": 0, "last_daily": None, "inventory": {}}
    
    if mode == "add":
        data[str_id][key] += value
    elif mode == "set":
        data[str_id][key] = value
    save_economy(data)

def add_item(user_id, item_code):
    data = load_economy()
    str_id = str(user_id)
    if str_id not in data: get_data(user_id)
    
    inventory = data[str_id].get("inventory", {})
    inventory[item_code] = inventory.get(item_code, 0) + 1
    data[str_id]["inventory"] = inventory
    save_economy(data)

def remove_item(user_id, item_code):
    data = load_economy()
    str_id = str(user_id)
    if str_id not in data: return False
    inventory = data[str_id].get("inventory", {})
    
    if inventory.get(item_code, 0) > 0:
        inventory[item_code] -= 1
        data[str_id]["inventory"] = inventory
        save_economy(data)
        return True
    return False

# --- CENNIK SKLEPU ---
SHOP_ROLES = {
    "VIP": 5000,
    "Bogacz": 10000,
    "Słodziak": 2500,
    "Królowa Dram": 3000
}

SHOP_ITEMS = {
    "kick_ticket": {"name": "🎫 Bilet na Kicka", "price": 15000, "desc": "Wyrzuć kogoś raz (nie działa na adminów!)"},
    "mute_ticket": {"name": "🤐 Taśma Klejąca", "price": 5000, "desc": "Wycisz kogoś na 10 min"},
    "unwarn_ticket": {"name": "📜 Czysta Kartoteka", "price": 20000, "desc": "Resetuje twoje przewinienia (RP)"}
}

# --- FUNKCJE POMOCNICZE ---
async def send_dm_log(member, guild_name, reason, action_type):
    try:
        color = KAWAII_RED if action_type == "BAN" else discord.Color.orange()
        embed = discord.Embed(title=f"🚨 Zostałeś ukarany: {action_type}!", color=color)
        embed.add_field(name="🏰 Serwer", value=guild_name, inline=False)
        embed.add_field(name="📝 Powód", value=reason, inline=False)
        embed.set_footer(text="Decyzja jest ostateczna (chyba że kupisz unbana UwU)")
        await member.send(embed=embed)
    except: pass

# --- WIDOK WERYFIKACJI ---
class VerifyView(View):
    def __init__(self, bot, member, verified_role, channel):
        super().__init__(timeout=None)
        self.bot = bot
        self.member = member
        self.verified_role = verified_role
        self.channel = channel

    @discord.ui.button(label="✅ ZATWIERDŹ (BILECIK)", style=discord.ButtonStyle.green, emoji="🎟️")
    async def verify_button(self, interaction: discord.Interaction, button: Button):
        # Tylko admin lub mod może zatwierdzić
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("⛔ Czekamy na administratora!", ephemeral=True)
            return

        await self.member.add_roles(self.verified_role)
        
        # Bonus na start
        update_data(self.member.id, "balance", 100, "add")
        
        await interaction.response.send_message(f"🎉 **{self.member.name}** zweryfikowany! Kanał zostanie usunięty za 5s.")
        
        # Powitanie na ogólnym
        general = discord.utils.get(interaction.guild.text_channels, name="ogólny")
        if general:
            embed = discord.Embed(description=f"Witamy **{self.member.mention}** w rodzinie! (≧◡≦) ♡\nNadano rolę **Bilecik był**! 🎟️", color=KAWAII_PINK)
            await general.send(embed=embed)

        await asyncio.sleep(5)
        await self.channel.delete()

# --- WIDOK SĄDU ---
class TrialView(View):
    def __init__(self, bot, member, role_izolatka, role_verified, channel):
        super().__init__(timeout=None)
        self.bot = bot
        self.member = member
        self.role_izolatka = role_izolatka
        self.role_verified = role_verified
        self.channel = channel

    @discord.ui.button(label="🔨 SKAZANIE (BAN)", style=discord.ButtonStyle.danger, emoji="⚖️")
    async def ban_button(self, interaction: discord.Interaction, button: Button):
        is_judge = "Sędzia" in [r.name for r in interaction.user.roles]
        if not is_judge and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("⛔ Tylko Sędzia może wydać wyrok!", ephemeral=True)
            return

        embed = discord.Embed(title="⚖️ WYROK ZAPADŁ!", description=f"**{self.member.name}** został uznany za winnego!\nKara: **BAN**", color=KAWAII_RED)
        embed.set_image(url=random.choice(GIFS_BAN))
        await interaction.response.send_message(embed=embed)
        
        await send_dm_log(self.member, interaction.guild.name, "Wyrok Sądu (Domena)", "BAN")
        await asyncio.sleep(3)
        try:
            await self.member.ban(reason="Wyrok Sądu (Domena)")
        except:
            await self.channel.send("❌ Błąd! Nie udało się zbanować.")
        await asyncio.sleep(2)
        await self.channel.delete()

    @discord.ui.button(label="🕊️ UŁASKAWIENIE", style=discord.ButtonStyle.success, emoji="🍀")
    async def pardon_button(self, interaction: discord.Interaction, button: Button):
        is_judge = "Sędzia" in [r.name for r in interaction.user.roles]
        if not is_judge and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("⛔ Tylko Sędzia może wydać wyrok!", ephemeral=True)
            return

        embed = discord.Embed(title="🍀 UŁASKAWIENIE", description=f"**{self.member.name}** jest wolny! Oddaję bilecik! ✨", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)
        
        try:
            await self.member.remove_roles(self.role_izolatka)
            # Oddajemy rolę "Bilecik był"
            if self.role_verified:
                await self.member.add_roles(self.role_verified)
        except:
            await self.channel.send("❌ Nie udało się zaktualizować ról.")
            
        await asyncio.sleep(5)
        await self.channel.delete()


# --- ZDARZENIA BOTA ---
@bot.event
async def on_ready():
    print(f'✨ Zalogowano jako {bot.user.name} (ID: {bot.user.id}) ✨')
    while True:
        await bot.change_presence(activity=discord.Game(name="!pomoc | Weryfikuję Bileciki 🎟️"))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Twoich sekretów 🤫"))
        await asyncio.sleep(15)

@bot.event
async def on_member_join(member):
    guild = member.guild
    
    # Znajdź lub stwórz rolę "Bilecik był"
    verified_role = discord.utils.get(guild.roles, name="Bilecik był")
    if not verified_role:
        verified_role = await guild.create_role(name="Bilecik był", color=discord.Color.from_rgb(255, 182, 193)) # LightPink

    # Tworzenie kanału weryfikacyjnego (prywatnego)
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        bot.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        # Dajemy dostęp adminom żeby mogli zatwierdzić
        guild.me: discord.PermissionOverwrite(view_channel=True, manage_channels=True) 
    }
    
    # Dodaj uprawnienia dla ról z manage_roles (modów)
    for role in guild.roles:
        if role.permissions.manage_roles:
            overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

    channel_name = f"weryfikacja-{member.name}".lower().replace("#", "")
    try:
        channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
        
        embed = discord.Embed(title=f"🌸 Witaj {member.name}!", description="Aby dostać dostęp do serwera, napisz tutaj **kilka słów o sobie**.\n\nAdministrator przeczyta to i kliknie przycisk, aby nadać Ci **Bilecik**! 🎟️", color=KAWAII_PINK)
        view = VerifyView(bot, member, verified_role, channel)
        await channel.send(f"{member.mention}", embed=embed, view=view)
    except Exception as e:
        print(f"Błąd weryfikacji: {e}")

@bot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="ogólny")
    if channel:
        embed = discord.Embed(description=f"O nie... **{member.name}** uciekł... 💔\nZostawił po sobie tylko pustkę... (qwq)", color=discord.Color.dark_grey())
        await channel.send(embed=embed)

# --- FUNKCJE SPOŁECZNOŚCIOWE (Z GIFAMI) ---

@bot.command()
async def przytul(ctx, member: discord.Member):
    """Przytula kogoś"""
    embed = discord.Embed(description=f"**{ctx.author.name}** mocno przytula **{member.name}**! ⊂(・﹏・⊂)", color=KAWAII_PINK)
    embed.set_image(url=random.choice(GIFS_HUG))
    await ctx.send(embed=embed)

@bot.command()
async def pocaluj(ctx, member: discord.Member):
    """Daje buziaka"""
    embed = discord.Embed(description=f"**{ctx.author.name}** całuje **{member.name}**! Mwa! 💋", color=KAWAII_RED)
    embed.set_image(url=random.choice(GIFS_KISS))
    await ctx.send(embed=embed)

@bot.command()
async def policzek(ctx, member: discord.Member):
    """Uderza z liścia"""
    embed = discord.Embed(description=f"**{ctx.author.name}** uderza **{member.name}**! Baka! 💢", color=0xFF4500)
    embed.set_image(url=random.choice(GIFS_SLAP))
    await ctx.send(embed=embed)

@bot.command()
async def pat(ctx, member: discord.Member):
    """Głaszcze po głowie"""
    embed = discord.Embed(description=f"**{ctx.author.name}** głaszcze **{member.name}** po główce! Grzeczny! 🌸", color=KAWAII_GOLD)
    embed.set_image(url=random.choice(GIFS_PAT))
    await ctx.send(embed=embed)

@bot.command()
async def ship(ctx, member: discord.Member):
    """Oblicza miłość"""
    procent = random.randint(0, 100)
    serca = "💖" * (procent // 10)
    msg = f"Miłość między **{ctx.author.name}** a **{member.name}** wynosi **{procent}%**!\n{serca}"
    if procent > 90: msg += "\nTo przeznaczenie! (♥ω♥*)"
    elif procent < 20: msg += "\nMoże zostańcie przyjaciółmi... (cJc)"
    await ctx.send(msg)

@bot.command()
async def kula(ctx, *, pytanie):
    """Magiczna kula"""
    odpowiedzi = ["Oczywiście! 💖", "Raczej nie... (qwq)", "To pewne! 🌟", "Nie licz na to >_<", "Spytaj później ✨"]
    await ctx.send(f"🔮 **Pytanie:** {pytanie}\n✨ **Odpowiedź:** {random.choice(odpowiedzi)}")

# --- KOMENDY ADMIN (TROLL & POWER) ---

@bot.command()
@commands.has_permissions(administrator=True)
async def sudo(ctx, member: discord.Member, *, message):
    await ctx.message.delete()
    webhook = await ctx.channel.create_webhook(name=member.display_name)
    await webhook.send(str(message), username=member.display_name, avatar_url=member.avatar.url if member.avatar else member.default_avatar.url)
    await webhook.delete()

@bot.command()
@commands.has_permissions(administrator=True)
async def fakeban(ctx, member: discord.Member):
    await ctx.message.delete()
    embed = discord.Embed(title="🔨 BAN HAMMER UDERZYŁ!", description=f"Baka **{member.name}** został zbanowany!\n**Powód:** Bycie zbyt słodkim\nNie wracaj tu bez ciasteczek! (MX_X)", color=KAWAII_RED)
    embed.set_image(url=random.choice(GIFS_BAN))
    embed.set_footer(text="To tylko żart... chyba? ( ͡° ͜ʖ ͡°)")
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    channel_pos = ctx.channel.position
    new_channel = await ctx.channel.clone()
    await new_channel.edit(position=channel_pos)
    await ctx.channel.delete()
    embed = discord.Embed(title="☢️ NUKE DETONATED ☢️", description="Kanał zresetowany! ✨", color=KAWAII_GOLD)
    embed.set_image(url=random.choice(GIFS_NUKE))
    await new_channel.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def slowmode(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"🐢 Tryb żółwia: **{seconds}s**!")

@bot.command()
@commands.has_permissions(administrator=True)
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)

# --- ADMINISTRACJA (MODERACJA) ---

@bot.command()
@commands.has_permissions(ban_members=True)
async def kick(ctx, member: discord.Member, *, reason="Brak powodu"):
    if member.top_role >= ctx.author.top_role:
        await ctx.send("❌ Nie możesz wyrzucić kogoś z wyższą rangą!")
        return
    await send_dm_log(member, ctx.guild.name, reason, "KICK")
    try:
        await member.kick(reason=reason)
        embed = discord.Embed(title="👋 WYRZUCONO!", description=f"**{member.name}** wyleciał!\n**Powód:** {reason}", color=discord.Color.orange())
        embed.set_image(url=random.choice(GIFS_KICK))
        await ctx.send(embed=embed)
    except: await ctx.send("❌ Błąd uprawnień.")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Brak powodu"):
    if member.top_role >= ctx.author.top_role:
        await ctx.send("❌ Nie możesz zbanować kogoś z wyższą rangą!")
        return
    await send_dm_log(member, ctx.guild.name, reason, "BAN")
    try:
        await member.ban(reason=reason)
        embed = discord.Embed(title="🔨 ZBANOWANO!", description=f"**{member.name}** wygnany!\n**Powód:** {reason}", color=KAWAII_RED)
        embed.set_image(url=random.choice(GIFS_BAN))
        await ctx.send(embed=embed)
    except: await ctx.send("❌ Błąd uprawnień.")

@bot.command()
@commands.has_permissions(moderate_members=True)
async def mute(ctx, member: discord.Member, minutes: int, *, reason="Spam"):
    if member.top_role >= ctx.author.top_role:
        await ctx.send("❌ Nie możesz wyciszyć admina!")
        return
    duration = timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    embed = discord.Embed(title="🤐 MUTE", description=f"**{member.name}** uciszony na **{minutes}m**.\n**Powód:** {reason}", color=discord.Color.dark_grey())
    embed.set_image(url=random.choice(GIFS_MUTE))
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send("🔒 Kanał zablokowany!")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("🔓 Kanał odblokowany!")

# --- DOMENA (SĄD Z OBSŁUGĄ RÓL) ---
@bot.command()
@commands.has_permissions(administrator=True)
async def domena(ctx, member: discord.Member):
    guild = ctx.guild
    
    # Obsługa ról
    judge_role = discord.utils.get(guild.roles, name="Sędzia")
    if not judge_role: judge_role = await guild.create_role(name="Sędzia", color=discord.Color.gold(), hoist=True)
    
    jail_role = discord.utils.get(guild.roles, name="Izolatka")
    if not jail_role:
        jail_role = await guild.create_role(name="Izolatka", color=discord.Color.dark_grey())
        for channel in guild.channels: await channel.set_permissions(jail_role, view_channel=False)

    verified_role = discord.utils.get(guild.roles, name="Bilecik był")
    
    # Zabieramy bilecik, dajemy izolatkę
    if verified_role and verified_role in member.roles:
        await member.remove_roles(verified_role)
    await member.add_roles(jail_role)
    
    # Tworzenie kanału sądu
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        jail_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        judge_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        bot.user: discord.PermissionOverwrite(view_channel=True)
    }
    
    channel_name = f"sąd-nad-{member.name}".lower().replace("#", "")
    trial_channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
    
    embed = discord.Embed(title="⚖️ DOMENA SĄDOWA", description=f"Oskarżony: {member.mention}\nZabrano rolę **Bilecik był**.", color=0x800000)
    embed.set_image(url="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnY2Y2gxeDR3MGMydDM3YjRpa2JhZjluZGJ5YWlobnp0YTM2eDc2YiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/A3Fe9A2d3bbDXxxR6t/giphy.gif")
    
    # Przekazujemy role do View, aby przy ułaskawieniu je zamienić
    view = TrialView(bot, member, jail_role, verified_role, trial_channel)
    await trial_channel.send(f"{member.mention} {judge_role.mention}", embed=embed, view=view)
    await ctx.send(f"⛓️ **{member.name}** trafił do Domeny (stracił Bilecik)!")

# --- EKONOMIA I SKLEP ---

@bot.command()
async def portfel(ctx):
    data = get_data(ctx.author.id)
    inv_text = ""
    for item, count in data["inventory"].items():
        if count > 0:
            name = SHOP_ITEMS.get(item, {}).get("name", item)
            inv_text += f"\n📦 **{name}**: x{count}"
    if not inv_text: inv_text = "\n*(Pusto...)*"
    embed = discord.Embed(title="👛 Twój Portfel", color=KAWAII_GOLD)
    embed.add_field(name="💰 Monetki", value=f"**{data['balance']}**", inline=False)
    embed.add_field(name="🎒 Plecak", value=inv_text, inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def daily(ctx):
    user_id = str(ctx.author.id)
    data = get_data(user_id)
    now = datetime.now()
    if data["last_daily"]:
        last = datetime.fromisoformat(data["last_daily"])
        if now - last < timedelta(hours=24):
            await ctx.send(f"⏳ Wróć jutro! (Cooldown)")
            return
    update_data(user_id, "balance", 200, "add")
    data = load_economy()
    data[user_id]["last_daily"] = now.isoformat()
    save_economy(data)
    await ctx.send("🎁 Odebrałeś **200** monet!")

@bot.command()
async def sklep(ctx):
    embed = discord.Embed(title="🏪 Super Sklep Kawaii", description="Wpisz `!kup <nazwa>`", color=KAWAII_PINK)
    roles_txt = ""
    for r, p in SHOP_ROLES.items(): roles_txt += f"🏷️ **{r}** - `{p}`\n"
    embed.add_field(name="👑 Role", value=roles_txt, inline=False)
    items_txt = ""
    for k, v in SHOP_ITEMS.items(): items_txt += f"📦 **{k}** ({v['name']}) - `{v['price']}`\n*{v['desc']}*\n"
    embed.add_field(name="🛠️ Przedmioty", value=items_txt, inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def kup(ctx, *, item_name):
    user_id = ctx.author.id
    balance = get_data(user_id)["balance"]
    
    for r, p in SHOP_ROLES.items():
        if r.lower() == item_name.lower():
            if balance < p:
                await ctx.send("💸 Nie stać cię!")
                return
            role_obj = discord.utils.get(ctx.guild.roles, name=r)
            if not role_obj:
                await ctx.send("❌ Rola nie istnieje.")
                return
            update_data(user_id, "balance", balance - p, "set")
            await ctx.author.add_roles(role_obj)
            await ctx.send(f"🎉 Kupiłeś rolę **{r}**!")
            return

    if item_name in SHOP_ITEMS:
        item = SHOP_ITEMS[item_name]
        if balance < item["price"]:
            await ctx.send("💸 Nie stać cię!")
            return
        update_data(user_id, "balance", balance - item["price"], "set")
        add_item(user_id, item_name)
        await ctx.send(f"🎒 Kupiłeś **{item['name']}**! Użyj komendą `!uzyj`.")
        return
    await ctx.send("❌ Nie ma takiego towaru.")

@bot.command()
async def uzyj(ctx, item_code, target: discord.Member = None):
    user_id = ctx.author.id
    data = get_data(user_id)
    inventory = data.get("inventory", {})
    if inventory.get(item_code, 0) <= 0:
        await ctx.send("❌ Nie masz tego przedmiotu!")
        return

    if item_code == "kick_ticket":
        if not target or target.guild_permissions.administrator:
            await ctx.send("⚠️ Błąd celu!")
            return
        remove_item(user_id, item_code)
        try:
            await target.kick(reason="Użycie przedmiotu")
            await ctx.send(f"👋 **{target.name}** wyrzucony biletem!")
        except:
            add_item(user_id, item_code)
            await ctx.send("❌ Błąd bota.")

    elif item_code == "mute_ticket":
        if not target or target.guild_permissions.administrator:
            await ctx.send("⚠️ Błąd celu!")
            return
        remove_item(user_id, item_code)
        await target.timeout(timedelta(minutes=10), reason="Przedmiot")
        await ctx.send(f"🤐 **{target.name}** wyciszony!")

    elif item_code == "unwarn_ticket":
        remove_item(user_id, item_code)
        await ctx.send(f"📜 **{ctx.author.name}** czyści kartotekę!")

# --- GRY ---
@bot.command()
async def slots(ctx, amount: int):
    bal = get_data(ctx.author.id)["balance"]
    if bal < amount: return
    update_data(ctx.author.id, "balance", bal - amount, "set")
    emojis = ["🍒", "💎", "7️⃣"]
    a, b, c = random.choice(emojis), random.choice(emojis), random.choice(emojis)
    msg = await ctx.send(f"🎰 | {a} | {b} | {c} |")
    if a == b == c:
        win = amount * 5
        update_data(ctx.author.id, "balance", win, "add")
        await ctx.send(f"🎉 JACKPOT! +{win}")
    else: await ctx.send("❌ Przegrana.")

@bot.command()
async def rzut(ctx, amount: int, wybor: str):
    bal = get_data(ctx.author.id)["balance"]
    if bal < amount: return
    update_data(ctx.author.id, "balance", bal - amount, "set")
    wynik = random.choice(["orzeł", "reszka"])
    if wybor.lower() in [wynik, "orzel" if wynik=="orzeł" else "x"]:
        win = amount * 2
        update_data(ctx.author.id, "balance", win, "add")
        await ctx.send(f"🪙 Wypadł {wynik}! Wygrywasz {win}!")
    else: await ctx.send(f"🪙 Wypadł {wynik}. Przegrałeś.")

# --- UTILITY ---
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(title=f"🌸 {member.name}", color=member.color)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Konto od", value=member.created_at.strftime("%Y-%m-%d"))
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(title=f"🏰 {guild.name}", color=KAWAII_GOLD)
    embed.add_field(name="Właściciel", value=guild.owner.mention)
    embed.add_field(name="Liczba osób", value=guild.member_count)
    if guild.icon: embed.set_thumbnail(url=guild.icon.url)
    await ctx.send(embed=embed)

# --- POMOC ---
@bot.command()
async def pomoc(ctx):
    embed = discord.Embed(title="🌸 Menu Główne", color=KAWAII_PINK)
    embed.add_field(name="💰 Ekonomia", value="`!sklep`, `!kup`, `!uzyj`, `!portfel`, `!daily`", inline=False)
    embed.add_field(name="🎰 Gry", value="`!slots`, `!rzut`", inline=False)
    embed.add_field(name="🧸 Social", value="`!przytul`, `!pocaluj`, `!policzek`, `!pat`, `!ship`, `!kula`", inline=False)
    embed.add_field(name="ℹ️ Info", value="`!userinfo`, `!serverinfo`", inline=False)
    embed.set_footer(text="Dla adminów: !pomoca")
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def pomoca(ctx):
    embed = discord.Embed(title="🛡️ Menu Admina", color=KAWAII_RED)
    embed.add_field(name="😈 Troll", value="`!sudo`, `!fakeban`", inline=False)
    embed.add_field(name="☢️ Admin", value="`!nuke`, `!slowmode`, `!lock`, `!unlock`, `!say`", inline=False)
    embed.add_field(name="⚖️ Kary", value="`!ban`, `!kick`, `!mute`, `!domena`", inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("⛔ Brak uprawnień!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Brakuje argumentu!")
    else: print(f"Error: {error}")

# --- URUCHOMIENIE ---
# ... (START KEEPALIVE)
keep_alive()

# POBIERANIE TOKENU ZE ZMIENNYCH ŚRODOWISKOWYCH (BEZPIECZNIE)
TOKEN = os.environ.get('DISCORD_TOKEN')

if not TOKEN:
    print("❌ Błąd: Nie znaleziono tokenu w zmiennych środowiskowych (Environment Variables)!")
    print("Upewnij się, że dodałeś DISCORD_TOKEN w ustawieniach Render.")
else:
    bot.run(TOKEN)