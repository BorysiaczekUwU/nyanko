import discord
from discord.ext import commands
import json
import os
import uuid
from datetime import datetime

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.events_file = "data/events.json"
        
        # Inicjalizacja pliku z eventami
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.events_file):
            with open(self.events_file, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def load_events(self):
        with open(self.events_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_events(self, events):
        with open(self.events_file, "w", encoding="utf-8") as f:
            json.dump(events, f, indent=4, ensure_ascii=False)

    @commands.group(invoke_without_command=True)
    async def event(self, ctx):
        """Moduł do zarządzania wydarzeniami serwerowymi."""
        embed = discord.Embed(title="📅 System Eventów", color=discord.Color.purple())
        embed.add_field(name="`!event create <nazwa> | <data> | <opis>`", value="Tworzy nowe wydarzenie (wymaga uprawnień)", inline=False)
        embed.add_field(name="`!event list`", value="Wyświetla aktywne wydarzenia", inline=False)
        embed.add_field(name="`!event join <id>`", value="Zapisuje Cię na wydarzenie", inline=False)
        embed.add_field(name="`!event leave <id>`", value="Wypisuje Cię z wydarzenia", inline=False)
        embed.add_field(name="`!event cancel <id>`", value="Anuluje wydarzenie (wymaga uprawnień)", inline=False)
        await ctx.send(embed=embed)

    @event.command()
    @commands.has_permissions(manage_events=True)
    async def create(self, ctx, *, args: str):
        """Tworzy nowe wydarzenie. Użycie: !event create Nazwa | Data | Opis"""
        try:
            parts = [p.strip() for p in args.split("|")]
            if len(parts) < 3:
                raise ValueError("Brakuje argumentów.")
            
            name = parts[0]
            date = parts[1]
            desc = parts[2]
            
            event_id = str(uuid.uuid4())[:6] # Proste krótkie ID
            
            events = self.load_events()
            events[event_id] = {
                "name": name,
                "date": date,
                "description": desc,
                "creator": ctx.author.name,
                "participants": []
            }
            self.save_events(events)
            
            embed = discord.Embed(title="🎉 ZAPOWIEDŹ WYDARZENIA!", color=discord.Color.green())
            embed.add_field(name="📌 Nazwa", value=name, inline=False)
            embed.add_field(name="📅 Kiedy", value=date, inline=False)
            embed.add_field(name="📜 Opis", value=desc, inline=False)
            embed.add_field(name="🛠️ ID Eventu", value=f"`{event_id}` (użyj do zapisu: `!event join {event_id}`)", inline=False)
            embed.set_footer(text=f"Utworzono przez: {ctx.author.name}")
            
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"❌ Błąd składni. Użycie: `!event create Moje Super Party | 20:00 Jutro | Będzie super zabawa`")

    @event.command(name="list")
    async def event_list(self, ctx):
        """Wyświetla nadchodzące wydarzenia."""
        events = self.load_events()
        if not events:
            return await ctx.send("📭 Obecnie nie ma zaplanowanych żadnych wydarzeń.")
            
        embed = discord.Embed(title="📅 Nadchodzące Wydarzenia", color=discord.Color.purple())
        for e_id, e_data in events.items():
            party_count = len(e_data["participants"])
            embed.add_field(
                name=f"[{e_id}] {e_data['name']}", 
                value=f"**Kiedy:** {e_data['date']}\n**Osoby:** {party_count} zapisanych\n**Opis:** {e_data['description']}", 
                inline=False
            )
        await ctx.send(embed=embed)

    @event.command()
    async def join(self, ctx, event_id: str):
        """Zapisuje na wybrane wydarzenie po jego ID."""
        events = self.load_events()
        if event_id not in events:
            return await ctx.send("❌ Nie znaleziono wydarzenia o tym ID.")
            
        user_id = str(ctx.author.id)
        if user_id in events[event_id]["participants"]:
            return await ctx.send("⚠️ Jesteś już zapisany na to wydarzenie!")
            
        events[event_id]["participants"].append(user_id)
        self.save_events(events)
        await ctx.send(f"✅ Pomyślnie zapisano Cię na wydarzenie **{events[event_id]['name']}**!")

    @event.command()
    async def leave(self, ctx, event_id: str):
        """Wypisuje z wybranego wydarzenia."""
        events = self.load_events()
        if event_id not in events:
            return await ctx.send("❌ Nie znaleziono wydarzenia o tym ID.")
            
        user_id = str(ctx.author.id)
        if user_id not in events[event_id]["participants"]:
            return await ctx.send("⚠️ Nawet nie jesteś na nie zapisany!")
            
        events[event_id]["participants"].remove(user_id)
        self.save_events(events)
        await ctx.send(f"👋 Wypisałeś się z wydarzenia **{events[event_id]['name']}**.")

    @event.command()
    @commands.has_permissions(manage_events=True)
    async def cancel(self, ctx, event_id: str):
        """Anuluje wydarzenie."""
        events = self.load_events()
        if event_id not in events:
            return await ctx.send("❌ Nie znaleziono wydarzenia o tym ID.")
            
        name = events[event_id]['name']
        del events[event_id]
        self.save_events(events)
        await ctx.send(f"🗑️ Wydarzenie **{name}** zostało anulowane i usunięte z kalendarza.")

async def setup(bot):
    await bot.add_cog(Events(bot))
