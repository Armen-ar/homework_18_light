from flask_restx import Resource, Namespace

from models import GenresSchema, Genre
from setup_db import db

genre_ns = Namespace('genres')

genre_schema = GenresSchema()
genres_schema = GenresSchema(many=True)


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        all_genres = db.session.query(Genre).all()

        return genres_schema.dump(all_genres), 200


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    def get(self, gid: int):
        try:
            genre = db.session.query(Genre).filter(Genre.id == gid).one()
            return genre_schema.dump(genre), 200
        except Exception as e:
            return str(e), 404

