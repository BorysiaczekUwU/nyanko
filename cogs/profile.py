import discord
from discord.ext import commands
from discord.ui import Modal, TextInput, View, Select
from utils import get_profile_data, update_profile, get_level_data, get_data, KAWAII_PINK, KAWAII_BLUE, KAWAII_GOLD

# --- MODAL DO WPISYWANIA BIO ---
class BioModal(Modal, title="Opisz siebie ✨"):
    bio_input = TextInput(
        label="Twoje Bio",
        style=discord.TextStyle.paragraph,
        placeholder="Napisz coś fajnego o sobie...",
        max_length=300,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        update_profile(interaction.user.id, "bio", self.bio_input.value)
        await interaction.response.send_message("✅ Bio zaktualizowane! Wygląda super! 💖", ephemeral=True)

# --- WYBÓR PŁCI ---
class GenderSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Chłopak", emoji="👦", value="Chłopak"),
            discord.SelectOption(label="Dziewczyna", emoji="👧", value="Dziewczyna"),
            discord.SelectOption(label="Inna / Tajemnica", emoji="👽", value="Tajemnica"),
        ]
        super().__init__(placeholder="Wybierz płeć...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        update_profile(interaction.user.id, "gender", self.values[0])
        await interaction.response.send_message(f"✅ Ustawiono płeć: **{self.values[0]}**", ephemeral=True)

# --- WYBÓR WIEKU ---
class AgeSelect(Select):
    def __init__(self):
        options = []
        # Generujemy przedziały wiekowe
        ranges = ["< 13", "13-15", "16-18", "19-21", "22-25", "25+"]
        for r in ranges:
            options.append(discord.SelectOption(label=r, value=r))
        super().__init__(placeholder="Wybierz wiek...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        update_profile(interaction.user.id, "age", self.values[0])
        await interaction.response.send_message(f"✅ Ustawiono wiek: **{self.values[0]}**", ephemeral=True)

# --- GŁÓWNY WIDOK USTAWIEŃ ---
class SetBioView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GenderSelect())
        self.add_item(AgeSelect())

    @discord.ui.button(label="📝 Napisz Bio", style=discord.ButtonStyle.primary, emoji="✍️")
    async def bio_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BioModal())

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setbio(self, ctx):
        """Otwiera panel ustawiania profilu"""
        embed = discord.Embed(
            title="🎨 Kreator Profilu",
            description="Użyj menu poniżej, aby ustawić swoje informacje!\nMożesz wybrać wiek, płeć i napisać coś o sobie. ✨",
            color=KAWAII_BLUE
        )
        await ctx.send(embed=embed, view=SetBioView())

    @commands.command()
    async def bio(self, ctx, member: discord.Member = None):
        """Wyświetla piękny profil użytkownika"""
        member = member or ctx.author
        
        # Pobieranie wszystkich danych
        profile = get_profile_data(member.id)
        economy = get_data(member.id)
        level_data = get_level_data(member.id)
        
        # Role (pomijamy @everyone)
        roles = [r.mention for r in member.roles if r.name != "@everyone"]
        # Odwracamy żeby najważniejsze były na początku i bierzemy max 5
        roles = roles[::-1][:5] 
        roles_str = " ".join(roles) if roles else "Brak ról"

        embed = discord.Embed(color=member.color if member.color != discord.Color.default() else KAWAII_PINK)
        
        # Nagłówek
        embed.set_author(name=f"Profil użytkownika {member.name}", icon_url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

        # Sekcja Główna
        embed.add_field(name="👤 O mnie", value=f"```\n{profile['bio']}\n```", inline=False)
        
        # Info podstawowe
        embed.add_field(name="🎂 Wiek", value=profile['age'], inline=True)
        embed.add_field(name="⚧ Płeć", value=profile['gender'], inline=True)
        embed.add_field(name="📅 Dołączył", value=member.joined_at.strftime("%d/%m/%Y"), inline=True)

        # Statystyki (Level & Kasa)
        stats = (
            f"⭐ **Level:** {level_data['level']}\n"
            f"✨ **XP:** {level_data['xp']}\n"
            f"❤️ **Reputacja:** {level_data['rep']}"
        )
        embed.add_field(name="📊 Statystyki", value=stats, inline=True)

        money_stats = (
            f"💰 **Portfel:** {economy['balance']}\n"
            f"📦 **Przedmioty:** {sum(economy['inventory'].values())}"
        )
        embed.add_field(name="💎 Ekonomia", value=money_stats, inline=True)

        # Role
        embed.add_field(name="🎭 Główne Role", value=roles_str, inline=False)
        
        # Stopka
        embed.set_footer(text=f"ID: {member.id} • Użyj !setbio aby edytować")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Profile(bot))