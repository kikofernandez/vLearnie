from django.db import IntegrityError

class DuplicateValuesAreNotUnique(IntegrityError):
    pass
    