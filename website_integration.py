import aiohttp
import asyncio
from bs4 import BeautifulSoup
import logging
from datetime import datetime
from config import config

logger = logging.getLogger(__name__)

async def fetch_products_from_website():
    website_url = config.get_setting("website_url")
    if not website_url:
        logger.error("Website URL not configured")
        return []

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(website_url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    products = []
                    # This is a basic example - you'll need to adjust the selectors
                    # based on your website's HTML structure
                    product_elements = soup.select('.product-item')  # Adjust selector
                    
                    for product_elem in product_elements:
                        try:
                            product = {
                                'name': product_elem.select_one('.product-name').text.strip(),
                                'price': float(product_elem.select_one('.product-price').text.strip().replace('$', '')),
                                'description': product_elem.select_one('.product-description').text.strip(),
                                'full_description': product_elem.select_one('.product-full-description').text.strip(),
                                'image_url': product_elem.select_one('img')['src']
                            }
                            products.append(product)
                            
                        except Exception as e:
                            logger.error(f"Error processing product: {str(e)}")
                            continue
                    
                    # Update product cache
                    config.update_product_cache(products)
                    logger.info(f"Successfully fetched {len(products)} products")
                    return products
                else:
                    logger.error(f"Failed to fetch website: {response.status}")
                    return []
    
    except Exception as e:
        logger.error(f"Error fetching products: {str(e)}")
        return []

async def schedule_product_sync():
    while True:
        await fetch_products_from_website()
        # Sync every 6 hours
        await asyncio.sleep(6 * 60 * 60)

async def start_product_sync():
    asyncio.create_task(schedule_product_sync()) 