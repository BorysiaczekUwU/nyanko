import discord
from discord.ext import commands
import os
import asyncio
import logging
from flask import Flask
from threading import Thread

# --- KONFIGURACJA LOGOWANIA ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("kawaii_bot")

# --- KONFIGURACJA SERWERA WWW (DLA RENDER) ---
app = Flask('')

@app.route('/')
def home():
    return "I am alive! Bot działa."

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web_server)
    t.start()
# ---------------------------------------------

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Lista plików do załadowania
COGS = ['cogs.admin', 'cogs.economy', 'cogs.social', 'cogs.general', 'cogs.levels', 'cogs.profile', 'cogs.games']

@bot.event
async def on_ready():
    logger.info(f'✨ Zalogowano jako {bot.user.name} (ID: {bot.user.id}) ✨')
    print('~ System modułowy (Cogs) aktywny! ~')
    
    # Ładowanie rozszerzeń
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            logger.info(f'✅ Załadowano: {cog}')
        except Exception as e:
            logger.error(f'❌ Błąd ładowania {cog}: {e}', exc_info=True)

    while True:
        await bot.change_presence(activity=discord.Game(name="!pomoc | Moduły ⚙️"))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Twoich sekretów 🤫"))
        await asyncio.sleep(15)

@bot.command()
@commands.has_permissions(administrator=True)
async def logs(ctx):
    """(Admin) Wyświetla ostatnie 20 linii logów"""
    try:
        if not os.path.exists("bot.log"):
            await ctx.send("📜 Plik logów jest pusty lub nie istnieje.")
            return

        with open("bot.log", "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_lines = lines[-20:]
            text = "".join(last_lines)
            if not text.strip():
                text = "Brak logów."
            if len(text) > 1900:
                text = text[-1900:]

            await ctx.send(f"📜 **Ostatnie logi systemowe:**\n```log\n{text}\n```")
    except Exception as e:
        await ctx.send(f"❌ Błąd odczytu logów: {e}")

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
        logger.error(f"Unhandled error in command {ctx.command}: {error}", exc_info=True)
        # Informujemy użytkownika o nieznanym błędzie
        embed = discord.Embed(title="⚠️ Nieoczekiwany Błąd", description=f"Wystąpił błąd podczas wykonywania komendy.\nZostał on zapisany w logach.", color=discord.Color.red())
        embed.set_footer(text=f"Kod błędu: {error}")
        await ctx.send(embed=embed)

# Uruchomienie serwera WWW
keep_alive()

# Pobieranie tokenu
TOKEN = os.environ.get('DISCORD_TOKEN')

if not TOKEN:
    logger.critical("❌ BŁĄD KRYTYCZNY: Nie znaleziono DISCORD_TOKEN w zakładce Environment na Renderze!")
    raise ValueError("❌ BŁĄD KRYTYCZNY: Nie znaleziono DISCORD_TOKEN w zakładce Environment na Renderze!")
else:
    try:
        bot.run(TOKEN)
    except Exception as e:
        logger.critical(f"❌ Błąd podczas logowania: {e}", exc_info=True)
        raise ValueError(f"❌ Błąd podczas logowania (czy token jest poprawny?): {e}")
