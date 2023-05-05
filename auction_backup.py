
import random # Import the random library for generating random numbers
import Tkinter as tk # Import the Tkinter library for creating the GUI
import tkMessageBox # Import tkMessageBox for displaying message boxes
import ttk # Import the ttk module for themed widgets

class NameEntryWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self) # Initialize the Tkinter window
        self.geometry("300x200") # Set the window geometry
        self.title("Enter Your Name") # Set the window title

        # Create and pack the name label
        self.name_label = tk.Label(self, text="Enter your name:")
        self.name_label.pack()

        # Create and pack the name entry field
        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        # Create and pack the submit button with the submit_name function as its command
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_name)
        self.submit_button.pack()

    # Function to submit the name and start the game
    def submit_name(self):
        user_name = self.name_entry.get()  # Get the entered name
        if user_name:  # If a name is entered
            self.destroy()  # Close the name entry window
            main(user_name)  # Call the main function with the entered name as an argument


# Define the SHOP_INVENTORY dictionary to store the available items and their prices and quantities
SHOP_INVENTORY = {
"Water": {"price": 5, "quantity": 10},
"Meat": {"price": 10, "quantity": 10},
"Bread": {"price": 7, "quantity": 10},
"Cloth": {"price": 8, "quantity": 10},
"Fire": {"price": 6, "quantity": 10}
}

# Define the Player class for managing player data
class Player:
    def init(self, name, money):
        self.name = name # Set the player's name
        self.money = money # Set the player's money
        # Initialize the player's items with random quantities
        self.items = {
            "Water": random.randint(4, 10),
            "Meat": random.randint(1, 3),
            "Bread": random.randint(2, 5),
            "Cloth": random.randint(1, 3),
            "Fire": random.randint(2, 5),
        }
        # Function to bid an amount of money
    def bid(self, amount):
        if amount <= self.money:  # Check if the player has enough money to bid
            self.money -= amount  # Subtract the bid amount from the player's money
            return amount  # Return the bid amount
        else:
            return 0  # Return 0 if the player does not have enough money to bid

    # Function to add an item to the player's inventory
    def add_item(self, item):
        self.items[item] += 1  # Increase the item count by 1

    # Function to consume items and check if the player is still alive
    def consume_items(self):
        if self.money <= 0:  # Check if the player has no money left
            return False

        if self.items["Water"] > 0:  # Check if the player has any water
            self.items["Water"] -= 1  # Consume one unit of water
        else:
            return False  # Return False if the player has no water left

        if self.items["Meat"] > 0:  # Check if the player has any meat
            self.items["Meat"] -= 0.5  # Consume half a unit of meat
        elif self.items["Bread"] > 0:  # Check if the player has any bread
            self.items["Bread"] -= 1  # Consume one unit of bread
        else:
            return False  # Return False if the player has no meat or bread left

        if self.items["Fire"] > 0:  # Check if the player has any fire
            self.items["Fire"] -= 1  # Consume one unit of fire
        elif self.items["Cloth"] > 0:  # Check if the player has any cloth
            self.items["Cloth"] -= 0.5  # Consume half a unit of cloth
        else:
            return False  # Return False if the player has no fire or cloth left

        return True  # Return True if the player is still alive

    # Function to increase the player's money by a specified amount
    def increase_money(self, amount):
        self.money += amount  # Add the amount to the player's money

    # Function to buy an item at a specified price
    def buy_item(self, item, price):
        if self.money >= price:  # Check if the player has enough money to buy the item
            self.money -= price  # Subtract the item price from the player's money
            self.items[item] += 1  # Add the item to the player's inventory
            return True  # Return True if the item was bought
        else:
            return False  # Return False if the player does not have enough money to buy the item

