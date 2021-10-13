"""add data

Revision ID: 025144069685
Revises: a0c8f752df9b
Create Date: 2021-10-05 11:32:17.314955

"""
import json
from pathlib import Path

from alembic import op
from api.strawberry_sqlalchemy.movie_model_example import DirectorModel as Director
from api.strawberry_sqlalchemy.movie_model_example import MovieModel as Movie
from sqlalchemy import orm, select
from sqlalchemy.exc import NoResultFound

# revision identifiers, used by Alembic.
revision = "025144069685"
down_revision = "a0c8f752df9b"
branch_labels = None
depends_on = None


current_dir = Path(__file__).parent.resolve()
data_file = current_dir.parent.parent / "common-data" / "movies.json"


def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    with data_file.open() as f:
        json_data = json.load(f)

    for movie_data in json_data:
        try:
            director = session.execute(
                select(Director).filter_by(name=movie_data["director"]["name"])
            ).scalar_one()
        except NoResultFound:
            director = Director(name=movie_data["director"]["name"])
            session.add(director)
            session.commit()

        movie = Movie(
            imdb_id=movie_data["imdb_id"],
            title=movie_data["title"],
            year=movie_data["year"],
            image_url=movie_data["image_url"],
            imdb_rating=movie_data["imdb_rating"],
            imdb_rating_count=movie_data["imdb_rating_count"],
            director=director,
        )
        session.add(movie)
        session.commit()


def downgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    session.execute("DELETE FROM movies")
    session.execute("DELETE FROM directors")
    session.commit()
    session.close()
