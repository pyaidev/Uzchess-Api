from django.db.models import TextChoices


class LanguageChoices(TextChoices):
    UZB = ('uz', "O'Z")
    RUS = ('ru', 'РУ')


class LevelChoices(TextChoices):
    BEGINNER = ("Beginner", "Boshlangich")
    INTERMEDIATE = ('Intermediate', 'Havaskor')
    ADVANCED = ('Professional', 'Professional')


class StatusChoices(TextChoices):
    NEW = ('new', 'Yangi')
    ACCEPTED = ('accepted', 'Tasdiqlangan')
    CANCELED = ('canceled', 'Canceled')
