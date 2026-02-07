import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import asyncio
from datetime import timedelta
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
            embed = discord.Embed(description=f"Witamy **{self.member.mention}**! (≧◡≦) ♡\nNadano rolę **Bilecik był**! 🎟️", color=KAWAII_PINK)
            await general.send(embed=embed)

        await asyncio.sleep(5)
        await self.channel.delete()

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
        try:
            await self.member.remove_roles(self.role_izolatka)
            if self.role_verified: await self.member.add_roles(self.role_verified)
        except: pass
        await asyncio.sleep(5)
        await self.channel.delete()

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # --- LISTENER: Weryfikacja po wejściu ---
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = member.guild
        verified_role = discord.utils.get(guild.roles, name="Bilecik był")
        if not verified_role:
            verified_role = await guild.create_role(name="Bilecik był", color=discord.Color.from_rgb(255, 182, 193))

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
            embed = discord.Embed(title=f"🌸 Witaj {member.name}!", description="Napisz coś o sobie! Admin nada Ci **Bilecik**! 🎟️", color=KAWAII_PINK)
            view = VerifyView(self.bot, member, verified_role, channel)
            await channel.send(f"{member.mention}", embed=embed, view=view)
        except Exception as e: print(f"Błąd weryfikacji: {e}")

    # --- KOMENDY ---
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sudo(self, ctx, member: discord.Member, *, message):
        await ctx.message.delete()
        webhook = await ctx.channel.create_webhook(name=member.display_name)
        await webhook.send(str(message), username=member.display_name, avatar_url=member.avatar.url or member.default_avatar.url)
        await webhook.delete()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def fakeban(self, ctx, member: discord.Member):
        await ctx.message.delete()
        embed = discord.Embed(title="🔨 BAN HAMMER!", description=f"Baka **{member.name}** zbanowany!\nPowód: Bycie zbyt słodkim", color=KAWAII_RED)
        embed.set_image(url=random.choice(GIFS_BAN))
        embed.set_footer(text="To tylko żart... ( ͡° ͜ʖ ͡°)")
        await ctx.send(embed=embed)

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
    @commands.has_permissions(moderate_members=True)
    async def mute(self, ctx, member: discord.Member, minutes: int, *, reason="Spam"):
        if member.top_role >= ctx.author.top_role: return
        await member.timeout(timedelta(minutes=minutes), reason=reason)
        embed = discord.Embed(title="🤐 MUTE", description=f"**{member.name}** uciszony na **{minutes}m**.", color=discord.Color.dark_grey())
        embed.set_image(url=random.choice(GIFS_MUTE))
        await ctx.send(embed=embed)

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

        verified_role = discord.utils.get(guild.roles, name="Bilecik był")
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

async def setup(bot):
    await bot.add_cog(Admin(bot))