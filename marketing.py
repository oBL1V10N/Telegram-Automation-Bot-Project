import asyncio
from datetime import datetime, timedelta
import logging
from aiogram import Bot, Dispatcher, types
from config import config

logger = logging.getLogger(__name__)
bot = Bot(token=config.bot_token)
dp = Dispatcher(bot)

# Admin commands
async def set_website_url(message: types.Message):
    if message.from_user.id == config.admin_id:
        url = message.text.split(" ", 1)[1]
        config.update_setting("website_url", url)
        await message.reply(f"Website URL set to {url}")
    else:
        await message.reply("You are not authorized to perform this action.")

async def set_payment_methods(message: types.Message):
    if message.from_user.id == config.admin_id:
        methods = message.text.split(" ", 1)[1]
        config.update_setting("enabled_payment_methods", methods)
        await message.reply(f"Payment methods set to {methods}")
    else:
        await message.reply("You are not authorized to perform this action.")

async def start_scraping(message: types.Message):
    if message.from_user.id == config.admin_id:
        interval = message.text.split(" ", 1)[1]  # Example format: "every 6 hours"
        config.update_setting("scraping_interval", interval)
        await message.reply(f"Product scraping set to {interval}")
    else:
        await message.reply("You are not authorized to perform this action.")

async def get_help(message: types.Message):
    help_text = """
    - /set_website <URL>: Set the website URL for scraping.
    - /set_payment_methods <methods>: Set the available payment methods (e.g., paypal, bitcoin).
    - /start_scraping <interval>: Start scraping products with the given interval.
    - /help: Display this help message.
    """
    await message.reply(help_text)

# Register commands
@dp.message_handler(commands=['set_website'])
async def cmd_set_website(message: types.Message):
    await set_website_url(message)

@dp.message_handler(commands=['set_payment_methods'])
async def cmd_set_payment_methods(message: types.Message):
    await set_payment_methods(message)

@dp.message_handler(commands=['start_scraping'])
async def cmd_start_scraping(message: types.Message):
    await start_scraping(message)

@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await get_help(message)

async def send_marketing_message(user_id: int, message: str):
    try:
        await bot.send_message(user_id, message)
        return True
    except Exception as e:
        logger.error(f"Error sending marketing message to user {user_id}: {str(e)}")
        return False

async def send_daily_tips():
    while True:
        try:
            if not config.marketing_enabled:
                await asyncio.sleep(60)
                continue

            current_time = datetime.utcnow()
            marketing_messages = config.get_setting("marketing_messages")
            
            for message_data in marketing_messages:
                schedule = message_data.get("schedule", {})
                
                if (current_time.hour == schedule.get("hour", config.daily_tips_hour) and 
                    current_time.minute == schedule.get("minute", config.daily_tips_minute)):
                    message = message_data["message"]
                    # Send to all active chats
                    await send_marketing_message(config.admin_id, message)
                    message_data["created_at"] = current_time
            
            await asyncio.sleep(60)
            
        except Exception as e:
            logger.error(f"Error in daily tips scheduler: {str(e)}")
            await asyncio.sleep(60)

async def start_marketing_scheduler():
    asyncio.create_task(send_daily_tips())

# Start the bot
async def on_start():
    asyncio.create_task(start_marketing_scheduler())
    await dp.start_polling()