def rank_change(player_rank, lobby_avg_rank, won, max_swing=58, elo_gap=600):
    "elo gap means that at a match where the player's srr is 600 above or below their expected to win or lose"
    "max_swing means the most elo someone can gain is 58 but mainly at a game at the players own rank"
    "the result minus expected equation would result in 0.5 making 29 be the gain which aligns with my experince"

    if lobby_avg_rank - player_rank > 500 or lobby_avg_rank - player_rank < -500:
        "This is to check whether the player is in wide match meaning the max swing for a win or lose is significantly less"
        max_swing = 29
    expected = 1 / (1 + 10 ** ((lobby_avg_rank - player_rank) / elo_gap))
    result = 1 if won else 0
    elo_amount = round(max_swing * (result - expected))
    elo_amount = str(elo_amount)
    return elo_amount



print(rank_change(1550, 1300, 0))

