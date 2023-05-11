from typing import Optional
from wtforms.validators import ValidationError
from better_profanity import profanity


class NoProfanity(object):
    def __init__(self, message: Optional[str] = None):
        if not message:
            message = 'Profanity is not acceptable on Runnerspace'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)
