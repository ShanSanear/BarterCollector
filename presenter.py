from datetime import datetime, timedelta

from flask import Flask, render_template

from tradeables import create_dataframes_from_tradables

app = Flask(__name__)


class Fetcher:
    def __init__(self):
        self._cached_tradables_data = []
        self._last_call = datetime.now()
        self._max_diff = timedelta(hours=6)
        self.fetch_tradables()

    def fetch_tradables(self):
        self._cached_tradables_data = create_dataframes_from_tradables('raw_data')
        self._last_call = datetime.now()

    @property
    def dataframes(self):
        if datetime.now() - self._last_call > self._max_diff:
            self.fetch_tradables()
        return self._cached_tradables_data


fetcher = Fetcher()

@app.route("/")
def hello():
    games = fetcher.dataframes
    return render_template('index.html', games=games)


if __name__ == '__main__':
    app.run()
