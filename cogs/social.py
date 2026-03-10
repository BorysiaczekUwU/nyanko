import discord
from discord.ext import commands
import random
from utils import KAWAII_PINK, KAWAII_RED, KAWAII_GOLD, get_profile_data, update_profile

GIFS_HUG = [
    "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExcmRsaWN4N3h0eGV3eWdvZXowcHF1YTR6NmcxNW9nOTYyNzkwYXBwMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/1JmGiBtqTuehfYxuy9/giphy.gif",
    "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmFmejR0Z201NTkxc3J2bjYzMDcwODNhZHJvcG5yeG13ZW53MjM4MyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5sokLWDYub7efuAD1M/giphy.gif",
    "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExOG5mYW94NHMwZHk1OXg1MWY4enM4ajE1OXlidnF4OXh3cTBldWVjdCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PHZ7v9tfQu0o0/giphy.gif"
]
GIFS_KISS = [
    "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExOGgyc2xzeHF1anN2eGs1MXg5YzQ5eGx5Nnloa3h3YzV2dGMza2t2OCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/W1hd3uXRIbddu/giphy.gif",
    "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExY2hmZGc1ODJ4ZGYzaDltcDVqZDBsaWtueXZiNmJ5a2Y2a2Y1ZHcyZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/8AduCFP7qQ660NEKns/giphy.gif"
]
GIFS_SLAP = [
    "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZXV2aDU3a2VycnRjZGhocGRwdXNmcHN3NHJkNnZlNmszZGo4aDV6biZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/mEtSQlxqBtWWA/giphy.gif",
    "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmtodWozZ3A0M2hpczN1ZDNhamowNjlvZGU4dXJiMHU1bHI2dzVzcCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/JXuGatu6v9pUA/giphy.gif"
]
GIFS_PAT = [
    "https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExaWJ3YmkxMG5ycWVsdzJtaXNoNG8xbTRhdDUydmQzZTlyZm4xNmJvOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/t9igJ3odrXBixqXtgf/giphy.gif",
    "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExN2ZkeGJsc3VubXRqenQzYnAzMTJ1aGp0Zm5jajRnNmt6eHdudTkwayZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/FH0EiKkU2vjPHZ5op1/giphy.gif"
]
GIFS_BITE = [
    "https://media.giphy.com/media/10gZpyX9hDlwD6/giphy.gif",
    "https://media.giphy.com/media/OqQvwiFWD0hck/giphy.gif"
]
GIFS_LICK = [
    "https://media.giphy.com/media/G1EXcEbQnU0h2/giphy.gif",
    "https://media.giphy.com/media/aB1Q0Y49iQ2uQ/giphy.gif"
]
GIFS_CHASE = [
    "https://media.giphy.com/media/11zTElH1h51Ohi/giphy.gif",
    "https://media.giphy.com/media/l41YkxvU8c7J7Bba0/giphy.gif"
]
GIFS_DANCE = [
    "https://media.giphy.com/media/1tHzw9PZCB3gY/giphy.gif",
    "https://media.giphy.com/media/4ZgPHE43XklyM/giphy.gif"
]
GIFS_BONK = [
    "https://media.giphy.com/media/HxMhuDg7O4pKOhhcRC/giphy.gif",
    "https://media.giphy.com/media/qs4ll1FSxKnNHeSmom/giphy.gif"
]
GIFS_WOREK = [
    "https://media.giphy.com/media/xT1XGYVvVNNxqBMEJG/giphy.gif",
    "https://media.giphy.com/media/26FPCXdkvDbKBbgOI/giphy.gif"
]
GIFS_MIZIAJ = [
    "https://media.giphy.com/media/LmqDkEaB1R7h2bTuhE/giphy.gif",
    "https://media.giphy.com/media/k5qEoy7wK2r4d8tYw6/giphy.gif"
]
GIFS_KUKSANIEC = [
    "https://media.giphy.com/media/1wXdllYvJqECN8l1f9/giphy.gif",
    "https://media.giphy.com/media/26BRuXn1O009B0Z2g/giphy.gif"
]
GIFS_ZACZEP = [
    "https://media.giphy.com/media/3o7TKSx0B7ZWeAozxS/giphy.gif",
    "https://media.giphy.com/media/l41lc5kUKJ45I5b0Y/giphy.gif"
]
GIFS_UKRYJ = [
    "https://media.giphy.com/media/d9T4sCj3K3X9kG1c2L/giphy.gif",
    "https://media.giphy.com/media/13HgwGsXF0aiGY/giphy.gif"
]
GIFS_PISTOLET = [
    "https://media.giphy.com/media/xT9KVteixWgVlXckQE/giphy.gif",
    "https://media.giphy.com/media/26ufncG0N0nE6Z2lq/giphy.gif"
]

