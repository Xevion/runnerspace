from typing import Optional
from profanity_filter import ProfanityFilter
from wtforms.validators import ValidationError

pf = ProfanityFilter()


class NoProfanity(object):
    def __init__(self, message: Optional[str] = None):
        if not message:
            message = 'Profanity is not acceptable on Runnerspace'
        self.message = message

    def __call__(self, form, field):
        if pf.is_profane(field.data):
            raise ValidationError(self.message)
