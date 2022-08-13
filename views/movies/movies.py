from flask import request
from flask_restx import Resource, Namespace

from models import MoviesSchema, Movie, Director, Genre
from setup_db import db

movie_ns = Namespace('movies')

movie_schema = MoviesSchema()
movies_schema = MoviesSchema(many=True)


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        movies_with_director_and_genre_and_year = db.session.query(Movie.id, Movie.title, Movie.description,
                                                                   Movie.trailer, Movie.year, Movie.rating,
                                                                   Director.name.label('director'),
                                                                   Genre.name.label('genre')).join(Director).join(Genre)
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        year = request.args.get('year')
        if director_id:
            movies_with_director_and_genre_and_year = movies_with_director_and_genre_and_year.filter(
                Movie.director_id == director_id)
        if genre_id:
            movies_with_director_and_genre_and_year = movies_with_director_and_genre_and_year.filter(
                Movie.genre_id == genre_id)
        if year:
            movies_with_director_and_genre_and_year = movies_with_director_and_genre_and_year.filter(
                Movie.year == year)

        select_movies = movies_with_director_and_genre_and_year.all()

        return movies_schema.dump(select_movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)

        with db.session.begin():
            db.session.add(new_movie)

            return "", 201


@movie_ns.route('/<int:mid>')
class MovieView(Resource):
    def get(self, mid: int):
        try:
            movie = db.session.query(Movie).filter(Movie.id == mid).one()
            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404

    def put(self, mid: int):
        movie = db.session.query(Movie).get(mid)
        req_json = request.json

        movie.title = req_json.get("title")
        movie.description = req_json.get("description")
        movie.trailer = req_json.get("trailer")
        movie.year = req_json.get("year")
        movie.rating = req_json.get("rating")
        movie.genre = req_json.get("genre")
        movie.director = req_json.get("director")

        db.session.add(movie)
        db.session.commit()

        return "", 204

    def patch(self, mid: int):
        movie = db.session.query(Movie).get(mid)
        req_json = request.json

        if "title" in req_json.get:
            movie.title = req_json.get("title")
        if "description" in req_json.get:
            movie.description = req_json.get("description")
        if "trailer" in req_json.get:
            movie.trailer = req_json.get("trailer")
        if "year" in req_json.get:
            movie.year = req_json.get("year")
        if "rating" in req_json.get:
            movie.rating = req_json.get("rating")
        if "genre" in req_json.get:
            movie.genre = req_json.get("genre")
        if "director" in req_json.get:
            movie.director = req_json.get("director")

        db.session.add(movie)
        db.session.commit()

        return "", 204

    def delete(self, mid: int):
        movie = db.session.query(Movie).get(mid)

        db.session.delete(movie)
        db.session.commit()

        return "", 204
