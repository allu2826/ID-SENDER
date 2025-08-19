import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# Load token from .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Setup bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Events
@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

@bot.event
async def on_message(message):
    print(f"📥 Message received: {message.content} by {message.author}")
    await bot.process_commands(message)

# Command: !post
@bot.command()
async def post(ctx):
    print("🟢 !post command triggered")

    folder = "./assets"
    allowed_extensions = [".png", ".jpg", ".jpeg", ".webp"]

    try:
        all_files = [
            f for f in os.listdir(folder)
            if any(f.lower().endswith(ext) for ext in allowed_extensions)
        ]
    except FileNotFoundError:
        await ctx.send("❌ Folder `assets` not found.")
        return

    if not all_files:
        await ctx.send("⚠️ No images found in /assets folder.")
        return

    # First message with text
    text = (
        "🔥 **ACCOUNT AVAILABLE FOR SELL**\n\n"
        "💰 **Price - PRICE**\n\n"
        "🖥️ **PLATFORM - CHANGABLE**\n\n"
        "🎟️ **Create a ticket OR DM To Buy**"
    )

    batch_size = 10
    for i in range(0, len(all_files), batch_size):
        batch = all_files[i:i + batch_size]
        files = [discord.File(os.path.join(folder, f)) for f in batch]

        if i == 0:
            await ctx.send(content=text, files=files)
        else:
            await ctx.send(files=files)

# Run the bot
print("Loaded TOKEN:", TOKEN[:10], "...")
bot.run(TOKEN)
