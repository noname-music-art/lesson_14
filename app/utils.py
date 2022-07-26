import sqlite3
from flask import jsonify, Response


def get_movie_by_title(title: str) -> Response:

    columns = ["title", "country", "release_year", "genre", "description"]
    with sqlite3.connect('data/netflix.db') as connection:
        cur = connection.cursor()
        cur.execute("SELECT title, country, release_year, listed_in, description FROM netflix "
                    "WHERE `title` = :title", {"title": title})
        data = cur.fetchall()
        zipped = dict(zip(columns, data[0]))
        return jsonify(zipped)


def get_movie_by_date_range(start: int, stop: int) -> Response:
    columns = ["title", "release_year"]
    zipped = []
    with sqlite3.connect('data/netflix.db') as connection:
        cur = connection.cursor()
        cur.execute("SELECT title, release_year FROM netflix "
                    "WHERE release_year BETWEEN :start AND :stop ", {"start": start, "stop": stop})
        data = cur.fetchall()
        for item in data:
            zipped.append(dict(zip(columns, item)))
        return jsonify(zipped)


def get_movie_by_rating(*rating: str) -> Response:
    columns = ["title", "rating", "description"]
    zipped = []

    with sqlite3.connect('data/netflix.db') as connection:
        cur = connection.cursor()
        cur.execute("SELECT title, rating, description FROM netflix "
                    "WHERE rating IN {}".format(rating))
        data = cur.fetchall()
        for item in data:
            zipped.append(dict(zip(columns, item)))
        return jsonify(zipped)


def get_movie_by_genre(genre: str) -> Response:
    columns = ["title", "description"]
    zipped = []

    with sqlite3.connect('data/netflix.db') as connection:
        cur = connection.cursor()
        cur.execute("SELECT title, description FROM netflix "
                    "WHERE listed_in LIKE :genre "
                    "ORDER BY release_year DESC LIMIT 10 ", {"genre": f"%{genre}%"})
        data = cur.fetchall()
        for item in data:
            zipped.append(dict(zip(columns, item)))
        return jsonify(zipped)
