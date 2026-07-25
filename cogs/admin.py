import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import asyncio
from datetime import datetime, timedelta, timezone
from typing import Union
from utils import KAWAII_RED, KAWAII_PINK, KAWAII_GOLD, update_data, get_profile_data, update_profile


# Gify
GIFS_BAN = ["https://media.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif", "https://media.giphy.com/media/AC1HrkBir3bzq/giphy.gif"]
GIFS_KICK = ["https://media.giphy.com/media/wQCWMHY9EHLfq/giphy.gif", "https://media.giphy.com/media/26FPn4rR1damB0MQo/giphy.gif"]
GIFS_MUTE = ["https://media.giphy.com/media/hfBvLPfHXRLO1gYgJv/giphy.gif", "https://media.giphy.com/media/liW10vuLjuUA8/giphy.gif"]
GIFS_NUKE = ["https://media.giphy.com/media/OE6FE4GZF78nm/giphy.gif"]

def has_perms_or_borysiaczek(**perms):
    def predicate(ctx):
        if ctx.author.name.lower() in ["≽^borysiaczekuwu^≼", "borysiaczekuwu"]:
            return True
        permissions = ctx.channel.permissions_for(ctx.author)
        missing = [perm for perm, value in perms.items() if getattr(permissions, perm) != value]
        if not missing:
            return True
        raise commands.MissingPermissions(missing)
    return commands.check(predicate)

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

