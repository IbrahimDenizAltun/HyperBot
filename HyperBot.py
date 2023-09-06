import os
import requests
import nextcord
from nextcord.ext import commands
import random
import asyncio
import aiosqlite
from pass_gen import passgen
from pass_gen10 import passgen10
from head_or_tails import head_or_tails

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = "$", intents = intents)



def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity = nextcord.Game(name = "Roblox"))
    async with aiosqlite.connect("HyperBot.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER, guild INTEGER)")
        await db.commit()

@bot.command()
async def hello(ctx):
    await ctx.send("Yo!")
@bot.command()
async def bye(ctx):
    await ctx.send(":wave:")
@bot.command()
async def bruh(ctx):
    await ctx.send("https://media.tenor.com/I46wH_jfv1YAAAAC/bruh-moment.gif")
@bot.command()
async def pass_gen(ctx, lengthy = "8"):
    await ctx.send(passgen(lengthy))
@bot.command()
async def cmds(ctx):
    await ctx.send("$cmds to see all commands\n$hello makes the bot say Yo!\n$bye makes the bot say :wave:\n$pass_gen (...) generates a random password that is as long as the number you put in\n$Head_or_Tails (i think this one is obvious lol)\n$bruh responds with a bruh gif\n$happybd {mention} celebrates the mentioned's birthday!\n$guessnumber makes you guess a number between 1 and 10\n$randomduck for random ducks\n$gif to make @Hyper Bot join you sending a gif\n$randommeme to see some random meme photos")
@bot.command()
async def Head_or_Tails(ctx):
    await ctx.send(head_or_tails())
@bot.command()
async def happybd(ctx, mentioned = "the people who have birthday today"):
    await ctx.send("Happy birthday, " + mentioned + "!")
@bot.command()
async def guessnumber(ctx):
    await ctx.send('Lets guess a number between 1 and 10!')

    def is_correct(m):
        return m.author == m.author and m.content.isdigit()

    answer = random.randint(1, 10)

    try:
        guess = await bot.wait_for('message', check=is_correct, timeout=5.0)
    except asyncio.TimeoutError:
        return await ctx.send(f'Dude, you took too long the answer was {answer}.')

    if int(guess.content) == answer:
        await ctx.send('You got it right!')
    else:
        await ctx.send(f'Nope! It was actually {answer}.')
@bot.command()
async def adduser(ctx, member:nextcord.Member):
    member = ctx.author
    async with aiosqlite.connect("HyperBot.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute("SELECT id FROM users WHERE id = ? AND guild = ?", (member.id, ctx.guild.id))
            data = await cursor.fetchone()
            if data:
                await cursor.execute("UPDATE users SET id = ? WHERE guild = ?", (member.id, ctx.guild.id))
                message = await ctx.send('User is already added!')
            else:
                await cursor.execute("INSERT INTO users (id, guild) VALUES (?, ?)", (member.id, ctx.guild.id))
                message = await ctx.send('User added!')
                emoji = "\N{WHITE HEAVY CHECK MARK}"
                await message.add_reaction(emoji)
        await db.commit()
@bot.command()
async def randommeme(ctx):
    randomnumber = random.randint(1,4)
    with open('Goofy Photos/goofy' + str(randomnumber) + ".png", 'rb' ) as f:
        pic = nextcord.File(f)
    await ctx.send(file = pic)
    print(os.listdir("Goofy Photos"))
@bot.command("randomduck")
async def randomduck(ctx):
    image_url = get_duck_image_url()
    await ctx.send(image_url)
@bot.command("gif")
async def gif(ctx, link = "https://media.tenor.com/mXoUIFADXXQAAAAd/rick-roll-discord.gif"):
    await ctx.send(link)
