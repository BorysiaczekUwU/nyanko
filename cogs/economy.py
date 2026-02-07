import discord
from discord.ext import commands
import random
from datetime import datetime, timedelta
from utils import get_data, update_data, add_item, remove_item, load_economy, save_economy, KAWAII_PINK, KAWAII_GOLD

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

    @commands.command()
    async def portfel(self, ctx):
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
        await ctx.send(embed=embed)

    @commands.command()
    async def daily(self, ctx):
        user_id = str(ctx.author.id)
        data = get_data(user_id)
        now = datetime.now()
        if data["last_daily"]:
            last = datetime.fromisoformat(data["last_daily"])
            if now - last < timedelta(hours=24):
                await ctx.send(f"⏳ Wróć jutro! (Cooldown)")
                return
        
        update_data(user_id, "balance", 200, "add")
        data = load_economy()
        data[user_id]["last_daily"] = now.isoformat()
        save_economy(data)
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

    @commands.command()
    async def slots(self, ctx, amount: int):
        bal = get_data(ctx.author.id)["balance"]
        if bal < amount: return
        update_data(ctx.author.id, "balance", bal - amount, "set")
        emojis = ["🍒", "💎", "7️⃣"]
        a, b, c = random.choice(emojis), random.choice(emojis), random.choice(emojis)
        msg = await ctx.send(f"🎰 | {a} | {b} | {c} |")
        if a == b == c:
            win = amount * 5
            update_data(ctx.author.id, "balance", win, "add")
            await ctx.send(f"🎉 JACKPOT! +{win}")
        else: await ctx.send("❌ Przegrana.")

    @commands.command()
    async def rzut(self, ctx, amount: int, wybor: str):
        bal = get_data(ctx.author.id)["balance"]
        if bal < amount: return
        update_data(ctx.author.id, "balance", bal - amount, "set")
        wynik = random.choice(["orzeł", "reszka"])
        if wybor.lower() in [wynik, "orzel" if wynik=="orzeł" else "x"]:
            win = amount * 2
            update_data(ctx.author.id, "balance", win, "add")
            await ctx.send(f"🪙 Wypadł {wynik}! Wygrywasz {win}!")
        else: await ctx.send(f"🪙 Wypadł {wynik}. Przegrałeś.")

async def setup(bot):
    await bot.add_cog(Economy(bot))