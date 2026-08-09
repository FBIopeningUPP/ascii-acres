from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, Static
from state import game_state

class BarnScreen(ModalScreen):
    CSS = """
    BarnScreen { align: center middle; background: rgba(0, 0, 0, 0.7); }
    #barn-dialog { width: 60; height: 25; background: $surface; border: thick$accent; padding: 1 2;}
    .animal-row { height: 3; align: left middle; }
    """

    BINDINGS = [("escape", "close_barn", "Close Barn")]

    def compose(self) -> ComposeResult:
        with Vertical(id="barn-dialog"):
            yield Static("🏚️ Welcome to the Barn! (Press ESC to exit)\n")
        
            if not game_state.barn_animals:
                yield Static("It is empty in here! Buy animals in the shop.")
            else:
                for idx, animal in enumerate(game_state.barn_animals):
                    with Horizontal(classes="animal-row"):
                        status = "✅ Fed" if animal["fed_today"] else "❌ Hungry"
                        yield Static(f"{animal['emoji']} {animal['name']} ({status})", classes="animal-lbl")

                        if not animal["fed_today"]:
                            yield Button("Feed", id=f"feed_{idx}", variant="primary")
                        else:
                            yield Button(f"Collect {animal['product_name']}", id=f"collect_{idx}", variant="success")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        action, idx_str = event.button.id.split("_")
        idx = int(idx_str)
        animal = game_state.barn_animals[idx]

        if action == "feed":
            animal["fed_today"] = True
            self.app.notify(f"Fed the {animal['name']}!")
            self.app.pop_screen()
            self.app.push_screen(BarnScreen())

        elif action == "collect":
            if animal["fed_today"]:
                game_state.inventory_animal_products[animal["product"]] += 1
                animal["fed_today"] = False
                self.app.notify(f"Collected 1 {animal['product_name']}!")
                self.app.pop_screen()
                self.app.push_screen(BarnScreen())

    def action_close_barn(self) -> None:
        self.app.pop_screen()