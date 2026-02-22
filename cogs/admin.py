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

# --- WIDOKI (Przyciski) ---
class VerifyView(View):
    def __init__(self, bot, member, verified_role, channel):
        super().__init__(timeout=None)
        self.bot = bot
        self.member = member
        self.verified_role = verified_role
        self.channel = channel

    @discord.ui.button(label="✅ ZATWIERDŹ (BILECIK)", style=discord.ButtonStyle.green, emoji="🎟️")
    async def verify_button(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("⛔ Czekamy na administratora!", ephemeral=True)
            return

        await self.member.add_roles(self.verified_role)
        update_data(self.member.id, "balance", 100, "add") # Bonus
        
        await interaction.response.send_message(f"🎉 **{self.member.name}** zweryfikowany! Kanał zniknie za 5s.")
        general = discord.utils.get(interaction.guild.text_channels, name="ogólny")
        if general:
            embed = discord.Embed(description=f"Witamy **{self.member.mention}**! (≧◡≦) ♡\nNadano rolę **—͟͞✅・Bilecik**! 🎟️", color=KAWAII_PINK)
            await general.send(embed=embed)

        await asyncio.sleep(5)
        await self.channel.delete()

    @discord.ui.button(label="👋 WYRZUĆ", style=discord.ButtonStyle.danger, emoji="👢")
    async def kick_button(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("⛔ Brak uprawnień do wyrzucania!", ephemeral=True)
            return

        try:
            await interaction.response.send_message(f"👢 Wypierdalaj {self.member.mention}...", ephemeral=True)
            await self.member.kick(reason=f"Wyrzucono przy weryfikacji przez {interaction.user.name}")

            embed = discord.Embed(title="👋 WYRZUCONO!", description=f"**{self.member.name}** nie przeszedł weryfikacji.", color=discord.Color.orange())
            embed.set_image(url=random.choice(GIFS_KICK))
            await self.channel.send(embed=embed)

            await asyncio.sleep(5)
            await self.channel.delete()
        except Exception as e:
            await self.channel.send(f"❌ Nie udało się wyrzucić użytkownika: {e}")

    @discord.ui.button(label="🔨 ZBANUJ", style=discord.ButtonStyle.danger, emoji="🔨")
    async def ban_button(self, interaction: discord.Interaction, button: Button):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("⛔ Brak uprawnień do banowania!", ephemeral=True)
            return

        try:
            await interaction.response.send_message(f"🔨 Wypierdalaj i nie wracaj {self.member.mention}...", ephemeral=True)
            await self.member.ban(reason=f"Zbanowano przy weryfikacji przez {interaction.user.name}")

            embed = discord.Embed(title="🔨 ZBANOWANO!", description=f"**{self.member.name}** nie przeszedł weryfikacji.", color=KAWAII_RED)
            embed.set_image(url=random.choice(GIFS_BAN))
            await self.channel.send(embed=embed)

            await asyncio.sleep(5)
            await self.channel.delete()
        except Exception as e:
            await self.channel.send(f"❌ Nie udało się zbanować użytkownika: {e}")

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
            await interaction.response.send_message("⛔ Tylko Sędzia!", ephemeral=True)
            return

        embed = discord.Embed(title="⚖️ WYROK ZAPADŁ!", description=f"**{self.member.name}** winny! Kara: **BAN**", color=KAWAII_RED)
        embed.set_image(url=random.choice(GIFS_BAN))
        await interaction.response.send_message(embed=embed)

        # Publiczne ogłoszenie wyroku
        general = discord.utils.get(interaction.guild.text_channels, name="ogólny")
        if general:
            await general.send(f"⚖️ **WYROK SĄDU:** Użytkownik {self.member.mention} został skazany na banicję! 🔨")

        await send_dm_log(self.member, interaction.guild.name, "Wyrok Sądu", "BAN")
        await asyncio.sleep(3)
        try:
            await self.member.ban(reason="Wyrok Sądu")
        except:
            await self.channel.send("❌ Błąd bana.")
        await asyncio.sleep(2)
        await self.channel.delete()

    @discord.ui.button(label="🕊️ UŁASKAWIENIE", style=discord.ButtonStyle.success, emoji="🍀")
    async def pardon_button(self, interaction: discord.Interaction, button: Button):
        is_judge = "Sędzia" in [r.name for r in interaction.user.roles]
        if not is_judge and not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("⛔ Tylko Sędzia!", ephemeral=True)
            return

        embed = discord.Embed(title="🍀 UŁASKAWIENIE", description=f"**{self.member.name}** wolny! Oddaję bilecik! ✨", color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

        # Publiczne ogłoszenie ułaskawienia
        general = discord.utils.get(interaction.guild.text_channels, name="ogólny")
        if general:
            await general.send(f"🍀 **UŁASKAWIENIE:** Użytkownik {self.member.mention} powrócił do nas! Witamy z powrotem! 🎉")

        try:
            await self.member.remove_roles(self.role_izolatka)
            if self.role_verified: await self.member.add_roles(self.role_verified)
        except: pass
        await asyncio.sleep(5)
        await self.channel.delete()

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.join_times = {} # {guild_id: [datetime, ...]}
        self.raid_mode = {}  # {guild_id: bool}
        self.raid_end_time = {} # {guild_id: datetime}

    # --- LISTENER: Weryfikacja po wejściu ---
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # --- ANTI-RAID SYSTEM ---
        guild_id = member.guild.id
        now = datetime.now(timezone.utc)

        # Inicjalizacja dla gildii
        if guild_id not in self.join_times: self.join_times[guild_id] = []
        if guild_id not in self.raid_mode: self.raid_mode[guild_id] = False
        if guild_id not in self.raid_end_time: self.raid_end_time[guild_id] = None

        # Czyszczenie starych wpisów (> 60s)
        self.join_times[guild_id] = [t for t in self.join_times[guild_id] if (now - t).total_seconds() < 60]
        self.join_times[guild_id].append(now)

        # Sprawdzenie czy włączyć Raid Mode
        if len(self.join_times[guild_id]) > 10 and not self.raid_mode[guild_id]:
            self.raid_mode[guild_id] = True
            self.raid_end_time[guild_id] = now + timedelta(minutes=5)
            print(f"🚨 RAID MODE AKTYWOWANY W {member.guild.name} DO {self.raid_end_time[guild_id]}!")

            # Opcjonalnie: Powiadomienie na kanale
            general = discord.utils.get(member.guild.text_channels, name="ogólny")
            if general:
                await general.send("🚨 **SYSTEM ANTY-RAID AKTYWOWANY!** Nowi użytkownicy będą wyrzucani przez 5 minut.")

        # Obsługa Raid Mode
        if self.raid_mode[guild_id]:
            if now > self.raid_end_time[guild_id]:
                self.raid_mode[guild_id] = False
                print(f"🚨 Raid Mode zakończony w {member.guild.name}.")
                general = discord.utils.get(member.guild.text_channels, name="ogólny")
                if general:
                    await general.send("✅ **Sytuacja opanowana.** System Anty-Raid wyłączony.")
            else:
                # Wyrzucamy użytkownika
                try:
                    await member.send("⛔ Serwer jest w trybie ochrony przed rajdem. Spróbuj ponownie za 5 minut.")
                    await member.kick(reason="Anti-Raid System")
                    return # Przerywamy dalszą obsługę (weryfikację)
                except Exception as e:
                    print(f"Błąd kicka (raid): {e}")

        guild = member.guild
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

        channel_name = f"weryfikacja-{member.name}".lower().replace("#", "")
        try:
            channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
            embed = discord.Embed(title=f"🌸 Witaj {member.name}!", description="Napisz coś o sobie! W międzyczasie możesz użyć komendy !setbio", color=KAWAII_PINK)
            view = VerifyView(self.bot, member, verified_role, channel)
            await channel.send(f"{member.mention}", embed=embed, view=view)
        except Exception as e: print(f"Błąd weryfikacji: {e}")

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
    @commands.has_permissions(administrator=True)
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
