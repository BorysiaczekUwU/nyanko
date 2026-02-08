import discord
from discord.ext import commands
import os
import asyncio

# Próba importu keep_alive
try:
    from keep_alive import keep_alive
except ImportError:
    print("⚠️ BŁĄD: Brak pliku keep_alive.py lub biblioteki Flask!")
    def keep_alive(): pass

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True # WAŻNE: Potrzebne do śledzenia VC!

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Lista plików do załadowania - DODANO cogs.profile
COGS = ['cogs.admin', 'cogs.economy', 'cogs.social', 'cogs.general', 'cogs.levels', 'cogs.profile']

@bot.event
async def on_ready():
    print(f'✨ Zalogowano jako {bot.user.name} (ID: {bot.user.id}) ✨')
    print('~ System modułowy (Cogs) aktywny! ~')
    
    # Ładowanie rozszerzeń
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f'✅ Załadowano: {cog}')
        except Exception as e:
            print(f'❌ Błąd ładowania {cog}: {e}')

    while True:
        await bot.change_presence(activity=discord.Game(name="!pomoc | Moduły ⚙️"))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Twoich sekretów 🤫"))
        await asyncio.sleep(15)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("⛔ Brak uprawnień!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("⚠️ Brakuje argumentu!")
    elif isinstance(error, commands.CommandNotFound):
        pass # Ignoruj nieznane komendy
    else:
        print(f"Error: {error}")

# Uruchomienie serwera WWW (dla Rendera)
keep_alive()

# Pobieranie tokenu
TOKEN = os.environ.get('DISCORD_TOKEN')

if not TOKEN:
    raise ValueError("❌ BŁĄD KRYTYCZNY: Nie znaleziono DISCORD_TOKEN w zakładce Environment na Renderze!")
else:
    try:
        bot.run(TOKEN)
    except Exception as e:
        raise ValueError(f"❌ Błąd podczas logowania (czy token jest poprawny?): {e}")