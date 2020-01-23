from sqlalchemy import String, Integer, Column, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Fetches(Base):
    FETCH_ID = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    FETCH_DATE = Column(TIMESTAMP, nullable=False)


class Games(Base):
    GAME_ID = Column(Integer, primary_key=True, nullable=False, unique=True)
    GAME_TITLE = Column(String, nullable=False)
    PRICE = Column(Integer)
    RELEASE_YEAR = Column(Integer)
    REVIEWS_POSITIVE = Column(Integer)
    REVIEWS_TOTAL = Column(Integer)
    ACHIEVEMENTS = Column(Integer)
    CARDS = Column(Integer)


class Statistics(Base):
    STAT_ID = Column(Integer, primary_key=True, nullable=False, autoincrement=True, unique=True)
    FETCH_ID = Column(Integer, ForeignKey(Fetches.FETCH_ID))
    GAME_ID = Column(Integer, ForeignKey(Games.GAME_ID))
    TRADEABLES = Column(Integer)
    WISHLIST = Column(Integer)
    LIBRARY = Column(Integer)
