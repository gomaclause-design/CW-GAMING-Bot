import os
import threading
import discord
from discord.ext import commands
from flask import Flask

# 1. Configuración del servidor Flask en el hilo principal (para que Render detecte el puerto al instante)
app = Flask(__name__)

@app.route('/')
def home():
    return "¡El bot de CW Gaming está activo y en línea! 🤖💜"


# 2. Configuración del Bot de Discord
intents = discord.Intents.default()
intents.members = True  # Necesario para detectar entradas de usuarios
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'¡Bot conectado con éxito como {bot.user}!')
    print('CW Gaming Bot está listo para la acción 🎮')

@bot.event
async def on_member_join(member):
    canal_bienvenida = discord.utils.get(member.guild.text_channels, name="👋│bienvenida")
    
    if not canal_bienvenida:
        canal_bienvenida = discord.utils.get(member.guild.text_channels, lambda c: "bienvenida" in c.name)
    
    if canal_bienvenida:
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

def run_discord_bot():
    TOKEN = os.getenv("DISCORD_TOKEN")
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ Error: No se encontró la variable de entorno DISCORD_TOKEN.")


# 3. Ejecución: El bot de Discord corre en segundo plano y Flask toma el control principal del puerto
if __name__ == "__main__":
    # Lanzamos el bot de Discord en un hilo independiente
    discord_thread = threading.Thread(target=run_discord_bot)
    discord_thread.daemon = True
    discord_thread.start()
    print("🤖 Bot de Discord lanzado en segundo plano.")

    # Flask se queda ejecutándose en el hilo principal abriendo el puerto para Render
    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 Iniciando servidor web de Flask en el puerto {port}...")
    app.run(host="0.0.0.0", port=port)