# Function to handle the auction process
def auction(players, user_bid, item_to_auction, starting_bid):
    highest_bid = starting_bid # Initialize the highest bid variable
    highest_bidder = None # Initialize the highest bidder variable

    bids = {}  # Initialize the bids dictionary to store player bids

    # Loop through all the players except the user
    for player in players[1:]:
        item_count = player.items[item_to_auction]  # Get the player's item count for the item to auction
        if item_count < 2:  # Check if the player has less than two of the item
            max_bid = int(player.money / 2) + 1  # Set the maximum bid to half of the player's money plus one
        else:
            max_bid = int(player.money / 2)  # Set the maximum bid to half of the player's money

        # Place a random bid for the player between the starting bid and the player's maximum bid
        bid_amount = player.bid(random.randint(starting_bid, min(player.money, max_bid)))
        if bid_amount > highest_bid:  # Check if the player's bid is the highest bid
            highest_bid = bid_amount  # Set the highest bid to the player's bid
            highest_bidder = player  # Set the highest bidder to the current player
        bids[player.name] = bid_amount  # Add the player's bid to the bids dictionary

    # Place the user's bid
    user_bid_amount = players[0].bid(user_bid)
    bids[players[0].name] = user_bid_amount  # Add the user's bid to the bids dictionary

    if user_bid_amount > highest_bid:  # Check if the user's bid is the highest bid
        highest_bid = user_bid_amount  # Set the highest bid to the user's bid
        highest_bidder = players[0]  # Set the highest bidder to the user

    if highest_bidder:  # Check if there is a highest bidder
        highest_bidder.add_item(item_to_auction)  # Add the auction item to the highest bidder's inventory
        return highest_bidder.name, highest_bid, item_to_auction, bids  # Return the auction results


