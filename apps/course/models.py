from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField

from apps.common.models import BaseModel
from .choosen import COURSE_LEVEL, SECTION_TYPE
from mutagen.mp4 import MP4, MP4StreamInfoError

from helpers.utils import get_timer


class Category(BaseModel):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name


class Course(BaseModel):
    title = models.CharField(max_length=80)
    image = models.ImageField(upload_to='media/course_images')
    level = models.CharField(max_length=30, choices=COURSE_LEVEL, default='Beginner')
    description = RichTextField()
    demo_video = models.FileField()
    author = models.CharField('Author', max_length=150)
    price = models.DecimalField(default=0, max_digits=5, decimal_places=2)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    language = models.CharField(max_length=60)
    is_discount = models.BooleanField('Chegirma', default=False)
    discount_price = models.DecimalField('Chegirmadagi narxi', max_digits=12, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:20])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class CourseLesson(BaseModel):
    title = models.CharField(max_length=70)
    description = RichTextField()
    order = models.PositiveIntegerField('Tartib nomeri', default=1)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson_status = models.CharField(max_length=40,
                                     choices=SECTION_TYPE,
                                     default="Ko'rilmagan")
    slug = models.SlugField(unique=True, blank=True)
    video_count = models.PositiveIntegerField(default=0)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:20])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CourseVideo(BaseModel):
    course = models.ForeignKey('course.CourseLesson', on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    video = models.FileField()
    slug = models.SlugField(unique=True, blank=True)
    length = models.DecimalField(default=0, max_digits=100, decimal_places=2, blank=True, null=True,
                                 help_text='Video uzunligi ozi yozadi yozmasangiz  bo\'ladi')
    is_viewed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title[:4])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_video_length(self):
        try:
            video = MP4(self.video)
            return video.info.length

        except MP4StreamInfoError:
            return 0.0

    def get_video_length_time(self):
        return get_timer(self.length)

    def get_video(self):
        return self.video.path

    def save(self, *args, **kwargs):
        self.length = self.get_video_length()
        les_obj = CourseLesson.objects.get(id=self.course.id)
        les_obj.video_count += 1
        les_obj.save()

        return super().save(*args, **kwargs)


class CourseViewed(BaseModel):
    user_id = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    video_id = models.ForeignKey(CourseVideo, on_delete=models.CASCADE)

    def __str__(self):
        return self.video_id.title

    class Meta:
        verbose_name = 'Course Viewed'
        verbose_name_plural = 'Courses Viewed'


class CourseCompleted(BaseModel):
    course = models.ForeignKey('account.PurchasedCourse', on_delete=models.CASCADE)
    user = models.ForeignKey('account.Account', on_delete=models.CASCADE)

    def __str__(self):
        return self.course.title

    class Meta:
        verbose_name = 'Course Completed'
        verbose_name_plural = 'Courses Completed'


class CourseComment(BaseModel):
    course = models.ForeignKey('course.CourseCompleted', on_delete=models.CASCADE)
    rank = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()

    class Meta:
        verbose_name = 'Course Comment'
        verbose_name_plural = 'Courses Comments'

    def __str__(self):
        return self.course.course.title


class Certificate(BaseModel):
    user = models.ForeignKey(
        'account.Account', on_delete=models.CASCADE, related_name='certificates',
    )
    course = models.ForeignKey(
        'course.Course', on_delete=models.CASCADE, related_name='certificates',
    )
    # cid = models.CharField(max_length=255, default=randomize_certificate_number)
    certificate_url = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.certificate_url = f'/home/nurmuhammad/uic/uzchess/static/certicats/{self.user}-{self.course.title}.jpg'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'

    def __str__(self):
        return self.user.first_name

