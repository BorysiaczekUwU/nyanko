import discord
from discord.ext import commands
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