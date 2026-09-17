import discord
from discord.ext import commands
import os

# Configuración de intents (necesario para detectar cuando entran miembros)
intents = discord.Intents.default()
intents.members = True  # ¡Importante! Activar en el Discord Developer Portal
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'¡Bot conectado con éxito como {bot.user}!')
    print('CW Gaming Bot está listo para la acción 🎮')

@bot.event
async def on_member_join(member):
    # Buscar el canal de bienvenida por su nombre (o puedes poner el ID exacto del canal)
    canal_bienvenida = discord.utils.get(member.guild.text_channels, name="👋│bienvenida")
    
    if not canal_bienvenida:
        # Si no lo encuentra por el nombre exacto con emojis, busca uno que contenga "bienvenida"
        canal_bienvenida = discord.utils.get(member.guild.text_channels, lambda c: "bienvenida" in c.name)
    
    if canal_bienvenida:
        # Mensaje decorado que diseñamos
        mensaje = (
            "```ini\n"
            "[ 🚀 ¡NUEVO JUGADOR CONECTADO! ]\n"
            "```\n"
            f"¡Bienvenido/a a **CW Gaming**, {member.mention}! 💜 Nos alegra un montón tenerte por aquí.\n\n"
            "🌐 **Estás entrando al siguiente nivel de la Era Gaming.** Antes de comenzar tu aventura, echa un vistazo por aquí:\n\n"
            "📜 Lee las normas en el canal correspondiente para mantener el orden.\n"
            "💬 Pásate por `#💬│chat-general` para presentarte y saludar a la comunidad.\n"
            "😂 Comparte tus mejores risas en `#😂│memes`.\n"
            "👥 Busca compañeros para tus partidas en `#👥│buscar-escuadrón`.\n\n"
            "¡Disfruta del servidor y prepárate para la partida! 🎮🔥"
        )
        await canal_bienvenida.send(mensaje)

# Para correr el bot de manera local o en Render usando variables de entorno
TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ Error: No se encontró la variable de entorno DISCORD_TOKEN.")
