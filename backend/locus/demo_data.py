"""
VERDIX Demo Data — Realistic simulated responses for demonstration.
Used when the Locus wallet has insufficient USDC for live API calls.
When funded, VERDIX automatically switches to live Locus wrapped APIs.
"""

import random
import asyncio
from typing import Dict, Any, List, Optional

# Simulated product catalogs by category
PRODUCT_CATALOG: Dict[str, List[Dict[str, Any]]] = {
    "mouse": [
        {
            "name": "Logitech G102 Lightsync Gaming Mouse",
            "price": 18.99,
            "url": "https://www.amazon.com/dp/B08LT9BMPP",
            "seller": "Logitech Official Store",
            "source": "exa",
        },
        {
            "name": "Redragon M908 Impact RGB Gaming Mouse",
            "price": 22.49,
            "url": "https://www.amazon.com/dp/B01LXC1QL0",
            "seller": "Redragon Direct",
            "source": "exa",
        },
        {
            "name": "SteelSeries Rival 3 Gaming Mouse",
            "price": 19.99,
            "url": "https://www.amazon.com/dp/B07YPHXKFL",
            "seller": "SteelSeries",
            "source": "exa",
        },
        {
            "name": "Boat Gaming Mouse BM200",
            "price": 8.99,
            "url": "https://www.boatlifestyle.com/bm200",
            "seller": "new_seller_98",
            "source": "exa",
        },
        {
            "name": "Razer DeathAdder Essential",
            "price": 24.99,
            "url": "https://www.razer.com/gaming-mice/razer-deathadder-essential",
            "seller": "Razer Inc.",
            "source": "exa",
        },
    ],
    "headphones": [
        {
            "name": "JBL Tune 510BT Wireless Headphones",
            "price": 29.95,
            "url": "https://www.jbl.com/wireless-headphones/TUNE510BT.html",
            "seller": "JBL Official",
            "source": "exa",
        },
        {
            "name": "Sony WH-CH520 Wireless Headphones",
            "price": 38.00,
            "url": "https://electronics.sony.com/audio/headphones/all-headphones/p/whch520-l",
            "seller": "Sony Electronics",
            "source": "exa",
        },
        {
            "name": "Boat Rockerz 450 Pro",
            "price": 14.99,
            "url": "https://www.boatlifestyle.com/rockerz450pro",
            "seller": "BoatOfficial",
            "source": "exa",
        },
        {
            "name": "Logitech Zone Vibe 100",
            "price": 49.99,
            "url": "https://www.logitech.com/zone-vibe-100",
            "seller": "Logitech Store",
            "source": "exa",
        },
    ],
    "keyboard": [
        {
            "name": "Redragon K552 Mechanical Keyboard",
            "price": 27.99,
            "url": "https://www.amazon.com/dp/B016MAK38U",
            "seller": "Redragon Direct",
            "source": "exa",
        },
        {
            "name": "Logitech K380 Multi-Device Keyboard",
            "price": 29.99,
            "url": "https://www.logitech.com/k380",
            "seller": "Logitech Official Store",
            "source": "exa",
        },
        {
            "name": "Royal Kludge RK61 60% Keyboard",
            "price": 42.99,
            "url": "https://rkgaming.com/rk61",
            "seller": "RKGaming",
            "source": "exa",
        },
    ],
    "default": [
        {
            "name": "Generic Product A - Premium Edition",
            "price": 29.99,
            "url": "https://example.com/product-a",
            "seller": "TechStore Official",
            "source": "exa",
        },
        {
            "name": "Generic Product B - Budget Pick",
            "price": 14.99,
            "url": "https://example.com/product-b",
            "seller": "ValueMart",
            "source": "exa",
        },
        {
            "name": "Generic Product C - Clearance",
            "price": 9.99,
            "url": "https://example.com/product-c",
            "seller": "new_seller_42",
            "source": "exa",
        },
    ],
}


def _detect_category(query: str) -> str:
    """Detect product category from search query."""
    q = query.lower()
    for keyword in ["mouse", "mice"]:
        if keyword in q:
            return "mouse"
    for keyword in ["headphone", "headset", "earphone", "earbuds"]:
        if keyword in q:
            return "headphones"
    for keyword in ["keyboard", "keycap"]:
        if keyword in q:
            return "keyboard"
    return "default"


async def demo_search(query: str, num_results: int = 5) -> Dict[str, Any]:
    """Simulate an Exa search with realistic delay and product data."""
    await asyncio.sleep(random.uniform(0.3, 0.8))
    category = _detect_category(query)
    products = PRODUCT_CATALOG.get(category, PRODUCT_CATALOG["default"])
    results = [
        {
            "title": p["name"],
            "name": p["name"],
            "url": p["url"],
            "price": p["price"],
            "seller": p["seller"],
            "source": p["source"],
        }
        for p in products[:num_results]
    ]
    return {
        "data": {"results": results},
        "cost": 0.0100,
    }


