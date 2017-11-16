# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from lego import db

class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, index=True, nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    team = db.relationship('Team', backref='task', cascade='all, delete-orphan',
                           single_parent=True)
    attempt = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)

    __table_args__ = (db.UniqueConstraint('task_id', 'team_id', 'attempt',
                                          name='team_task_attempt'),)
