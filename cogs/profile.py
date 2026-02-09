import discord
from discord.ext import commands
import asyncio
from discord.ui import Modal, TextInput, View, Select
from utils import get_profile_data, update_profile, get_level_data, get_data, KAWAII_PINK, KAWAII_BLUE

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

# --- MODAL DO WPISYWANIA URODZIN ---
class BirthdayModal(Modal, title="Kiedy masz urodziny? 🎂"):
    bday_input = TextInput(
        label="Data urodzin",
        placeholder="np. 15.04 lub 12 Grudnia",
        max_length=20,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        update_profile(interaction.user.id, "birthday", self.bday_input.value)
        await interaction.response.send_message(f"✅ Zapisano urodziny: **{self.bday_input.value}**! 🎂", ephemeral=True)

# --- MODAL DLA NIESTANDARDOWEJ PŁCI ---
class CustomGenderModal(Modal, title="Wpisz swoją płeć ⚧"):
    gender_input = TextInput(
        label="Twoja Płeć",
        placeholder="np. Kosmita, Dąb, Czołg...",
        max_length=20,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        update_profile(interaction.user.id, "gender", self.gender_input.value)
        await interaction.response.send_message(f"✅ Ustawiono niestandardową płeć: **{self.gender_input.value}**", ephemeral=True)

# --- WYBÓR PŁCI ---
class GenderSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Chłopak", emoji="👦", value="Chłopak"),
            discord.SelectOption(label="Dziewczyna", emoji="👧", value="Dziewczyna"),
            discord.SelectOption(label="Niestandardowa...", emoji="⚧", value="custom"),
            discord.SelectOption(label="Inna / Tajemnica", emoji="👽", value="Tajemnica"),
        ]
        super().__init__(placeholder="Wybierz płeć...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        val = self.values[0]
        if val == "custom":
            await interaction.response.send_modal(CustomGenderModal())
        else:
            update_profile(interaction.user.id, "gender", val)
            await interaction.response.send_message(f"✅ Ustawiono płeć: **{val}**", ephemeral=True)

# --- WYBÓR ZAIMKÓW ---
class PronounsSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="On/Jego", value="On/Jego"),
            discord.SelectOption(label="Ona/Jej", value="Ona/Jej"),
            discord.SelectOption(label="Oni/Ich", value="Oni/Ich"),
            discord.SelectOption(label="Inne", value="Inne"),
        ]
        super().__init__(placeholder="Wybierz zaimki...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        update_profile(interaction.user.id, "pronouns", self.values[0])
        await interaction.response.send_message(f"✅ Ustawiono zaimki: **{self.values[0]}**", ephemeral=True)

# --- WYBÓR STATUSU ZWIĄZKU ---
class StatusSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Singiel/ka", emoji="🔓", value="Singiel/ka"),
            discord.SelectOption(label="W związku", emoji="💍", value="W związku"),
            discord.SelectOption(label="To skomplikowane", emoji="🌀", value="To skomplikowane"),
            discord.SelectOption(label="Szukam", emoji="🔎", value="Szukam"),
            discord.SelectOption(label="Nie szukam", emoji="⛔", value="Nie szukam"),
        ]
        super().__init__(placeholder="Twój status...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        update_profile(interaction.user.id, "status", self.values[0])
        await interaction.response.send_message(f"✅ Ustawiono status: **{self.values[0]}**", ephemeral=True)

# --- WYBÓR WIEKU ---
class AgeSelect(Select):
    def __init__(self):
        options = []
        ranges = ["< 13", "13-15", "16-18", "19-21", "22-25", "25+"]
        for r in ranges:
            options.append(discord.SelectOption(label=r, value=r))
        super().__init__(placeholder="Wybierz wiek...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        update_profile(interaction.user.id, "age", self.values[0])
        await interaction.response.send_message(f"✅ Ustawiono wiek: **{self.values[0]}**", ephemeral=True)

# --- WYBÓR PARTNERA ---
class PartnerSelect(discord.ui.UserSelect):
    def __init__(self):
        super().__init__(placeholder="Wybierz swoją drugą połówkę... 💍", min_values=1, max_values=1, row=3)

    async def callback(self, interaction: discord.Interaction):
        target = self.values[0] # User/Member object

        # Walidacja
        if target.id == interaction.user.id:
            await interaction.response.send_message("❌ Nie możesz wziąć ślubu ze sobą!", ephemeral=True)
            return
        if target.bot:
            await interaction.response.send_message("❌ Nie możesz wziąć ślubu z botem!", ephemeral=True)
            return

        # Zapisz w bazie
        update_profile(interaction.user.id, "partner", target.id)
        await interaction.response.send_message(f"✅ Ustawiono partnera: **{target.name}**! 💍", ephemeral=True)

# --- GŁÓWNY WIDOK USTAWIEŃ ---
class SetBioView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(GenderSelect())
        self.add_item(PronounsSelect())
        self.add_item(StatusSelect())
        self.add_item(AgeSelect())
        self.add_item(PartnerSelect())

    @discord.ui.button(label="📝 Napisz Bio", style=discord.ButtonStyle.primary, emoji="✍️", row=4)
    async def bio_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BioModal())

    @discord.ui.button(label="🎂 Ustaw Urodziny", style=discord.ButtonStyle.secondary, emoji="📅", row=4)
    async def bday_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(BirthdayModal())

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def setbio(self, ctx):
        """Otwiera panel ustawiania profilu (Prywatnie)"""
        try:
            await ctx.message.delete()
        except:
            pass

        embed = discord.Embed(
            title="🎨 Kreator Profilu",
            description="Użyj menu poniżej, aby ustawić swoje informacje!\nMożesz wybrać wiek, płeć, datę urodzin i napisać coś o sobie. ✨",
            color=KAWAII_BLUE
        )
        embed.set_footer(text="Bot stworzony przez BorysiaczekUwU 💖")

        try:
            await ctx.author.send(embed=embed, view=SetBioView())
            # Opcjonalne potwierdzenie na kanale (znika po 5s)
            temp_msg = await ctx.send(f"{ctx.author.mention}, wysłałam Ci panel ustawień w wiadomości prywatnej! 📩")
            await asyncio.sleep(5)
            await temp_msg.delete()
        except discord.Forbidden:
            await ctx.send(f"❌ {ctx.author.mention}, nie mogę wysłać Ci wiadomości prywatnej! Odblokuj DM.")

    @commands.command()
    async def bio(self, ctx, member: discord.Member = None):
        """Wyświetla piękny profil użytkownika"""
        member = member or ctx.author
        
        # Pobieranie danych (Teraz z MongoDB przez utils)
        profile = get_profile_data(member.id)
        economy = get_data(member.id)
        level_data = get_level_data(member.id)
        
        roles = [r.mention for r in member.roles if r.name != "@everyone"]
        roles = roles[::-1][:5] 
        roles_str = " ".join(roles) if roles else "Brak ról"

        embed = discord.Embed(color=member.color if member.color != discord.Color.default() else KAWAII_PINK)
        
        embed.set_author(name=f"Profil użytkownika {member.name}", icon_url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

        embed.add_field(name="👤 O mnie", value=f"```\n{profile.get('bio', 'Pusto...')}\n```", inline=False)
        
        embed.add_field(name="⚧ Płeć", value=profile.get('gender', 'Nieznana'), inline=True)
        embed.add_field(name="🗣️ Zaimki", value=profile.get('pronouns', 'Nieznane'), inline=True)
        embed.add_field(name="📅 Wiek", value=profile.get('age', 'Nieznany'), inline=True)
        embed.add_field(name="🎂 Urodziny", value=profile.get('birthday', 'Nieznane'), inline=True)
        embed.add_field(name="💞 Status", value=profile.get('status', 'Nieznany'), inline=True)

        partner_id = profile.get('partner')
        partner_txt = "Brak"
        if partner_id:
             try:
                 p_user = await self.bot.fetch_user(partner_id)
                 partner_txt = f"{p_user.name} 💍"
             except:
                 partner_txt = "Nieznany"
        embed.add_field(name="💖 Partner", value=partner_txt, inline=True)

        stats = (
            f"⭐ **Level:** {level_data['level']}\n"
            f"✨ **XP:** {level_data['xp']}\n"
            f"❤️ **Reputacja:** {level_data['rep']}"
        )
        embed.add_field(name="📊 Statystyki", value=stats, inline=True)

        money_stats = (
            f"💰 **Portfel:** {economy['balance']}\n"
            f"📦 **Przedmioty:** {sum(economy.get('inventory', {}).values())}"
        )
        embed.add_field(name="💎 Ekonomia", value=money_stats, inline=True)

        embed.add_field(name="🎭 Główne Role", value=roles_str, inline=False)
        
        # Podpis twórcy
        embed.set_footer(text=f"Stworzony przez BorysiaczekUwU 💖 • ID: {member.id}")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Profile(bot))