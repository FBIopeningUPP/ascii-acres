import json
import os
import random

class GameState:
    def __init__(self):
        self.money = 100
        self.day = 1
        self.season = "Spring"
        self.weather = "Sunny"

        self.inventory_seeds = {"parsnip": 5, "potato": 2}
        self.inventory_crops = {}
        self.grid_state = []

        self.inventory_animal_products = {"egg":0, "milk": 0}
        self.barn_animals = []

    def generate_tomorrow_weather(self):
        if random.random() < 0.2:
            self.weather = "Rainy"
        else:
            self.weather = "Sunny"

    def advance_time(self):
        """Move to the next day, handling season changes."""
        self.day += 1
        if self.day > 28:
            self.day = 1
            if self.season == "Spring":
                self.season = "Summer"
            elif self.season == "Summer":
                self.season = "Fall"
            elif self.season == "Fall":
                self.season = "Spring"
        self.generate_tomorrow_weather()

    def save(self):
        data = {
            "money": self.money,
            "day": self.day,
            "season": self.season,
            "weather": self.weather,
            "inventory_seeds": self.inventory_seeds,
            "inventory_crops": self.inventory_crops,
            "grid_state": self.grid_state,
            "inventory_animal_products": self.inventory_animal_products,
            "barn_animals": self.barn_animals
        }
        with open("save_game.json", "w") as f:
            json.dump(data, f)

    def load(self):
        if os.path.exists("save_game.json"):
            with open("save_game.json", "r") as f:
                data = json.load(f)
                self.money = data.get("money", 100)
                self.day = data.get("day", 1)
                self.season = data.get("season", "Spring")
                self.weather = data.get("weather", "Sunny")
                self.inventory_seeds = data.get("inventory_seeds", {"parsnip" : 5, "potato": 2})
                self.inventory_crops = data.get("inventory_crops", {})
                self.grid_state = data.get("grid_state", [])
                self.inventory_animal_products = data.get("inventory_animal_products", {"egg":0, "milk":0})

game_state = GameState()
game_state.load()
