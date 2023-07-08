import random
import pandas as pd

def generate_synthetic_data(num_users, places_by_tag, num_transactions_per_user):
    # Initialize lists to hold the synthetic data
    synthetic_users = []
    synthetic_transactions = []
    synthetic_tags = []

    # Initialize a dictionary to hold the places used for each user
    places_used_by_user = {}

    # List of possible transaction prefixes
    transaction_prefixes = ['MPS', 'POS', 'BIL', 'ME DC SI']

    # Loop over the number of users
    for i in range(1, num_users + 1):
        user = f'User{i}'
        # Initialize the list of places used for this user
        places_used_by_user[user] = []

        # Generate synthetic transactions for this user
        for _ in range(num_transactions_per_user):
            # Randomly select a tag
            tag = random.choice(list(places_by_tag.keys()))

            # Randomly select a place for this transaction that hasn't been used for this user yet
            unused_places = [p for p in places_by_tag[tag] if p not in places_used_by_user[user]]
            if not unused_places:  # if all places have been used, allow places to be reused
                unused_places = places_by_tag[tag]
            place = random.choice(unused_places)

            # Add the place to the list of places used for this user
            places_used_by_user[user].append(place)

            # Randomly select a transaction prefix
            transaction_prefix = random.choice(transaction_prefixes)

            # Randomly decide whether to include a sequence of 'X's
            if random.random() < 0.5:  # 50% chance of including 'X's
                xs = 'X' * random.randint(10, 15)  # random number of 'X's between 10 and 15
                transaction = f"{transaction_prefix} {xs} {place} /{random.randint(202300000000, 202399999999)}/{random.randint(100000, 999999)}/BANGALORE"
            else:
                transaction = f"{transaction_prefix}/{place} /{random.randint(202300000000, 202399999999)}/{random.randint(100000, 999999)}/BANGALORE"

            # Add the synthetic data to the lists
            synthetic_users.append(user)
            synthetic_transactions.append(transaction)
            synthetic_tags.append(tag)

    # Create a DataFrame from the synthetic data
    synthetic_data = pd.DataFrame({
        'User': synthetic_users,
        'Transaction': synthetic_transactions,
        'Tag': synthetic_tags
    })

    return synthetic_data
