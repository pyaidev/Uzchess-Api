# post_save bazaga saqlab bulgandan sung ishga tushadi
# pre_save - bazaga saqlashidan oldin ishga tushadi
from django.db.models import Sum
from django.db.models.signals import post_save, pre_save
from .models import Account, UserProfile, PurchasedCourse
from django.dispatch import receiver

from ..course.models import CourseLesson


@receiver(post_save, sender=Account)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(pre_save, sender=PurchasedCourse)
def purchase_course_post_save(instance, sender, *args, **kwargs):
    if instance is not None:
        obj = CourseLesson.objects.filter(course__id=instance.course.id).aggregate(Sum('video_count'))
        instance.lessons_video_count = obj.get('video_count__sum')
        instance.save()

