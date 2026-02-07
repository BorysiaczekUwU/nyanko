import discord
from discord.ext import commands
from utils import KAWAII_PINK, KAWAII_RED, KAWAII_GOLD

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="ogólny")
        if channel:
            embed = discord.Embed(description=f"O nie... **{member.name}** uciekł... 💔", color=discord.Color.dark_grey())
            await channel.send(embed=embed)

    @commands.command()
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"🌸 {member.name}", color=member.color)
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Konto od", value=member.created_at.strftime("%Y-%m-%d"))
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"🏰 {guild.name}", color=KAWAII_GOLD)
        embed.add_field(name="Właściciel", value=guild.owner.mention)
        embed.add_field(name="Liczba osób", value=guild.member_count)
        if guild.icon: embed.set_thumbnail(url=guild.icon.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def pomoc(self, ctx):
        embed = discord.Embed(title="🌸 Menu Główne", color=KAWAII_PINK)
        embed.add_field(name="💰 Ekonomia", value="`!sklep`, `!kup`, `!uzyj`, `!portfel`, `!daily`", inline=False)
        embed.add_field(name="🎰 Gry", value="`!slots`, `!rzut`", inline=False)
        embed.add_field(name="🧸 Social", value="`!przytul`, `!pocaluj`, `!policzek`, `!pat`, `!ship`, `!kula`", inline=False)
        embed.add_field(name="ℹ️ Info", value="`!userinfo`, `!serverinfo`, `!bio`, `!setbio`", inline=False)
        embed.set_footer(text="Dla adminów: !pomoca")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def pomoca(self, ctx):
        embed = discord.Embed(title="🛡️ Menu Admina", color=KAWAII_RED)
        embed.add_field(name="😈 Troll", value="`!sudo`, `!fakeban`, `!duch`, `!dm`", inline=False)
        embed.add_field(name="☢️ Admin", value="`!nuke`, `!slowmode`, `!lock`, `!unlock`, `!say`", inline=False)
        embed.add_field(name="⚖️ Kary & Role", value="`!ban`, `!unban`, `!kick`, `!mute`, `!domena`\n`!nadaj_role`, `!zabierz_role`", inline=False)
        embed.add_field(name="💰 Ekonomia", value="`!daj_kase`, `!zabierz_kase`", inline=False)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(General(bot))