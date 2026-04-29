import discord
from discord.ext import commands
import asyncio
from cogs.admin import has_perms_or_borysiaczek
from utils import KAWAII_RED
import random
import re

class MassTroll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cursed_italiano = {}
        self.cursed_femboy = {}

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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.webhook_id:
            return
            
        is_italiano = message.author.id in getattr(self, 'cursed_italiano', {})
        is_femboy = message.author.id in getattr(self, 'cursed_femboy', {})
        
        if not is_italiano and not is_femboy:
            return
            
        ctx = await self.bot.get_context(message)
        if ctx.valid and ctx.command:
            return 
            
        content = message.content
        if not content: return
        
        if is_italiano:
            stage = self.cursed_italiano[message.author.id]
            self.cursed_italiano[message.author.id] += 1
            content = await self.apply_italiano_curse(content, stage)
            username = message.author.display_name + " 🤌"
            avatar = message.author.display_avatar.url
            
        elif is_femboy:
            stage = self.cursed_femboy[message.author.id]
            self.cursed_femboy[message.author.id] += 1
            content = await self.apply_femboy_curse(content, stage)
            username = message.author.display_name + " :3"
            avatar = message.author.display_avatar.url

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
            await webhook.send(
                content=content[:2000],
                username=username[:80],
                avatar_url=avatar
            )
        except Exception as e:
            print(f"Błąd troll webhooka: {e}")

async def setup(bot):
    await bot.add_cog(MassTroll(bot))
