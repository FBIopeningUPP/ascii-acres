# ASCII Acres 🌾

**ASCII Acres** is a massive-scope, fully-featured terminal-based farming simulator inspired by Stardew Valley, built entirely in Python using the Textual TUI framework. It features a full day/night/season cycle, a dynamic shop, animal husbandry, a 5x5 saveable farming grid, and progressive tool upgrades (like the 3x3 Steel Watering Can).

## Why I Made This
I wanted to challenge myself to build a complex, state-driven game using only terminal UI elements. Most terminal games are very simple, but I wanted to prove that you could create a rich, relaxing, long-form farming game with saving, loading, economy, and dynamic weather, right inside the command line. This project was built for my Macondo submission to push my Python and UI layout skills to the limit!

## How to Use It
1. Clone this repository and navigate into the folder.
2. Install the required dependency (Textual):
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python main.py
   ```
4. **Controls**:
   - `s` - Open the Shop to buy seeds, animals, and tool upgrades.
   - `b` - Open the Barn to feed animals and collect milk/eggs.
   - `n` - Sleep and move to the next day.
   - `ctrl+s` - Save your game.
   - `q` - Quit.

## Visuals
![ASCII Acres Gameplay](image.png)

## AI Usage
ai was mostly used in the ui and all that stuff in the game