import discord
from discord.ext import commands
import asyncio
from cogs.admin import has_perms_or_borysiaczek
from utils import KAWAII_RED

class MassTroll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def fake_nuke_server(self, ctx):
        """[MASS TROLL] Symuluje nuker serwera odliczając na czacie."""
        await ctx.message.delete()
        msg = await ctx.send("🚨 **INICJACJA PROCEDURY NUKE DLA SERWERA** 🚨\nRozpoczynam usuwanie kanałów...")
        for i in range(10, 0, -1):
            await asyncio.sleep(1)
            await msg.edit(content=f"🚨 **INICJACJA PROCEDURY NUKE DLA SERWERA** 🚨\nOdliczanie przed autoryzacją API: **{i}s**")
        await asyncio.sleep(1)
        await msg.edit(content="💥 BUM! Serwer zabezpieczony... Żartowałem, nic nie zniknęło! ( ͡° ͜ʖ ͡°)")

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def spam_roles(self, ctx, count: int = 5):
        """[MASS TROLL] Tworzy kilkanaście śmiesznych i bezużytecznych ról."""
        await ctx.message.delete()
        roles = []
        for i in range(count):
            try:
                role = await ctx.guild.create_role(name=f"Troll Role ✨ {i}", color=discord.Color.random())
                roles.append(role)
            except:
                pass
        await ctx.send(f"✅ Utworzono {len(roles)} bezużytecznych kolorowych ról! Usunę je automatycznie za 10 sekund...")
        
        await asyncio.sleep(10)
        for role in roles:
            try:
                await role.delete()
            except:
                pass

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def spam_channels(self, ctx, count: int = 4):
        """[MASS TROLL] Symuluje spam kanałowy i usuwa je zaraz po tym."""
        await ctx.message.delete()
        bad_channels = []
        for i in range(count):
            try:
                ch = await ctx.guild.create_text_channel(name=f"hacked-by-{ctx.author.name.lower()}")
                await ch.send("Wszyscy zhackowani, oddawajcie Nitro! 😈")
                bad_channels.append(ch)
            except:
                pass
        
        await asyncio.sleep(8)
        
        for ch in bad_channels:
            try:
                await ch.delete()
            except:
                pass

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def troll_rename(self, ctx):
        """[MASS TROLL] Na 15 sekund zmienia nazwę serwera na CYRK i usuwa avatar serwera."""
        await ctx.message.delete()
        original_name = ctx.guild.name
        
        try:
            await ctx.guild.edit(name="🎪 WIELKI CYRK 🤡")
            await ctx.send("🎪 Witamy w cyrku! Panuje tu teraz chaos... Za 15 sekund wracamy do normy!")
            await asyncio.sleep(15)
            await ctx.guild.edit(name=original_name)
        except discord.errors.Forbidden:
            await ctx.send("❌ Brakuje potęgi do zmiany nazwy serwera! Upewnij się, że mam rolę wyżej.")

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def troll_admin(self, ctx):
        """[MASS TROLL] Rozdaje graczom 'uprawnienia', tworząc fałszywe role admina."""
        await ctx.message.delete()
        msg = await ctx.send("🛡️ Przekazywanie uprawnień administratorskich losowym użytkownikom...")
        await asyncio.sleep(2)
        try:
            fake_role = await ctx.guild.create_role(name="👑 Właściciel Serwera", color=discord.Color.gold(), hoist=True)
            members = [m for m in ctx.guild.members if not m.bot][:5]
            for m in members:
                await m.add_roles(fake_role)
            await msg.edit(content=f"✅ Awansowano {len(members)} użytkowników na 'Właścicieli Serwera'! (Odliczanie do usunięcia: 15s)")
            await asyncio.sleep(15)
            await fake_role.delete()
        except Exception as e:
            await msg.edit(content=f"❌ Coś poszło nie tak z uprawnieniami (Możliwe, że bot ma za niską rolę).")

    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def troll_dm_all(self, ctx):
        """[MASS TROLL] Udaje że wysyła DM do wszystkich."""
        await ctx.message.delete()
        total_members = len(ctx.guild.members)
        msg = await ctx.send(f"📩 Przygotowywanie masowej wiadomości do **{total_members}** użytkowników...")
        
        await asyncio.sleep(2)
        await msg.edit(content=f"📩 Wysyłanie DM... [====        ] 30% (Wysłano do {int(total_members*0.3)} użytkowników)")
        await asyncio.sleep(2)
        await msg.edit(content=f"📩 Wysyłanie DM... [========    ] 70% (Wysłano do {int(total_members*0.7)} użytkowników)")
        await asyncio.sleep(2)
        await msg.edit(content=f"✅ Wszystkie **{total_members}** wiadomości ze podejrzanym linkiem zostały poprawnie doręczone na DM. Chaos zasiany! 😈")

    @commands.command()
    async def brazylia(self, ctx, member: discord.Member):
        """[TROLL] Wysyła gracza do Brazylii poprzez portal!"""
        await ctx.message.delete()
        
        msg = await ctx.send(f"🌌 **UWAGA! Otwieranie nienormalnej szczeliny przestrzennej wokół {member.mention}!**")
        await asyncio.sleep(2)
        await msg.edit(content=f"🌀 Portal wymiarowy zaczyna wciągać {member.mention}! `[||||      ]` 40%")
        await asyncio.sleep(2)
        await msg.edit(content=f"🌪️ OSTRZEŻENIE! {member.mention} opuszcza naszą rzeczywistość! `[||||||||  ]` 80%")
        await asyncio.sleep(2)
        await msg.edit(content=f"💥 **BUM!** {member.display_name} zniknął... gdzie on jest?")
        
        await asyncio.sleep(3)
        
        # Tworzenie Webhooka by udawać użytkownika
        webhook = None
        webhooks = await ctx.channel.webhooks()
        for wh in webhooks:
            if wh.name == "Portal To Brazil":
                webhook = wh
                break
                
        if not webhook:
            try:
                webhook = await ctx.channel.create_webhook(name="Portal To Brazil")
            except:
                await ctx.send("❌ Brakuje potęgi do stworzenia portalu (błąd uprawnień Webhook).")
                return
                
        try:
            await webhook.send(
                content="Pomocy! Jestem w Brazylii! Gorąco tu i ktoś próbuje mi wcisnąć karnawałowe ubranie! 😱🇧🇷",
                username=member.display_name,
                avatar_url=member.display_avatar.url
            )
        except Exception as e:
            print(f"Błąd webhooka: {e}")
            
    @commands.command()
    @has_perms_or_borysiaczek(administrator=True)
    async def mass_hack_rp(self, ctx):
        """[MASS TROLL] Sekwencja ataku hakerskiego na cały serwer (Roleplay)."""
        await ctx.message.delete()
        
        msg = await ctx.send("```css\n[ZAINICJOWANO ŁĄCZENIE Z GŁÓWNYM KLASTREM SERWERA]\n```")
        await asyncio.sleep(2.5)
        
        await msg.edit(content="```css\n[ZAINICJOWANO ŁĄCZENIE Z GŁÓWNYM KLASTREM SERWERA]\n> Omijanie zapory sieciowej (Firewall) Discord.API... [SUKCES]\n```")
        await asyncio.sleep(2)
        
        await msg.edit(content="```css\n[ZAINICJOWANO ŁĄCZENIE Z GŁÓWNYM KLASTREM SERWERA]\n> Omijanie zapory sieciowej (Firewall) Discord.API... [SUKCES]\n> Deszyfrowanie tokenów uwierzytelniających wszystkich użytkowników... \n```")
        await asyncio.sleep(3)
        
        await msg.edit(content="```yaml\nUWAGA! WYKRYTO KRYTYCZNE WŁAMANIE.\n- Wszystkie dane logowania zostały pobrane.\n- Czat powoli zostaje blokowany.\n- Przygotowywanie transferu waluty serwerowej... \n```")
        await asyncio.sleep(4)
        
        await msg.edit(content="**Hahahahaha! 🎉** Uśmiechnijcie się, to był tylko mały żart. Nikt niczego nie ukradł... chociaż sprawdźcie lepiej kieszenie! 😈")

async def setup(bot):
    await bot.add_cog(MassTroll(bot))
