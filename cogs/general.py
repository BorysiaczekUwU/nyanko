import discord
from discord.ext import commands
import aiohttp
import asyncio
from utils import KAWAII_PINK, KAWAII_RED, KAWAII_GOLD

class HelpSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="💰 Ekonomia", description="Giełda, Tycoon, Sklep, Praca", emoji="💰"),
            discord.SelectOption(label="🎰 Gry", description="Kasyno, Kostka, Pojedynki", emoji="🎰"),
            discord.SelectOption(label="🧸 Social", description="Przytulanie, Śluby, Roleplay", emoji="🧸"),
            discord.SelectOption(label="ℹ️ Info & Profil", description="Statystyki, Bio", emoji="ℹ️"),
            discord.SelectOption(label="🛡️ Administracja", description="Komendy moderatorskie", emoji="🛡️"),
            discord.SelectOption(label="⚔️ Klany", description="Zarządzaj swoją drużyną", emoji="⚔️")
        ]
        super().__init__(placeholder="Wybierz kategorię...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        choice = self.values[0]
        embed = discord.Embed(color=KAWAII_PINK)
        embed.set_footer(text="Wybierz inną kategorię z listy poniżej ⬇️")

        if choice == "💰 Ekonomia":
            embed.title = "💰 Ekonomia & Tycoon"
            embed.description = (
                "**Podstawowe:**\n"
                "`!daily` - Odbierz dzienną nagrodę\n"
                "`!portfel` - Sprawdź stan konta, akcje i ekwipunek\n"
                "`!sklep` - Kup przedmioty i role\n"
                "`!kup <nazwa>` - Kup przedmiot\n"
                "`!uzyj <kod>` - Użyj przedmiotu\n\n"
                "**📈 Giełda:**\n"
                "`!gielda` - Kursy akcji\n"
                "`!wykres <ticker>` - Wykres ceny\n"
                "`!kup_akcje <ticker> <ilość>`\n"
                "`!sprzedaj_akcje <ticker> <ilość>`\n\n"
                "**🏭 Tycoon:**\n"
                "`!tycoon` - Status twojego imperium\n"
                "`!sklep_tycoon` - Lista maszyn\n"
                "`!kup_maszyne <nazwa>`\n"
                "`!odbierz` - Odbierz wyprodukowaną kasę"
            )

        elif choice == "🎰 Gry":
            embed.title = "🎰 Kasyno & Gry"
            embed.description = (
                "`!maszyna <stawka>` - Jednoręki bandyta\n"
                "`!ruletka <stawka> <wybór>` - Ruletka (red/black/green/numer)\n"
                "`!moneta <stawka> <orzel/reszka>` - Rzut monetą\n"
                "`!kostka <stawka>` - Pojedynek na kości\n"
                "`!wojna <stawka>` - Wojna karciana\n"
                "`!zgadnij <stawka> <1-10>` - Zgadnij liczbę\n"
                "`!blackjack <stawka>` - Oczko z krupierem (Hit/Stand)\n"
                "`!zdrapka <koszt>` - Kup e-zdrapkę z nagrodami\n"
                "`!wyscig <stawka> <zolw/krolik/pies/kot>` - Wyścigi zwierząt\n"
                "`!kubki <stawka> <1/2/3>` - Gdzie jest piłeczka?"
            )

        elif choice == "🧸 Social":
            embed.title = "🧸 Social & Roleplay"
            embed.description = (
                "`!przytul`, `!pocaluj`, `!policzek`, `!pat`\n"
                "`!ugryz`, `!liz`, `!pogon`, `!taniec`, `!bonk`\n"
                "`!kill`, `!feed`, `!highfive`\n"
                "`!ship <osoba>` - Sprawdź miłość\n"
                "`!kula <pytanie>` - Magiczna kula 8\n"
                "`!slub <osoba>` - Weź ślub\n"
                "`!rozwod` - Weź rozwód\n"
                "`!adoptuj <osoba>` - Adoptuj dziecko do rodziny"
            )

        elif choice == "ℹ️ Info & Profil":
            embed.title = "ℹ️ Informacje"
            embed.description = (
                "`!botinfo` - O bocie\n"
                "`!serverinfo` - O serwerze\n"
                "`!userinfo <osoba>` - O użytkowniku\n"
                "`!bio` - Pokaż swoje bio\n"
                "`!setbio` - Ustaw bio (interaktywnie)\n"
                "`!report <osoba> <powód>` - Zgłoś gracza"
            )

        elif choice == "🛡️ Administracja":
            if not interaction.user.guild_permissions.kick_members:
                embed.color = KAWAII_RED
                embed.description = "⛔ Nie masz uprawnień do przeglądania tej sekcji!"
            else:
                embed.title = "🛡️ Panel Admina"
                embed.description = (
                    "**Moderacja:**\n"
                    "`!kick`, `!ban`, `!unban`\n"
                    "`!mute`, `!unmute`, `!lock`, `!unlock`\n"
                    "`!clear_user`, `!purge <ilość>`\n"
                    "`!nuke`, `!slowmode <s.>`, `!domena`\n\n"
                    "**Zarządzanie:**\n"
                    "`!ogloszenie <tekst>`\n"
                    "`!ankieta <pytanie|opcja1|opcja2...>`\n"
                    "`!say`, `!dm`, `!sudo`, `!chname`\n\n"
                    "**Ekonomia i Eventy:**\n"
                    "`!qte <kwota> <min.> <max_osob>`\n"
                    "`!daj_kase <user> <kwota>`\n"
                    "`!zabierz_kase <user> <kwota>`\n\n"
                    "**Społeczność & Trolle:**\n"
                    "`!wyroznij <user> <powód>`\n"
                    "`!impreza`, `!temat`, `!pochwal`\n"
                    "`!fake_mute`, `!scam_nitro`, `!duch`\n"
                    "`!rosyjska_ruletka`, `!timeout_ruletka`, `!impostor`\n"
                    "`!ghost_ping`, `!hack`, `!uwuify`, `!wirus`\n"
                    "**🔥 Mass Trolle:**\n"
                    "`!fake_nuke_server`, `!troll_rename`\n"
                    "`!spam_roles <ile>`, `!spam_channels <ile>`\n"
                    "`!troll_admin`, `!troll_dm_all`"
                )

        elif choice == "⚔️ Klany":
            embed.title = "⚔️ System Klanów"
            embed.description = (
                "**Dla wszystkich:**\n"
                "`!zaloz_klan <nazwa>` - Aplikuj o własny klan (Wymagany Lvl 12)\n"
                "`!klan [nazwa/osoba]` - Pokaż statystyki i profil klanu\n"
                "`!opusc_klan` - Wychodzi z obecnego klanu\n"
                "`!zestawienie_klanow` - Ranking wpływów (Top 10)\n\n"
                "**Zarządzanie:**\n"
                "`!zapros_do_klanu <osoba>` - Zaprasza gracza\n"
                "`!opis_klanu <tekst>` - Zmienia opis klanu\n"
                "`!sklad_klanu` - Lista graczy w klanie\n"
                "`!powiadom_klan <tekst>` - Oznacza członków klanu\n"
                "`!wyrzuc_klan <osoba>` - Wyrzuca gracza (Tylko Owner)\n"
                "`!usun_klan` - Trwałe usunięcie klanu (Tylko Owner)"
            )

        await interaction.response.edit_message(embed=embed)

class HelpView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=180)
        self.add_item(HelpSelect())

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="💬・pogadanki")
        if channel:
            embed = discord.Embed(description=f"O nie... **{member.name}** uciekł... Trzymaj się gdziekolwiek tam jesteś! 💔", color=discord.Color.dark_grey())
            await channel.send(embed=embed)

    @commands.command()
    async def botinfo(self, ctx):
        """Informacje o bocie i twórcy"""
        embed = discord.Embed(title="🌸 O mnie 🌸", color=KAWAII_PINK)
        embed.description = (
            "Heeej! Jestem Twoim osobistym, słodkim asystentem serwerowym! (≧◡≦) ♡\n"
            "Pomagam w ekonomii, zarządzaniu poziomami i pilnuję porządku! ✨"
        )
        embed.add_field(name="🛠️ Twórca", value="**BorysiaczekUwU** 💖", inline=False)
        embed.add_field(name="🎂 Wersja", value="2.5 (Economy Update)", inline=True)
        embed.add_field(name="🏓 Ping", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else self.bot.user.default_avatar.url)
        embed.set_footer(text="Dziękuję że jesteś z nami! 🌸")
        await ctx.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"🌸 {member.name}", color=member.color)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Konto od", value=member.created_at.strftime("%Y-%m-%d"))
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text="Bot by BorysiaczekUwU")
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"🏰 {guild.name}", color=KAWAII_GOLD)
        embed.add_field(name="Właściciel", value=guild.owner.mention)
        embed.add_field(name="Liczba osób", value=guild.member_count)
        if guild.icon: embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text="Bot by BorysiaczekUwU")
        await ctx.send(embed=embed)

    @commands.command()
    async def pomoc(self, ctx):
        embed = discord.Embed(
            title="🌸 Menu Pomocy 🌸",
            description="Wybierz kategorię z menu poniżej, aby zobaczyć komendy! 👇",
            color=KAWAII_PINK
        )
        embed.set_footer(text="Stworzony przez BorysiaczekUwU 💖 v2.5")
        await ctx.send(embed=embed, view=HelpView())

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def pomoca(self, ctx):
        embed = discord.Embed(title="🛡️ Menu Admina (Legacy)", description="Użyj `!pomoc` i wybierz kategorię Admin!", color=KAWAII_RED)
        await ctx.send(embed=embed)

    @commands.command()
    async def report(self, ctx, member: discord.Member, *, powod: str):
        """Zgłoś gracza administracji."""
        try:
            await ctx.message.delete()
        except:
            pass
            
        channel = discord.utils.get(ctx.guild.text_channels, name="⚠️・reporty")
        if not channel:
            temp_msg = await ctx.send("❌ Nie znaleziono kanału `⚠️・reporty`. Zgłoś to bezpośrednio administratorowi!")
            await asyncio.sleep(5)
            try:
                await temp_msg.delete()
            except:
                pass
            return
            
        embed = discord.Embed(
            title="🚨 Nowy Raport 🚨",
            color=KAWAII_RED,
            timestamp=ctx.message.created_at
        )
        embed.add_field(name="Zgłaszający", value=f"{ctx.author.mention} ({ctx.author.name})", inline=True)
        embed.add_field(name="Zgłoszony", value=f"{member.mention} ({member.name})", inline=True)
        embed.add_field(name="Powód", value=powod, inline=False)
        embed.set_footer(text=f"ID Zgłoszonego: {member.id} | ID Zgłaszającego: {ctx.author.id}")
        
        # Ping administracji. Jeśli jest rola "Administracja", oznacz ją. W przeciwnym wypadku @here.
        admin_role = discord.utils.get(ctx.guild.roles, name="Administracja")
        ping_text = admin_role.mention if admin_role else "@here"
        
        await channel.send(content=f"🔔 {ping_text} - wpłynęło nowe zgłoszenie!", embed=embed)
        
        try:
            await ctx.author.send(f"✅ Twój raport na użytkownika **{member.name}** z powodu: `{powod}` został pomyślnie wysłany i administracja wkrótce się nim zajmie.")
        except:
            pass

async def setup(bot):
    await bot.add_cog(General(bot))
