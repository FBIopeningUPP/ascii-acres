from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, Static
from state import game_state
from crops import CROPS

class ShopScreen(ModalScreen):
    CSS = """
    ShopScreen { align: center middle; background: rgba(0, 0, 0, 0.7); }
    #shop-dialog { width: 60; height: 25; background: $surface; border: thick $accent; padding: 1 2; }
    .shop-row { height: 3; align: left middle; }
    .shop-item-name { width: 25; }
    """
    BINDINGS = [
        ("escape", "close_shop", "Close Shop")
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="shop-dialog"):
            yield Static("🛒 Welcome to the Shop! (Press ESC to exit)\n")
            yield Static(f"Your Money: ${game_state.money}\n", id="shop-money")
            
            yield Static("--- Buy Seeds ---")
            for crop_id, crop in CROPS.items():
                with Horizontal(classes="shop-row"):
                    yield Static(f"{crop.seed_emoji} {crop.name} Seeds (-${crop.buy_price})", classes="shop-item-name")
                    yield Button("Buy", id=f"buy_{crop_id}", variant="success")
            
            yield Static("\n--- Sell Crops ---")
            for crop_id, crop in CROPS.items():
                with Horizontal(classes="shop-row"):
                    yield Static(f"{crop.emoji} {crop.name} (+${crop.sell_price})", classes="shop-item-name")
                    count = game_state.inventory_crops.get(crop_id, 0)
                    yield Button(f"Sell (Have: {count})", id=f"sell_{crop_id}", variant="warning")
                    
            yield Button("Close Shop", id="btn_close", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "btn_close":
            self.app.pop_screen()
            return
            
        action, crop_id = button_id.split("_")
        crop = CROPS[crop_id]
        
        if action == "buy":
            if game_state.money >= crop.buy_price:
                game_state.money -= crop.buy_price
                game_state.inventory_seeds[crop_id] = game_state.inventory_seeds.get(crop_id, 0) + 1
                self.app.notify(f"Bought 1 {crop.name} seed!")
            else:
                self.app.notify("Not enough money!", severity="error")
                
        elif action == "sell":
            if game_state.inventory_crops.get(crop_id, 0) > 0:
                game_state.inventory_crops[crop_id] -= 1
                game_state.money += crop.sell_price
                self.app.notify(f"Sold 1 {crop.name}!")
            else:
                self.app.notify("You don't have any to sell!", severity="error")
                
        self.app.money_tracker = game_state.money
        self.query_one("#shop-money", Static).update(f"Your Money: ${game_state.money}\n")
        
        for btn in self.query(Button):
            if btn.id and btn.id.startswith("sell_"):
                cid = btn.id.split("_")[1]
                count = game_state.inventory_crops.get(cid, 0)
                btn.label = f"Sell (Have: {count})"

        self.app.query_one("HUD").refresh_inventory()

    def action_close_shop(self) -> None:
        """Closes The Shop when escape is pressed."""
        self.app.pop_screen()