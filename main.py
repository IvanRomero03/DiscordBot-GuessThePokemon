from discord.ext import commands
import pandas as pd

TOKEN = "TOKEN"

# Initialize Bot and Denote The Command Prefix
bot = commands.Bot(command_prefix="!")

# Runs when Bot Succesfully Connects

pokemonCorrecto = 'piplup'
pokemonDataSet = pd.read_csv('pokemon.csv')
pokemonDataSet = pokemonDataSet['name'].tolist()
# nombre del participante, numero de preguntas restantes y numero de intentos restantes
participantes = {
    'Ivansin': [10, 1]
}


@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')


@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@bot.command()
async def guess(ctx, *, guess):
    # formato de nombre:
    # mayuscula inicial, minusculas restantes
    guess = guess.lower()
    guess = guess.capitalize()
    print(guess)

    if ctx.author in participantes.keys():
        if participantes[ctx.author][1] == 0:
            await ctx.send('Ya no tienes más intentos:(')
            return

    if guess not in pokemonDataSet:
        await ctx.send(f'{guess} no es un pokemon!')
    else:
        if guess == pokemonCorrecto.capitalize():
            await ctx.send(f'{guess} es correcto!')
            await ctx.send(f'{ctx.author} ha adivinado!')
        else:
            keys = participantes.keys()
            if ctx.author in keys:
                participantes[ctx.author][1] -= 1
                await ctx.send(f'{guess} no es correcto!')
                await ctx.send(f'Te quedan {participantes[ctx.author][1]} intentos')
            else:
                participantes[ctx.author] = [0, 0]
                await ctx.send(f'{guess} no es correcto!')
                await ctx.send(f'Te quedan {participantes[ctx.author][1]} intentos')


@bot.command()
async def intentos(ctx):
    keys = participantes.keys()
    if ctx.author in keys:
        await ctx.send(f'Te quedan {participantes[ctx.author][1]} intentos')
    else:
        await ctx.send(f'No has participado todavía, te queda 1 intento!')


@bot.command()
async def preguntas(ctx):
    keys = participantes.keys()
    if ctx.author in keys:
        await ctx.send(f'Te quedan {participantes[ctx.author][0]} preguntas')
    else:
        await ctx.send(f'No has participado todavía, te quedan 10 preguntas!')


@bot.command()
async def pregunta(ctx, *, pregunta):
    print(pregunta)
    print(ctx)
    if ctx.author in participantes.keys():
        if participantes[ctx.author][0] == 0 or participantes[ctx.author][1] == 0:
            await ctx.send('Ya no tienes más preguntas:(')
            return
    else:
        participantes[ctx.author] = [10, 1]
    msg = await ctx.send(f'{ctx.author} pregunta: {pregunta}')
    participantes[ctx.author][0] -= 1
    emoji = '\N{THUMBS UP SIGN}'
    await msg.add_reaction(emoji)
    emoji = '\N{THUMBS DOWN SIGN}'
    await msg.add_reaction(emoji)


@bot.command()
async def setPokemonCorrecto(ctx, *, pokemon):
    global pokemonCorrecto
    idProf = 'EllieWalaur'
    if ctx.author.name == idProf:
        pokemonCorrecto = pokemon
        pokemonCorrecto.lower()
        pokemonCorrecto.capitalize()
        if pokemonCorrecto not in pokemonDataSet:
            pokemonDataSet.append(pokemonCorrecto)
    print(pokemonCorrecto)


@bot.command()
async def verPokemonCorrecto(ctx):
    global pokemonCorrecto
    print(pokemonCorrecto)


@bot.command()
async def reglas(ctx):
    await ctx.send('''
1) Tienen 10 preguntas disponibles, una por cada clase que se haya tomado.
2) Sólo pueden hacer preguntas donde mi respuesta sea "Sí" o "No".
3) Pueden participar de forma individual, de hacerlo no participan en las decisiones de este grupo.
4) Sólo las personas que participen en la dinámica podrán acceder a las recompensas, es criterio de todxs lxs participantes otorgar o no la acreditación de la participación.
5) Pueden discutir lo que quieran en el foro de qué deberían preguntar, pero sólo responderé a aquella que ustedes me digan que cuenta como la pregunta...
''')


@bot.command()
async def ayuda(ctx):
    await ctx.send('!reglas')
    await ctx.send('!pregunta <pregunta>')
    await ctx.send('!preguntas')
    await ctx.send('!intentos')
    await ctx.send('!guess <nombre del pokemon>')


bot.run(TOKEN)