class QTEView(View):
    def __init__(self, amount: int, max_users: int, timeout: int):
        super().__init__(timeout=timeout)
        self.amount = amount
        self.max_users = max_users
        self.claimed_users = set()
        self.message = None

    @discord.ui.button(label="ZGARNIJ KASĘ!", style=discord.ButtonStyle.success, emoji="💸")
    async def claim_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id in self.claimed_users:
            return await interaction.response.send_message("❌ Już odebrałeś zrzut!", ephemeral=True)
            
        if len(self.claimed_users) >= self.max_users:
            button.disabled = True
            await interaction.message.edit(view=self)
            return await interaction.response.send_message("😢 Niestety, inni byli szybsi!", ephemeral=True)
            
        self.claimed_users.add(interaction.user.id)
        update_data(interaction.user.id, "balance", self.amount, "add")
        await interaction.response.send_message(f"🎉 Brawo! Zgarniasz **{self.amount} monet**!", ephemeral=True)
        
        if len(self.claimed_users) >= self.max_users:
            button.disabled = True
            button.label = f"Wyczerpane ({self.max_users}/{self.max_users})"
            button.style = discord.ButtonStyle.secondary
            await interaction.message.edit(view=self)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
            child.label = f"Koniec czasu! ({len(self.claimed_users)}/{self.max_users})"
            child.style = discord.ButtonStyle.secondary
        if self.message:
            try:
                await self.message.edit(view=self)
            except: pass

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- KOMENDY ---
    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def sudo(self, ctx, member: discord.Member, *, message):
        """Pisze jako inny użytkownik (Webhook)"""
        await ctx.message.delete()
        webhook = await ctx.channel.create_webhook(name=member.display_name)
        await webhook.send(str(message), username=member.display_name, avatar_url=member.avatar.url or member.default_avatar.url)
        await webhook.delete()

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def fakeban(self, ctx, member: discord.Member):
        """Udawany ban"""
        await ctx.message.delete()
        embed = discord.Embed(title="🔨 BAN HAMMER!", description=f"Baka **{member.name}** zbanowany!\nPowód: Bycie zbyt słodkim", color=KAWAII_RED)
        embed.set_image(url=random.choice(GIFS_BAN))
        embed.set_footer(text="To tylko żart... ( ͡° ͜ʖ ͡°)")
        await ctx.send(embed=embed)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def dm(self, ctx, member: discord.Member, *, message):
        """Wysyła wiadomość prywatną jako bot"""
        await ctx.message.delete()
        try:
            await member.send(f"📩 **Wiadomość od Administracji:**\n{message}")
            await ctx.send(f"✅ Wysłano DM do {member.name}.", delete_after=5)
        except:
            await ctx.send(f"❌ Użytkownik ma zablokowane DM.", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def duch(self, ctx, member: discord.Member):
        """(Troll) Straszy użytkownika na DM"""
        await ctx.message.delete()
        try:
            await member.send("👻 BUUU! Widzę Cię... 👀")
            await ctx.send(f"👻 Nastraszono {member.name}!", delete_after=5)
        except:
             await ctx.send("❌ Nie udało się nastraszyć (DM zablokowane).")

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def nuke(self, ctx):
        pos = ctx.channel.position
        new_ch = await ctx.channel.clone()
        await new_ch.edit(position=pos)
        await ctx.channel.delete()
        embed = discord.Embed(title="☢️ NUKE!", description="Kanał zresetowany! ✨", color=KAWAII_GOLD)
        embed.set_image(url=random.choice(GIFS_NUKE))
        await new_ch.send(embed=embed)

    @commands.command()
    @has_perms_or_borysiaczek(manage_messages=True)
    async def clear_user(self, ctx, member: discord.Member, amount: int = 10):
        """Wyczyść wiadomości konkretnej osoby"""
        def check(m):
            return m.author == member

        deleted = await ctx.channel.purge(limit=amount, check=check)
        await ctx.send(f"🗑️ Usunięto **{len(deleted)}** wiadomości od {member.name}.", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(manage_channels=True)
    async def lockdown(self, ctx):
        """Zablokuj kanał dla @everyone"""
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 KANAŁ ZABLOKOWANY!")

    @commands.command()
    @has_perms_or_borysiaczek(manage_channels=True)
    async def unlockdown(self, ctx):
        """Odblokuj kanał dla @everyone"""
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("🔓 KANAŁ ODBLOKOWANY!")

    @commands.command()
    @has_perms_or_borysiaczek(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"🐢 Slowmode: **{seconds}s**!")

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    @has_perms_or_borysiaczek(manage_roles=True)
    async def nadaj_role(self, ctx, member: discord.Member, role: discord.Role):
        if ctx.author.top_role <= role:
            return await ctx.send("⛔ Ta rola jest powyżej Twojej!")
        try:
            await member.add_roles(role)
            await ctx.send(f"✅ Nadano rolę **{role.name}** użytkownikowi {member.mention}!")
        except Exception as e:
            await ctx.send(f"❌ Błąd: {e}")

    @commands.command()
    @has_perms_or_borysiaczek(manage_roles=True)
    async def zabierz_role(self, ctx, member: discord.Member, role: discord.Role):
        if ctx.author.top_role <= role:
            return await ctx.send("⛔ Ta rola jest powyżej Twojej!")
        try:
            await member.remove_roles(role)
            await ctx.send(f"🗑️ Zabrano rolę **{role.name}** użytkownikowi {member.mention}!")
        except Exception as e:
            await ctx.send(f"❌ Błąd: {e}")

    @commands.command()
    @has_perms_or_borysiaczek(ban_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Brak"):
        if member.top_role >= ctx.author.top_role: return
        await send_dm_log(member, ctx.guild.name, reason, "KICK")
        try:
            await member.kick(reason=reason)
            embed = discord.Embed(title="👋 WYRZUCONO!", description=f"**{member.name}** wyleciał!\nPowód: {reason}", color=discord.Color.orange())
            embed.set_image(url=random.choice(GIFS_KICK))
            await ctx.send(embed=embed)
        except: await ctx.send("❌ Błąd.")

    @commands.command()
    @has_perms_or_borysiaczek(ban_members=True)
    async def ban(self, ctx, target: Union[discord.Member, discord.User], *, reason="Brak"):
        if isinstance(target, discord.Member):
            if target.top_role >= ctx.author.top_role: return
        await send_dm_log(target, ctx.guild.name, reason, "BAN")
        try:
            await ctx.guild.ban(target, reason=reason)
            embed = discord.Embed(title="🔨 ZBANOWANO!", description=f"**{target.name}** wygnany!\nPowód: {reason}", color=KAWAII_RED)
            embed.set_image(url=random.choice(GIFS_BAN))
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Błąd: {e}")

    @commands.command()
    @has_perms_or_borysiaczek(ban_members=True)
    async def unban(self, ctx, *, user_input):
        """Odbanowuje użytkownika (ID lub nazwa)"""
        try:
            user_id = int(user_input)
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user)
            await ctx.send(f"🔓 Odbanowano **{user.name}**!")
            return
        except: pass
        
        banned_users = [entry async for entry in ctx.guild.bans()]
        for ban_entry in banned_users:
            user = ban_entry.user
            if user.name == user_input:
                await ctx.guild.unban(user)
                await ctx.send(f"🔓 Odbanowano **{user.name}**!")
                return
        await ctx.send("❌ Nie znaleziono takiego bana.")

    @commands.command()
    @has_perms_or_borysiaczek(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int, *, reason="Spam"):
        if member.top_role >= ctx.author.top_role: return
        await member.timeout(timedelta(minutes=minutes), reason=reason)
        embed = discord.Embed(title="🤐 MUTE", description=f"**{member.name}** uciszony na **{minutes}m**.", color=discord.Color.dark_grey())
        embed.set_image(url=random.choice(GIFS_MUTE))
        await ctx.send(embed=embed)

    @commands.command()
    @has_perms_or_borysiaczek(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        """Zdejmuje wyciszenie"""
        if member.top_role >= ctx.author.top_role: return
        await member.timeout(None)
        await ctx.send(f"🔊 **{member.name}** odzyskał głos!")

    @commands.command()
    @has_perms_or_borysiaczek(manage_messages=True)
    async def purge(self, ctx, amount: int = 10):
        """Usuwa określoną liczbę wiadomości"""
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🗑️ Wyczyszczono **{amount}** wiadomości!", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(manage_channels=True)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 Zablokowano!")

    @commands.command()
    @has_perms_or_borysiaczek(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("🔓 Odblokowano!")

    # --- SYSTEM OSTRZEŻEŃ (WARNS) ---
    def load_warns(self):
        import json
        import os
        if not os.path.exists("data/warns.json"):
            if not os.path.exists("data"): os.makedirs("data")
            with open("data/warns.json", "w") as f: json.dump({}, f)
        with open("data/warns.json", "r") as f: return json.load(f)

    def save_warns(self, warns_data):
        import json
        with open("data/warns.json", "w") as f: json.dump(warns_data, f, indent=4)

    def load_forbidden_words(self):
        import json
        import os
        if not os.path.exists("data/forbidden_words.json"):
            if not os.path.exists("data"): os.makedirs("data")
            # Default forbidden words to preserve original behavior
            default_words = ["praca", "zatrudnienie"]
            with open("data/forbidden_words.json", "w", encoding="utf-8") as f:
                json.dump(default_words, f, ensure_ascii=False, indent=4)
            return default_words
        with open("data/forbidden_words.json", "r", encoding="utf-8") as f:
            return json.load(f)

    def save_forbidden_words(self, words):
        import json
        with open("data/forbidden_words.json", "w", encoding="utf-8") as f:
            json.dump(words, f, ensure_ascii=False, indent=4)

    @commands.command()
    @has_perms_or_borysiaczek(moderate_members=True)
    async def warn(self, ctx, member: discord.Member, *, reason="Brak powodu"):
        """Narzędzia: Nadaje ostrzeżenie użytkownikowi."""
        if member.bot or member.top_role >= ctx.author.top_role:
            return await ctx.send("⛔ Nie możesz nadać warna temu użytkownikowi.")
        
        warns = self.load_warns()
        user_id = str(member.id)
        if user_id not in warns: warns[user_id] = []
        
        warns[user_id].append({"reason": reason, "moderator": ctx.author.name, "date": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))})
        self.save_warns(warns)

        embed = discord.Embed(title="⚠️ OSTRZEŻENIE", description=f"Użytkownik {member.mention} otrzymał ostrzeżenie!", color=discord.Color.orange())
        embed.add_field(name="Powód:", value=reason)
        embed.set_footer(text=f"Aktualna liczba ostrzeżeń: {len(warns[user_id])}")
        await ctx.send(embed=embed)
        try: await member.send(f"⚠️ Zostałeś ostrzeżony na serwerze **{ctx.guild.name}** za: `{reason}`.")
        except: pass

    @commands.command(aliases=['warns'])
    @has_perms_or_borysiaczek(moderate_members=True)
    async def warnings(self, ctx, member: discord.Member):
        """Pokazuje listę ostrzeżeń użytkownika."""
        warns = self.load_warns()
        user_id = str(member.id)
        
        if user_id not in warns or len(warns[user_id]) == 0:
            return await ctx.send(f"✨ {member.name} ma czyste konto!")

        embed = discord.Embed(title=f"⚠️ Ostrzeżenia: {member.name}", color=discord.Color.orange())
        for idx, w in enumerate(warns[user_id], 1):
            embed.add_field(name=f"Warn #{idx} (od {w['moderator']})", value=f"Powód: {w['reason']}\nData: {w['date']}", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def clearwarns(self, ctx, member: discord.Member):
        """Czyści wszystkie ostrzeżenia użytkownika."""
        warns = self.load_warns()
        user_id = str(member.id)
        if user_id in warns:
            warns[user_id] = []
            self.save_warns(warns)
            await ctx.send(f"🧹 Pomyślnie wyczyszczono wszystkie ostrzeżenia dla {member.name}!")
        else:
            await ctx.send(f"⚠️ {member.name} nie ma żadnych ostrzeżeń.")

    @commands.command(name="dodaj_slowo", aliases=["add_badword"])
    @has_perms_or_borysiaczek(administrator=True)
    async def dodaj_slowo(self, ctx, *, slowo: str):
        """[MODERACJA] Dodaje słowo do listy słów zakazanych."""
        slowo = slowo.strip().lower()
        if not slowo:
            return await ctx.send("⚠️ Słowo nie może być puste!")
        
        words = self.load_forbidden_words()
        if slowo in words:
            embed = discord.Embed(title="⚠️ Błąd", description=f"Słowo `{slowo}` jest już na liście zakazanych słów.", color=discord.Color.orange())
            return await ctx.send(embed=embed)
        
        words.append(slowo)
        self.save_forbidden_words(words)
        
        embed = discord.Embed(title="✅ Dodano słowo zakazane", description=f"Pomyślnie dodano słowo `{slowo}` do listy zakazanych słów.", color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name="usun_slowo", aliases=["remove_badword"])
    @has_perms_or_borysiaczek(administrator=True)
    async def usun_slowo(self, ctx, *, slowo: str):
        """[MODERACJA] Usuwa słowo z listy słów zakazanych."""
        slowo = slowo.strip().lower()
        if not slowo:
            return await ctx.send("⚠️ Słowo nie może być puste!")
            
        words = self.load_forbidden_words()
        if slowo not in words:
            embed = discord.Embed(title="⚠️ Błąd", description=f"Słowo `{slowo}` nie znajduje się na liście zakazanych słów.", color=discord.Color.orange())
            return await ctx.send(embed=embed)
            
        words.remove(slowo)
        self.save_forbidden_words(words)
        
        embed = discord.Embed(title="✅ Usunięto słowo zakazane", description=f"Pomyślnie usunięto słowo `{slowo}` z listy zakazanych słów.", color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name="zakazane", aliases=["zakazane_slowa", "badwords"])
    @has_perms_or_borysiaczek(moderate_members=True)
    async def zakazane(self, ctx):
        """[MODERACJA] Pokazuje listę wszystkich słów zakazanych."""
        words = self.load_forbidden_words()
        if not words:
            embed = discord.Embed(title="🚫 Zakazane Słowa", description="Lista słów zakazanych jest obecnie pusta.", color=KAWAII_PINK)
            return await ctx.send(embed=embed)
            
        words_formatted = ", ".join(f"`{w}`" for w in words)
        embed = discord.Embed(title="🚫 Lista Zakazanych Słów", description=words_formatted, color=KAWAII_PINK)
        embed.set_footer(text=f"Łącznie słów: {len(words)}")
        await ctx.send(embed=embed)

    @commands.command()
    async def temat(self, ctx):
        """Podaje losowy temat do rozmowy lub kontrowersyjne pytanie."""
        topics = [
            "Czy ananas pasuje na pizzę?",
            "Gdybyś mógł zamienić się z kimś życiem na jeden dzień, kto by to był?",
            "Jaka jest najbardziej bezużyteczna supermoc, jaką mógłbyś mieć?",
            "Czy hot dog to kanapka?",
            "Jaka jest twoja najbardziej kontrowersyjna opinia, której nikt nie popiera?",
            "Jeśli kosmici wylądowali na Ziemi i kazali ci opisać ludzkość w trzech słowach, co byś powiedział?",
            "Keczup na frytkach, obok frytek, czy bez keczupa?",
            "Czy płatki z mlekiem to zupa?",
            "Jaka jest najgorsza wymówka, jakiej kiedykolwiek użyłeś z sukcesem?",
            "Co było pierwsze: jajko czy kura?",
            "Gdybyś musiał jeść tylko jeden posiłek do końca życia, co by to było?",
            "Kawa czy herbata? Dlaczego?",
            "Czy zawsze trzeba mówić prawdę, nawet jeśli kogoś to zrani?",
            "Gdybyś miał wehikuł czasu, wolałbyś cofnąć się w przeszłość czy polecieć w przyszłość?",
            "Jakie jest najgłupsze prawo, o którym słyszałeś?",
            "Psy czy koty?",
            "Czy wierzysz w istnienie duchów?",
            "Czy zdrada emocjonalna jest gorsza od fizycznej?",
            "Co jest ważniejsze: miłość czy pieniądze?",
            "Jeśli mógłbyś zlikwidować jedną rzecz na świecie, co by to było?",
            "Czy lepsza jest bolesna prawda czy słodkie kłamstwo?",
            "Jaka jest najdziwniejsza rzecz w twojej lodówce?",
            "Czy to w porządku płakać w miejscach publicznych?",
            "Gdybyś mógł ożywić jedną postać z filmu/książki, kto by to był?",
            "Czy inteligencja to przekleństwo czy dar?",
            "Wolałbyś stracić węch czy smak?",
            "Czy ludzie w dzisiejszych czasach są bardziej samotni z powodu internetu?",
            "Co jest najgorszą cechą u drugiego człowieka?",
            "Jeśli twoje życie byłoby filmem, jaki by nosiło tytuł?",
            "Jakiego przedmiotu powinno się uczyć w szkole, a się nie uczy?",
            "Czy jesteśmy sami we wszechświecie?",
            "Co jest Twoim największym lękiem?",
            "Wolałbyś wiedzieć KIEDY umrzesz czy JAK umrzesz?",
            "Jaka jest najlepsza wymówka od wyjścia na imprezę?",
            "Czy wierzysz, że wszystko dzieje się po coś?",
            "Z jakim historycznym władcą umówiłbyś się na piwo?",
            "Jaki jest twój ulubiony suchar?",
            "Gdybyś obudził się z milionem złotych, co kupiłbyś najpierw?",
            "Jaka gra komputerowa zasługuje na miano arcydzieła?",
            "W jakim uniwersum z filmów lub gier chciałbyś zamieszkać?",
            "Co myślisz o sztucznej inteligencji, zabierze nam pracę czy pomoże?",
            "Najbardziej przypałowa sytuacja z czasów szkolnych to...?",
            "Czy wierzysz w karmę?",
            "Jaka jest jedyna rzecz, której nigdy byś nie zrobił nawet za milion dolarów?",
            "Czy lepiej być biednym i szczęśliwym, czy bogatym i nieszczęśliwym?",
            "Co jest najtrudniejsze w byciu dorosłym?",
            "Jaką jedną rzecz powiedziałbyś sobie 10 lat temu?",
            "Czy łatwiej jest wybaczyć czy zapomnieć?",
            "Jaka piosenka idealnie opisuje twój obecny nastrój?",
            "Czym według ciebie jest prawdziwe szczęście?"
        ]
        embed = discord.Embed(title="🗣️ Temat do rozmowy", description=random.choice(topics), color=0x3498db)
        await ctx.send(embed=embed)

    @commands.command()
    async def pochwal(self, ctx):
        """Wysyła pozytywną wiadomość dla całego serwera, by każdemu umilić dzień."""
        compliments = [
            "Jesteście niesamowici! Dziękuję, że tu jesteście!",
            "Ten serwer nie byłby taki sam bez Was wszystkich. Jesteście super! ❤️",
            "Każdy z Was wnosi tu tyle dobrej energii, oby tak dalej!",
            "Pamiętajcie, że każdy z Was jest wartościowy i wyjątkowy. Miłego dnia!",
            "Uwielbiam czas spędzany z Wami. Jesteście najlepszą społecznością. 🥰",
            "Jesteście dowodem na to, że w internecie można znaleźć cudownych ludzi!",
            "Wysyłam dużo uścisków i pozytywnej energii dla każdego z Was! ✨",
            "Oby dzisiejszy dzień przyniósł Wam same powody do uśmiechu!",
            "Jesteście jak promień słońca w pochmurny dzień. Trzymajcie się cieplutko!",
            "Dobra robota za samo bycie sobą! Ten serwer ma szczęście, że Was ma. 🌟"
        ]
        embed = discord.Embed(title="🌸 Chwila pozytywności", description=random.choice(compliments), color=KAWAII_PINK)
        await ctx.send(embed=embed)

    @commands.command()
    @has_perms_or_borysiaczek(manage_nicknames=True)
    async def chname(self, ctx, member: discord.Member, *, new_name):
        """[ZARZĄDZANIE] Zmienia pseudonim użytkownika na serwerze."""
        try:
            old_name = member.display_name
            await member.edit(nick=new_name)
            await ctx.send(f"✅ Zmieniono nick z **{old_name}** na **{new_name}**!")
        except Exception as e:
            await ctx.send(f"❌ Nie mogłem zmienić nicku: {e}")

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def qte(self, ctx, kwota: int, minuty: int, max_osob: int):
        """[EVENT] Quick Time Event! Rzuca pieniądze na czat."""
        await ctx.message.delete()
        if kwota <= 0 or minuty <= 0 or max_osob <= 0:
            return await ctx.send("Parametry muszą być większe od 0!", delete_after=5)
            
        embed = discord.Embed(
            title="⚡ QUICK TIME EVENT! ⚡",
            description=f"Admin rzucił pieniędzmi!\nCzeka na was **{kwota} monet**!\n"
                        f"⏰ Czas: **{minuty} min**\n👥 Maksymalnie dla: **{max_osob} osób**\n\nKliknij przycisk poniżej, aby zgarnąć kasę!",
            color=KAWAII_GOLD
        )
        embed.set_image(url="https://media.giphy.com/media/l0Ex6kAKAoFRsFh6M/giphy.gif")
        
        view = QTEView(amount=kwota, max_users=max_osob, timeout=minuty * 60)
        msg = await ctx.send(embed=embed, view=view)
        view.message = msg

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def ankieta(self, ctx, *, tresc):
        """[ZARZĄDZANIE] Tworzy ankietę (pytanie | opcja1 | opcja2)"""
        await ctx.message.delete()
        elementy = [e.strip() for e in tresc.split("|")]
        if len(elementy) < 2:
            embed = discord.Embed(title="📊 Szybka Ankieta", description=tresc, color=KAWAII_PINK)
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("👍")
            await msg.add_reaction("👎")
            return
            
        pytanie = elementy[0]
        opcje = elementy[1:]
        if len(opcje) > 10:
            return await ctx.send("❌ Maksymalnie 10 opcji!", delete_after=5)
            
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        opis = ""
        for i, opcja in enumerate(opcje):
            opis += f"{emojis[i]} **{opcja}**\n\n"
            
        embed = discord.Embed(title=f"📊 {pytanie}", description=opis, color=KAWAII_PINK)
        embed.set_footer(text=f"Zadane przez {ctx.author.name}")
        msg = await ctx.send(embed=embed)
        for i in range(len(opcje)):
            await msg.add_reaction(emojis[i])

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def ogloszenie(self, ctx, *, tresc):
        """[ZARZĄDZANIE] Wysyła oficjalne ogłoszenie."""
        await ctx.message.delete()
        embed = discord.Embed(title="📢 OGŁOSZENIE", description=tresc, color=KAWAII_RED)
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.set_footer(text=f"Nadane przez dumną Administrację")
        await ctx.send(embed=embed)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def wyroznij(self, ctx, member: discord.Member, *, powod="Za bycie wspaniałym!"):
        """[SOCIAL] Wyróżnia użytkownika i daje mu 500 monet."""
        await ctx.message.delete()
        update_data(member.id, "balance", 500, "add")
        
        embed = discord.Embed(
            title="🌸 CERTYFIKAT SŁODZIAKA 🌸",
            description=f"Dzisiejsze specjalne wyróżnienie wędruje do...\n\n💖 {member.mention} 💖\n\n**Za co?**\n*{powod}*",
            color=KAWAII_PINK
        )
        embed.add_field(name="Nagroda", value="W wirtualnym portfelu ląduje bonusowe **500 monet**! 💰")
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_image(url="https://media.giphy.com/media/26vUxJ9rqfwuIEkTu/giphy.gif")
        await ctx.send(embed=embed)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def fake_mute(self, ctx, member: discord.Member, minuty: int = 10):
        """[TROLL] Wysyła info o mutowaniu użytkownika, ale tego nie robi."""
        await ctx.message.delete()
        embed = discord.Embed(
            title="🤐 MUTE", 
            description=f"**{member.name}** uciszony na **{minuty}m**.", 
            color=discord.Color.dark_grey()
        )
        embed.set_image(url=random.choice(GIFS_MUTE))
        embed.set_footer(text="(Ale tak naprawdę nie 🤫)")
        await ctx.send(embed=embed)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def scam_nitro(self, ctx, member: discord.Member):
        """[TROLL] Wysyła Rickrolla zapakowanego w fejkowe Nitro jako DM."""
        await ctx.message.delete()
        embed = discord.Embed(
            title="🎁 Masz prezent!",
            description="Znajomy podarował Ci subskrypcję **Discord Nitro** na 1 miesiąc!\n\n**[Kliknij tutaj, aby odebrać](https://c.tenor.com/_4YgA77ExHEAAAAC/tenor.gif)**",
            color=0x2b2d31
        )
        embed.set_thumbnail(url="https://i.imgur.com/w9aiD6n.png")
        try:
            await member.send(embed=embed)
            await ctx.send(f"😜 Fejkowe nitro wysłane do {member.name}!", delete_after=5)
        except:
            await ctx.send(f"❌ {member.name} ma zablokowane DM.", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def impreza(self, ctx):
        """[SOCIAL] Rozpoczyna wielką imprezę na kanale!"""
        await ctx.message.delete()
        embed = discord.Embed(
            title="🎉 IMPREZA! 🎊",
            description=f"{ctx.author.mention} rozkręca imprezę!\nWszycy na parkiet! 🕺💃",
            color=KAWAII_GOLD
        )
        embed.set_image(url="https://media.giphy.com/media/l2JHRhAtnJSDNJ2py/giphy.gif")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("🥳")
        await msg.add_reaction("🍻")
        await msg.add_reaction("✨")

    @commands.command()
    async def rosyjska_ruletka(self, ctx):
        """[TROLL] Rosyjska ruletka. 1/6 szans na wyrzucenie (kick) z serwera!"""
        if random.randint(1, 6) == 1:
            try:
                await ctx.author.send("💥 Pif paf! Przegrałeś w ruletkę...")
                await ctx.author.kick(reason="Przegrał w rosyjską ruletkę.")
                await ctx.send(f"💥 **{ctx.author.name}** przegrał w ruletkę i wyleciał z serwera!")
            except:
                await ctx.send(f"💥 **{ctx.author.name}** miał wylecieć przez ruletkę, ale ma zbyt potężną zbroję (brak uprawnień)!")
        else:
            await ctx.send(f"🔫 *Klik*... **{ctx.author.name}** miał szczęście. Następnym razem uważaj!")

    @commands.command()
    async def prawdziwa_ruletka(self, ctx):
        """[WYZWANIE] Prawdziwa ruletka. 1/6 szans na permanentnego bana, ale 5/6 szans na 100,000 monet!"""
        if random.randint(1, 6) == 1:
            try:
                await ctx.author.send("💥 Pif paf! Przegrałeś w prawdziwą ruletkę... Żegnaj na zawsze.")
                await ctx.author.ban(reason="Przegrał w prawdziwą ruletkę.")
                await ctx.send(f"💥 **{ctx.author.name}** przegrał w prawdziwą ruletkę i wyleciał z serwera z hukiem!")
            except:
                await ctx.send(f"💥 **{ctx.author.name}** miał dostać perma-bana przez ruletkę, ale ma zbyt potężną zbroję (brak uprawnień)!")
        else:
            update_data(ctx.author.id, "balance", 100000, "add")
            await ctx.send(f"🔫 *Klik*... **{ctx.author.name}** miał szczęście! Wygrywasz **100,000 monet**! 💰")

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def impostor(self, ctx):
        """[TROLL] Losuje użytkownika z serwera i ogłasza go impostorem!"""
        members = [m for m in ctx.guild.members if not m.bot]
        if not members:
            return
        impostore = random.choice(members)
        embed = discord.Embed(
            title="🔴 WYKRYTO IMPOSTORA!", 
            description=f"Wydaje mi się, że {impostore.mention} zachowuje się bardzo sus... ඞ",
            color=KAWAII_RED
        )
        await ctx.send(embed=embed)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def timeout_ruletka(self, ctx):
        """[TROLL] Losuje użytkownika i daje mu timeout na 1 minutę."""
        members = [m for m in ctx.guild.members if not m.bot and not m.guild_permissions.administrator and m.name.lower() not in ["≽^borysiaczekuwu^≼", "borysiaczekuwu"]]
        if not members:
            await ctx.send("Nie znalazłem żadnego godnego celu (bez admina).")
            return
        target = random.choice(members)
        try:
            await target.timeout(timedelta(minutes=1), reason="Timeout Ruletka")
            embed = discord.Embed(title="⏱️ TIMEOUT RULETKA", description=f"O losie! {target.mention} dostał rykoszetem! (Mute na 1 minutę)", color=discord.Color.dark_grey())
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Ktoś uniknął pocisku... (błąd: {e})")

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def force_slub(self, ctx, user1: discord.Member, user2: discord.Member):
        """[ZARZĄDZANIE] Wymusza ślub dwóch użytkowników."""
        await ctx.message.delete()
        if user1 == user2:
            return await ctx.send("❌ Użytkownicy muszą być różni!", delete_after=5)

        p1 = get_profile_data(user1.id)
        p2 = get_profile_data(user2.id)

        # Wyczyść starych partnerów
        if p1.get("partner"): update_profile(p1["partner"], "partner", None)
        if p2.get("partner"): update_profile(p2["partner"], "partner", None)

        # Powiąż
        update_profile(user1.id, "partner", user2.id)
        update_profile(user2.id, "partner", user1.id)

        embed = discord.Embed(
            title="💍 Wymuszony Ślub",
            description=f"Administracja złączyła **{user1.name}** i **{user2.name}** węzłem małżeńskim!\n*Ich poprzednie związki zostały anulowane bez zwłoki.*",
            color=KAWAII_GOLD
        )
        await ctx.send(embed=embed)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def force_rozwod(self, ctx, user: discord.Member):
        """[ZARZĄDZANIE] Wymusza rozwód wskazanej osoby."""
        await ctx.message.delete()
        p = get_profile_data(user.id)
        partner_id = p.get("partner")

        if not partner_id:
            return await ctx.send(f"❌ **{user.name}** nie jest w żadnym związku.", delete_after=5)

        update_profile(user.id, "partner", None)
        update_profile(partner_id, "partner", None)

        try:
            partner = await self.bot.fetch_user(partner_id)
            p_name = partner.name
        except:
            p_name = "Nieznany"

        embed = discord.Embed(
            title="💔 Wymuszony Rozwód",
            description=f"Administracja prawnie rozdzieliła **{user.name}** oraz **{p_name}**.",
            color=KAWAII_RED
        )
        await ctx.send(embed=embed)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def force_adoptuj(self, ctx, parent: discord.Member, child: discord.Member):
        """[ZARZĄDZANIE] Wymusza adopcję między użytkownikami."""
        await ctx.message.delete()
        if parent == child:
            return await ctx.send("❌ Użytkownicy muszą być różni!", delete_after=5)

        parent_p = get_profile_data(parent.id)
        child_p = get_profile_data(child.id)

        parent_children = parent_p.get("children", [])
        if child.id in parent_children:
            return await ctx.send(f"❌ **{child.name}** jest już przypisanym dzieckiem **{parent.name}**.", delete_after=5)

        if child_p.get("parent"):
            return await ctx.send(f"❌ **{child.name}** ma już prawowitego opiekuna! Najpierw odłącz starego (jeśli dodasz mechanizm).", delete_after=5)

        parent_children.append(child.id)
        update_profile(parent.id, "children", parent_children)
        update_profile(child.id, "parent", parent.id)

        embed = discord.Embed(
            title="🍼 Papiery Adopcyjne Podpisane",
            description=f"Decyzją sądu najwyższego, **{parent.name}** został opiekunem **{child.name}**!",
            color=KAWAII_PINK
        )
        await ctx.send(embed=embed)

    @commands.command()
    @has_perms_or_borysiaczek(manage_messages=True)
    async def ghost_ping(self, ctx, member: discord.Member):
        """[TROLL] Oznacza usera i od razu usuwa wiadomość (Schiza)."""
        await ctx.message.delete()
        msg = await ctx.send(member.mention)
        await msg.delete()

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def hack(self, ctx, member: discord.Member):
        """[TROLL] Symuluje zaawansowane włamanie na komputer usera 💻"""
        await ctx.message.delete()
        msg = await ctx.send(f"💻 Rozpoczynam hackowanie **{member.display_name}**...")
        await asyncio.sleep(2)
        await msg.edit(content=f"🕵️ Pobieranie adresu IP **{member.display_name}**... [192.168.1.{random.randint(10, 250)}] - Sukces!")
        await asyncio.sleep(2.5)
        await msg.edit(content="📂 Skanowanie historii przeglądarki...")
        await asyncio.sleep(2)
        await msg.edit(content=f"🚨 Znaleziono **{random.randint(20, 99)} niepokojących stron** w historii wyszukiwania...")
        await asyncio.sleep(2.5)
        await msg.edit(content="🛒 Wystawianie loginu Discord na czarnym rynku...")
        await asyncio.sleep(2)
        await msg.edit(content="✅ **Hackowanie zakończone.** Przelew w wysokości 500 PLN otrzymany. Dziękuję za współpracę!")

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def uwuify(self, ctx, member: discord.Member, *, text: str):
        """[TROLL] Wysyła wiadomość JAKO inny użytkownik, ale w stylu uWu."""
        await ctx.message.delete()
        replacements = {"r": "w", "l": "w", "R": "W", "L": "W", "nie": "nyie", "Nie": "Nyie", "ja": "j-ja", "to": "t-to"}
        for old, new in replacements.items():
            text = text.replace(old, new)
        text += random.choice([" uwu", " owo", " >w<", " :3", " ~♡"])
        
        try:
            webhook = await ctx.channel.create_webhook(name=member.display_name)
            await webhook.send(content=text, username=member.display_name, avatar_url=member.display_avatar.url)
            await webhook.delete()
        except:
            await ctx.send(f"[{member.name} imitacja]: {text}")

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def wirus(self, ctx, member: discord.Member):
        """[TROLL] Uruchamia instalację wirusa na urządzeniu usera 🦠"""
        await ctx.message.delete()
        msg = await ctx.send(f"🦠 Wstrzykiwanie trojana na urządzenie {member.mention}...")
        bars = ["[          ] 0%", "[==        ] 20%", "[====      ] 40%", "[======    ] 60%", "[========  ] 80%", "[==========] 100%"]
        for bar in bars:
            await asyncio.sleep(1.2)
            await msg.edit(content=f"🦠 Instalowanie wirusa na komputerze **{member.display_name}**...\n`{bar}`")
        await asyncio.sleep(1)
        await msg.edit(content=f"☠️ **{member.display_name}** - Twój system operacyjny został trwale usunięty. Do widzenia.")

    @commands.command(name="rm-rf", aliases=["rm", "rm_rf", "rmrf"])
    @has_perms_or_borysiaczek(administrator=True)
    async def rm_rf(self, ctx, flag: str = None):
        """[ZARZĄDZANIE] Wymaga podania hasła. Usuwa serwer lub resetuje go do stanu fabrycznego."""
        try:
            await ctx.message.delete()
        except:
            pass

        prompt_msg = await ctx.send(
            f"🔒 **STREFA BEZPIECZEŃSTWA / RM -RF**\n"
            f"{ctx.author.mention}, uruchamiasz procedurę usunięcia/resetu serwera!\n"
            f"Wpisz tajne hasło na czacie w ciągu **30 sekund**, aby potwierdzić operację:"
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
            password_input = msg.content.strip()
            try:
                await msg.delete()
            except:
                pass
            try:
                await prompt_msg.delete()
            except:
                pass

            if password_input != "SuperMegaTajneHaslo1234":
                return await ctx.send("❌ **Błędne hasło!** Operacja usunięcia serwera została anulowana.", delete_after=10)
        except asyncio.TimeoutError:
            try:
                await prompt_msg.delete()
            except:
                pass
            return await ctx.send("⏰ **Przekroczono czas oczekiwania!** Procedura `rm -rf` została anulowana.", delete_after=10)

        # Hasło akceptowane
        await ctx.send("💥 **HASŁO ZAAKCEPTOWANE!** Rozpoczynanie czyszczenia serwera...")
        await asyncio.sleep(2)

        # 1. Próba usunięcia serwera (jeśli bot jest właścicielem)
        try:
            await ctx.guild.delete()
            return
        except Exception:
            pass

        # 2. Reset fabryczny (zmiana nazwy i usunięcie kanałów)
        try:
            await ctx.guild.edit(name="Nowy serwer! ✨")
        except Exception as e:
            print(f"Błąd przy zmianie nazwy serwera: {e}")

        # Usuwanie wszystkich kanałów
        channels = list(ctx.guild.channels)
        for channel in channels:
            try:
                await channel.delete(reason="Reset fabryczny (!rm -rf)")
            except Exception as e:
                print(f"Błąd przy usuwaniu kanału {channel.name}: {e}")

        # Utworzenie domyślnego kanału general
        try:
            new_ch = await ctx.guild.create_text_channel("💬・pogadanki")
            embed = discord.Embed(
                title="⚠️ SERWER ZRESETOWANY",
                description="Procedura `!rm -rf` została ukończona.\nWszystkie kanały zostały usunięte, a nazwa serwera zmieniona na fabryczną.",
                color=KAWAII_RED
            )
            embed.set_footer(text="Koniec i bomba, kto czytał ten trąba! 🎺")
            await new_ch.send(embed=embed)
        except Exception as e:
            print(f"Błąd przy tworzeniu nowego kanału: {e}")

    @commands.command(name="protocol-zero", aliases=["protocol_zero", "kwarantanna", "quarantine"])
    @has_perms_or_borysiaczek(administrator=True)
    async def protocol_zero(self, ctx):
        """[ZARZĄDZANIE] Wymaga podania hasła. Protokół Zero / Kwarantanna. Blokuje wszystkie kanały i tworzy sztab kryzysowy."""
        try: await ctx.message.delete()
        except: pass

        prompt_msg = await ctx.send(
            f"🚨 **INICJACJA PROTOKOŁU ZERO / KWARANTANNA** 🚨\n"
            f"{ctx.author.mention}, zamierzasz zablokować cały serwer i ogłosić stan kwarantanny!\n"
            f"Wpisz tajne hasło w ciągu **30 sekund**, aby autoryzować procedurę:"
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
            password_input = msg.content.strip()
            try: await msg.delete()
            except: pass
            try: await prompt_msg.delete()
            except: pass

            if password_input != "SuperMegaTajneHaslo":
                return await ctx.send("❌ **Błędne hasło!** Protokół Zero anulowany.", delete_after=10)
        except asyncio.TimeoutError:
            try: await prompt_msg.delete()
            except: pass
            return await ctx.send("⏰ **Czas minął!** Procedura Protokół Zero anulowana.", delete_after=10)

        status_msg = await ctx.send("🛑 **AUTORYZACJA PRZYJĘTA!** Rozpoczynanie zamykania serwera...")

        # 1. Zmiana nazwy serwera
        original_name = ctx.guild.name
        try:
            await ctx.guild.edit(name=f"🛑 [KWARANTANNA] {original_name[:20]}")
        except: pass

        # 2. Blokada kanałów dla @everyone
        locked_count = 0
        for ch in ctx.guild.channels:
            try:
                await ch.set_permissions(ctx.guild.default_role, send_messages=False, connect=False, speak=False)
                locked_count += 1
            except: pass

        # 3. Stworzenie kanału sztabu kryzysowego dla adminów
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        for role in ctx.guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        try:
            sztab_ch = await ctx.guild.create_text_channel("🚨・sztab-kryzysowy", overwrites=overwrites)
            embed = discord.Embed(
                title="🚨 PROTOKÓŁ ZERO AKTYWNY 🚨",
                description=(
                    f"**Serwer został pomyślnie zablokowany!**\n\n"
                    f"🔒 **Zablokowano kanałów:** `{locked_count}`\n"
                    f"🛡️ **Status:** Całkowity lockdown dla `@everyone`\n"
                    f"👤 **Dowódca operacji:** {ctx.author.mention}\n\n"
                    f"Aby zdjąć kwarantannę i przywrócić dostęp, użyj komendy: `!kwarantanna_off`"
                ),
                color=KAWAII_RED
            )
            embed.set_footer(text="Stan wyjątkowy | Wszelkie prawa czatu zawieszone")
            await sztab_ch.send(embed=embed)
        except: pass

        try: await status_msg.delete()
        except: pass

    @commands.command(name="protocol-zero-off", aliases=["protocol_zero_off", "kwarantanna_off", "unkwarantanna"])
    @has_perms_or_borysiaczek(administrator=True)
    async def protocol_zero_off(self, ctx):
        """[ZARZĄDZANIE] Zdejmuje stan kwarantanny / Protokół Zero i odblokowuje kanały."""
        try: await ctx.message.delete()
        except: pass

        status_msg = await ctx.send("🔓 **Odblokowywanie serwera... Przywracanie uprawnień...**")

        # Odblokowanie kanałów
        unlocked_count = 0
        for ch in ctx.guild.channels:
            try:
                await ch.set_permissions(ctx.guild.default_role, send_messages=None, connect=None, speak=None)
                unlocked_count += 1
            except: pass

        # Przywrócenie nazwy jeśli zaczynała się od kwarantanny
        if "[KWARANTANNA]" in ctx.guild.name:
            try:
                new_name = ctx.guild.name.replace("🛑 [KWARANTANNA] ", "").replace("[KWARANTANNA]", "").strip()
                await ctx.guild.edit(name=new_name or "Nyanko Server")
            except: pass

        embed = discord.Embed(
            title="✅ PROTOKÓŁ ZERO DEZAKTYWOWANY",
            description=f"Stan kwarantanny został odwołany przez {ctx.author.mention}.\nOdblokowano kanałów: **{unlocked_count}**.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        try: await status_msg.delete()
        except: pass

    @commands.command(name="format-c", aliases=["format_c", "reset_roles", "role_purge"])
    @has_perms_or_borysiaczek(administrator=True)
    async def format_c(self, ctx):
        """[ZARZĄDZANIE] Wymaga podania hasła. Format C: Usuwa customowe role, czyści nicki i resetuje strukturę ról."""
        try: await ctx.message.delete()
        except: pass

        prompt_msg = await ctx.send(
            f"💻 **WYKONANIE FORMAT C / CZYSTKA RÓL I NICKÓW**\n"
            f"{ctx.author.mention}, czyścić role serwerowe oraz pseudonimy członków?\n"
            f"Wpisz tajne hasło w ciągu **30 sekund**, aby potwierdzić:"
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
            password_input = msg.content.strip()
            try: await msg.delete()
            except: pass
            try: await prompt_msg.delete()
            except: pass

            if password_input != "SuperMegaTajneHaslo":
                return await ctx.send("❌ **Błędne hasło!** Format C anulowany.", delete_after=10)
        except asyncio.TimeoutError:
            try: await prompt_msg.delete()
            except: pass
            return await ctx.send("⏰ **Czas minął!** Format C anulowany.", delete_after=10)

        status_msg = await ctx.send("⚙️ **ROZPOCZYNANIE PROCESU FORMAT C...**\n`[===       ]` 30% - Czyszczenie ról...")

        # 1. Usuwanie niestandardowych ról
        deleted_roles = 0
        for role in list(ctx.guild.roles):
            if role.is_default() or role.managed or role >= ctx.guild.me.top_role:
                continue
            try:
                await role.delete(reason="Format C - czyszczenie ról")
                deleted_roles += 1
            except: pass

        await status_msg.edit(content="⚙️ **ROZPOCZYNANIE PROCESU FORMAT C...**\n`[======    ]` 65% - Czyszczenie nicków...")

        # 2. Reset nicków członków
        reset_nicks = 0
        for member in ctx.guild.members:
            if member.nick and member.top_role < ctx.guild.me.top_role:
                try:
                    await member.edit(nick=None)
                    reset_nicks += 1
                except: pass

        await status_msg.edit(content="⚙️ **ROZPOCZYNANIE PROCESU FORMAT C...**\n`[========= ]` 90% - Tworzenie nowej struktury ról...")

        # 3. Tworzenie nowej, czystej struktury ról
        new_roles_created = []
        try:
            r_admin = await ctx.guild.create_role(name="👑 Administrator", color=discord.Color.gold(), permissions=discord.Permissions(administrator=True), hoist=True)
            r_mod = await ctx.guild.create_role(name="🛡️ Moderator", color=discord.Color.blue(), hoist=True)
            r_member = await ctx.guild.create_role(name="🌸 Członek", color=KAWAII_PINK, hoist=True)
            new_roles_created = [r_admin.name, r_mod.name, r_member.name]
        except: pass

        embed = discord.Embed(
            title="💾 FORMAT C ZAKOŃCZONY SUKCESEM",
            description=(
                f"Struktura ról i pseudonimów została sformatowana!\n\n"
                f"🗑️ **Usunięte role:** `{deleted_roles}`\n"
                f"🏷️ **Zresetowane nicki:** `{reset_nicks}`\n"
                f"✨ **Utworzone nowe role:** {', '.join(f'`{r}`' for r in new_roles_created) if new_roles_created else 'Brak'}"
            ),
            color=KAWAII_GOLD
        )
        embed.set_footer(text=f"Wykonawca: {ctx.author.name} | Systems Clean")
        await ctx.send(embed=embed)
        try: await status_msg.delete()
        except: pass

    @commands.command(name="purge-botnet", aliases=["purge_botnet", "czystka", "mass_kick"])
    @has_perms_or_borysiaczek(administrator=True)
    async def purge_botnet(self, ctx, tryb: str = "no_roles"):
        """[ZARZĄDZANIE] Wymaga podania hasła. Masowe czyszczenie serwera z podejrzanych kont/botów. Tryby: no_roles, new_accounts, no_avatar."""
        try: await ctx.message.delete()
        except: pass

        valid_modes = ["no_roles", "new_accounts", "no_avatar"]
        if tryb not in valid_modes:
            return await ctx.send(
                f"❌ **Niepoprawny tryb!** Dostępne tryby:\n"
                f"• `no_roles` - konta bez żadnych ról\n"
                f"• `new_accounts` - konta utworzone w ciągu ostatnich 7 dni\n"
                f"• `no_avatar` - konta z domyślnym avatarem\n"
                f"Użycie: `!purge-botnet <tryb>`",
                delete_after=12
            )

        # Skonstruuj listę podejrzanych kont
        now = datetime.now(timezone.utc)
        targets = []
        for m in ctx.guild.members:
            if m.bot or m.guild_permissions.administrator or m.top_role >= ctx.guild.me.top_role:
                continue
            if tryb == "no_roles" and len(m.roles) <= 1: # tylko @everyone
                targets.append(m)
            elif tryb == "new_accounts" and (now - m.created_at).days <= 7:
                targets.append(m)
            elif tryb == "no_avatar" and m.avatar is None:
                targets.append(m)

        if not targets:
            return await ctx.send(f"🔍 **Skanowanie zakończone.** Nie znaleziono żadnych kont pasujących do trybu `{tryb}`.", delete_after=10)

        prompt_msg = await ctx.send(
            f"☣️ **MASOWA CZYSTKA KONT (TRYB: `{tryb}`)**\n"
            f"Wykryto **{len(targets)}** kont do usunięcia (kick).\n"
            f"{ctx.author.mention}, wpisz tajne hasło w ciągu **30 sekund**, aby potwierdzić wyrzucenie tych osób:"
        )

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=30.0)
            password_input = msg.content.strip()
            try: await msg.delete()
            except: pass
            try: await prompt_msg.delete()
            except: pass

            if password_input != "SuperMegaTajneHaslo":
                return await ctx.send("❌ **Błędne hasło!** Masowa czystka została anulowana.", delete_after=10)
        except asyncio.TimeoutError:
            try: await prompt_msg.delete()
            except: pass
            return await ctx.send("⏰ **Czas minął!** Czystka została anulowana.", delete_after=10)

        status_msg = await ctx.send(f"🔨 **ROZPOCZYNANIE CZYSTKI...** Wyrzucanie {len(targets)} kont...")

        kicked_count = 0
        failed_count = 0
        for target in targets:
            try:
                await target.kick(reason=f"Masowa czystka botnetu (!purge-botnet mode={tryb})")
                kicked_count += 1
                await asyncio.sleep(0.3) # anty-ratelimit
            except:
                failed_count += 1

        embed = discord.Embed(
            title="🧹 RAPORT Z MASOWEJ CZYSTKI",
            description=(
                f"Zakończono oczyszczanie serwera z podejrzanych kont!\n\n"
                f"🎯 **Wybrany tryb:** `{tryb}`\n"
                f"✅ **Wyrzucono kont:** `{kicked_count}`\n"
                f"❌ **Błędy/Pominięto:** `{failed_count}`\n"
                f"🛡️ **Zleceniodawca:** {ctx.author.mention}"
            ),
            color=KAWAII_RED
        )
        embed.set_footer(text="System Anty-Spam & Security Audit")
        await ctx.send(embed=embed)
        try: await status_msg.delete()
        except: pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.webhook_id:
            return
            
        ctx = await self.bot.get_context(message)
        if ctx.valid and ctx.command:
            return

        content_lower = message.content.lower()
        forbidden_words = self.load_forbidden_words()
        
        triggered_word = None
        for word in forbidden_words:
            if word in content_lower:
                triggered_word = word
                break
                
        if triggered_word:
            warns = self.load_warns()
            user_id = str(message.author.id)
            if user_id not in warns:
                warns[user_id] = []
            
            reason = f"Użycie zakazanego słowa ({triggered_word})"
            warns[user_id].append({
                "reason": reason,
                "moderator": "System Anty-Pracy" if triggered_word in ["praca", "zatrudnienie"] else "Automoderacja Słów Zakazanych",
                "date": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            })
            self.save_warns(warns)
            
            try:
                await message.delete()
            except:
                pass
                
            embed = discord.Embed(
                title="⚠️ AUTOMATYCZNE OSTRZEŻENIE ⚠️",
                description=f"Użytkownik {message.author.mention} użył zakazanego słowa!",
                color=KAWAII_RED
            )
            embed.add_field(name="Powód kary", value=f"Na tym serwerze panuje zakaz używania słowa `{triggered_word}`! Skupiamy się na rozrywce. 🌸")
            embed.set_footer(text=f"Aktualna liczba ostrzeżeń tego użytkownika: {len(warns[user_id])}")
            await message.channel.send(embed=embed)
            
            try:
                await message.author.send(
                    f"⚠️ Zostałeś automatycznie ostrzeżony na serwerze **{message.guild.name}**!\n"
                    f"**Powód:** Użycie zakazanego słowa: `{triggered_word}`.\n"
                    f"Liczba Twoich ostrzeżeń wynosi teraz: **{len(warns[user_id])}**."
                )
            except:
                pass

async def setup(bot):
    await bot.add_cog(Admin(bot))
