# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

from sqlalchemy.ext.hybrid import hybrid_property

from lego import app, db


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
    round_2 = db.Column(db.Integer, nullable=True)
    quarter = db.Column(db.Integer, nullable=True)
    semi = db.Column(db.Integer, nullable=True)
    final_1 = db.Column(db.Integer, nullable=True)
    final_2 = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        name = self.__class__.__name__
        return '<{!s}(id={!r}, number={!r}, name={!r}>' \
            .format(name, self.id, self.number, self.name)

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        stage = app.load_stage()

        if stage == 4:
            if self.final_total < other.final_total:
                return True

            if self.final_total > other.final_total:
                return False

        if stage >= 3:
            if (self.semi or -1) < (other.semi or -1):
                return True

            if (self.semi or -1) > (other.semi or -1):
                return False

        if stage >= 2:
            if (self.quarter or -1) < (other.quarter or -1):
                return True

            if (self.quarter or -1) > (other.quarter or -1):
                return False

        if stage >= 1:
            if (self.round_2 or -1) < (other.round_2 or -1):
                return True

            if (self.round_2 or -1) > (other.round_2 or -1):
                return False

        if stage >= 0:
            s_attempt = [a if a is not None else -1 for a in self.attempts]
            o_attempt = [a if a is not None else -1 for a in other.attempts]

            s_attempt.sort(reverse=True)
            o_attempt.sort(reverse=True)

            for s, o in zip(s_attempt, o_attempt):
                if s < o:
                    return True

                if s > o:
                    return False

        # we want to order by score highest to lowest
        # but if we fall back to this, we order by lowest number to highest
        if self.number > other.number:
            return True

        return False

    def __gt__(self, other):
        stage = app.load_stage()

        if stage == 4:
            if self.final_total > other.final_total:
                return True

            if self.final_total < other.final_total:
                return False

        if stage >= 3:
            if (self.semi or -1) > (other.semi or -1):
                return True

            if (self.semi or -1) < (other.semi or -1):
                return False

        if stage >= 2:
            if (self.quarter or -1) > (other.quarter or -1):
                return True

            if (self.quarter or -1) < (other.quarter or -1):
                return False

        if stage >= 1:
            if (self.round_2 or -1) > (other.round_2 or -1):
                return True

            if (self.round_2 or -1) < (other.round_2 or -1):
                return False

        if stage >= 0:
            s_attempt = [a if a is not None else -1 for a in self.attempts]
            o_attempt = [a if a is not None else -1 for a in other.attempts]

            s_attempt.sort(reverse=True)
            o_attempt.sort(reverse=True)

            for s, o in zip(s_attempt, o_attempt):
                if s > o:
                    return True

                if s < o:
                    return False

        # we want to order by score highest to lowest
        # but if we fall back to this, we order by lowest number to highest
        if self.number < other.number:
            return True

        return False

    @hybrid_property
    def attempts(self):
        return [self.attempt_1, self.attempt_2, self.attempt_3]


    @hybrid_property
    def round_1_total(self):
        return sum([a or 0 for a in self.attempts])

    @hybrid_property
    def finals(self):
        return [self.final_1, self.final_2]

    @hybrid_property
    def final_total(self):
        return sum([self.final_1 or 0, self.final_2 or 0])

    @hybrid_property
    def highest_score(self):
        stage = app.load_stage()
        if stage == 0:
            return max(self.attempt_1 or 0, self.attempt_2 or 0, self.attempt_3 or 0)

        if stage == 1:
            return self.round_2 or 0

        if stage == 2:
            return self.quarter or 0

        if stage == 3:
            return self.semi or 0

        return max(self.final_1 or 0, self.final_2 or 0)


    def set_score(self, score):
        stage = app.load_stage()
        app.logger.debug('Stage: %s', stage)
        app.logger.debug('Team: %s', str(self.__dict__))

        # first round
        if stage == 0:
            if self.attempt_1 is None:
                self.attempt_1 = score
            elif self.attempt_2 is None:
                self.attempt_2 = score
            elif self.attempt_3 is None:
                self.attempt_3 = score
            else:
                raise Exception('All attempts have been made for this stage.')

        # second round
        elif stage == 1:
            if self.round_2 is None:
                self.round_2 = score
            else:
                raise Exception('All attempts have been made for this stage.')

        # quarter finals
        elif stage == 2:
            if self.quarter is None:
                self.quarter = score
            else:
                raise Exception('All attempts have been made for this stage.')

        # semi finals
        elif stage == 3:
            if self.semi is None:
                self.semi = score
            else:
                raise Exception('All attempts have been made for this stage.')

        # finals
        elif stage == 4:
            if self.final_1 is None:
                self.final_1 = score
            elif self.final_2 is None:
                self.final_2 = score
            else:
                raise Exception('All attempts have been made for this stage.')

        else:
            raise Exception('Invalid value for stage.')


    def edit_round_score(self, key, score):
        app.logger.info('Setting %s to %d for team: %s (%d)', key, score, self.name, self.number)
        setattr(self, key, int(score))


    def reset_round_score(self, round):
        app.logger.info('Resetting %s for team: %s (%d)', key, self.name, self.number)
        setattr(self, key, None)
