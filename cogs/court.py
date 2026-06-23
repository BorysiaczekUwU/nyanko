import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import asyncio
from datetime import datetime, timedelta
from utils import KAWAII_RED, KAWAII_PINK, KAWAII_GOLD, update_data

class TrialView(View):
    def __init__(self, bot, member, jail_role, channel):
        super().__init__(timeout=None)
        self.bot = bot
        self.member = member
        self.jail_role = jail_role
        self.channel = channel

    @discord.ui.button(label="Ułaskaw", style=discord.ButtonStyle.green, emoji="🕊️")
    async def pardon(self, interaction: discord.Interaction, button: Button):
        is_judge = any(r.name == "Sędzia" for r in interaction.user.roles)
        is_admin = interaction.user.guild_permissions.administrator
        is_owner = interaction.user.name.lower() == "≽^BorysiaczekUwU^≼"
        
        if not (is_judge or is_admin or is_owner):
            return await interaction.response.send_message("❌ Tylko Sędzia lub Administrator może wydać werdykt!", ephemeral=True)
            
        await interaction.response.send_message("🕊️ **Werdykt: Ułaskawienie.** Kanał rozprawy zostanie zamknięty za 5 sekund...")
        
        embed = discord.Embed(
            title="🕊️ ROZPRAWA SĄDOWA: UŁASKAWIENIE",
            description=f"Oskarżony {self.member.mention} został uznany za **niewinnego** i ułaskawiony przez sędziego {interaction.user.mention}!",
            color=discord.Color.green()
        )
        await self.channel.send(embed=embed)
        
        try:
            await self.member.remove_roles(self.jail_role)
            verified_role = discord.utils.get(interaction.guild.roles, name="—͟͞✅・Bilecik")
            if verified_role:
                await self.member.add_roles(verified_role)
        except Exception as e:
            await self.channel.send(f"⚠️ Błąd podczas modyfikacji ról: {e}")
            
        await asyncio.sleep(5)
        try:
            await self.channel.delete()
        except:
            pass

    @discord.ui.button(label="Ucisz (24h)", style=discord.ButtonStyle.secondary, emoji="🤐")
    async def mute(self, interaction: discord.Interaction, button: Button):
        is_judge = any(r.name == "Sędzia" for r in interaction.user.roles)
        is_admin = interaction.user.guild_permissions.administrator
        is_owner = interaction.user.name.lower() == "≽^BorysiaczekUwU^≼"
        
        if not (is_judge or is_admin or is_owner):
            return await interaction.response.send_message("❌ Tylko Sędzia lub Administrator może wydać werdykt!", ephemeral=True)
            
        await interaction.response.send_message("🤐 **Werdykt: Wyciszenie na 24h.** Kanał rozprawy zostanie zamknięty za 5 sekund...")
        
        embed = discord.Embed(
            title="🤐 ROZPRAWA SĄDOWA: WYCISZENIE",
            description=f"Oskarżony {self.member.mention} został uznany za **winnego** i wyciszony na 24 godziny przez sędziego {interaction.user.mention}!",
            color=discord.Color.orange()
        )
        await self.channel.send(embed=embed)
        
        try:
            await self.member.remove_roles(self.jail_role)
            verified_role = discord.utils.get(interaction.guild.roles, name="—͟͞✅・Bilecik")
            if verified_role:
                await self.member.add_roles(verified_role)
            await self.member.timeout(timedelta(days=1), reason="Werdykt sędziowski: Mute 24h")
        except Exception as e:
            await self.channel.send(f"⚠️ Błąd podczas modyfikacji ról lub mutowania: {e}")
            
        await asyncio.sleep(5)
        try:
            await self.channel.delete()
        except:
            pass

    @discord.ui.button(label="Winny (Ban)", style=discord.ButtonStyle.danger, emoji="🔨")
    async def guilty(self, interaction: discord.Interaction, button: Button):
        is_judge = any(r.name == "Sędzia" for r in interaction.user.roles)
        is_admin = interaction.user.guild_permissions.ban_members
        is_owner = interaction.user.name.lower() == "≽^BorysiaczekUwU^≼"
        
        if not (is_judge or is_admin or is_owner):
            return await interaction.response.send_message("❌ Tylko Sędzia lub Administrator z prawami do banowania może wydać werdykt!", ephemeral=True)
            
        await interaction.response.send_message("🔨 **Werdykt: Banicja.** Oskarżony zostanie zbanowany, a kanał zostanie zamknięty za 5 sekund...")
        
        embed = discord.Embed(
            title="🔨 ROZPRAWA SĄDOWA: BAN",
            description=f"Oskarżony {self.member.mention} został uznany za **winnego** i zbanowany z serwera przez sędziego {interaction.user.mention}!",
            color=discord.Color.red()
        )
        await self.channel.send(embed=embed)
        
        await asyncio.sleep(5)
        try:
            await self.member.ban(reason="Domena Sądowa: Winny (Werdykt)")
        except Exception as e:
            await self.channel.send(f"⚠️ Błąd podczas banowania oskarżonego: {e}")
            return
            
        try:
            await self.channel.delete()
        except:
            pass

