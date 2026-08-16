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

# Step 4 - red_black_card_game_value (not yet solved)
# TODO: implement

# Step 5 - make_quotes (not yet solved)
# TODO: implement

# Step 6 - execute_trade (not yet solved)
# TODO: implement

# Step 7 - mark_to_market_pnl (not yet solved)
# TODO: implement

# Step 8 - adverse_selection_loss (not yet solved)
# TODO: implement

# Step 9 - uncertainty_spread (not yet solved)
# TODO: implement

# Step 10 - inventory_skewed_quotes (not yet solved)
# TODO: implement

# Step 11 - update_fair_value_from_trade (not yet solved)
# TODO: implement

# Step 12 - update_remaining_card_value (not yet solved)
# TODO: implement

# Step 13 - run_market_making_episode (not yet solved)
# TODO: implement

# Step 14 - summarize_episode_pnls (not yet solved)
# TODO: implement

