import discord
from discord.ext import commands
import requests
import json

# Definir las intenciones requeridas para el bot
intents = discord.Intents.default()
intents.message_content = True  

bot = commands.Bot(command_prefix='as!', intents=intents)


# Cargar datos almacenados previamente en el archivo (si existe)
try:
    with open('datos.json', 'r') as f:
        datos_guardados = json.load(f)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    datos_guardados = {}


# Evento que se ejecuta cuando el bot está listo y conectado
@bot.event
async def on_ready():
    print(f'¡El bot está listo como {bot.user}!')




@bot.command()
async def post(ctx, link: str, user: str):
    # Crear un objeto Embed
    # embed = discord.Embed(title='Se añadió correctamente a nuestra web. :)', description='Todo correcto!!', color=discord.Color.green())

    # Agregar campos adicionales al Embed con las opciones recibidas
    # embed.add_field(name='Opción 1', value=link, inline=True)
    # embed.add_field(name='Opción 2', value=user, inline=True)

    # Almacenar los datos en el diccionario "datos_guardados"
    datos_guardados[link] = user

    # Guardar los datos en el archivo
    with open('datos.json', 'w') as f:
      json.dump(datos_guardados, f)

    # URL de la web a la que enviaremos los datos
    url = 'http://127.0.0.1:3000/web/index.html'

    # Datos que enviaremos en formato JSON
    data = {
        'link': link,
        'user': user
    }

    try:
        # Enviar los datos al servidor Flask utilizando WebSockets
        response = requests.post(url + 'socket.io/?EIO=3&transport=polling&t=Nlh3NKo', json=data)
        # Es importante que el endpoint 'socket.io' y los parámetros en la URL sean correctos para Flask-SocketIO

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            await ctx.send('Datos enviados correctamente.')
        else:
            await ctx.send('Hubo un error al enviar los datos.')
    except requests.exceptions.RequestException as e:
        await ctx.send(f'Error: {e}')

    # Enviar el Embed como respuesta
    # await ctx.send(embed=embed)

@bot.command()
async def mostrar_datos(ctx):
    # Mostrar los datos almacenados en el archivo
    await ctx.send(datos_guardados)

@bot.command()
async def helpy(ctx):
    embedhelp = discord.Embed(title='Ayuda 🆘', description='Este es el bot oficial de Adversting Sell', color=discord.Color.blue())

    # Agregar campos adicionales al Embed
    embedhelp.add_field(name='Comandos basicos', value="`as!help`: lo acabas de utilizar \n `as!post`: para subir tus servicios a la web oficial \n `as!web`: para ir a nuestra web oficial", inline=False)
    embedhelp.add_field(name='as!post', value="`as!post <link><user> [image_link || secondlink]`", inline=False)
        

    # Enviar el Embed como respuesta
    await ctx.send(embed=embedhelp)


  
# Manejo de errores para el comando "!ping"
@post.error
async def ping_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        # Crear un objeto Embed para mostrar el mensaje de error
        embed = discord.Embed(title='Error', description='Faltan argumentos. Uso correcto: as!post <link><user>', color=discord.Color.red())

        # Enviar el Embed como respuesta
        await ctx.send(embed=embed)


# Ejecutar el bot con el token de tu bot

bot.run('MTEzNTk2NDQwMjc2MDMwMjY1Mg.Ggfm97.4Gw_WPcTMnZ2H-hDB7Skq6JO7MvIB7YfR2Q9SI')