def is_court_channel():
    async def predicate(ctx):
        if not ctx.channel.name.startswith("sąd-nad-"):
            try:
                await ctx.message.delete()
            except:
                pass
            embed = discord.Embed(
                title="⚖️ Sala Sądowa",
                description="Ta komenda roleplay może być użyta **tylko** wewnątrz aktywnej sali rozpraw (Domeny Sądowej)!",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed, delete_after=5)
            return False
        return True
    return commands.check(predicate)

class Court(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.evidence_counts = {}

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def domena(self, ctx, member: discord.Member, *, powod="Brak określonego powodu"):
        """Tworzy salę sądową dla oskarżonego użytkownika."""
        guild = ctx.guild
        
        # Przygotowanie roli Sędzia
        judge_role = discord.utils.get(guild.roles, name="Sędzia")
        if not judge_role:
            judge_role = await guild.create_role(name="Sędzia", color=discord.Color.gold(), hoist=True)
        
        # Przygotowanie roli Izolatka
        jail_role = discord.utils.get(guild.roles, name="Izolatka")
        if not jail_role:
            jail_role = await guild.create_role(name="Izolatka", color=discord.Color.dark_grey())
            for channel in guild.channels:
                try:
                    await channel.set_permissions(jail_role, view_channel=False)
                except:
                    pass

        # Odebranie roli Bilecik i nadanie Izolatki
        verified_role = discord.utils.get(guild.roles, name="—͟͞✅・Bilecik")
        if verified_role and verified_role in member.roles:
            try:
                await member.remove_roles(verified_role)
            except:
                pass
        try:
            await member.add_roles(jail_role)
        except Exception as e:
            return await ctx.send(f"❌ Nie udało się nadać roli Izolatka dla {member.mention}. Błąd: {e}")
        
        # Uprawnienia dla nowego kanału
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            jail_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            judge_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            self.bot.user: discord.PermissionOverwrite(view_channel=True)
        }
        
        ch_name = f"sąd-nad-{member.name}".lower().replace("#", "")
        # Zapisujemy ID oskarżonego w temacie kanału (topic)
        trial_ch = await guild.create_text_channel(ch_name, overwrites=overwrites, topic=str(member.id))
        
        # Prezentacja sali rozpraw
        embed = discord.Embed(
            title="⚖️ ROZPOCZĘTO ROZPRAWĘ SĄDOWĄ", 
            description=f"Wysoki Sąd zebrał się w sprawie obywatela {member.mention}.\n\n"
                        f"**Powód oskarżenia:**\n`{powod}`", 
            color=0x800000
        )
        embed.add_field(
            name="📋 Dostępne Komendy Roleplay:",
            value="🔹 `!rp oskarzenie <powód>` - Odczytanie zarzutów\n"
                  "🔹 `!rp obrona <argumenty>` - Argumenty obrony\n"
                  "🔹 `!rp dowod <szczegóły>` - Wniesienie dowodu (można załączyć obrazek)\n"
                  "🔹 `!rp swiadek <@użytkownik>` - Wezwanie świadka na salę\n"
                  "🔹 `!rp usun_swiadka <@użytkownik>` - Odesłanie świadka\n"
                  "🔹 `!rp sprzeciw [powód]` - Wniesienie sprzeciwu (*Objection!*)\n"
                  "🔹 `!rp ugoda <treść>` - Zaproponowanie ugody\n"
                  "🔹 `!rp mlotek` - Uciszenie sali rozpraw 🔨\n"
                  "🔹 `!rp wyrok <sentencja>` - Ustne ogłoszenie wyroku\n",
            inline=False
        )
        embed.set_image(url="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnY2Y2gxeDR3MGMydDM3YjRpa2JhZjluZGJ5YWlobnp0YTM2eDc2YiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/A3Fe9A2d3bbDXxxR6t/giphy.gif")
        embed.set_footer(text="Sędziowie mogą korzystać z poniższych przycisków szybkiego werdyktu.")
        
        view = TrialView(self.bot, member, jail_role, trial_ch)
        await trial_ch.send(f"{member.mention} {judge_role.mention}", embed=embed, view=view)
        await ctx.send(f"⛓️ **{member.name}** został doprowadzony do sali rozpraw! ({trial_ch.mention})")

    # --- GRUPA KOMEND RP ---
    @commands.group(name="rp", invoke_without_command=True)
    @is_court_channel()
    async def rp(self, ctx):
        """Pomoc dotycząca roleplay'u sądowego."""
        embed = discord.Embed(title="⚖️ KANCELARIA RP BOTA NYANKO", color=0x2b2d31)
        embed.description = (
            "Witaj w oficjalnym systemie Roleplay Sądowego!\n"
            "Te komendy działają **wyłącznie** na kanałach rozpraw (`sąd-nad-...`).\n\n"
            "**Dostępne komendy RP:**\n"
            "🔸 `!rp pomoc` - Wyświetla to menu pomocnicze\n"
            "🔸 `!rp oskarzenie <powód>` - Formalne odczytanie aktu oskarżenia\n"
            "🔸 `!rp obrona <argumenty>` - Oświadczenie obrony oskarżonego\n"
            "🔸 `!rp dowod <opis / link>` - Wniesienie nowego dowodu do sprawy\n"
            "🔸 `!rp swiadek <@użytkownik>` - Powołanie świadka (nadaje dostęp do kanału)\n"
            "🔸 `!rp usun_swiadka <@użytkownik>` - Usunięcie świadka z rozprawy\n"
            "🔸 `!rp sprzeciw [powód]` - Klasyczne *Objection!* w stylu Phoenix Wright\n"
            "🔸 `!rp ugoda <propozycja>` - Zaoferowanie ugody oskarżycielowi\n"
            "🔸 `!rp mlotek` - Uderzenie młotkiem sędziowskim (wezwanie do ciszy)\n"
            "🔸 `!rp wyrok <kara / powód>` - Ogłoszenie wyroku przez sędziego\n"
        )
        embed.set_footer(text="Nieznajomość prawa nie zwalnia z odpowiedzialności!")
        await ctx.send(embed=embed)

    @rp.command(name="pomoc")
    @is_court_channel()
    async def pomoc(self, ctx):
        """Wyświetla pomoc dla komend RP."""
        await self.rp(ctx)

    @rp.command(name="oskarzenie")
    @is_court_channel()
    async def oskarzenie(self, ctx, *, powod: str):
        """Odczytuje akt oskarżenia."""
        accused_id = int(ctx.channel.topic) if ctx.channel.topic and ctx.channel.topic.isdigit() else None
        accused = ctx.guild.get_member(accused_id) if accused_id else None
        
        embed = discord.Embed(title="📜 SPECJALNY AKT OSKARŻENIA", color=0x800000)
        embed.set_thumbnail(url="https://media.giphy.com/media/A3Fe9A2d3bbDXxxR6t/giphy.gif")
        embed.add_field(name="⚖️ Wysoki Sądzie,", value="Wnoszę oficjalny akt oskarżenia przeciwko obywatelowi:", inline=False)
        embed.add_field(name="👤 Oskarżony", value=f"{accused.mention} ({accused.name})" if accused else "Nieznany sprawca", inline=True)
        embed.add_field(name="👮 Oskarżyciel", value=ctx.author.mention, inline=True)
        embed.add_field(name="📜 Zarzuty i uzasadnienie", value=powod, inline=False)
        embed.set_footer(text="Sprawa w toku... Prosimy o zachowanie powagi.")
        await ctx.send(embed=embed)

    @rp.command(name="obrona")
    @is_court_channel()
    async def obrona(self, ctx, *, argument: str):
        """Prezentuje argumenty obrony."""
        embed = discord.Embed(title="🛡️ OŚWIADCZENIE OBRONY", color=0x3498db)
        embed.add_field(name="👤 Obrońca / Oskarżony", value=ctx.author.mention, inline=True)
        embed.add_field(name="💬 Argumentacja obrony", value=argument, inline=False)
        embed.set_footer(text="Niewinny dopóki wina nie zostanie udowodniona!")
        await ctx.send(embed=embed)

    @rp.command(name="dowod")
    @is_court_channel()
    async def dowod(self, ctx, *, opis: str):
        """Wnosi dowód do sprawy."""
        ch_id = ctx.channel.id
        self.evidence_counts[ch_id] = self.evidence_counts.get(ch_id, 0) + 1
        count = self.evidence_counts[ch_id]
        
        embed = discord.Embed(title=f"📁 DOWÓD RZECZOWY #{count}", color=0xe67e22)
        embed.add_field(name="🔍 Wnoszący", value=ctx.author.mention, inline=True)
        embed.add_field(name="📂 Szczegóły dowodu", value=opis, inline=False)
        
        if ctx.message.attachments:
            embed.set_image(url=ctx.message.attachments[0].url)
            
        embed.set_footer(text="Dowód włączony do akt sprawy.")
        await ctx.send(embed=embed)

    @rp.command(name="swiadek")
    @is_court_channel()
    async def swiadek(self, ctx, member: discord.Member):
        """Wzywa świadka na salę rozpraw."""
        await ctx.channel.set_permissions(member, view_channel=True, send_messages=True)
        
        embed = discord.Embed(title="🗣️ WEZWANIE ŚWIADKA", color=0x9b59b6)
        embed.description = f"{ctx.author.mention} powołuje na świadka użytkownika {member.mention}!\nZostały mu nadane tymczasowe prawa do wglądu i wypowiadania się w tej sali sądowej."
        embed.set_image(url="https://media.giphy.com/media/xT39C1yV1r9rV7sU00/giphy.gif")
        await ctx.send(embed=embed)

    @rp.command(name="usun_swiadka")
    @is_court_channel()
    async def usun_swiadka(self, ctx, member: discord.Member):
        """Odbiera świadkowi dostęp do sali rozpraw."""
        await ctx.channel.set_permissions(member, overwrite=None)
        
        embed = discord.Embed(title="👋 ZWOLNIENIE ŚWIADKA", color=0x95a5a6)
        embed.description = f"Świadek {member.mention} został zwolniony z dalszego składania zeznań i usunięty z sali rozpraw."
        await ctx.send(embed=embed)

    @rp.command(name="sprzeciw")
    @is_court_channel()
    async def sprzeciw(self, ctx, *, powod: str = None):
        """Wnosi sprzeciw (Objection!)."""
        gifs = [
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3ZhcjQyN3lxbzB5N3Y5ZWNwcTN4ODdsZGtzcncyNngybndsdnh2OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3jx7gLw5asg80/giphy.gif",
            "https://media.giphy.com/media/qE4aESRe9F7k4/giphy.gif",
            "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExczM1ZWZqZnpyZ3pxczE1amNqZGdwb3ZsdmpxdmR3MmNrbXZlOXhhbyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5Mv68aAQC5P1K/giphy.gif"
        ]
        quotes = [
            "Zeznania świadka rażąco mijają się z prawdą!",
            "Oskarżyciel nie przedstawił żadnych dowodów na tę tezę!",
            "Te argumenty są całkowicie bezpodstawne!",
            "Proszę trzymać się faktów, a nie spekulacji!",
            "Ten dowód nie ma żadnego związku ze sprawą!"
        ]
        quote = powod if powod else random.choice(quotes)
           
        embed = discord.Embed(title="⚡ SPRZECIW! (OBJECTION!)", color=0xe74c3c)
        embed.description = f"**{ctx.author.name}** wnosi oficjalny sprzeciw!\n\n*\" {quote} \"*"
        embed.set_image(url=random.choice(gifs))
        await ctx.send(embed=embed)

    @rp.command(name="ugoda")
    @is_court_channel()
    async def ugoda(self, ctx, *, tekst: str):
        """Proponuje ugodę."""
        embed = discord.Embed(title="🤝 PROPOZYCJA UGODY", color=0x1abc9c)
        embed.add_field(name="Proponujący", value=ctx.author.mention, inline=True)
        embed.add_field(name="Warunki ugody", value=tekst, inline=False)
        embed.set_footer(text="Czy oskarżyciel/sędzia zaakceptuje te warunki?")
        await ctx.send(embed=embed)

    @rp.command(name="mlotek")
    @is_court_channel()
    async def mlotek(self, ctx):
        """Wzywa salę do zachowania ciszy."""
        embed = discord.Embed(title="🔨 CISZA NA SALI! (ORDER IN COURT!)", color=0xf39c12)
        embed.description = f"**{ctx.author.name}** uderza młotkiem sędziowskim!\nProszę natychmiast zachować spokój i porządek!"
        embed.set_image(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExdzB2MndhY2JkOXEzdWVhZGtxMDJmaGk0YjVmbTJ4ZW5zMWRsb2F6MSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/rCItxkkwzr2W4/giphy.gif")
        await ctx.send(embed=embed)

    @rp.command(name="wyrok")
    @is_court_channel()
    async def wyrok(self, ctx, *, kara: str):
        """Ogłasza oficjalny wyrok (Tylko Sędzia/Admin)."""
        is_judge = any(r.name == "Sędzia" for r in ctx.author.roles)
        is_admin = ctx.author.guild_permissions.administrator
        is_owner = ctx.author.name.lower() == "≽^BorysiaczekUwU^≼"
        
        if not (is_judge or is_admin or is_owner):
            return await ctx.send("❌ Tylko Sędzia lub Administrator może wydać oficjalny wyrok!")
            
        accused_id = int(ctx.channel.topic) if ctx.channel.topic and ctx.channel.topic.isdigit() else None
        accused = ctx.guild.get_member(accused_id) if accused_id else None
        
        embed = discord.Embed(title="⚖️ OFICJALNY WYROK SĄDOWY", color=0x800000)
        embed.add_field(name="👨‍⚖️ Skład orzekający", value=ctx.author.mention, inline=True)
        embed.add_field(name="👤 Skazany", value=accused.mention if accused else "Nieznany oskarżony", inline=True)
        embed.add_field(name="📜 Sentencja wyroku", value=kara, inline=False)
        embed.set_image(url="https://media.giphy.com/media/A3Fe9A2d3bbDXxxR6t/giphy.gif")
        embed.set_footer(text="Wyrok orzeczony w imieniu sprawiedliwości serwerowej.")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Court(bot))
