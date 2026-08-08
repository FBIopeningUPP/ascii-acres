from dataclasses import dataclass

@dataclass
class CropData:
    name: str
    emoji: str
    seed_emoji: str
    buy_price: int
    sell_price: int
    growth_days: int

CROPS = {
    "parsnip": CropData("Parsnip", "🌾", "🫘", buy_price=10, sell_price=25, growth_days=4),
    "potato": CropData("Potato", "🥔", "🥔", buy_price=30, sell_price=60, growth_days=6),
    "pumpkin": CropData("Pumpkin", "🎃", "🎃", buy_price=50, sell_price=150, growth_days=10),
}