import discord
from discord.ext import commands, tasks
import os
import asyncio
from flask import Flask
from threading import Thread

# --- KONFIGURACJA SERWERA WWW (DLA RENDER) ---
# Integrujemy to bezpośrednio tutaj, aby uniknąć błędów importu
app = Flask('')

@app.route('/')
def home():
    return "I am alive! Bot działa."

def run_web_server():
    # Pobieramy port z otoczenia (wymóg Render) lub ustawiamy 8080
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web_server)
    t.start()
# ---------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True # WAŻNE: Potrzebne do śledzenia VC!

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Lista plików do załadowania - DODANO cogs.profile, cogs.games
COGS = ['cogs.admin', 'cogs.economy', 'cogs.social', 'cogs.general', 'cogs.levels', 'cogs.profile', 'cogs.games']

@tasks.loop(seconds=30)
async def status_loop():
    await bot.change_presence(activity=discord.Game(name="!pomoc | Moduły ⚙️"))
    await asyncio.sleep(15)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Twoich sekretów 🤫"))

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

    if not status_loop.is_running():
        status_loop.start()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title="⛔ Brak uprawnień", description="Nie masz wystarczających uprawnień, by tego użyć!", color=discord.Color.red())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="⚠️ Błąd argumentów", description=f"Brakuje wymaganych danych!\nUżycie: `{ctx.prefix}{ctx.command.name} {ctx.command.signature}`", color=discord.Color.orange())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(title="⚠️ Błędne dane", description="Podałeś nieprawidłowy format danych.", color=discord.Color.orange())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="⏳ Cooldown", description=f"Musisz poczekać {round(error.retry_after, 1)}s.", color=discord.Color.orange())
        await ctx.send(embed=embed)
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        print(f"Error: {error}")

# Uruchomienie serwera WWW
keep_alive()

# Pobieranie tokenu
TOKEN = os.environ.get('DISCORD_TOKEN')

if not TOKEN:
    # Wyrzucamy głośny błąd, żebyś widział w logach, co jest nie tak
    raise ValueError("❌ BŁĄD KRYTYCZNY: Nie znaleziono DISCORD_TOKEN w zakładce Environment na Renderze!")
else:
    try:
        bot.run(TOKEN)
    except Exception as e:
        raise ValueError(f"❌ Błąd podczas logowania (czy token jest poprawny?): {e}")