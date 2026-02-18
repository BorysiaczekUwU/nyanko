import discord
from discord.ext import commands, tasks
from discord.ui import Button, View
import asyncio
from datetime import datetime, timedelta, timezone
from utils import KAWAII_PINK, KAWAII_RED, KAWAII_GOLD, get_ticket_user, update_ticket_user

class TicketView(View):
    def __init__(self, bot, member, channel):
        super().__init__(timeout=None)
        self.bot = bot
        self.member = member
        self.channel = channel

    @discord.ui.button(label="🔒 ZAMKNIJ", style=discord.ButtonStyle.danger, emoji="🔒")
    async def close_button(self, interaction: discord.Interaction, button: Button):
        await interaction.response.send_message("🔒 Zamykam ticket za 5 sekund...")

        # Wiadomość pożegnalna (wymóg z promptu)
        embed = discord.Embed(title="👋 DO ZOBACZENIA!", description=f"Dziękujemy za kontakt {self.member.name}! Ticket zostaje zamknięty.", color=KAWAII_GOLD)
        await self.channel.send(embed=embed)

        await asyncio.sleep(5)
        await self.channel.delete()

    @discord.ui.button(label="👋 WYRZUĆ (KICK)", style=discord.ButtonStyle.danger, emoji="👢")
    async def kick_button(self, interaction: discord.Interaction, button: Button):
        # Sprawdzamy uprawnienia (tylko admin/mod może wyrzucić)
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("⛔ Brak uprawnień do wyrzucania!", ephemeral=True)
            return

        # Potwierdzenie
        await interaction.response.send_message(f"👢 Wyrzucam {self.member.mention} z serwera...", ephemeral=True)
        try:
            await self.member.kick(reason=f"Wyrzucono z poziomu ticketu przez {interaction.user.name}")
            await self.channel.send(f"✅ **{self.member.name}** został wyrzucony z serwera!")
        except Exception as e:
            await self.channel.send(f"❌ Nie udało się wyrzucić użytkownika: {e}")

class CreateTicketView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="📩 OTWÓRZ TICKET", style=discord.ButtonStyle.primary, emoji="🎫", custom_id="create_ticket_btn")
    async def create_ticket(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        member = interaction.user

        # Sprawdzamy czy już ma ticket
        category = discord.utils.get(guild.categories, name="TICKETY")
        if not category:
            category = await guild.create_category("TICKETY")

        channel_name = f"ticket-{member.name}".lower().replace("#", "")
        existing_channel = discord.utils.get(guild.text_channels, name=channel_name)
        if existing_channel:
            await interaction.response.send_message(f"⛔ Masz już otwarty ticket: {existing_channel.mention}", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            self.bot.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, manage_channels=True)
        }

        # Dodajemy uprawnienia dla adminów/modów
        for role in guild.roles:
            if role.permissions.manage_channels or role.permissions.kick_members:
                overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        try:
            channel = await guild.create_text_channel(channel_name, category=category, overwrites=overwrites)

            # Sprawdzamy czy to pierwszy ticket
            ticket_data = get_ticket_user(member.id)
            is_first_time = not ticket_data.get("has_opened_ticket", False)

            if is_first_time:
                embed = discord.Embed(title=f"🎉 Twój pierwszy ticket, {member.name}!",
                                      description="Witamy w supporcie! Cieszymy się, że jesteś z nami. Opisz swój problem, a administracja wkrótce pomoże! 💖",
                                      color=KAWAII_PINK)
                update_ticket_user(member.id, "has_opened_ticket", True)
            else:
                embed = discord.Embed(title="🎫 Pomoc techniczna",
                                      description=f"Witaj {member.mention}! W czym możemy pomóc?",
                                      color=KAWAII_PINK)

            view = TicketView(self.bot, member, channel)
            await channel.send(embed=embed, view=view)
            await interaction.response.send_message(f"✅ Utworzono ticket: {channel.mention}", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"❌ Błąd tworzenia ticketu: {e}", ephemeral=True)

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_inactive_tickets.start()
        # Rejestracja widoku dla persystencji (żeby działał po restarcie)
        self.bot.add_view(CreateTicketView(self.bot))

    def cog_unload(self):
        self.check_inactive_tickets.cancel()

    @tasks.loop(minutes=5)
    async def check_inactive_tickets(self):
        # Sprawdzamy wszystkie kanały tekstowe w poszukiwaniu nieaktywnych ticketów
        for guild in self.bot.guilds:
            category = discord.utils.get(guild.categories, name="TICKETY")
            if not category: continue

            for channel in category.text_channels:
                if not channel.name.startswith("ticket-"): continue

                try:
                    # Pobieramy ostatnią wiadomość
                    last_message = None
                    async for message in channel.history(limit=1):
                        last_message = message
                        break

                    if not last_message:
                        # Pusty kanał od dawna? (można sprawdzić channel.created_at)
                        time_diff = datetime.now(timezone.utc) - channel.created_at
                    else:
                        time_diff = datetime.now(timezone.utc) - last_message.created_at

                    # Jeśli brak aktywności przez 24h (86400s)
                    if time_diff.total_seconds() > 86400:
                        embed = discord.Embed(title="💤 BRAK AKTYWNOŚCI",
                                              description="Ten ticket był nieaktywny przez ponad 24h. Zostanie zamknięty automatycznie.",
                                              color=discord.Color.light_grey())
                        await channel.send(embed=embed)

                        # Wiadomość pożegnalna
                        farewell = discord.Embed(title="👋 DO ZOBACZENIA!", description=f"Ticket zamknięty z powodu braku aktywności.", color=KAWAII_GOLD)
                        await channel.send(embed=farewell)

                        await asyncio.sleep(5)
                        await channel.delete()

                except Exception as e:
                    print(f"Błąd sprawdzania ticketu {channel.name}: {e}")

    @check_inactive_tickets.before_loop
    async def before_check_inactive_tickets(self):
        await self.bot.wait_until_ready()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup_ticket(self, ctx):
        """Tworzy panel ticketów"""
        await ctx.message.delete()
        embed = discord.Embed(title="📨 CENTRUM POMOCY", description="Kliknij przycisk poniżej, aby otworzyć prywatny kanał z administracją! 👇", color=KAWAII_PINK)
        view = CreateTicketView(self.bot)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Tickets(bot))