# Negotiation response templates
SELLER_RESPONSES = {
    "budget": (
        "Thank you for your interest! I understand you're looking for the best value. "
        "As a returning customer, I can offer a 10% discount, bringing the price down to "
        "${final_price:.2f}. This is our best price for this item, and it includes "
        "our standard warranty. Would you like to proceed?"
    ),
    "balanced": (
        "We appreciate your loyalty as a returning customer! I'd be happy to offer you "
        "a courtesy discount. I can bring the price down to ${final_price:.2f}, which is "
        "a {pct:.0f}% savings. Additionally, I can include free expedited shipping. "
        "This is a limited-time offer — shall we finalize?"
    ),
    "premium": (
        "Welcome back, valued customer! For our premium buyers, I have a special bundle offer. "
        "I can offer the product at ${final_price:.2f} — that's {pct:.0f}% off — and I'll include "
        "an extended 2-year warranty plus priority support. This exclusive deal reflects "
        "your VIP status with us."
    ),
}

BUYER_RESPONSES = {
    "budget": (
        "I appreciate the offer at ${seller_price:.2f}, but given my budget constraints "
        "and the current market prices, I'd like to counter at ${counter:.2f}. "
        "I've been a loyal customer and I've seen similar products at lower prices. "
        "Can we meet at ${final_price:.2f}?"
    ),
    "balanced": (
        "That's a reasonable offer. I've checked comparable products and ${seller_price:.2f} "
        "is fair with the free shipping. I'll accept at ${final_price:.2f} — that works "
        "for both of us. Let's proceed with the purchase."
    ),
    "premium": (
        "The bundle offer is attractive. With the extended warranty and priority support "
        "included at ${final_price:.2f}, that represents good value for a premium purchase. "
        "I'd like to finalize this deal. Please proceed with the order at the agreed price."
    ),
}


async def demo_ai_chat(
    system: str,
    user: str,
    model: str = "gpt-4o-mini",
    params: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Simulate an OpenAI chat call with realistic negotiation responses."""
    await asyncio.sleep(random.uniform(0.5, 1.2))

    mode = "balanced"
    original_price = 0.0
    if params:
        mode = params.get("mode", mode)
        original_price = float(params.get("original_price", 0.0))

    # Determine if this is a seller or buyer response
    is_seller = system.lower().strip().startswith("you are a seller")

    if is_seller:
        # Generate seller response
        discount = {"budget": 0.10, "balanced": 0.12, "premium": 0.08}
        pct = discount.get(mode, 0.10)
        # Extract price from user message
        import re
        prices = re.findall(r"[\$₹]?\s*(\d+(?:,\d{3})*(?:\.\d+)?)", user)
        orig = 25.0
        if prices:
            try:
                orig = float(prices[-1].replace(",", ""))
            except ValueError:
                pass
        final = round(orig * (1 - pct), 2)
        text = SELLER_RESPONSES.get(mode, SELLER_RESPONSES["balanced"]).replace(
            "${final_price:.2f}", f"${final:.2f}"
        ).replace("{pct:.0f}", f"{pct * 100:.0f}")
        return {"output": text, "cost": 0.0015}
    else:
        # Generate buyer response
        if original_price > 0:
            extra = {"budget": 0.15, "balanced": 0.12, "premium": 0.08}
            pct = extra.get(mode, 0.12)
            seller_price = original_price * 0.90
            counter = original_price * (1 - pct - 0.02)
            final = round(original_price * (1 - pct), 2)
            text = BUYER_RESPONSES.get(mode, BUYER_RESPONSES["balanced"])
            text = text.replace("${seller_price:.2f}", f"${seller_price:.2f}")
            text = text.replace("${counter:.2f}", f"${counter:.2f}")
            text = text.replace("${final_price:.2f}", f"${final:.2f}")
            return {"output": text, "cost": 0.0015}
        else:
            return {
                "output": "I'd like to accept this offer and proceed with the purchase at the discussed price.",
                "cost": 0.0010,
            }


async def demo_balance() -> Dict[str, Any]:
    """Return a simulated wallet balance for demo purposes."""
    return {
        "data": {
            "wallet_address": "0x043d82f4c96d2c13a22d5667f5ebb53a67bcc364",
            "chain": "base",
            "usdc_balance": "50.00",
        },
        "cost": 0.0,
        "balance": 50.0,
    }
