import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime, timedelta
from utils import get_data, update_data, add_item, remove_item, KAWAII_PINK, KAWAII_GOLD

SHOP_ROLES = {
    "VIP": 5000,
    "Bogacz": 10000,
    "Słodziak": 2500,
    "Królowa Dram": 3000
}

SHOP_ITEMS = {
    "kick_ticket": {"name": "🎫 Bilet na Kicka", "price": 15000, "desc": "Wyrzuć kogoś raz (nie działa na adminów!)"},
    "mute_ticket": {"name": "🤐 Taśma Klejąca", "price": 5000, "desc": "Wycisz kogoś na 10 min"},
    "unwarn_ticket": {"name": "📜 Czysta Kartoteka", "price": 20000, "desc": "Resetuje twoje przewinienia (RP)"}
}

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # NOWE KOMENDY ADMINISTRA - DODAWANIE/ZABIERANIE KASY
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def daj_kase(self, ctx, member: discord.Member, amount: int):
        update_data(member.id, "balance", amount, "add")
        await ctx.send(f"💸 **ADMIN:** Dodano **{amount}** monet dla {member.mention}!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def zabierz_kase(self, ctx, member: discord.Member, amount: int):
        update_data(member.id, "balance", -amount, "add")
        await ctx.send(f"📉 **ADMIN:** Zabrano **{amount}** monet użytkownikowi {member.mention}!")

    @commands.command()
    async def portfel(self, ctx):
        """Sprawdź swój stan konta (Prywatnie)"""
        try:
            await ctx.message.delete()
        except:
            pass

        data = get_data(ctx.author.id)
        inv_text = ""
        for item, count in data["inventory"].items():
            if count > 0:
                name = SHOP_ITEMS.get(item, {}).get("name", item)
                inv_text += f"\n📦 **{name}**: x{count}"
        if not inv_text: inv_text = "\n*(Pusto...)*"
        
        embed = discord.Embed(title="👛 Twój Portfel", color=KAWAII_GOLD)
        embed.add_field(name="💰 Monetki", value=f"**{data['balance']}**", inline=False)
        embed.add_field(name="🎒 Plecak", value=inv_text, inline=False)

        try:
            await ctx.author.send(embed=embed)
        except discord.Forbidden:
            temp = await ctx.send(f"❌ {ctx.author.mention}, odblokuj DM!")
            await asyncio.sleep(5)
            await temp.delete()

    @commands.command()
    async def daily(self, ctx):
        user_id = ctx.author.id
        data = get_data(user_id)
        now = datetime.now()

        if data.get("last_daily"):
            try:
                last = datetime.fromisoformat(data["last_daily"])
                if now - last < timedelta(hours=24):
                    diff = last + timedelta(hours=24) - now
                    hours, remainder = divmod(diff.seconds, 3600)
                    minutes, _ = divmod(remainder, 60)
                    await ctx.send(f"⏳ Wróć jutro! Za **{hours}h {minutes}m**.")
                    return
            except ValueError:
                pass # Błąd parsowania daty, resetujemy
        
        update_data(user_id, "balance", 200, "add")
        update_data(user_id, "last_daily", now.isoformat(), "set")

        await ctx.send("🎁 Odebrałeś **200** monet!")

    @commands.command()
    async def sklep(self, ctx):
        embed = discord.Embed(title="🏪 Super Sklep Kawaii", description="Wpisz `!kup <nazwa>`", color=KAWAII_PINK)
        roles_txt = ""
        for r, p in SHOP_ROLES.items(): roles_txt += f"🏷️ **{r}** - `{p}`\n"
        embed.add_field(name="👑 Role", value=roles_txt, inline=False)
        items_txt = ""
        for k, v in SHOP_ITEMS.items(): items_txt += f"📦 **{k}** ({v['name']}) - `{v['price']}`\n*{v['desc']}*\n"
        embed.add_field(name="🛠️ Przedmioty", value=items_txt, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def kup(self, ctx, *, item_name):
        user_id = ctx.author.id
        balance = get_data(user_id)["balance"]
        
        # Kupowanie Ról
        for r, p in SHOP_ROLES.items():
            if r.lower() == item_name.lower():
                if balance < p:
                    await ctx.send("💸 Nie stać cię!")
                    return
                role_obj = discord.utils.get(ctx.guild.roles, name=r)
                if not role_obj:
                    await ctx.send("❌ Rola nie istnieje.")
                    return
                update_data(user_id, "balance", balance - p, "set")
                await ctx.author.add_roles(role_obj)
                await ctx.send(f"🎉 Kupiłeś rolę **{r}**!")
                return

        # Kupowanie Przedmiotów
        if item_name in SHOP_ITEMS:
            item = SHOP_ITEMS[item_name]
            if balance < item["price"]:
                await ctx.send("💸 Nie stać cię!")
                return
            update_data(user_id, "balance", balance - item["price"], "set")
            add_item(user_id, item_name)
            await ctx.send(f"🎒 Kupiłeś **{item['name']}**! Użyj komendą `!uzyj`.")
            return
        
        await ctx.send("❌ Nie ma takiego towaru.")

    @commands.command()
    async def uzyj(self, ctx, item_code, target: discord.Member = None):
        user_id = ctx.author.id
        data = get_data(user_id)
        inventory = data.get("inventory", {})
        
        if inventory.get(item_code, 0) <= 0:
            await ctx.send("❌ Nie masz tego przedmiotu!")
            return

        if item_code == "kick_ticket":
            if not target or target.guild_permissions.administrator:
                await ctx.send("⚠️ Błąd celu (nie podano lub to admin)!")
                return
            remove_item(user_id, item_code)
            try:
                await target.kick(reason="Użycie przedmiotu (Bilet)")
                await ctx.send(f"👋 **{target.name}** wyrzucony biletem!")
            except:
                add_item(user_id, item_code)
                await ctx.send("❌ Błąd bota.")

        elif item_code == "mute_ticket":
            if not target or target.guild_permissions.administrator:
                await ctx.send("⚠️ Błąd celu!")
                return
            remove_item(user_id, item_code)
            await target.timeout(timedelta(minutes=10), reason="Przedmiot (Taśma)")
            await ctx.send(f"🤐 **{target.name}** wyciszony!")

        elif item_code == "unwarn_ticket":
            remove_item(user_id, item_code)
            await ctx.send(f"📜 **{ctx.author.name}** czyści kartotekę!")


async def setup(bot):
    await bot.add_cog(Economy(bot))