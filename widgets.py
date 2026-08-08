from textual.containers import Container, Horizontal
from textual.widgets import Static, Button
from textual.reactive import reactive
from state import game_state
from crops import CROPS

class Plot(Static):
    state = reactive("dirt")
    watered = reactive(False)
    crop_id = ""
    days_grown = 0
    
    def on_mount(self) -> None:
        self.update_display()
        
    def watch_state(self, old_state: str, new_state: str) -> None:
        self.update_display()
        
    def watch_watered(self, old_val: bool, new_val: bool) -> None:
        self.update_display()
        
    def update_display(self) -> None:
        bg = "🟦 " if self.watered else ""
        
        if self.state == "dirt":
            self.update(f"{bg}🟫")
        elif self.state == "tilled":
            self.update(f"{bg}〰️")
        elif self.state == "planted":
            self.update(f"{bg}🌱")
        elif self.state == "ready":
            emoji = CROPS[self.crop_id].emoji if self.crop_id else "🌾"
            self.update(f"{bg}{emoji}")
            
    def on_click(self) -> None:
        tool = self.app.selected_tool
        
        if tool == "hoe" and self.state == "dirt":
            self.state = "tilled"
        elif tool == "seed" and self.state == "tilled":
            if game_state.inventory_seeds.get("parsnip", 0) > 0:
                self.state = "planted"
                self.crop_id = "parsnip"
                self.days_grown = 0
                game_state.inventory_seeds["parsnip"] -= 1
                self.app.query_one("#inv-seeds", Static).update(f"- 🫘 Seeds: {game_state.inventory_seeds['parsnip']}")
            else:
                self.app.notify("You are out of seeds! Buy more in the shop.", severity="error")
        elif tool == "water" and self.state in ["tilled", "planted"]:
            self.watered = True
        elif tool == "scythe" and self.state == "ready":
            self.state = "dirt"
            self.watered = False
            game_state.inventory_crops[self.crop_id] = game_state.inventory_crops.get(self.crop_id, 0) + 1
            self.app.query_one("#inv-crops", Static).update(f"- 🌾 Crops: {game_state.inventory_crops[self.crop_id]}")
            self.app.notify(f"Harvested a {CROPS[self.crop_id].name}!")
            self.crop_id = ""
        else:
            self.app.notify(f"Can't use the {tool} here!", severity="warning")

class FarmGrid(Container):
    def compose(self):
        for _ in range(25):
            yield Plot()

class Toolbar(Horizontal):
    def compose(self):
        yield Button("⛏️ Hoe", id="btn-hoe", variant="primary")
        yield Button("🫘 Seeds", id="btn-seed", variant="default")
        yield Button("💧 Water", id="btn-water", variant="default")
        yield Button("🪝 Scythe", id="btn-scythe", variant="default")
        
    def on_button_pressed(self, event: Button.Pressed) -> None:
        for btn in self.query(Button):
            btn.variant = "default"
        event.button.variant = "primary"
        
        tool_id = event.button.id
        if tool_id == "btn-hoe":
            self.app.selected_tool = "hoe"
        elif tool_id == "btn-seed":
            self.app.selected_tool = "seed"
        elif tool_id == "btn-water":
            self.app.selected_tool = "water"
        elif tool_id == "btn-scythe":
            self.app.selected_tool = "scythe"

class HUD(Static):
    def compose(self):
        yield Static(f"💰 Money: ${game_state.money}", id="hud-money")
        yield Static(f"☀️ Day: {game_state.day}", id="hud-day")
        yield Static("\n🎒 Inventory:", id="hud-inventory-title")
        yield Static(f"- 🫘 Seeds: {game_state.inventory_seeds.get('parsnip', 0)}", id="inv-seeds")
        yield Static(f"- 🌾 Crops: {game_state.inventory_crops.get('parsnip', 0)}", id="inv-crops")