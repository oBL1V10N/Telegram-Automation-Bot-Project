# Business Telegram Bot

A comprehensive Telegram bot for business automation, client engagement, and order management. This bot helps businesses manage their products, handle customer inquiries, and automate marketing tasks without requiring a database.

## Features

- Multi-language support with automatic language detection
- Live chat integration
- Payment method selection and management
- Product listing and order placement
- Automated marketing and CRM features
- Website product integration
- Admin control panel
- Settings management

## Setup Instructions

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with the following variables:
   ```
   BOT_TOKEN=your_telegram_bot_token
   ADMIN_ID=your_telegram_user_id
   WEBSITE_URL=your_website_url
   ```
4. Run the bot:
   ```bash
   python main.py
   ```

## Admin Commands

- `/setwebsite [url]` - Set the website URL for product fetching
- `/setpayment [method]` - Add a new payment method
- `/setlanguage [code]` - Add a new language
- `/broadcast [message]` - Send a broadcast message to all users
- `/help` - Show all available commands

## User Commands

- `/start` - Start the bot
- `/help` - Show this help message
- `/language` - Change language
- `/products` - View available products
- `/payment` - Select payment method

## Website Integration

The bot automatically fetches products from your website every 6 hours. Products should be structured with the following HTML elements:
- `.product-item` - Container for each product
- `.product-name` - Product name
- `.product-price` - Product price
- `.product-description` - Short description
- `.product-full-description` - Detailed description
- `img` - Product image

## Marketing Features

- Automated daily tips and promotions
- Scheduled broadcast messages
- Customizable marketing schedules
- Product updates and announcements

## Security

- Admin-only access to sensitive commands
- Rate limiting on commands
- Input validation and sanitization
- Secure payment method handling

## Contributing

Feel free to submit issues and enhancement requests! 