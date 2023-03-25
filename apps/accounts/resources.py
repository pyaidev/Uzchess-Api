from import_export.resources import ModelResource

from apps.accounts.models import PurchasedCourse


class PurchasedCourseResource(ModelResource):
    class Meta:
        model = PurchasedCourse
        fields = ('id', 'course__title', 'user__first_name', 'lessons_video_count', 'viewed_video_count', 'is_finished')
