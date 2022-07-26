from flask import Blueprint
from app.utils import get_movie_by_title, get_movie_by_date_range, get_movie_by_rating, get_movie_by_genre

main_blueprint = Blueprint('main_blueprint', __name__)


@main_blueprint.route("/movies/<title>")
def page_movies(title):
    return get_movie_by_title(title)


@main_blueprint.route("/movies/<start>/to/<stop>")
def page_movies_date_ranged(start, stop):
    return get_movie_by_date_range(start, stop)


@main_blueprint.route("/rating/children")
def page_children_movies():
    return get_movie_by_rating("!", "G")


@main_blueprint.route("/rating/family")
def page_family_movies():
    return get_movie_by_rating("G", "PG", "PG-13")


@main_blueprint.route("/rating/adult")
def page_adult_movies():
    return get_movie_by_rating("R", "NC-17")


@main_blueprint.route("/genre/<genre>")
def page_movies_by_genre(genre):
    return get_movie_by_genre(genre)

