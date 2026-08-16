"""
Market-Making & Betting-Game Simulator

Assembled from your step-by-step solutions.
"""

import numpy as np

# Step 1 - expected_value
def expected_value(values, probabilities):
    # Expected value = sum(outcome * probability)
    return float(sum(value * probability for value, probability in zip(values, probabilities)))

# Step 2 - one_reroll_die_value
def one_reroll_die_value(sides):
    # Expected value of the second roll
    probabilities = [1 / sides] * sides
    faces = list(range(1, sides + 1))
    reroll_value = expected_value(faces, probabilities)

    # Reroll when the first-roll face is worse than the expected
    # value of taking the mandatory second roll.
    reroll_faces = [face for face in faces if face < reroll_value]

    # Expected winnings under the optimal keep-or-reroll policy
    optimal_values = [
        reroll_value if face in reroll_faces else face
        for face in faces
    ]
    value = expected_value(optimal_values, probabilities)

    return {
        'value': value,
        'reroll_faces': sorted(reroll_faces)
    }

# Step 3 - pay_per_reroll_die_game
def pay_per_reroll_die_game(sides, reroll_cost):
    # Evaluate every possible keep-threshold.
    # For threshold t, faces < t are rerolled and faces >= t are kept.
    # If V is the value at the start:
    #
    # V = (sum(kept faces) + (# rerolls) * (V - reroll_cost)) / sides
    #
    # Solving for V:
    # V = (sum(kept faces) - (# rerolls) * reroll_cost) / (# kept faces)

    best_threshold = 1
    best_value = float("-inf")

    for threshold in range(1, sides + 1):
        kept_faces = list(range(threshold, sides + 1))
        reroll_count = threshold - 1

        kept_sum = sum(kept_faces)
        kept_count = len(kept_faces)

        value = (
            kept_sum - reroll_count * reroll_cost
        ) / kept_count

        # Use < so that the smallest threshold is selected when
        # multiple thresholds have the same expected value.
        if value > best_value:
            best_value = value
            best_threshold = threshold

    return {
        'threshold': best_threshold,
        'value': float(best_value)
    }

# Step 4 - red_black_card_game_value
def red_black_card_game_value(num_red, num_black):
    # Dynamic programming with memoization.
    # V(r, b) is the optimal expected payout with r red and b black cards remaining.
    memo = {}

    def value(r, b):
        if r == 0 and b == 0:
            return 0.0

        state = (r, b)
        if state in memo:
            return memo[state]

        total = r + b

        red_value = 0.0
        if r > 0:
            red_value = 1 + value(r - 1, b)

        black_value = 0.0
        if b > 0:
            black_value = -1 + value(r, b - 1)

        continuation_value = (
            r / total * red_value
            + b / total * black_value
        )

        # The player can always stop and receive 0.
        # Ties resolve in favor of stopping.
        memo[state] = max(0.0, continuation_value)
        return memo[state]

    continuation_value = value(num_red, num_black)

    return {
        'value': float(continuation_value),
        'stop_now': continuation_value == 0.0
    }

# Step 5 - make_quotes
def make_quotes(fair_value, spread_width):
    half_spread = spread_width / 2

    return {
        'bid': fair_value - half_spread,
        'ask': fair_value + half_spread
    }

# Step 6 - execute_trade
def execute_trade(state, side, bid, ask, size=1):
    cash = state['cash']
    inventory = state['inventory']

    if side == 'buy':
        # Counterparty buys from us at our ask.
        cash += ask * size
        inventory -= size

    elif side == 'sell':
        # Counterparty sells to us at our bid.
        cash -= bid * size
        inventory += size

    else:
        raise ValueError("side must be 'buy' or 'sell'")

    return {
        'cash': float(cash),
        'inventory': float(inventory)
    }

# Step 7 - mark_to_market_pnl
def mark_to_market_pnl(cash, inventory, settlement_value):
    return float(cash + inventory * settlement_value)

# Step 8 - adverse_selection_loss
def adverse_selection_loss(fair_value, bid, ask, informed_values, informed_probabilities):
    values = np.asarray(informed_values, dtype=float)
    probabilities = np.asarray(informed_probabilities, dtype=float)

    # Loss when an informed counterparty buys from us at the ask
    # because the true value is above our ask.
    ask_loss = np.sum(
        (values - ask) * (values > ask) * probabilities
    )

    # Loss when an informed counterparty sells to us at the bid
    # because the true value is below our bid.
    bid_loss = np.sum(
        (bid - values) * (values < bid) * probabilities
    )

    return float(max(0.0, ask_loss + bid_loss))

# Step 9 - uncertainty_spread
def uncertainty_spread(base_spread, uncertainty):
    """Return a spread width >= base_spread that grows with uncertainty."""
    return float(base_spread + uncertainty)

# Step 10 - inventory_skewed_quotes
def inventory_skewed_quotes(fair_value, spread_width, inventory, skew_strength):
    half_spread = spread_width / 2

    # Long inventory -> shift quotes downward.
    # Short inventory -> shift quotes upward.
    shift = inventory * skew_strength
    center = fair_value - shift

    return {
        'bid': center - half_spread,
        'ask': center + half_spread
    }

# Step 11 - update_fair_value_from_trade
def update_fair_value_from_trade(fair_value, side, bid, ask, adjustment):
    if side == 'buy':
        # Counterparty bought at our ask, suggesting true value is higher.
        return float(fair_value + adjustment)

    elif side == 'sell':
        # Counterparty sold at our bid, suggesting true value is lower.
        return float(fair_value - adjustment)

    else:
        raise ValueError("side must be 'buy' or 'sell'")

# Step 12 - update_remaining_card_value
def update_remaining_card_value(remaining_counts, revealed_value):
    # Create a copy so the input dictionary is not mutated.
    updated_counts = dict(remaining_counts)

    # Decrement the revealed card's count.
    if revealed_value not in updated_counts:
        raise ValueError("revealed_value is not present in remaining_counts")

    updated_counts[revealed_value] -= 1

    # Remove the entry when no cards of that value remain.
    if updated_counts[revealed_value] == 0:
        del updated_counts[revealed_value]

    # Compute the expected value of a uniformly drawn card from the remaining deck.
    total_cards = sum(updated_counts.values())

    if total_cards == 0:
        expected = 0.0
    else:
        values = list(updated_counts.keys())
        probabilities = [
            count / total_cards
            for count in updated_counts.values()
        ]
        expected = expected_value(values, probabilities)

    return {
        'remaining_counts': updated_counts,
        'expected_value': float(expected)
    }

# Step 13 - run_market_making_episode (not yet solved)
# TODO: implement

# Step 14 - summarize_episode_pnls (not yet solved)
# TODO: implement

