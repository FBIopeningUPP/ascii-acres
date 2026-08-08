from dataclasses import dataclass
from typing import List

@dataclass
class CropData:
    name: str
    emoji: str
    seed_emoji: str
    buy_price: int
    sell_price: int 
    growth_days: int
    seasons: List[str]

CROPS = {
    "parsnip": CropData("Parsnip", "🌾", "🫘", 10, 25, 4, ["Spring"]),
    "potato": CropData("Potato", "🥔", "🥔", 30, 60, 6, ["Spring"]),
    "strawberry": CropData("Strawberry", "🍓", "🍓", 100, 250, 8, ["Spring"]),

    "tomato": CropData("Tomato", "🍅", "🍅", 50, 100, 11, ["Summer"]),
    "corn": CropData("Corn", "🌽", "🌽", 150, 300, 14, ["Summer", "Fall"]),
    "sunflower": CropData("Sunflower", "🌻", "🌻", 200, 400, 8, ["Summer"]),

    "pumpkin": CropData("Pumpkin", "🎃", "🎃", 100, 320, 13, ["Fall"]),
    "eggplant": CropData("EggPlant", "🍆", "🍆", 20, 50, 5, ["Fall"]),
    "grapes": CropData("Grapes", "🍇", "🍇", 60, 120, 10, ["Fall"]),
}