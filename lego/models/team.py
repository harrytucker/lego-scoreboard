# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from sqlalchemy.ext.hybrid import hybrid_property

from lego import db


class Team(db.Model):
    __tablename__ = 'team'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(80), index=True, unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    is_practice = db.Column(db.Boolean, default=False, nullable=False)
    attempt_1 = db.Column(db.Integer, nullable=True)
    attempt_2 = db.Column(db.Integer, nullable=True)
    attempt_3 = db.Column(db.Integer, nullable=True)


    @hybrid_property
    def attempts(self):
        return [self.attempt_1, self.attempt_2, self.attempt_3]


    @hybrid_property
    def scored_attempts(self):
        ret = []

        if self.attempt_1 is not None:
            ret.append(self.attempt_1)

        if self.attempt_2 is not None:
            ret.append(self.attempt_2)

        if self.attempt_3 is not None:
            ret.append(self.attempt_3)

        return ret

    @hybrid_property
    def highest_score(self):
        return max(self.attempt_1 or 0, self.attempt_2 or 0, self.attempt_3 or 0)
