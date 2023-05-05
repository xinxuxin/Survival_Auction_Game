# Auction Game
Auction Game is a simple Python-based game built with the Tkinter library. The game simulates an auction where you compete against computer-controlled players to bid for items. The goal of the game is to outlast your opponents by managing your resources effectively.

## Features
User-friendly graphical interface using Tkinter
Four computer-controlled players with different bidding strategies
Randomly generated auction items
Countdown timer for each round
Real-time updates of player money and inventory
End game conditions: win when all opponents are out, lose when you run out of resources

## Requirements
Python 2.7 or 3.x
Tkinter library (should be installed by default with Python)

## How to Run
Clone this repository or download the source code as a ZIP file and extract it.
Open a terminal or command prompt, navigate to the directory containing the source code.
Run the following command:
python <filename.py>
Replace <filename.py> with the name of the Python file containing the game code.

The game window will appear. Enter your name and start playing!

## How to Play
Enter your name and click the "Submit" button.
The game window will appear, showing the auction item for the current round, your bid input, and the remaining time.
Enter your bid for the auction item and click the "Submit Bid" button. Be aware that you only have 30 seconds to place your bid.
After each round, the game will display the winning bidder and their bid amount. Players will also receive additional money.
The game continues until you or all computer-controlled players run out of resources.

## Game Rules
Each player starts with 100 money and a random amount of each item.
Players consume items each round to stay alive:
1 Water
0.5 Meat or 1 Bread
1 Fire or 0.5 Cloth
If a player cannot consume the required items, they are out of the game.
Each player earns 10 money after every round.
The game ends when you run out of resources (loss) or when all opponents run out of resources (win).

## License
This project is open-source and available under the MIT License.