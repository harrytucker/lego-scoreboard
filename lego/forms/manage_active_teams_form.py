# -----------------------------------------------------------------------------
# A form for moving up the stages.
# -----------------------------------------------------------------------------

from flask_wtf import FlaskForm


class ManageActiveTeamsForm(FlaskForm):
    def __init__(self):
        super().__init__()

        teams = Team.query.filter_by(is_practice=False).order_by('number ASC').all()
        self.teams = ','.join(str(t.id) for t in teams)

        for t in _teams:
            setattr(self, '{!s}_active'.format(t.id), BooleanField(t.name, default=t.active))
