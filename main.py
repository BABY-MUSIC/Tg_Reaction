import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from aiohttp import web
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

API_ID="16457832"
API_HASH="3030874d0befdb5d05597deacc3e83ab"

BOT_TOKEN_1="7581171239:AAG99QESgSiKQuV2vizw4wHF1WypJjoN5Ik"   # Replace with actual token
BOT_TOKEN_2="7756406698:AAHdNxkWNc9beej769fJI5wtGf31J619N6Q"   # Optional: Add more tokens



# Collect all bot tokens (e.g., BOT_TOKEN_1, BOT_TOKEN_2, ...)
BOT_TOKENS = [v for k, v in os.environ.items() if k.startswith("BOT_TOKEN_")]

EMOJIS = ["🥰", "❤️", "😁", "💋", "😱", "🤣", "😘", "❤️‍🔥", "👌", "🫡", "😍"]

bots = []

def create_bot(token, index):
    bot = Client(
        name=f"bot_{index}",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=token
    )

    @bot.on_message(filters.incoming)
    async def react_to_messages(client: Client, message: Message):
        try:
            emoji = random.choice(EMOJIS)
            await message.react(emoji)
        except Exception as e:
            print(f"[Bot {index}] Error: {e}")

    return bot

async def handle(request):
    return web.Response(text="✅ Bot is alive!")

async def run_web():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8000)
    await site.start()

async def main():
    global bots
    bots = [create_bot(token, i) for i, token in enumerate(BOT_TOKENS)]

    await asyncio.gather(
        *(bot.start() for bot in bots),
        run_web()
    )
    print("Bots and web server are running.")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
