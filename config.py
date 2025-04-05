import os
from typing import Dict

class Config:
    def __init__(self):
        # Load environment variables
        self._load_env_vars()

    def _load_env_vars(self):
        from dotenv import load_dotenv
        load_dotenv()

    def get_setting(self, key: str):
        return os.getenv(key)

    def update_setting(self, key: str, value: str):
        os.environ[key] = value

    def _parse_payment_methods(self) -> Dict[str, str]:
        methods_str = os.getenv("ENABLED_PAYMENT_METHODS", "paypal,bitcoin,bank,crypto")
        methods = methods_str.split(",")
        
        # Move payment_methods_map dictionary before it's used
        payment_methods_map = {
            "paypal": "💳 PayPal",
            "bitcoin": "₿ Bitcoin",
            "bank": "🏦 Bank Transfer",
            "crypto": "🔒 Crypto"
        }

        return {method: payment_methods_map.get(method.strip().lower(), method) for method in methods}

    def update_product_cache(self, products: list):
        # You can add cache updating logic here
        pass
