from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static
from textual.reactive import reactive

from widgets import HUD, FarmGrid, Toolbar, Plot
from shop import ShopScreen
from state import game_state
from crops import CROPS
from barn import BarnScreen

class ASCIIAcresApp(App):
    TITLE = "ASCII Acres"
    
    selected_tool = reactive("hoe")
    selected_seed = reactive("parsnip")
    money_tracker = reactive(game_state.money) 
    
    CSS = """
    Screen { background: #1e1e2e; }
    
    #sidebar {
        width: 25%; height: 100%; dock: left;
        padding: 2; background: #181825; 
        border-right: thick #89b4fa; color: #cdd6f4;
    }

    #sidebar Static { margin-bottom: 1; }
    
    #main-farm { 
        width: 75%; height: 100%; 
        align: center middle; background: #1e1e2e; 
    }
    
    FarmGrid {
        layout: grid; grid-size: 5 5; grid-columns: 6; grid-rows: 3;
        grid-gutter: 1; width: 40; height: 20;
        border: double #a6e3a1; padding: 1; background: #313244;
    }
    
    Plot { 
        width: 100%; height: 100%; content-align: center middle; 
        background: #45475a; border: solid #585b70;
    }
    
    Plot:hover { background: #89b4fa; border: solid #b4befe; }
    
    Toolbar { 
        height: 5; width: 100%; margin-top: 3; 
        align: center middle; 
    }
    
    Button { margin: 0 1; min-width: 14; }
    Select { width: 30; margin: 0 1; }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("s", "shop", "Open Shop"),
        ("n", "next_day", "Next Day"),
        ("ctrl+s", "save_game", "Save Game"),
        ("b", "barn", "Open Barn")
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Horizontal(
            Vertical(HUD(), id="sidebar"),
            Vertical(FarmGrid(), Toolbar(), id="main-farm")
        )
        yield Footer()

    def watch_money_tracker(self, old_val: int, new_val: int) -> None:
        self.query_one("#hud-money", Static).update(f"💰 Money: ${new_val}")

    def action_shop(self) -> None:
        self.push_screen(ShopScreen())

    def action_barn(self) -> None:
        """Opens the Barn Screen."""
        self.push_screen(BarnScreen())

    def action_next_day(self) -> None:
        game_state.advance_time()
        self.query_one("#hud-day", Static).update(f"📅 {game_state.season}, Day {game_state.day}")
        self.query_one("#hud-weather", Static).update(f"☁️ Weather: {game_state.weather}")

        for plot in self.query(Plot):
            if plot.state == "planted":
                if game_state.season not in CROPS[plot.crop_id].seasons:
                    plot.state = "dirt"
                    plot.watered = False
                    plot.crop_id = ""
                    continue

                if plot.watered:
                    plot.days_grown += 1
                    if plot.days_grown >= CROPS[plot.crop_id].growth_days:
                        plot.state = "ready"

            plot.watered = (game_state.weather == "Rainy")

        for animal in game_state.barn_animals:
            if animal.get("fed_today", False):
                animal["has_product"] = True
                animal["fed_today"] = False

        self.notify(f"Good morning! It is now {game_state.season} Day {game_state.day}.")

    def action_save_game(self) -> None:
        """Saves the game when ctrl+s is presed."""
        from widgets import Plot
        grid_data = []
        for plot in self.query(Plot):
            grid_data.append({
                "state": plot.state,
                "watered": plot.watered,
                "crop_id": plot.crop_id,
                "days_grown": plot.days_grown
            })

        game_state.grid_state = grid_data
        game_state.save()
        self.notify("Game saved successfully!")