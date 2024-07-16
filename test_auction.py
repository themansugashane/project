import numpy as np
import random
import matplotlib.pyplot as plt

class User:
    """Class to represent a user with a secret probability of clicking on an ad."""

    def __init__(self):
        """Generating a probability between 0 and 1 from a uniform distribution."""
        self._probability = np.random.uniform(0, 1)

    def __repr__(self):
        '''User object with secret probability'''
        return f"User(probability={self._probability:.3f})"

    def __str__(self):
        '''User object with a secret likelihood of clicking on an ad'''
        return f"User(probability={self._probability:.3f})"

    def show_ad(self):
        """Returns True to represent the user clicking on an ad or False otherwise."""
        return random.random() < self._probability

class Auction:
    """Class to represent an online second-price ad auction."""
    
    def __init__(self, users, bidders):
        """
        Initializing users, bidders, and dictionary to store balances for each bidder in the auction.
        
        Parameters:
        - users (list): A list of User objects representing the users in the auction.
        - bidders (list): A list of Bidder objects representing the bidders in the auction.
        """
        self.users = users
        self.bidders = bidders
        self.balances = {bidder: 0 for bidder in bidders}
        self.history = []

    def __repr__(self):
        '''Return auction object with users and qualified bidders'''
        return f"Auction(users={len(self.users)}, bidders={len(self.bidders)})"

    def __str__(self):
        '''Return auction object with users and qualified bidders'''
        return f"Auction(users={len(self.users)}, bidders={len(self.bidders)})"

    def execute_round(self):
        """
        Executes a single round of an auction, completing the following steps:
        - random user selection
        - bids from every qualified bidder in the auction
        - selection of winning bidder based on maximum bid
        - selection of actual price (second-highest bid)
        - showing ad to user and finding out whether or not they click
        - notifying winning bidder of price and user outcome and updating balance
        - notifying losing bidders of price.
        """
        
        
        user = random.choice(self.users)
        user_id = self.users.index(user)
        
        
        bids = {bidder: bidder.bid(user_id) for bidder in self.bidders}
        
        
        sorted_bids = sorted(bids.items(), key=lambda x: x[1], reverse=True)
        winner, winning_bid = sorted_bids[0]
        second_price = sorted_bids[1][1] if len(sorted_bids) > 1 else 0
        
        
        clicked = user.show_ad()
        
        
        self.balances[winner] -= second_price
        if clicked:
            self.balances[winner] += 1
        
        
        for bidder, bid in bids.items():
            if bidder == winner:
                bidder.notify(True, second_price, clicked, user_id)
            else:
                bidder.notify(False, second_price, None, user_id)
        
        
        if self.balances[winner] < -1000:
            self.bidders.remove(winner)
            print(f"Bidder {winner} disqualified for bankruptcy.")
        
        # Log the round history
        self.history.append({
            'user_id': user_id,
            'bids': bids,
            'winner': winner,
            'winning_bid': winning_bid,
            'second_price': second_price,
            'clicked': clicked,
            'balances': self.balances.copy()
        })

    def plot_history(self):
        """
        Creates a visual representation of the auction history with multiple subplots.
        """
        fig, axs = plt.subplots(2, 1, figsize=(12, 10))  # 2 rows, 1 column for subplots

        rounds = range(1, len(self.history) + 1)
        prices = [round['second_price'] for round in self.history]
        balances = {bidder: [round['balances'][bidder] for round in self.history]
                    for bidder in self.bidders}

        
        axs[0].plot(rounds, prices, marker='o', linestyle='-', color='blue', label='Winning Price')
        axs[0].set_xlabel('Round')
        axs[0].set_ylabel('Price ($)')
        axs[0].set_title('Winning Prices Over Rounds')
        axs[0].legend()
        axs[0].grid(axis='y')

        
        for bidder, balance in balances.items():
            axs[1].plot(rounds, balance, marker='x', linestyle='--', label=f'Bidder {bidder}')
        axs[1].set_xlabel('Round')
        axs[1].set_ylabel('Balance ($)')
        axs[1].set_title('Bidder Balances Over Rounds')
        axs[1].legend()
        axs[1].grid(axis='y')

        plt.tight_layout()
        plt.show()