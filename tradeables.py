import json
import os
from datetime import datetime
from pathlib import Path
import pandas
import sqlalchemy
from sqlalchemy import create_engine
import requests
from sqlalchemy.orm import sessionmaker, Session

from models import Fetches, Games, Statistics


def get_postgres_engine():
    engine_type = 'postgresql'
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    database = os.getenv("DATABASE")
    server_url = os.getenv("SERVER_URL")
    conn_string = f"{engine_type}://{username}:{password}@{server_url}/{database}"
    return create_engine(conn_string)


class Rolling:
    def __init__(self, session):
        self.session = session
        self.fetch = None

    def create_fetch_instance(self):
        self.fetch = Fetches(FETCH_DATE=datetime.now())
        self.session.add(self.fetch)
        self.session.commit()

    def add_game(self):
        game = Games(GAME_ID=1, GAME_TITLE="A", PRICE=999, RELEASE_YEAR=2010, REVIEWS_POSITIVE=80, REVIEWS_TOTAL=2222,
                     ACHIEVEMENTS=100, CARDS=1)
        statistics = Statistics(FETCH_ID=self.fetch, GAME_ID=game, TRADEABLES=100, WISHLIST=100, LIBRARY=100)


engine = get_postgres_engine()
session = Session(bind=engine)
roll = Rolling(session)
roll.create_fetch_instance()
