import sys

import numpy as np
import pandas as pd


def get_plus_minus_corr(player_url: str) -> float:
    """
    Reaches out to a player's basketball-reference url
    and pulls the stat box for the current season

    Then it does a bit of regex magic to extract their
    `+/-` and the team's win/loss margin and returns
    the correlation between the two
    """

    dfs = pd.read_html(player_url)

    # lots of tables, only one big table, find the biggest
    stat_table_idx = np.argmax([len(df.columns) for df in dfs])
    df = dfs[stat_table_idx]

    # few tables have headers again, in the middle
    df = df[df["Date"] != "Date"]

    # only need these two columns
    margin = df["Unnamed: 7"].str.extract("([\-\d]+)").astype(int)
    plus_minus = df["+/-"].str.extract("([\-\d]+)").astype(int)

    return margin.corrwith(plus_minus)[0]


if __name__ == "__main__":
    player_url = sys.argv[1]
    print(get_plus_minus_corr(player_url))