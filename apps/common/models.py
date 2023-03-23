from django.db import models
from django.utils.text import slugify


def generate_unique_slug(klass, field):
    origin_slug = slugify(field)  # noqa
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = "%s-%d" % (origin_slug, numb)
        numb += 1
    return unique_slug


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if hasattr(self, "slug") and hasattr(self, "title"):
            if not self.slug:
                self.slug = generate_unique_slug(self.__class__, self.title)

        if hasattr(self, "slug") and hasattr(self, "name"):
            if not self.slug:
                self.slug = generate_unique_slug(self.__class__, self.name)
        super().save(*args, **kwargs)

    class Meta:
        abstract = True