# Class to create the game window and handle the game logic
class GameWindow(tk.Tk):
    def init(self, players):
        tk.Tk.init(self) # Initialize the Tkinter window
        self.geometry("500x500") # Set the window size
        self.players = players # Store the list of players
        self.round = 1 # Initialize the game round variable
        self.title("Auction Game") # Set the window title
        self.countdown = 30 # Initialize the countdown variable

        # Create and display the round label
        self.round_label = tk.Label(self, text="Round {}".format(self.round))
        self.round_label.pack()

        # Create and display the item label
        self.item_label = tk.Label(self, text="")
        self.item_label.pack()

        # Create and display the user bid label
        self.user_bid_label = tk.Label(self, text="Enter your bid:")
        self.user_bid_label.pack()

        # Create and display the user bid entry
        self.user_bid_entry = tk.Entry(self)
        self.user_bid_entry.pack()

        # Create and display the bid button
        self.bid_button = tk.Button(self, text="Submit Bid", command=self.submit_bid, state="disabled")
        self.bid_button.pack()

        # Create and display the timer label
        self.timer_label = tk.Label(self, text="")
        self.timer_label.pack()

        # Create and display the result label
        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

        # Create and display the bids label
        self.bids_label = tk.Label(self, text="Bids:\n")
        self.bids_label.pack()

        # Create and display the inventory label
        self.inventory_label = tk.Label(self, text="")
        self.inventory_label.pack()

        # Create and display the quit button
        self.quit_button = tk.Button(self, text="Quit", command=self.quit_game)
        self.quit_button.pack(side=tk.BOTTOM)

        # Create a label for each player to display their name and money
        self.money_labels = []
        for player in self.players:
            label_text = "{}: ${}".format(player.name, player.money)
            label = tk.Label(self, text=label_text)
            label.pack()
            self.money_labels.append(label)

        # Create a label for each player to display their inventory
        self.inventory_labels = []
        for player in self.players:
            label = tk.Label(self, text="")
            label.pack()
            self.inventory_labels.append(label)

        self.timer_id = None  # Initialize the timer ID variable

        self.start_round()  # Start the first round
        self.update_inventory()  # Update the players' inventory

    # Function to quit the game
    def quit_game(self):
        if tkMessageBox.askokcancel("Quit", "Do you want to quit the game?"):
            self.destroy()  # Close the game window

    # Function to start a new round
    def start_round(self):
        self.update_inventory()  # Update the players' inventory
        self.item_to_auction = random.choice(["Water", "Meat", "Bread", "Cloth", "Fire"]) # Randomly select an item to auction
        self.item_label.config(text="Auction Item: {}".format(self.item_to_auction)) # Display the auction item
        self.user_bid_entry.delete(0, 'end')  # Clear the user bid entry field
        self.bid_button.config(state="normal")  # Enable the bid button

        self.countdown = 30  # Reset the countdown timer
        self.timer_label.config(text="Time remaining: {} seconds".format(self.countdown))  # Update the timer label

        # Cancel any pending calls to update_timer()
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)

        self.timer_id = self.after(1000, self.update_timer)  # Schedule the timer to update every second

    # Function to update the countdown timer
    def update_timer(self):
        self.countdown -= 1  # Decrement the countdown timer
        self.timer_label.config(text="Time remaining: {} seconds".format(self.countdown))  # Update the timer label
        if self.countdown == 0:  # Check if the countdown reached zero
            self.submit_bid()  # Automatically submit the user's bid
        else:
            self.timer_id = self.after(1000, self.update_timer)  # Schedule the timer to update again in one second

    # Function to submit the user's bid and handle the auction results
    def submit_bid(self):
        self.round += 1  # Increment the game round
        self.round_label.config(text="Round {}".format(self.round))  # Update the round label
        if self.bid_button['state'] == "normal":
            self.bid_button.config(state="disabled")  # Disable the bid button

            user_bid = int(self.user_bid_entry.get() or 0)  # Get the user's bid from the entry field
            winner_name, highest_bid, item_won, bids = auction(self.players, user_bid, self.item_to_auction, 1)  # Conduct the auction

            bid_text = "Bids:\n"
            for player_name, bid_amount in bids.items():
                bid_text += "{}: {}    ".format(player_name, bid_amount)

            self.bids_label.config(text=bid_text)  # Update the bids label with the auction results

            self.result_label.config(text="{} won the auction for {} with a bid of {}.".format(winner_name, item_won, highest_bid))  # Update the result label with the auction winner

            if self.timer_id is not None:
                self.after_cancel(self.timer_id)  # Cancel any pending calls to update_timer()

            game_status, _ = self.update_game_status()  # Update the game status
            if game_status == "lost":
                self.result_label.config(text="You lost! You survived {} rounds.".format(self.round - 1))
                self.bid_button.config(state="disabled")
                self.user_bid_entry.config(state="disabled")
            elif game_status == "won":
                self.result_label.config(text="You won the game!")
                self.bid_button.config(state="disabled")
                self.user_bid_entry.config(state="disabled")
            else:
                for player in self.players:
                    player.increase_money(10)  # Give each player 10 money at the end of the round
                for i, player in enumerate(self.players):
                    label_text = "{}: ${}".format(player.name, player.money)
                    self.money_labels[i].config(text=label_text)  # Update the money labels
                self.update_inventory()  # Update the players' inventory
                self.start_round()  # Start a new round

    # Function to update the game status and check if the game has ended
    def update_game_status(self):
        user_alive = self.players[0].consume_items() # Check if the user has enough items to consume
        robot_players_alive = sum([player.consume_items() for player in self.players[1:]]) # Check how many robot players have enough items to consume
        for i, player in enumerate(self.players):
            label_text = "{}: ${}".format(player.name, player.money)
            self.money_labels[i].config(text=label_text) # Update the money labels
        
        if not user_alive:  # If the user has no items left to consume, they have lost the game
            return "lost", None

        if robot_players_alive == 0:  # If all robot players have no items left to consume, the user has won the game
            return "won", None

        return "ongoing", robot_players_alive  # If the game has not ended, return the "ongoing" status and the number of robot players still alive

    # Function to update the players' inventory display
    def update_inventory(self):
        for i, player in enumerate(self.players):
            inventory_text = "{}'s Inventory:\n".format(player.name)  # Start the inventory text with the player's name
            for item, count in player.items.items():  # Iterate over the player's items
                inventory_text += "{}: {}    ".format(item, count)  # Add each item and its count to the inventory text
            self.inventory_labels[i].config(text=inventory_text)  # Update the inventory labels with the new inventory text

# Main function that sets up the game
def main(user_name):
    players = [
        Player(user_name, 100), # Create the user player with the provided name and 100 money
        Player("Angela", 100), # Create a robot player named Angela with 100 money
        Player("Tina", 100), # Create a robot player named Tina with 100 money
        Player("Eric", 100) # Create a robot player named Eric with 100 money
    ]
    app = GameWindow(players)  # Create the game window with the players
    app.mainloop()  # Run the game window main loop



if __name__ == "__main__":
    name_entry_app = NameEntryWindow() # Create the name entry window
    name_entry_app.mainloop() # Run the name entry window main loop
