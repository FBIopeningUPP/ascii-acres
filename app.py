from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static
from textual.reactive import reactive

from widgets import HUD, FarmGrid, Toolbar, Plot
from shop import ShopScreen
from state import game_state
from crops import CROPS

class ASCIIAcresApp(App):
    TITLE = "ASCII Acres"
    
    selected_tool = reactive("hoe")
    money_tracker = reactive(game_state.money) 
    
    CSS = """
    Screen { layout: horizontal; }
    
    #sidebar {
        width: 30%; height: 100%; dock: left;
        padding: 1 2; background: $boost; border-right: solid $accent;
    }
    
    #main-farm { width: 70%; height: 100%; align: center middle; }
    
    FarmGrid {
        layout: grid; grid-size: 5 5; grid-columns: 4; grid-rows: 2;
        grid-gutter: 1 2; width: 32; height: 17;
        border: thick $primary; padding: 1; background: $surface;
    }
    
    Plot { width: 100%; height: 100%; content-align: center middle; background: $panel; }
    Plot:hover { background: $accent; color: $text; }
    
    Toolbar { height: 3; width: 45; margin-top: 2; align: center middle; }
    Button { margin: 0 1; }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("s", "shop", "Open Shop"),
        ("n", "next_day", "Next Day")
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
        self.notify("Game and saved succeful")