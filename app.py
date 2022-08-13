from flask import Flask
from flask_restx import Api

from config import Config
from models import Movie, Director, Genre
from setup_db import db
from views.directors.directors import director_ns
from views.genres.genres import genre_ns
from views.movies.movies import movie_ns


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(movie_ns)
    api.add_namespace(director_ns)
    api.add_namespace(genre_ns)
    create_data(app, db)


def create_data(app, db):
    with app.app_context():
        db.create_all()

        m1 = Movie(id=1, title="movie1", description="test1", trailer="mast1", year=1000, rating=4, genre_id=4,
                   director_id=3)
        m2 = Movie(id=2, title="movie2", description="test2", trailer="mast2", year=2000, rating=5, genre_id=3,
                   director_id=2)
        m3 = Movie(id=3, title="movie3", description="test3", trailer="mast3", year=3000, rating=6, genre_id=2,
                   director_id=1)
        m4 = Movie(id=4, title="movie4", description="test4", trailer="mast4", year=4000, rating=7, genre_id=1,
                   director_id=4)

        d1 = Director(id=1, name="director1")
        d2 = Director(id=2, name="director2")
        d3 = Director(id=3, name="director3")
        d4 = Director(id=4, name="director4")

        g1 = Genre(id=1, name="genre1")
        g2 = Genre(id=2, name="genre2")
        g3 = Genre(id=3, name="genre3")
        g4 = Genre(id=4, name="genre4")

        with db.session.begin():
            db.session.add_all([m1, m2, m3, m4])
            db.session.add_all([d1, d2, d3, d4])
            db.session.add_all([g1, g2, g3, g4])


app = create_app(Config())
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", port=10001, debug=True)
