class GameState:
    def __init__(self):
        self.money = 100
        self.day = 1
        self.inventory_seeds = {"parsnip": 5}
        self.inventory_crops = {"parsnip": 0}

game_state = GameState()