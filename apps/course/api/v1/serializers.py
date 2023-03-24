from rest_framework import serializers

from apps.accounts.models import PurchasedCourse
from apps.course.models import Course, CourseLesson, CourseVideo, Category, CourseCompleted, \
    CourseComment, Certificate

from django.db.models import Sum, Q

from helpers.utils import get_timer


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class CourseListSerializer(serializers.ModelSerializer):
    category_id = serializers.StringRelatedField()
    ranking = serializers.DecimalField(max_digits=2, decimal_places=1, read_only=True)

    class Meta:
        model = Course
        fields = (
            'id', 'title', 'slug', 'category_id', 'demo_video', 'author', 'level', 'price', 'is_discount', 'discount_price',
            'ranking')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if representation['is_discount'] == False:
            del representation['is_discount']
            del representation['discount_price']

        return representation


class VideoSingleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseVideo
        fields = ('id', 'title', 'video', 'course', 'is_viewed', 'length', 'slug')


class CourseVideoSerializer(serializers.ModelSerializer):
    section_id = serializers.StringRelatedField()
    # video_length_time = serializers.SerializerMethodField()
    comments = serializers.DictField(read_only=True)

    class Meta:
        model = CourseVideo
        fields = ('title', 'slug',  'length', 'section_id', 'comments')



class CourseLessonSerializer(serializers.ModelSerializer):
    course_id = serializers.StringRelatedField()
    lesson_length_time = serializers.CharField(read_only=True)
    videos = serializers.DictField(read_only=True)

    class Meta:
        model = CourseLesson
        fields = (
            'title', 'order', 'lesson_status','course_id', 'lesson_length_time',
            'videos')

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        total_length = CourseVideo.objects.filter(course=instance).aggregate(Sum('length'))['length__sum']

        if total_length == None:
            total_length = 0

        section_length_time = get_timer(total_length)

        episodes = CourseVideo.objects.filter(course=instance)

        if episodes.exists():
            serializer = CourseVideoSerializer(episodes, many=True)
            representation['episodes'] = serializer.data

        representation['section_length_time'] = section_length_time

        return representation


class CompletedCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseCompleted
        fields = ('user_id', 'course_id')

class PurchasCourseUpdate(serializers.ModelSerializer):
    video_plus = serializers.IntegerField(required=False)
    class Meta:
        model = PurchasedCourse
        exclude = ('id', 'user','course','lessons_video_count',"viewed_video_count","is_finished")
        read_only_fields = ('id', 'user','course','lessons_video_count',"viewed_video_count","video_plus",)




class CourseCommentSerializer(serializers.ModelSerializer):
    completed_course = CompletedCourseSerializer()

    class Meta:
        model = CourseComment
        fields = ('completed_course', 'rank', 'comment')

class CertificateSerializerGet(serializers.ModelSerializer):
    # purchase_course = serializers.
    class Meta:
        model = Certificate
        fields = ('id', 'user', 'course', 'certificate_url')
        read_only_fields =("certificate_url",)


    def create(self, validated_data):
        return Certificate.objects.create(**validated_data)


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ("id", "course_id", "user_id",  "created_at", "updated_at")