class Social(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def przytul(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"**{ctx.author.name}** przytula **{member.name}**! ⊂(・﹏・⊂)", color=KAWAII_PINK)
        embed.set_image(url=random.choice(GIFS_HUG))
        await ctx.send(embed=embed)

    @commands.command()
    async def pocaluj(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"**{ctx.author.name}** całuje **{member.name}**! Mwa! 💋", color=KAWAII_RED)
        embed.set_image(url=random.choice(GIFS_KISS))
        await ctx.send(embed=embed)

    @commands.command()
    async def policzek(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"**{ctx.author.name}** uderza **{member.name}**! Baka! 💢", color=0xFF4500)
        embed.set_image(url=random.choice(GIFS_SLAP))
        await ctx.send(embed=embed)

    @commands.command()
    async def pat(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"**{ctx.author.name}** głaszcze **{member.name}**! 🌸", color=KAWAII_GOLD)
        embed.set_image(url=random.choice(GIFS_PAT))
        await ctx.send(embed=embed)

    @commands.command()
    async def ship(self, ctx, member: discord.Member):
        procent = random.randint(0, 100)
        serca = "💖" * (procent // 10)
        msg = f"Miłość między **{ctx.author.name}** a **{member.name}** wynosi **{procent}%**!\n{serca}"
        if procent > 90: 
            msg += "\nTo przeznaczenie! (♥ω♥*)"
            embed.set_image(url="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExaHVlazFzeHh6c2FzdWEzdnUxMTBia3U2b3pxemhzcjN5YTg3NTg3ZiZlcD12MV9naWZzX3NlYXJjaCZjdD1n/Vi0Ws3t4JSLOgdkaBq/giphy.gif")
        elif procent < 20: 
            msg += "\nMoże zostańcie przyjaciółmi... (cJc)"
            embed.set_image(url="https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExbDZjejdwOGd3ZGlodWoxbGVpNTU1Y3Z2ZWp0NWg1M2NzcWp1bDByOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xGDaiXa6ds8WS4jXUy/giphy.gif")
        await ctx.send(msg)

    @commands.command()
    async def kula(self, ctx, *, pytanie):
        odpowiedzi = ["Oczywiście! 💖", "Raczej nie... (qwq)", "To pewne! 🌟", "Nie licz na to >_<", "Spytaj później ✨"]
        await ctx.send(f"🔮 **Pytanie:** {pytanie}\n✨ **Odpowiedź:** {random.choice(odpowiedzi)}")

    @commands.command()
    async def slub(self, ctx, member: discord.Member):
        """Weź ślub z wybraną osobą! 💍"""
        if member == ctx.author:
            await ctx.send("Nie możesz poślubić samego siebie! (cJc)")
            return

        user_profile = get_profile_data(ctx.author.id)
        target_profile = get_profile_data(member.id)

        if user_profile.get("partner"):
            await ctx.send("Jesteś już w związku! Najpierw weź rozwód. (qwq)")
            return

        if target_profile.get("partner"):
            await ctx.send(f"**{member.name}** jest już w związku! 💔")
            return

        # Pytanie o zgodę
        embed = discord.Embed(
            title="💍 Oświadczyny!",
            description=f"**{ctx.author.name}** oświadcza się **{member.name}**!\nCzy przyjmujesz oświadczyny? (napisz `tak` lub `nie`)",
            color=KAWAII_PINK
        )
        await ctx.send(member.mention, embed=embed)

        def check(m):
            return m.author == member and m.channel == ctx.channel and m.content.lower() in ["tak", "nie"]

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60)
            if msg.content.lower() == "tak":
                update_profile(ctx.author.id, "partner", member.id)
                update_profile(member.id, "partner", ctx.author.id)

                success_embed = discord.Embed(
                    title="💒 Nowe Małżeństwo!",
                    description=f"🎉 Gratulacje! **{ctx.author.name}** i **{member.name}** są teraz małżeństwem! 💍💖",
                    color=KAWAII_GOLD
                )
                await ctx.send(embed=success_embed)
            else:
                await ctx.send("💔 Oświadczyny odrzucone... (qwq)")
        except:
            await ctx.send("⌛ Czas minął... Oświadczyny anulowane.")

    @commands.command()
    async def rozwod(self, ctx):
        """Weź rozwód ze swoim partnerem 💔"""
        user_profile = get_profile_data(ctx.author.id)
        partner_id = user_profile.get("partner")

        if not partner_id:
            await ctx.send("Nie masz z kim brać rozwodu! (cJc)")
            return

        # Czyścimy oba profile
        update_profile(ctx.author.id, "partner", None)
        update_profile(partner_id, "partner", None)

        # Próbujemy zdobyć nazwę partnera
        try:
            partner = await self.bot.fetch_user(partner_id)
            name = partner.name
        except:
            name = "Nieznany"

        embed = discord.Embed(
            title="💔 Rozwód",
            description=f"Związek z **{name}** został zakończony... 🌧️",
            color=KAWAII_RED
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['h5'])
    async def highfive(self, ctx, member: discord.Member):
        """Przybij piątkę! 🙌"""
        embed = discord.Embed(description=f"**{ctx.author.name}** przybija piątkę **{member.name}**! 🙌", color=KAWAII_GOLD)
        embed.set_image(url="https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExOXp0MGpvcmo4YXdtY2M4ZGNvZHVzMm41eHo5bGk5dWVjc3ExamdhMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/SsyFAgnM1s3jfFeroV/giphy.gif")
        await ctx.send(embed=embed)

    @commands.command()
    async def kill(self, ctx, member: discord.Member):
        """Wyeliminuj cel (RP) 🔪"""
        kills = [
            "rzuca w niego czołgiem!",
            "atakuje go poduszką!",
            "częstuje go zatrutym ciastkiem!",
            "wysyła go w kosmos bez skafandra!",
            "zrzuca na niego fortepian!"
        ]
        embed = discord.Embed(description=f"**{ctx.author.name}** {random.choice(kills)} **{member.name}** pada trupem! 💀", color=KAWAII_RED)
        await ctx.send(embed=embed)

    @commands.command()
    async def feed(self, ctx, member: discord.Member):
        """Nakarm kogoś 🍜"""
        embed = discord.Embed(description=f"**{ctx.author.name}** karmi **{member.name}**! Smacznego! 🍜", color=KAWAII_PINK)
        embed.set_image(url="https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbzFucW5nN2V6MWZzazg3bXY1eTY4ZTNmcnZ6MzIxZ3pyYTU3M3Q4bSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/QR7ci2sbhrkzxAuMHH/giphy.gif")
        await ctx.send(embed=embed)

    @commands.command()
    async def ugryz(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"**{ctx.author.name}** gryzie **{member.name}**! Chaps! 🧛‍♀️", color=KAWAII_RED)
        embed.set_image(url=random.choice(GIFS_BITE))
        await ctx.send(embed=embed)

    @commands.command()
    async def liz(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"**{ctx.author.name}** liże **{member.name}**! Mlem! 👅", color=KAWAII_PINK)
        embed.set_image(url=random.choice(GIFS_LICK))
        await ctx.send(embed=embed)

    @commands.command()
    async def pogon(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"**{ctx.author.name}** biegnie za **{member.name}**! Wracaj tu! 🏃‍♀️💨", color=KAWAII_BLUE)
        embed.set_image(url=random.choice(GIFS_CHASE))
        await ctx.send(embed=embed)

    @commands.command()
    async def taniec(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"**{ctx.author.name}** tańczy z **{member.name}** na parkiecie! 💃🕺", color=KAWAII_GOLD)
        embed.set_image(url=random.choice(GIFS_DANCE))
        await ctx.send(embed=embed)

    @commands.command()
    async def bonk(self, ctx, member: discord.Member):
        embed = discord.Embed(description=f"**{ctx.author.name}** robi BONK **{member.name}**! Idziesz do horny jail! 🏏", color=0xFF0000)
        embed.set_image(url=random.choice(GIFS_BONK))
        await ctx.send(embed=embed)

    @commands.command()
    async def adoptuj(self, ctx, member: discord.Member):
        """Adoptuj wybraną osobę do swojej wirtualnej rodziny! 🍼"""
        if member == ctx.author:
            return await ctx.send("❌ Nie możesz adoptować samego siebie!")

        user_p = get_profile_data(ctx.author.id)
        target_p = get_profile_data(member.id)
        
        user_children = user_p.get("children", [])
        if member.id in user_children:
            return await ctx.send(f"❌ **{member.name}** jest już Twoim urwisem!")
            
        if target_p.get("parent"):
            return await ctx.send(f"❌ **{member.name}** ma już prawowitego opiekuna!")

        embed = discord.Embed(
            title="🍼 Papiery Adopcyjne!",
            description=f"**{ctx.author.name}** pragnie Cię zaadoptować, **{member.name}**!\nCzy zgadzasz się na dołączenie do rodziny? (napisz `tak` lub `nie`)",
            color=KAWAII_PINK
        )
        await ctx.send(member.mention, embed=embed)

        def check(m):
            return m.author == member and m.channel == ctx.channel and m.content.lower() in ["tak", "nie"]

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60)
            if msg.content.lower() == "tak":
                # Aktualizacja obydwu profilów. MongoDB wspiera listy dla dzieci
                user_children.append(member.id)
                update_profile(ctx.author.id, "children", user_children)
                update_profile(member.id, "parent", ctx.author.id)

                success_embed = discord.Embed(
                    title="🎉 Nowa Rodzina!",
                    description=f"Wspaniale! **{ctx.author.name}** oficjalnie adoptował/a **{member.name}**! 💖🍼",
                    color=KAWAII_GOLD
                )
                await ctx.send(embed=success_embed)
            else:
                await ctx.send("💔 Adopcja odrzucona... (qwq)")
        except:
            await ctx.send("⌛ Dokumenty wygasły... Adopcja anulowana.")

    @commands.command()
    async def zagroz(self, ctx, member: discord.Member = None):
        """Losowa, komiczna groźba! 😈"""
        if member == ctx.author:
            return await ctx.send("❌ Nie możesz grozić samemu sobie, to dziwne...")
        
        grozby = [
            "Zaraz wyrwę ci zęby i zrobię z nich kwadratowy naszyjnik!",
            "Zrobię ci z twarzy puzzle i zgubię najważniejszy element!",
            "Wrzucę cię do pralki na program wirowania bez litości!",
            "Zaplotę ci rzęsy z brwiami na supeł!",
            "Nakręcę film o twoim życiu i nie dam ci głównej roli!",
            "Zrobię ci z włosów spaghetti i posypię parmezanem!",
            "Zamienię twoje palce u stóp u rąk miejscami!",
            "Nakleję ci na czoło karny chlebek ze smalcem!",
            "Utkam ci sweter z twoich własnych łez i zmuszę cię do jego noszenia!",
            "Skasuję ci konto w banku i kupię za wszystko zupki chińskie!",
            "Zwiążę ci sznurowadła tak, że co drugi krok będziesz lądować w wannie z budyniem!",
            "Zaraz wcisnę cię do butelki po keczupie i wstrząsnę!",
            "Wyślę cię pocztą do Timbuktu bez znaczka zwrotnego!",
            "Zablokuję ci dostęp do memów na 10 lat!",
            "Zjem ci cały zapas chipsów, mlaszcząc ci przy tym nad uchem!",
            "Wsadzę ci kostkę lodu za kołnierz, kiedy się tego najmniej spodziewasz!",
            "Przerobię cię na breloczek do kluczy, który ciągle będzie gubił się w torebce!",
            "Zmuszę cię do słuchania disco polo przez 48 godzin non stop!",
            "Pomaluję ci paznokcie na kolor wściekłej musztardy!",
            "Zmienię ci hasło do wifi na 100-znakowe zdanie z błędami ortograficznymi!",
            "Podłożę ci jeża do kapci!",
            "Kupię ci bilet na bezludną wyspę, ale zapomnę dołączyć mapę powrotną!",
            "Wypiję ci całą zimną wodę w upalny dzień!",
            "Zamienię ci dzwonek w telefonie na wycie wilkołaka!",
            "Zawrócę rzekę tak, by zalała ci trawnik!",
            "Podmieniam sól na cukier, a cukier na sól w twojej kuchni!",
            "Sprawię, że każda rurka, przez którą spróbujesz pić, będzie dziurawa!",
            "Ustawiam wszystkie twoje zegarki na 17 minut do tyłu!",
            "Zarządzę, by twoje skarpetki na zawsze straciły parę w praniu!",
            "Sprawię, że poduszka będzie ciepła z obydwu stron!"
        ]
        
        target = f"**{member.name}**" if member else "**wprost w eter**"
        embed = discord.Embed(
            description=f"**{ctx.author.name}** grozi {target}:\n\n> *\"{random.choice(grozby)}\"* 💥",
            color=KAWAII_RED
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def worek(self, ctx, member: discord.Member):
        """Pakuje kogoś do worka i porywa! 🎒"""
        if member == ctx.author:
            return await ctx.send("Jak zamierzasz wpakować się sam we własny worek? 🤔")
        embed = discord.Embed(description=f"🎒 **{ctx.author.name}** pakuje **{member.name}** do worka i ucieka! Wrrrruuum! 🏃‍♂️💨", color=KAWAII_RED)
        embed.set_image(url=random.choice(GIFS_WOREK))
        await ctx.send(embed=embed)

    @commands.command()
    async def miziaj(self, ctx, member: discord.Member):
        """Mizia kogoś czule! 🥰"""
        if member == ctx.author:
            return await ctx.send("Mizianie samego siebie jest smutne... (qwq)")
        embed = discord.Embed(description=f"🥰 **{ctx.author.name}** słodko mizia **{member.name}**... purr purr! 🐾", color=KAWAII_PINK)
        embed.set_image(url=random.choice(GIFS_MIZIAJ))
        await ctx.send(embed=embed)

    @commands.command()
    async def kuksaniec(self, ctx, member: discord.Member):
        """Daje komuś kuksanińca! 👉"""
        if member == ctx.author:
            return await ctx.send("Kuksasz się sam w żebro? Auć... 😳")
        embed = discord.Embed(description=f"👉 **{ctx.author.name}** daje wkurzającego kuksanińca w żebro **{member.name}**! Hehe! 😆", color=KAWAII_GOLD)
        embed.set_image(url=random.choice(GIFS_KUKSANIEC))
        await ctx.send(embed=embed)

    @commands.command()
    async def zaczep(self, ctx, member: discord.Member):
        """Zaczepia kogoś! 👋"""
        if member == ctx.author:
            return await ctx.send("Zaczepiasz lustro? (O_o)")
        embed = discord.Embed(description=f"👋 **{ctx.author.name}** zaczepia **{member.name}**! Hej, popatrz na mnie! 👀", color=KAWAII_PINK)
        embed.set_image(url=random.choice(GIFS_ZACZEP))
        await ctx.send(embed=embed)

    @commands.command()
    async def ukryj(self, ctx, member: discord.Member):
        """Ukryj się za kimś ze strachu! 🙈"""
        if member == ctx.author:
            return await ctx.send("Nie możesz schować się za sobą!")
        embed = discord.Embed(description=f"🙈 **{ctx.author.name}** przerażony(a) chowa się za plecami **{member.name}**! Ratunku! 😱", color=discord.Color.blue())
        embed.set_image(url=random.choice(GIFS_UKRYJ))
        await ctx.send(embed=embed)

    @commands.command()
    async def pistolet(self, ctx, member: discord.Member):
        """Wyciąga pistolet dla zabawy! 🔫"""
        if member == ctx.author:
            return await ctx.send("Ej, ej! Spokojnie, odłóż tę broń! 😨")
        embed = discord.Embed(description=f"🔫 **{ctx.author.name}** wyciąga znikąd pistolet na wodę i celuje w **{member.name}**! Ręce do góry! 💦", color=KAWAII_RED)
        embed.set_image(url=random.choice(GIFS_PISTOLET))
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Social(bot))
