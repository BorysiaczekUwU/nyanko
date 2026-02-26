import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import asyncio
from datetime import datetime, timedelta, timezone
from utils import KAWAII_RED, KAWAII_PINK, KAWAII_GOLD, update_data

# Gify
GIFS_BAN = ["https://media.giphy.com/media/fe4dDMD2cAU5RfEaCU/giphy.gif", "https://media.giphy.com/media/AC1HrkBir3bzq/giphy.gif"]
GIFS_KICK = ["https://media.giphy.com/media/wQCWMHY9EHLfq/giphy.gif", "https://media.giphy.com/media/26FPn4rR1damB0MQo/giphy.gif"]
GIFS_MUTE = ["https://media.giphy.com/media/hfBvLPfHXRLO1gYgJv/giphy.gif", "https://media.giphy.com/media/liW10vuLjuUA8/giphy.gif"]
GIFS_NUKE = ["https://media.giphy.com/media/OE6FE4GZF78nm/giphy.gif"]

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

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- KOMENDY ---
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sudo(self, ctx, member: discord.Member, *, message):
        """Pisze jako inny użytkownik (Webhook)"""
        await ctx.message.delete()
        webhook = await ctx.channel.create_webhook(name=member.display_name)
        await webhook.send(str(message), username=member.display_name, avatar_url=member.avatar.url or member.default_avatar.url)
        await webhook.delete()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def fakeban(self, ctx, member: discord.Member):
        """Udawany ban"""
        await ctx.message.delete()
        embed = discord.Embed(title="🔨 BAN HAMMER!", description=f"Baka **{member.name}** zbanowany!\nPowód: Bycie zbyt słodkim", color=KAWAII_RED)
        embed.set_image(url=random.choice(GIFS_BAN))
        embed.set_footer(text="To tylko żart... ( ͡° ͜ʖ ͡°)")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def dm(self, ctx, member: discord.Member, *, message):
        """Wysyła wiadomość prywatną jako bot"""
        await ctx.message.delete()
        try:
            await member.send(f"📩 **Wiadomość od Administracji:**\n{message}")
            await ctx.send(f"✅ Wysłano DM do {member.name}.", delete_after=5)
        except:
            await ctx.send(f"❌ Użytkownik ma zablokowane DM.", delete_after=5)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def duch(self, ctx, member: discord.Member):
        """(Troll) Straszy użytkownika na DM"""
        await ctx.message.delete()
        try:
            await member.send("👻 BUUU! Widzę Cię... 👀")
            await ctx.send(f"👻 Nastraszono {member.name}!", delete_after=5)
        except:
             await ctx.send("❌ Nie udało się nastraszyć (DM zablokowane).")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx):
        pos = ctx.channel.position
        new_ch = await ctx.channel.clone()
        await new_ch.edit(position=pos)
        await ctx.channel.delete()
        embed = discord.Embed(title="☢️ NUKE!", description="Kanał zresetowany! ✨", color=KAWAII_GOLD)
        embed.set_image(url=random.choice(GIFS_NUKE))
        await new_ch.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear_user(self, ctx, member: discord.Member, amount: int = 10):
        """Wyczyść wiadomości konkretnej osoby"""
        def check(m):
            return m.author == member

        deleted = await ctx.channel.purge(limit=amount, check=check)
        await ctx.send(f"🗑️ Usunięto **{len(deleted)}** wiadomości od {member.name}.", delete_after=5)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx):
        """Zablokuj kanał dla @everyone"""
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 KANAŁ ZABLOKOWANY!")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlockdown(self, ctx):
        """Odblokuj kanał dla @everyone"""
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("🔓 KANAŁ ODBLOKOWANY!")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"🐢 Slowmode: **{seconds}s**!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def nadaj_role(self, ctx, member: discord.Member, role: discord.Role):
        if ctx.author.top_role <= role:
            return await ctx.send("⛔ Ta rola jest powyżej Twojej!")
        try:
            await member.add_roles(role)
            await ctx.send(f"✅ Nadano rolę **{role.name}** użytkownikowi {member.mention}!")
        except Exception as e:
            await ctx.send(f"❌ Błąd: {e}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def zabierz_role(self, ctx, member: discord.Member, role: discord.Role):
        if ctx.author.top_role <= role:
            return await ctx.send("⛔ Ta rola jest powyżej Twojej!")
        try:
            await member.remove_roles(role)
            await ctx.send(f"🗑️ Zabrano rolę **{role.name}** użytkownikowi {member.mention}!")
        except Exception as e:
            await ctx.send(f"❌ Błąd: {e}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
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
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="Brak"):
        if member.top_role >= ctx.author.top_role: return
        await send_dm_log(member, ctx.guild.name, reason, "BAN")
        try:
            await member.ban(reason=reason)
            embed = discord.Embed(title="🔨 ZBANOWANO!", description=f"**{member.name}** wygnany!\nPowód: {reason}", color=KAWAII_RED)
            embed.set_image(url=random.choice(GIFS_BAN))
            await ctx.send(embed=embed)
        except: await ctx.send("❌ Błąd.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
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
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int, *, reason="Spam"):
        if member.top_role >= ctx.author.top_role: return
        await member.timeout(timedelta(minutes=minutes), reason=reason)
        embed = discord.Embed(title="🤐 MUTE", description=f"**{member.name}** uciszony na **{minutes}m**.", color=discord.Color.dark_grey())
        embed.set_image(url=random.choice(GIFS_MUTE))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def unmute(self, ctx, member: discord.Member):
        """Zdejmuje wyciszenie"""
        if member.top_role >= ctx.author.top_role: return
        await member.timeout(None)
        await ctx.send(f"🔊 **{member.name}** odzyskał głos!")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = 10):
        """Usuwa określoną liczbę wiadomości"""
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"🗑️ Wyczyszczono **{amount}** wiadomości!", delete_after=5)

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send("🔒 Zablokowano!")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
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

    @commands.command()
    @commands.has_permissions(moderate_members=True)
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
    @commands.has_permissions(moderate_members=True)
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
    @commands.has_permissions(administrator=True)
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

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def domena(self, ctx, member: discord.Member):
        guild = ctx.guild
        judge_role = discord.utils.get(guild.roles, name="Sędzia")
        if not judge_role: judge_role = await guild.create_role(name="Sędzia", color=discord.Color.gold(), hoist=True)
        
        jail_role = discord.utils.get(guild.roles, name="Izolatka")
        if not jail_role:
            jail_role = await guild.create_role(name="Izolatka", color=discord.Color.dark_grey())
            for channel in guild.channels: await channel.set_permissions(jail_role, view_channel=False)

        verified_role = discord.utils.get(guild.roles, name="—͟͞✅・Bilecik")
        if verified_role and verified_role in member.roles: await member.remove_roles(verified_role)
        await member.add_roles(jail_role)
        
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            jail_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            judge_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            self.bot.user: discord.PermissionOverwrite(view_channel=True)
        }
        
        ch_name = f"sąd-nad-{member.name}".lower().replace("#", "")
        trial_ch = await guild.create_text_channel(ch_name, overwrites=overwrites)
        
        embed = discord.Embed(title="⚖️ DOMENA SĄDOWA", description=f"Oskarżony: {member.mention}", color=0x800000)
        embed.set_image(url="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnY2Y2gxeDR3MGMydDM3YjRpa2JhZjluZGJ5YWlobnp0YTM2eDc2YiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/A3Fe9A2d3bbDXxxR6t/giphy.gif")
        
        view = TrialView(self.bot, member, jail_role, verified_role, trial_ch)
        await trial_ch.send(f"{member.mention} {judge_role.mention}", embed=embed, view=view)
        await ctx.send(f"⛓️ **{member.name}** trafił do Domeny!")

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
    @commands.has_permissions(manage_nicknames=True)
    async def chname(self, ctx, member: discord.Member, *, new_name):
        """[ZARZĄDZANIE] Zmienia pseudonim użytkownika na serwerze."""
        try:
            old_name = member.display_name
            await member.edit(nick=new_name)
            await ctx.send(f"✅ Zmieniono nick z **{old_name}** na **{new_name}**!")
        except Exception as e:
            await ctx.send(f"❌ Nie mogłem zmienić nicku: {e}")

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
    @commands.has_permissions(administrator=True)
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
    @commands.has_permissions(administrator=True)
    async def timeout_ruletka(self, ctx):
        """[TROLL] Losuje użytkownika i daje mu timeout na 1 minutę."""
        members = [m for m in ctx.guild.members if not m.bot and not m.guild_permissions.administrator]
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

async def setup(bot):
    await bot.add_cog(Admin(bot))
