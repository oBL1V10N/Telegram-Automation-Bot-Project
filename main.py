import os
import logging
import requests
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from dotenv import load_dotenv  

# ✅ Load environment variables
load_dotenv()  

# ✅ Get bot token from the environment
API_TOKEN = os.getenv("TELEGRAM_TOKEN")

# ✅ Check if the token is loaded correctly
if not API_TOKEN:
    raise ValueError("TELEGRAM_TOKEN is missing! Check your .env file.")

# ✅ Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ✅ Create bot instance
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)

# ✅ Create dispatcher
dp = Dispatcher()

# ✅ Create a router (Required for aiogram v3)
router = Router()

# ✅ WooCommerce API URL
API_URL = "https://oneupshroomsbar.com/wp-json/wp/v2/products"

# ✅ Fetch products from WooCommerce API
def fetch_products():
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        data = response.json()  # Parse the JSON response
        # Log only the first product in the list for simplicity
        if data:
            logging.info("First product in the response: %s", data[0])  # Log the first product only
        return data  # Return the list of products as JSON
    else:
        logging.error(f"Error fetching products. Status code: {response.status_code}")
        return None

# 🔹 Handle the /start and /help commands
@router.message(Command("start", "help"))
async def send_welcome(message: types.Message):
    await message.answer("Hello! I'm your bot 🤖\nHow can I assist you today?")

# 🔹 Handle the /products command to fetch product list
@router.message(Command("products"))
async def show_products(message: types.Message):
    products = fetch_products()
    if products:
        product_list = "\n\n".join(
            [f"Name: {product['name']}\nPrice: ${product['price']}\nDescription: {product.get('short_description', 'No description available.')}" for product in products]
        )
        await message.answer(f"Available Products:\n\n{product_list}")
    else:
        await message.answer("Error fetching products.")

# ✅ Main function to start polling
async def main():
    dp.include_router(router)  # ✅ Attach the router to the dispatcher
    logging.info("🤖 Bot is starting...")
    await dp.start_polling(bot, skip_updates=True)

# ✅ Run the bot
if __name__ == "__main__":
    asyncio.run(main())
