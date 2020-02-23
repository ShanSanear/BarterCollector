from argparse import ArgumentParser, Namespace
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Union

import pandas as pd
import requests

DATE_FORMAT = "%d-%m-%Y_%H-%M-%S"


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('--user_id', required=True, type=str,
                        help="Id of the user on barter, found in path after '/u/' in path to profile")
    parser.add_argument('--output_folder', required=True, type=Path,
                        help="Output folder, where files named tradeables_%d-%m-%Y_%H-%M-%S.json "
                             "will be saved as raw data")
    return parser.parse_args()


def get_tradeable_json(user_id: Union[str, int], output_path: Path):
    tradeables = requests.get(f"https://barter.vg/u/{user_id}/t/json/").json()
    output_path.write_text(json.dumps(tradeables, indent=4), encoding='utf-8')


def create_dataframes_from_tradables(raw_data_folder):
    tradeable_files = Path(raw_data_folder).glob("*.json")
    filtered_data = defaultdict(dict)
    for file in tradeable_files:
        date_in_file = datetime.strptime(file.stem, f"tradeables_{DATE_FORMAT}")
        data = json.loads(file.read_text())
        steam_games = data['by_platform']['1']
        for game_key, game_data in steam_games.items():
            if 'tradable' in game_data:
                game_key_with_title = (game_key, game_data['title'])
                filtered_data[game_key_with_title][date_in_file] = game_data
    dfs = {game_key_with_title:
               pd.DataFrame.from_dict(game_data, orient='index',
                                      columns=['tradable', 'wishlist', 'library', 'blacklist'])
           for game_key_with_title, game_data in filtered_data.items()
           }
    sorted_keys = sorted(dfs, key=lambda x: x[1].lower())
    dfs = {key: dfs[key] for key in sorted_keys}
    return dfs


def fetch_new_data():
    args = parse_arguments()
    current_date = datetime.now().strftime(DATE_FORMAT)
    output_path = args.output_folder / Path(f"tradeables_{current_date}").with_suffix('.json')
    get_tradeable_json(args.user_id, output_path)


if __name__ == '__main__':
    fetch_new_data()
