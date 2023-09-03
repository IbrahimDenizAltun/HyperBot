import discord
from discord.ext import commands
import random
import asyncio
import logging.handlers
import os
import asyncpg
from typing import List, Optional
from pass_gen import passgen
from pass_gen10 import passgen10
from head_or_tails import head_or_tails
from aiohttp import ClientSession


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix = "$", intents = intents)

class CustomBot(commands.Bot):
    def __init__(
        self,
        *args,
        initial_extensions: List[str],
        db_pool: asyncpg.Pool,
        web_client: ClientSession,
        testing_guild_id: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.db_pool = db_pool
        self.web_client = web_client
        self.testing_guild_id = testing_guild_id
        self.initial_extensions = initial_extensions

    async def setup_hook(self) -> None:

        # here, we are loading extensions prior to sync to ensure we are syncing interactions defined in those extensions.

        for extension in self.initial_extensions:
            await self.load_extension(extension)

        # In overriding setup hook,
        # we can do things that require a bot prior to starting to process events from the websocket.
        # In this case, we are using this to ensure that once we are connected, we sync for the testing guild.
        # You should not do this for every guild or for global sync, those should only be synced when changes happen.
        if self.testing_guild_id:
            guild = discord.Object(self.testing_guild_id)
            # We'll copy in the global commands to test with:
            self.tree.copy_global_to(guild=guild)
            # followed by syncing to the testing guild.
            await self.tree.sync(guild=guild)

        # This would also be a good place to connect to our database and
        # load anything that should be in memory prior to handling events.


async def main():

    # When taking over how the bot process is run, you become responsible for a few additional things.

    # 1. logging

    # for this example, we're going to set up a rotating file logger.
    # for more info on setting up logging,
    # see https://discordpy.readthedocs.io/en/latest/logging.html and https://docs.python.org/3/howto/logging.html

    logger = logging.getLogger('discord')
    logger.setLevel(logging.INFO)

    handler = logging.handlers.RotatingFileHandler(
        filename='discord.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Alternatively, you could use:
    # discord.utils.setup_logging(handler=handler, root=False)

    # One of the reasons to take over more of the process though
    # is to ensure use with other libraries or tools which also require their own cleanup.

    # Here we have a web client and a database pool, both of which do cleanup at exit.
    # We also have our bot, which depends on both of these.

    async with ClientSession() as our_client, asyncpg.create_pool(user='postgres', command_timeout=30) as pool:
        # 2. We become responsible for starting the bot.

        exts = ['general', 'mod', 'dice']
        async with CustomBot(commands.when_mentioned, db_pool=pool, web_client=our_client, initial_extensions=exts) as bot:

            await bot.start(os.getenv('MTE0MTc5MTU1NTMyMjEyMjI0MA.Gc-Ofo.dFNf8mlLGQIccr7J_l2FQ12rg3hwsRwuEJolwg', ''))


# For most use cases, after defining what needs to run, we can just tell asyncio to run it:
asyncio.run(main())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity = discord.Game(name = "Roblox"))

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
    await ctx.send("$cmds to see all commands\n$hello makes the bot say Yo!\n$bye makes the bot say :wave:\n$pass_gen (...) generates a random password that is as long as the number you put in\n$Head_or_Tails (i think this one is obvious lol)\n$bruh responds with a bruh gif\n$happybd {mention} celebrates the mentioned's birthday!\n$guessnumber makes you guess a number between 1 and 10")
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






















































bot.run("MTE0MTc5MTU1NTMyMjEyMjI0MA.Gc-Ofo.dFNf8mlLGQIccr7J_l2FQ12rg3hwsRwuEJolwg")