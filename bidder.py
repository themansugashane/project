import random
import numpy as np

class Bidder:
    """Class to represent a bidder in an online second-price ad auction"""

    def __init__(self, num_users, num_rounds):
        """
        Setting number of users, number of rounds, and round counter.

        Parameters:
        num_users (int): The total number of users in the system.
        num_rounds (int): The total number of rounds in the auction.

        Returns:
        None
        """
        self.num_users = num_users
        self.num_rounds = num_rounds
        self.round_counter = 0
       
        self.user_stats = {
            user_id: {"clicks": 0, "views": 0, "ctr": 0.5, "ucb_value": float('inf')} for user_id in range(num_users)
        }

    def __repr__(self):
        """
        Return a string representation of the Bidder object.

        Returns:
        str: A string representation of the Bidder object.
        """
        return f"Bidder(num_users={self.num_users}, num_rounds={self.num_rounds})"

    def __str__(self):
        """
        Return a user-friendly string representation of the Bidder object.

        Returns:
        str: A user-friendly string representation of the Bidder object.
        """
        return f"UCB1 Bidder"

    def bid(self, user_id):
        """
        Returns a non-negative bid amount.

        Parameters:
        user_id (int): The ID of the user for whom the bid is being calculated.

        Returns:
        float: The calculated bid amount.
        """
        self.round_counter += 1


        exploration_bonus = 1 / np.log1p(self.round_counter)


        alpha = self.user_stats[user_id]["clicks"] + 1  # Add a prior of 1 click
        beta = self.user_stats[user_id]["views"] - self.user_stats[user_id]["clicks"] + 1  # Add a prior of 1 non-click
        sampled_ctr = np.random.beta(alpha, beta)

       
        if self.user_stats[user_id]["views"] == 0:
            self.user_stats[user_id]["ucb_value"] = float('inf')
        else:
            confidence_interval = np.sqrt((2 * np.log(self.round_counter)) / self.user_stats[user_id]["views"])
            self.user_stats[user_id]["ucb_value"] = sampled_ctr + exploration_bonus * confidence_interval


        bid_amount = round(sampled_ctr * 0.25 + np.random.uniform(-0.01, 0.01), 3)

        return max(0, bid_amount)

    def notify(self, auction_winner, price, clicked, user_id):
        """
        Updates bidder attributes based on results from an auction round.

        Parameters:
        auction_winner (bool): Whether the bidder won the auction.
        price (float): The price paid for the winning bid.
        clicked (bool): Whether the user clicked on the ad.
        user_id (int): The ID of the user for whom the auction results are being reported.

        Returns:
        None
        """
        if auction_winner:

            self.user_stats[user_id]["views"] += 1
            if clicked:
                self.user_stats[user_id]["clicks"] += 1
            self.user_stats[user_id]["ctr"] = (
                self.user_stats[user_id]["clicks"] / self.user_stats[user_id]["views"]
            )