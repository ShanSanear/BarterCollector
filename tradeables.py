import json
from pathlib import Path
import pandas

import requests

user_id = 795
#tradeables = requests.get(f"https://barter.vg/u/{user_id}/t/json/").json()
#Path("tradeables.json").write_text(json.dumps(tradeables, indent=4), encoding='utf-8')
tradeables = json.loads(Path("tradeables.json").read_text())

for game_id, game in tradeables['by_platform']['1'].items():
    # print(game_id, game)
    title = game['title']
    tradeable = game.get("tradable", "n/a")
    wishlist = game.get('wishlist', "n/a")
    library = game.get('library', "n/a")
    print(f"""
Title: {title}
Tradeable: {tradeable}
Wishlists: {wishlist}
Library: {library}""")

df = pandas.DataFrame.from_dict(tradeables['by_platform']['1'], orient='index',
                                columns=['title', 'tradable', 'wishlist', 'library', 'item_type'])

only_games = df[df['item_type'] == 'Game']
only_games = only_games.drop(columns=['item_type'])
print(only_games)
