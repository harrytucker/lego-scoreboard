# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from lego import db

class Team(db.Model):
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), index=True, unique=True, nullable=False)


class Practice:
    id = -1
    name = 'Practice'
