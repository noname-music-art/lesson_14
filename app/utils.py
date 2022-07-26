import sqlite3, json
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
                    "WHERE release_year BETWEEN :start AND :stop "
                    "LIMIT 100", {"start": start, "stop": stop})
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


def get_by_actors(actor_1: str, actor_2: str) -> list:
    actors = {actor_1, actor_2}
    co_actors = []
    with sqlite3.connect('data/netflix.db') as connection:
        cur = connection.cursor()
        cur.execute("SELECT `cast` FROM netflix "
                    "WHERE `cast` LIKE :actor_1 AND `cast` LIKE :actor_2",
                    {"actor_1": f"%{actor_1}%", "actor_2": f"%{actor_2}%"})
        data = cur.fetchall()
    for item in data:
        actors_list = set(str(item).replace("'", "").lstrip("(").rstrip(")").rstrip(",").split(", "))
        actors_list -= actors
        for actor in actors_list:
            co_actors.append(actor)
    result = list(set([actor for actor in co_actors if co_actors.count(actor) >= 2]))
    # print(result)
    return result


def get_by_query(movie_type: str, year: int, genre: str) -> []:
    columns = ["title", "description"]
    zipped = []

    with sqlite3.connect('data/netflix.db') as connection:
        cur = connection.cursor()
        cur.execute("SELECT title, description FROM netflix "
                    "WHERE `type` = :movie_type "
                    "AND `release_year` = :year "
                    "AND `listed_in` LIKE :genre ", {"movie_type": movie_type, "year": year, "genre": f"%{genre}%"})
        data = cur.fetchall()
        for item in data:
            zipped.append(dict(zip(columns, item)))
        # print(json.dumps(zipped, indent=4))
        return json.dumps(data, indent=4)


# get_by_actors('Jack Black', 'Dustin Hoffman')
# get_by_query('Movie', 2020, 'Action')
