from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models import CharField, IntegerField, ForeignKey, SET_NULL, CASCADE, ImageField, DateField, SlugField, \
    TextField
from django.utils import timezone
from django.utils.text import gettext_lazy as _, slugify

from apps.common.models import BaseModel


class NewArticle(BaseModel):
    title = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True)
    image = ImageField(upload_to='news/photos/%Y/%m/%d')
    created = DateField(auto_now_add=True)
    description = RichTextUploadingField(config_name='portal_config')
    view = IntegerField(default=0)

    def __str__(self):
        return self.title

    @property
    def get_same_news(self):
        news = NewArticle.objects.filter(created=self.created).values()
        return list(news)

    class Meta:
        verbose_name = 'NewArticle'
        verbose_name_plural = 'NewArticle'


class NewArticleView(BaseModel):
    new = ForeignKey(
        "news.NewArticle",
        verbose_name=_("News"),
        on_delete=CASCADE,
        related_name="new_views",
    )
    user = ForeignKey(
        "account.Account",
        verbose_name=_("User"),
        on_delete=CASCADE,
        related_name="user_views",
        null=True,
        blank=True,
    )
    device_id = CharField(
        verbose_name=_("Device ID"),
        max_length=255,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'New Article View'
        verbose_name_plural = _('New Article View')
