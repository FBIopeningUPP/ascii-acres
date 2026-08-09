from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, Static
from state import game_state
from crops import CROPS

class ShopScreen(ModalScreen):
    CSS = """
    ShopScreen { align: center middle; background: rgba(0, 0, 0, 0.7); }
    #shop-dialog { width: 70; height: 80%; background: $surface; border: thick $accent; padding: 1 2; overflow-y: auto; }
    .shop-row { height: 3; align: left middle; }
    .shop-item-name { width: 35; }
    """
    
    BINDINGS = [("escape", "close_shop", "Close Shop")]

    def compose(self) -> ComposeResult:
        with Vertical(id="shop-dialog"):
            yield Static("🛒 Welcome to the Shop! (Press ESC to exit)\n")
            yield Static(f"Your Money: ${game_state.money}\n", id="shop-money")
            
            yield Static("--- Buy Seeds ---")
            for crop_id, crop in CROPS.items():
                with Horizontal(classes="shop-row"):
                    yield Static(f"{crop.seed_emoji} {crop.name} Seeds (-${crop.buy_price})", classes="shop-item-name")
                    yield Button("Buy", id=f"buy_seed_{crop_id}", variant="success")
                    
            yield Static("\n--- Buy Animals ---")
            with Horizontal(classes="shop-row"):
                yield Static("🐔 Chicken (-$500)", classes="shop-item-name")
                yield Button("Buy", id="buy_animal_chicken", variant="success")
            with Horizontal(classes="shop-row"):
                yield Static("🐮 Cow (-$1500)", classes="shop-item-name")
                yield Button("Buy", id="buy_animal_cow", variant="success")

            yield Static("\n--- Blacksmith Upgrades ---")
            with Horizontal(classes="shop-row"):
                status = "✅ Purchased" if game_state.steel_tools else "❌ Not Owned"
                yield Static(f"🚿 Steel Watering Can (-$5000) [{status}]", classes="shop-item-name")
                if not game_state.steel_tools:
                    yield Button("Upgrade", id="buy_upgrade_steel", variant="success")
            
            yield Static("\n--- Sell Crops & Products ---")
            for crop_id, crop in CROPS.items():
                with Horizontal(classes="shop-row"):
                    yield Static(f"{crop.emoji} {crop.name} (+${crop.sell_price})", classes="shop-item-name")
                    count = game_state.inventory_crops.get(crop_id, 0)
                    yield Button(f"Sell (Have: {count})", id=f"sell_crop_{crop_id}", variant="warning")
            
            with Horizontal(classes="shop-row"):
                yield Static("🥚 Egg (+$20)", classes="shop-item-name")
                count = game_state.inventory_animal_products.get("egg", 0)
                yield Button(f"Sell (Have: {count})", id="sell_product_egg", variant="warning")
                
            with Horizontal(classes="shop-row"):
                yield Static("🥛 Milk (+$50)", classes="shop-item-name")
                count = game_state.inventory_animal_products.get("milk", 0)
                yield Button(f"Sell (Have: {count})", id="sell_product_milk", variant="warning")
                    
            yield Button("Close Shop", id="btn_close", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "btn_close":
            self.app.pop_screen()
            return
            
        parts = button_id.split("_")
        action = parts[0] 
        category = parts[1] 
        item_id = parts[2]
        
        if action == "buy":
            if category == "seed":
                crop = CROPS[item_id]
                if game_state.money >= crop.buy_price:
                    game_state.money -= crop.buy_price
                    game_state.inventory_seeds[item_id] = game_state.inventory_seeds.get(item_id, 0) + 1
                    self.app.notify(f"Bought 1 {crop.name} seed!")
                else:
                    self.app.notify("Not enough money!", severity="error")
                    
            elif category == "animal":
                price = 500 if item_id == "chicken" else 1500
                if game_state.money >= price:
                    game_state.money -= price
                    if item_id == "chicken":
                        game_state.barn_animals.append({"type": "chicken", "name": "Chicken", "emoji": "🐔", "product": "egg", "product_name": "Egg", "fed_today": False})
                    else:
                        game_state.barn_animals.append({"type": "cow", "name": "Cow", "emoji": "🐮", "product": "milk", "product_name": "Milk", "fed_today": False})
                    self.app.notify(f"Bought a {item_id}!")
                else:
                    self.app.notify("Not enough money!", severity="error")

            elif category == "upgrade":
                if game_state.money >= 5000:
                    game_state.money -= 5000
                    game_state.steel_tools = True
                    self.app.notify("Upgraded to Steel Watering Can!")
                else:
                    self.app.notify("Not enough money!", severity="error")
                    
        elif action == "sell":
            if category == "crop":
                crop = CROPS[item_id]
                if game_state.inventory_crops.get(item_id, 0) > 0:
                    game_state.inventory_crops[item_id] -= 1
                    game_state.money += crop.sell_price
                    self.app.notify(f"Sold 1 {crop.name}!")
                else:
                    self.app.notify("You don't have any to sell!", severity="error")
                    
            elif category == "product":
                price = 20 if item_id == "egg" else 50
                if game_state.inventory_animal_products.get(item_id, 0) > 0:
                    game_state.inventory_animal_products[item_id] -= 1
                    game_state.money += price
                    self.app.notify(f"Sold 1 {item_id}!")
                else:
                    self.app.notify("You don't have any to sell!", severity="error")
                
        # Update the UI state
        self.app.money_tracker = game_state.money
        
        # refresh the whole shop by quickly popping and pushing it to update the "Have: X" text
        self.app.pop_screen()
        self.app.push_screen(ShopScreen())

    def action_close_shop(self) -> None:
        self.app.pop_screen()