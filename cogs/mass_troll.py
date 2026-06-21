import discord
from discord.ext import commands
import asyncio
from cogs.admin import has_perms_or_borysiaczek
from utils import KAWAII_RED, KAWAII_PINK, KAWAII_GOLD
import random
import re

SCHIZO_RESPONSES = [
    "Kto pytał? 🤔",
    "Aha. 👍",
    "Fascynujące... Opowiedz nam o tym więcej (żartuję, nie mów nic). 🤫",
    "Nikogo to nie obchodzi 💀",
    "Przestań mówić do siebie. 🤨",
    "Czy ktoś tu coś mówił? Bo nic nie słychać. 💨",
    "Bardzo ciekawe, a teraz wyjdź. 🚪",
    "Uuu, mocne słowa jak na kogoś bez Nitro. 💅",
    "Wyłącz komputer, wyjdź na dwór, dotknij trawy. 🌿"
]

class MassTroll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cursed_italiano = {}
        self.cursed_femboy = {}
        self.reaction_curses = {}
        self.mocking_users = set()
        self.ping_shields = set()
        self.frozen_users = set()
        self.typo_users = set()
        self.reversed_users = set()
        self.schizo_users = set()

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

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def troll_admin(self, ctx):
        """[MASS TROLL] Rozdaje graczom 'uprawnienia', tworząc fałszywe role admina."""
        await ctx.message.delete()
        msg = await ctx.send("🛡️ Przekazywanie uprawnień administratorskich losowym użytkownikom...")
        await asyncio.sleep(2)
        try:
            fake_role = await ctx.guild.create_role(name="👑 Właściciel Serwera", color=discord.Color.gold(), hoist=True)
            members = [m for m in ctx.guild.members if not m.bot][:5]
            for m in members:
                await m.add_roles(fake_role)
            await msg.edit(content=f"✅ Awansowano {len(members)} użytkowników na 'Właścicieli Serwera'! (Odliczanie do usunięcia: 15s)")
            await asyncio.sleep(15)
            await fake_role.delete()
        except Exception as e:
            await msg.edit(content=f"❌ Coś poszło nie tak z uprawnieniami (Możliwe, że bot ma za niską rolę).")

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def troll_dm_all(self, ctx):
        """[MASS TROLL] Udaje że wysyła DM do wszystkich."""
        await ctx.message.delete()
        total_members = len(ctx.guild.members)
        msg = await ctx.send(f"📩 Przygotowywanie masowej wiadomości do **{total_members}** użytkowników...")
        
        await asyncio.sleep(2)
        await msg.edit(content=f"📩 Wysyłanie DM... [====        ] 30% (Wysłano do {int(total_members*0.3)} użytkowników)")
        await asyncio.sleep(2)
        await msg.edit(content=f"📩 Wysyłanie DM... [========    ] 70% (Wysłano do {int(total_members*0.7)} użytkowników)")
        await asyncio.sleep(2)
        await msg.edit(content=f"✅ Wszystkie **{total_members}** wiadomości ze podejrzanym linkiem zostały poprawnie doręczone na DM. Chaos zasiany! 😈")

    @commands.command()
    async def brazylia(self, ctx, member: discord.Member):
        """[TROLL] Wysyła gracza do Brazylii poprzez portal!"""
        await ctx.message.delete()
        
        msg = await ctx.send(f"🌌 **UWAGA! Otwieranie nienormalnej szczeliny przestrzennej wokół {member.mention}!**")
        await asyncio.sleep(2)
        await msg.edit(content=f"🌀 Portal wymiarowy zaczyna wciągać {member.mention}! `[||||      ]` 40%")
        await asyncio.sleep(2)
        await msg.edit(content=f"🌪️ OSTRZEŻENIE! {member.mention} opuszcza naszą rzeczywistość! `[||||||||  ]` 80%")
        await asyncio.sleep(2)
        await msg.edit(content=f"💥 **BUM!** {member.display_name} zniknął... gdzie on jest?")
        
        await asyncio.sleep(3)
        
        # Tworzenie Webhooka by udawać użytkownika
        webhook = None
        webhooks = await ctx.channel.webhooks()
        for wh in webhooks:
            if wh.name == "Portal To Brazil":
                webhook = wh
                break
                
        if not webhook:
            try:
                webhook = await ctx.channel.create_webhook(name="Portal To Brazil")
            except:
                await ctx.send("❌ Brakuje potęgi do stworzenia portalu (błąd uprawnień Webhook).")
                return
                
        try:
            await webhook.send(
                content="Pomocy! Jestem w Brazylii! Gorąco tu i ktoś próbuje mi wcisnąć karnawałowe ubranie! 😱🇧🇷",
                username=member.display_name,
                avatar_url=member.display_avatar.url
            )
        except Exception as e:
            print(f"Błąd webhooka: {e}")
            
    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def mass_hack_rp(self, ctx):
        """[MASS TROLL] Sekwencja ataku hakerskiego na cały serwer (Roleplay)."""
        await ctx.message.delete()
        
        msg = await ctx.send("```css\n[ZAINICJOWANO ŁĄCZENIE Z GŁÓWNYM KLASTREM SERWERA]\n```")
        await asyncio.sleep(2.5)
        
        await msg.edit(content="```css\n[ZAINICJOWANO ŁĄCZENIE Z GŁÓWNYM KLASTREM SERWERA]\n> Omijanie zapory sieciowej (Firewall) Discord.API... [SUKCES]\n```")
        await asyncio.sleep(2)
        
        await msg.edit(content="```css\n[ZAINICJOWANO ŁĄCZENIE Z GŁÓWNYM KLASTREM SERWERA]\n> Omijanie zapory sieciowej (Firewall) Discord.API... [SUKCES]\n> Deszyfrowanie tokenów uwierzytelniających wszystkich użytkowników... \n```")
        await asyncio.sleep(3)
        
        await msg.edit(content="```yaml\nUWAGA! WYKRYTO KRYTYCZNE WŁAMANIE.\n- Wszystkie dane logowania zostały pobrane.\n- Czat powoli zostaje blokowany.\n- Przygotowywanie transferu waluty serwerowej... \n```")
        await asyncio.sleep(4)
        
        await msg.edit(content="**Hahahahaha! 🎉** Uśmiechnijcie się, to był tylko mały żart. Nikt niczego nie ukradł... chociaż sprawdźcie lepiej kieszenie! 😈")

    @commands.command()
    async def italiano(self, ctx, member: discord.Member):
        """[TROLL] Zamienia gracza w typowego Włocha 🤌"""
        await ctx.message.delete()
        if member.bot: return
        
        msg = await ctx.send(f"🍕 **Zarządzam operację #Pizza dla {member.mention}!**")
        await asyncio.sleep(2)
        await msg.edit(content=f"🍝 Podawanie espresso i wyrabianie ciasta na pizzę... `[|||       ]` 30%")
        await asyncio.sleep(2)
        await msg.edit(content=f"🤌 Montaż wirtualnych wąsów i lekcje gestykulacji... `[|||||||   ]` 70%")
        await asyncio.sleep(2)
        await msg.edit(content=f"🇮🇹 **Mamma Mia!** Operacja zakończona! {member.display_name} używa od teraz tylko włoskiego temperamentu!")
        
        self.cursed_italiano[member.id] = 1

    @commands.command()
    async def femboi(self, ctx, member: discord.Member):
        """[TROLL] Zamienia gracza w Kawaii Femboya z Blåhajem! :3"""
        await ctx.message.delete()
        if member.bot: return
        
        msg = await ctx.send(f"📦 **Kurier dotarł! Przesyłka priorytetowa dla {member.mention}... co to może być?**")
        await asyncio.sleep(2.5)
        await msg.edit(content=f"🧦 Otwieranie paczki... W środku są biało-różowe zakolanówki programisty! Zakładanie... `[||        ]` 20%")
        await asyncio.sleep(2.5)
        await msg.edit(content=f"🐱 Dodawanie mięciutkich kocich uszek oraz spódniczki... `[||||||||  ]` 60%")
        await asyncio.sleep(2.5)
        await msg.edit(content=f"🦈 Wręczanie ogromnego, puszystego Blåhaja do przytulania... `[||||||||||]` 100%")
        await asyncio.sleep(2)
        await msg.edit(content=f"✨ **UwU!** Proces transformacji zakończony pomyślnie! Przywitajcie nowego, uroczego {member.display_name}! :3")
        
        self.cursed_femboy[member.id] = 1

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def odczaruj(self, ctx, member: discord.Member):
        """[TROLL] Zdejmuje klątwę italiano/femboy z gracza."""
        await ctx.message.delete()
        removed = False
        if member.id in self.cursed_italiano:
            del self.cursed_italiano[member.id]
            removed = True
        if member.id in self.cursed_femboy:
            del self.cursed_femboy[member.id]
            removed = True
            
        if removed:
            await ctx.send(f"✨ Uff... {member.mention} powrócił do normy!")
        else:
            msg = await ctx.send(f"❓ {member.mention} nie jest pod wpływem żadnej klątwy.")
            await asyncio.sleep(3)
            await msg.delete()

    @commands.command()
    async def fake_join(self, ctx, *, nick: str):
        """[TROLL] Wyświetla fałszywą wiadomość o dołączeniu nowego gracza."""
        try:
            await ctx.message.delete()
        except:
            pass
        embed = discord.Embed(
            description=f"Witamy **{nick}**! (≧◡≦) ♡\n Cieszymy się że połączyłeś się z nami! 💖",
            color=KAWAII_PINK
        )
        embed.add_field(name="Zostawił takie bio:", value="Nowy gracz na streecie!")
        await ctx.send(embed=embed)

    @commands.command()
    async def fake_leave(self, ctx, member: discord.Member):
        """[TROLL] Wyświetla fałszywą wiadomość o odejściu gracza."""
        try:
            await ctx.message.delete()
        except:
            pass
        embed = discord.Embed(
            description=f"O nie... **{member.name}** uciekł... Trzymaj się gdziekolwiek tam jesteś! 💔",
            color=discord.Color.dark_grey()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def fake_level(self, ctx, member: discord.Member, level: int):
        """[TROLL] Wyświetla fałszywą wiadomość o awansie na nowy poziom."""
        try:
            await ctx.message.delete()
        except:
            pass
        embed = discord.Embed(
            title="🎉 LEVEL UP! 🎉",
            description=f"Brawo **{member.mention}**! Awansowałeś na poziom **{level}**! ✨",
            color=KAWAII_GOLD
        )
        embed.add_field(name="Nowa Ranga", value=f"**LVL {level}**")
        await ctx.send(embed=embed)

    @commands.command()
    async def fake_warn(self, ctx, member: discord.Member, *, powod: str = "Podejrzana aktywność"):
        """[TROLL] Wyświetla fałszywą wiadomość ostrzeżenia od systemu."""
        try:
            await ctx.message.delete()
        except:
            pass
        embed = discord.Embed(
            title="⚠️ OSTRZEŻENIE SYSTEMOWE ⚠️",
            description=f"Użytkownik **{member.mention}** otrzymał ostrzeżenie.",
            color=KAWAII_RED
        )
        embed.add_field(name="Powód:", value=powod)
        embed.set_footer(text="Wiadomość zautomatyzowana przez system nadzoru.")
        await ctx.send(embed=embed)

    async def apply_italiano_curse(self, text, message_count):
        level = min(4, message_count // 5 + 1)
        words = text.split()
        
        if level >= 2:
            replacements = {
                "tak": "si", "nie": "no", "co": "che", "dlaczego": "perché",
                "dobrze": "bene", "źle": "male", "cześć": "ciao", "hej": "ciao",
                "dzień": "giorno", "dzięki": "grazie", "proszę": "prego",
                "kurwa": "cazzo", "ja": "io", "ty": "tu", "bardzo": "molto",
                "jest": "è", "są": "sono", "pizza": "pizza 🍕"
            }
            for i, w in enumerate(words):
                match = re.match(r'^([^a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]*)([a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+)(.*)$', w)
                if match:
                    prefix, core, suffix = match.groups()
                    clean_w = core.lower()
                    if clean_w in replacements:
                        replacement = replacements[clean_w]
                        if core[0].isupper(): replacement = replacement.capitalize()
                        if core.isupper() and len(core) > 1: replacement = replacement.upper()
                        words[i] = f"{prefix}{replacement}{suffix}"
                        
        text = " ".join(words)
        
        if level >= 1:
            endings = ["🤌", "🍕", "🍝", "Mamma mia!", "Porca miseria!", "Che cazzo!", "Bellissimo!"]
            if random.random() < (0.3 * level):
                text += f" {random.choice(endings)}"
                
        if level >= 3:
            beginnings = ["Ascolta!", "Scusa...", "🤌 *gestykuluje* 🤌", "Allora..."]
            if random.random() < 0.4:
                text = f"{random.choice(beginnings)} {text}"
                
        if level >= 4:
            if random.random() < 0.3:
                text = text.upper() + " 🤌🤌🤌"
            text = text.replace("r", "rr").replace("R", "RR")
            if not text.endswith(("!", "?", ".")):
                text += " a" if text and not text[-1].lower() in "aeiouy" else ""
                
        return text

    async def apply_femboy_curse(self, text, message_count):
        level = min(4, message_count // 5 + 1)
        
        if level >= 2:
            words = text.split()
            for i, word in enumerate(words):
                if len(word) >= 3 and random.random() < (0.15 * level):
                    match = re.match(r'^([^a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]*)([a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ])(.*)$', word)
                    if match:
                        prefix, first_letter, rest = match.groups()
                        words[i] = f"{prefix}{first_letter}-{first_letter.lower()}{rest}"
            text = " ".join(words)
            text = text.replace("r", "w").replace("R", "W").replace("l", "w").replace("L", "W")
            
        if level >= 1:
            if random.random() < (0.25 * level):
                kaomoji = ["UwU", "OwO", ":3", ">~<", "૮ ˶o ﻌ o˶ ა", "🥺", "🌸", "✨"]
                text += f" {random.choice(kaomoji)}"
                
        if level >= 3:
            actions = ["*blushes*", "*giggles*", "*tuli Blåhaja*", "*poprawia zakolanówki*", "*macha ogonkiem*", "*puszy kocie uszka*", "*kręci się w spódniczce*", "*rumieni się*"]
            if random.random() < 0.4:
                text = f"{random.choice(actions)} {text}"
                
        if level >= 4:
            text = text.replace(".", " ~").replace("!", " ✨!")
            if random.random() < 0.3:
                text = f"Nya! {text}"
                
        return text

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def frame(self, ctx, member: discord.Member, *, tekst: str):
        """[BOSS] Wysyła wiadomość w imieniu innego użytkownika za pomocą Webhooka."""
        await ctx.message.delete()
        
        webhook = None
        webhooks = await ctx.channel.webhooks()
        for wh in webhooks:
            if wh.name == "Troll Webhook":
                webhook = wh
                break
        if not webhook:
            try:
                webhook = await ctx.channel.create_webhook(name="Troll Webhook")
            except:
                await ctx.send("❌ Brakuje uprawnień bota do zarządzania Webhookami.", delete_after=5)
                return
                
        try:
            await webhook.send(
                content=tekst,
                username=member.display_name,
                avatar_url=member.display_avatar.url
            )
        except Exception as e:
            print(f"Błąd webhooka w komendzie frame: {e}")

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def ghost_ping(self, ctx, member: discord.Member, count: int = 3):
        """[BOSS] Wysyła pustawe pingi, które od razu usuwa."""
        await ctx.message.delete()
        count = min(max(1, count), 10)
        
        channels = [ch for ch in ctx.guild.text_channels if ch.permissions_for(ctx.guild.me).send_messages]
        if not channels:
            return
            
        for _ in range(count):
            target_channel = random.choice(channels)
            try:
                msg = await target_channel.send(member.mention)
                await msg.delete()
            except:
                pass
            await asyncio.sleep(0.5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def klatwa_reakcji(self, ctx, member: discord.Member, *, emotki: str):
        """[BOSS] Nakłada klątwę reakcji. Podaj emotki oddzielone spacją."""
        await ctx.message.delete()
        if member.bot:
            return await ctx.send("❌ Nie możesz trollować botów!", delete_after=5)
            
        emoji_list = re.findall(r'<a?:[a-zA-Z0-9_]+:[0-9]+>|[\U00010000-\U0010ffff\u2600-\u27ff]', emotki)
        if not emoji_list:
            emoji_list = emotki.split()
            
        self.reaction_curses[member.id] = emoji_list
        await ctx.send(f"✅ Nałożono klątwę reakcji na {member.mention}! Emotki: {' '.join(emoji_list)}", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def odczaruj_reakcje(self, ctx, member: discord.Member):
        """[BOSS] Zdejmuje klątwę reakcji z użytkownika."""
        await ctx.message.delete()
        if member.id in self.reaction_curses:
            del self.reaction_curses[member.id]
            await ctx.send(f"✨ Zdjęto klątwę reakcji z {member.mention}!", delete_after=5)
        else:
            await ctx.send(f"❓ {member.mention} nie ma nałożonej klątwy reakcji.", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def papuga(self, ctx, member: discord.Member):
        """[BOSS] Włącza klątwę papugi (Alternating caps + 🤡 emoji)."""
        await ctx.message.delete()
        if member.bot:
            return await ctx.send("❌ Nie możesz trollować botów!", delete_after=5)
            
        self.mocking_users.add(member.id)
        await ctx.send(f"🤡 Uruchomiono tryb papugi dla {member.mention}! mOcKiNg sPoNgEbOb iNiTiAtEd!", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def odczaruj_papuge(self, ctx, member: discord.Member):
        """[BOSS] Wyłącza klątwę papugi."""
        await ctx.message.delete()
        if member.id in self.mocking_users:
            self.mocking_users.remove(member.id)
            await ctx.send(f"✨ Zdjęto klątwę papugi z {member.mention}!", delete_after=5)
        else:
            await ctx.send(f"❓ {member.mention} nie jest papugą.", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def tarcza(self, ctx, member: discord.Member = None):
        """[BOSS] Aktywuje tarczę anty-pingową (domyślnie dla Ciebie)."""
        await ctx.message.delete()
        target = member or ctx.author
        self.ping_shields.add(target.id)
        await ctx.send(f"🛡️ **Tarcza Anty-Pingowa aktywowana dla {target.mention}!** Nikt nie może go teraz spingować!", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def zdejmij_tarcze(self, ctx, member: discord.Member = None):
        """[BOSS] Dezaktywuje tarczę anty-pingową."""
        await ctx.message.delete()
        target = member or ctx.author
        if target.id in self.ping_shields:
            self.ping_shields.remove(target.id)
            await ctx.send(f"🛡️ Tarcza Anty-Pingowa dezaktywowana dla {target.mention}.", delete_after=5)
        else:
            await ctx.send(f"❓ {target.mention} nie ma aktywnej tarczy.", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def zamroz(self, ctx, member: discord.Member):
        """[BOSS] Zamraża użytkownika - kasuje każdą jego wiadomość na czacie."""
        await ctx.message.delete()
        if member.bot:
            return await ctx.send("❌ Nie możesz zamrozić bota!", delete_after=5)
            
        self.frozen_users.add(member.id)
        await ctx.send(f"❄️ **Użytkownik {member.mention} został zamrożony!** Jego wiadomości będą kasowane.", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def odmroz(self, ctx, member: discord.Member):
        """[BOSS] Odmraża użytkownika."""
        await ctx.message.delete()
        if member.id in self.frozen_users:
            self.frozen_users.remove(member.id)
            await ctx.send(f"🔥 Użytkownik {member.mention} został odmrożony!", delete_after=5)
        else:
            await ctx.send(f"❓ {member.mention} nie jest zamrożony.", delete_after=5)

    async def apply_typo_curse(self, text):
        words = text.split()
        for i, word in enumerate(words):
            if len(word) > 3 and random.random() < 0.3:
                idx = random.randint(1, len(word) - 2)
                chars = list(word)
                chars[idx], chars[idx+1] = chars[idx+1], chars[idx]
                words[i] = "".join(chars)
        return " ".join(words)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def dm(self, ctx, member: discord.Member, *, tekst: str):
        """[BOSS] Wysyła prywatną wiadomość do użytkownika w imieniu bota."""
        await ctx.message.delete()
        try:
            await member.send(tekst)
            await ctx.send(f"✅ Pomyślnie wysłano DM do {member.mention}.", delete_after=3)
        except:
            await ctx.send(f"❌ Nie udało się wysłać DM do {member.mention} (zablokowane wiadomości prywatne).", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def target_purge(self, ctx, member: discord.Member, limit: int = 50):
        """[BOSS] Usuwa wiadomości określonego użytkownika z obecnego kanału."""
        await ctx.message.delete()
        def is_target(m):
            return m.author.id == member.id
        try:
            deleted = await ctx.channel.purge(limit=limit, check=is_target)
            await ctx.send(f"🧹 Usunięto {len(deleted)} wiadomości użytkownika {member.mention}.", delete_after=3)
        except Exception as e:
            await ctx.send(f"❌ Wystąpił błąd: {e}", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def audit_roles(self, ctx):
        """[BOSS] Usuwa z serwera puste role (które mają 0 członków i nie są zarządzane)."""
        await ctx.message.delete()
        deleted_roles = []
        for role in ctx.guild.roles:
            if role.is_default() or role.managed:
                continue
            if len(role.members) == 0:
                try:
                    await role.delete(reason="Audyt pustych ról przez administratora")
                    deleted_roles.append(role.name)
                except:
                    pass
        if deleted_roles:
            await ctx.send(f"🧹 **Audyt Ról Zakończony!** Usunięto {len(deleted_roles)} pustych ról:\n" + ", ".join(deleted_roles), delete_after=10)
        else:
            await ctx.send("🧹 **Audyt Ról Zakończony!** Nie znaleziono żadnych pustych ról do usunięcia.", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def literowki(self, ctx, member: discord.Member):
        """[BOSS] Nakłada klątwę literówek na użytkownika."""
        await ctx.message.delete()
        if member.bot:
            return await ctx.send("❌ Nie możesz trollować botów!", delete_after=5)
        self.typo_users.add(member.id)
        await ctx.send(f"✍️ Nakładanie klątwy literówek na {member.mention}! Jego pisanie stanie się chaotyczne...", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def odczaruj_literowki(self, ctx, member: discord.Member):
        """[BOSS] Zdejmuje klątwę literówek."""
        await ctx.message.delete()
        if member.id in self.typo_users:
            self.typo_users.remove(member.id)
            await ctx.send(f"✨ Zdjęto klątwę literówek z {member.mention}!", delete_after=5)
        else:
            await ctx.send(f"❓ {member.mention} nie ma klątwy literówek.", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def odwrocenie(self, ctx, member: discord.Member):
        """[BOSS] Nakłada klątwę odwróconego tekstu."""
        await ctx.message.delete()
        if member.bot:
            return await ctx.send("❌ Nie możesz trollować botów!", delete_after=5)
        self.reversed_users.add(member.id)
        await ctx.send(f"🔄 Włączanie klątwy odwróconego tekstu dla {member.mention}! .tekst ynałwrdo tseyZ", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def odczaruj_odwrocenie(self, ctx, member: discord.Member):
        """[BOSS] Wyłącza klątwę odwrócenia."""
        await ctx.message.delete()
        if member.id in self.reversed_users:
            self.reversed_users.remove(member.id)
            await ctx.send(f"✨ Zdjęto klątwę odwrócenia z {member.mention}!", delete_after=5)
        else:
            await ctx.send(f"❓ {member.mention} nie ma klątwy odwrócenia.", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def schizo(self, ctx, member: discord.Member):
        """[BOSS] Włącza klątwę schizofrenii (losowe denerwujące odpowiedzi od bota)."""
        await ctx.message.delete()
        if member.bot:
            return await ctx.send("❌ Nie możesz trollować botów!", delete_after=5)
        self.schizo_users.add(member.id)
        await ctx.send(f"🧠 Włączono tryb schizofrenii dla {member.mention}! Bot zacznie na niego dziwnie reagować...", delete_after=5)

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def odczaruj_schizo(self, ctx, member: discord.Member):
        """[BOSS] Wyłącza klątwę schizofrenii."""
        await ctx.message.delete()
        if member.id in self.schizo_users:
            self.schizo_users.remove(member.id)
            await ctx.send(f"✨ Zdjęto klątwę schizofrenii z {member.mention}!", delete_after=5)
        else:
            await ctx.send(f"❓ {member.mention} nie ma klątwy schizofrenii.", delete_after=5)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.webhook_id:
            return
            
        # 1. Tarcza anty-pingowa
        pinged_shielded_users = [m for m in message.mentions if m.id in getattr(self, 'ping_shields', set()) and m.id != message.author.id]
        if pinged_shielded_users:
            # Upewnij się, że autor nie jest adminem
            author_is_admin = False
            if hasattr(message.author, 'guild_permissions'):
                author_is_admin = message.author.guild_permissions.administrator
            
            if not author_is_admin:
                try:
                    await message.delete()
                except:
                    pass
                warn_msg = await message.channel.send(f"⚠️ {message.author.mention} **Nie waż się pingować mojego Pana!** ⚡")
                await asyncio.sleep(4)
                try:
                    await warn_msg.delete()
                except:
                    pass
                return

        # 2. Zamrożenie (Freeze)
        if message.author.id in getattr(self, 'frozen_users', set()):
            try:
                await message.delete()
            except:
                pass
            warn_msg = await message.channel.send(f"❄️ {message.author.mention} **Twój czat został zamrożony przez Boga!**", delete_after=3)
            return

        # 3. Sprawdzanie innych klątw
        is_italiano = message.author.id in getattr(self, 'cursed_italiano', {})
        is_femboy = message.author.id in getattr(self, 'cursed_femboy', {})
        is_mocked = message.author.id in getattr(self, 'mocking_users', set())
        is_typo = message.author.id in getattr(self, 'typo_users', set())
        is_reversed = message.author.id in getattr(self, 'reversed_users', set())
        
        if not is_italiano and not is_femboy and not is_mocked and not is_typo and not is_reversed:
            if message.author.id in getattr(self, 'schizo_users', set()):
                if random.random() < 0.25:
                    try:
                        await message.reply(random.choice(SCHIZO_RESPONSES))
                    except:
                        pass
            if message.author.id in getattr(self, 'reaction_curses', {}):
                for emo in self.reaction_curses[message.author.id]:
                    try:
                        await message.add_reaction(emo)
                    except:
                        pass
            return
            
        ctx = await self.bot.get_context(message)
        if ctx.valid and ctx.command:
            return 
            
        content = message.content
        if not content: return
        
        username = message.author.display_name
        avatar = message.author.display_avatar.url
        
        if is_italiano:
            stage = self.cursed_italiano[message.author.id]
            self.cursed_italiano[message.author.id] += 1
            content = await self.apply_italiano_curse(content, stage)
            username += " 🤌"
            
        elif is_femboy:
            stage = self.cursed_femboy[message.author.id]
            self.cursed_femboy[message.author.id] += 1
            content = await self.apply_femboy_curse(content, stage)
            username += " :3"
            
        elif is_mocked:
            content = "".join([char.upper() if i % 2 == 0 else char.lower() for i, char in enumerate(content)])
            content += " 🤡"
            username += " 🤡"

        elif is_typo:
            content = await self.apply_typo_curse(content)
            username += " ✍️"

        elif is_reversed:
            content = content[::-1]
            username += " 🔄"

        try:
            await message.delete()
        except discord.errors.Forbidden:
            pass

        webhook = None
        webhooks = await message.channel.webhooks()
        for wh in webhooks:
            if wh.name == "Troll Webhook":
                webhook = wh
                break
                
        if not webhook:
            try:
                webhook = await message.channel.create_webhook(name="Troll Webhook")
            except:
                return
                
        try:
            sent_msg = await webhook.send(
                content=content[:2000],
                username=username[:80],
                avatar_url=avatar,
                wait=True
            )
            if message.author.id in getattr(self, 'reaction_curses', {}):
                for emo in self.reaction_curses[message.author.id]:
                    try:
                        await sent_msg.add_reaction(emo)
                    except:
                        pass
            if message.author.id in getattr(self, 'schizo_users', set()):
                if random.random() < 0.25:
                    try:
                        await sent_msg.reply(random.choice(SCHIZO_RESPONSES))
                    except:
                        pass
        except Exception as e:
            print(f"Błąd troll webhooka: {e}")

async def setup(bot):
    await bot.add_cog(MassTroll(bot))
