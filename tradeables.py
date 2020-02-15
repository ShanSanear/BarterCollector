from argparse import ArgumentParser, Namespace
import json
from datetime import datetime
from pathlib import Path
from typing import Union

import requests


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


def main():
    args = parse_arguments()
    current_date = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    output_path = args.output_folder / Path(f"tradeables_{current_date}").with_suffix('.json')
    get_tradeable_json(args.user_id, output_path)


if __name__ == '__main__':
    main()
