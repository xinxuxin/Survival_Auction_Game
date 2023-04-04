import random
import Tkinter as tk
import tkMessageBox
import ttk
class NameEntryWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("300x200")
        self.title("Enter Your Name")

        self.name_label = tk.Label(self, text="Enter your name:")
        self.name_label.pack()

        self.name_entry = tk.Entry(self)
        self.name_entry.pack()

        self.submit_button = tk.Button(self, text="Submit", command=self.submit_name)
        self.submit_button.pack()

    def submit_name(self):
        user_name = self.name_entry.get()
        if user_name:
            self.destroy()
            main(user_name)

SHOP_INVENTORY = {
    "Water": {"price": 5, "quantity": 10},
    "Meat": {"price": 10, "quantity": 10},
    "Bread": {"price": 7, "quantity": 10},
    "Cloth": {"price": 8, "quantity": 10},
    "Fire": {"price": 6, "quantity": 10}
}

class Player:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.items = {
            "Water": random.randint(4, 10),
            "Meat": random.randint(1, 3),
            "Bread": random.randint(2, 5),
            "Cloth": random.randint(1, 3),
            "Fire": random.randint(2, 5),
        }

    def bid(self, amount):
        if amount <= self.money:
            self.money -= amount
            return amount
        else:
            return 0

    def add_item(self, item):
        self.items[item] += 1

    def consume_items(self):
        if self.money <= 0:  # Check if the player has no money left
            return False

        if self.items["Water"] > 0:
            self.items["Water"] -= 1
        else:
            return False

        if self.items["Meat"] > 0:
            self.items["Meat"] -= 0.5
        elif self.items["Bread"] > 0:
            self.items["Bread"] -= 1
        else:
            return False

        if self.items["Fire"] > 0:
            self.items["Fire"] -= 1
        elif self.items["Cloth"] > 0:
            self.items["Cloth"] -= 0.5
        else:
            return False

        return True

    def increase_money(self, amount):
        self.money += amount

    def buy_item(self, item, price):
        if self.money >= price:
            self.money -= price
            self.items[item] += 1
            return True
        else:
            return False

def auction(players, user_bid, item_to_auction, starting_bid):
    highest_bid = starting_bid
    highest_bidder = None

    bids={}

    for player in players[1:]:
        item_count = player.items[item_to_auction]
        if item_count < 2:
            max_bid = int(player.money / 2) + 1
        else:
            max_bid = int(player.money / 2)

        bid_amount = player.bid(random.randint(starting_bid, min(player.money, max_bid)))
        if bid_amount > highest_bid:
            highest_bid = bid_amount
            highest_bidder = player
        bids[player.name] = bid_amount

    user_bid_amount = players[0].bid(user_bid)
    bids[players[0].name] = user_bid_amount
    if user_bid_amount > highest_bid:
        highest_bid = user_bid_amount
        highest_bidder = players[0]

    if highest_bidder:
        highest_bidder.add_item(item_to_auction)
        return highest_bidder.name, highest_bid, item_to_auction, bids

class GameWindow(tk.Tk):
    def __init__(self, players):
        tk.Tk.__init__(self)
        self.geometry("500x500")
        self.players = players
        self.round = 1
        self.title("Auction Game")
        self.countdown = 30  # Initialize countdown variable

        self.round_label = tk.Label(self, text="Round {}".format(self.round))
        self.round_label.pack()

        self.item_label = tk.Label(self, text="")
        self.item_label.pack()

        self.user_bid_label = tk.Label(self, text="Enter your bid:")
        self.user_bid_label.pack()

        self.user_bid_entry = tk.Entry(self)
        self.user_bid_entry.pack()

        self.bid_button = tk.Button(self, text="Submit Bid", command=self.submit_bid, state="disabled")
        self.bid_button.pack()

        self.timer_label = tk.Label(self, text="")
        self.timer_label.pack()

        self.result_label = tk.Label(self, text="")
        self.result_label.pack()

        self.bids_label = tk.Label(self, text="Bids:\n")
        self.bids_label.pack()

        self.inventory_label = tk.Label(self, text="")
        self.inventory_label.pack()

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

        self.timer_id = None  # Initialize timer ID variable

        self.start_round()
        self.update_inventory()
        self.update_shop_inventory()


    def quit_game(self):
        if tkMessageBox.askokcancel("Quit", "Do you want to quit the game?"):
            self.destroy()

    def start_round(self):
        self.update_inventory()
        self.item_to_auction = random.choice(["Water", "Meat", "Bread", "Cloth", "Fire"])
        self.item_label.config(text="Auction Item: {}".format(self.item_to_auction))

        self.user_bid_entry.delete(0, 'end')
        self.bid_button.config(state="normal")

        self.countdown = 30
        self.timer_label.config(text="Time remaining: {} seconds".format(self.countdown))

        # Cancel any pending calls to update_timer()
        if self.timer_id is not None:
            self.after_cancel(self.timer_id)

        self.timer_id = self.after(1000, self.update_timer)

    def update_timer(self):
        self.countdown -= 1
        self.timer_label.config(text="Time remaining: {} seconds".format(self.countdown))
        if self.countdown == 0:
            self.submit_bid()
        else:
            self.timer_id = self.after(1000, self.update_timer)

    def submit_bid(self):
        self.round += 1
        self.round_label.config(text="Round {}".format(self.round))
        if self.bid_button['state'] == "normal":
            self.bid_button.config(state="disabled")

            user_bid = int(self.user_bid_entry.get() or 0)
            winner_name, highest_bid, item_won, bids = auction(self.players, user_bid, self.item_to_auction, 1)

            bid_text = "Bids:\n"
            for player_name, bid_amount in bids.items():
                bid_text += "{}: {}    ".format(player_name, bid_amount)

            self.bids_label.config(text=bid_text)

            self.result_label.config(text="{} won the auction for {} with a bid of {}.".format(winner_name, item_won, highest_bid))

            if self.timer_id is not None:
                self.after_cancel(self.timer_id)

            game_status, _ = self.update_game_status()
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
                    player.increase_money(10)
                for i, player in enumerate(self.players):
                    label_text = "{}: ${}".format(player.name, player.money)
                    self.money_labels[i].config(text=label_text)
                self.update_inventory()
                self.start_round()


    def update_game_status(self):
        user_alive = self.players[0].consume_items()
        robot_players_alive = sum([player.consume_items() for player in self.players[1:]])
        for i, player in enumerate(self.players):
            label_text = "{}: ${}".format(player.name, player.money)
            self.money_labels[i].config(text=label_text)

        if not user_alive:
            return "lost", None

        if robot_players_alive == 0:
            return "won", None

        return "ongoing", robot_players_alive

    def update_inventory(self):

        for i, player in enumerate(self.players):
            inventory_text = "{}'s Inventory:\n".format(player.name)
            for item, count in player.items.items():
                inventory_text += "{}: {}    ".format(item, count)
            self.inventory_labels[i].config(text=inventory_text)


def main(user_name):
    players = [
        Player(user_name, 100),
        Player("Angela", 100),
        Player("Tina", 100),
        Player("Eric", 100)
    ]

    app = GameWindow(players)
    app.mainloop()


if __name__ == "__main__":
    name_entry_app = NameEntryWindow()
    name_entry_app.mainloop()
