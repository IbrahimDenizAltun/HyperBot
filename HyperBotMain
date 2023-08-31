import discord
import random
import asyncio
from pass_gen import passgen
from pass_gen10 import passgen10
from head_or_tails import head_or_tails

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity = discord.Game(name = "Roblox"))

@client.event
async def on_message(message):
    member = message.author
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send("Hi!")
    elif message.content.startswith('$bye'):
        await message.channel.send(":wave:")
    elif message.content.startswith('$bruh'):
        await message.channel.send("https://media.tenor.com/I46wH_jfv1YAAAAC/bruh-moment.gif")
    elif message.content.startswith("$passgen10"):
        await message.channel.send(passgen10())
    elif message.content.startswith("$passgen"):
        lengthy = message.content[8:].strip()
        await message.channel.send(passgen(lengthy))
    elif message.content.startswith("$cmds"):
        await message.channel.send("$cmds to see all commands\n$hello makes the bot say Yo!\n$bye makes the bot say :wave:\n$passgen (...) generates a random password that is as long as the number you put in\n$head or tails (i think this one is obvious lol)\n$bruh responds with a bruh gif\n$happybd {mention} celebrates the mentioned's birthday!\n$guessnumber makes you guess a number between 1 and 10")
    elif message.content.startswith("$head or tails"):
        await message.channel.send(head_or_tails())
    elif message.content.startswith("$happybd"):
        mentioned = message.content[8:].strip()
        await message.channel.send("Happy birthday, " + mentioned + "!")
    elif message.content.startswith('$guessnumber'):
        await message.channel.send('Lets guess a number between 1 and 10!')

        def is_correct(m):
            return m.author == message.author and m.content.isdigit()

        answer = random.randint(1, 10)

        try:
            guess = await client.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await message.channel.send(f'Dude, you took too long the answer was {answer}.')

        if int(guess.content) == answer:
            await message.channel.send('You got it right!')
        else:
            await message.channel.send(f'Nope! It was actually {answer}.')
