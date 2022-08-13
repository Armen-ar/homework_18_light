from flask_restx import Resource, Namespace

from models import DirectorsSchema, Director
from setup_db import db

director_ns = Namespace('directors')

director_schema = DirectorsSchema()
directors_schema = DirectorsSchema(many=True)


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        all_directors = db.session.query(Director).all()

        return directors_schema.dump(all_directors), 200


@director_ns.route('/<int:did>')
class DirectorView(Resource):
    def get(self, did: int):
        try:
            director = db.session.query(Director).filter(Director.id == did).one()
            return director_schema.dump(director), 200
        except Exception as e:
            return str(e), 404
