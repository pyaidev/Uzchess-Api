from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework import generics, status

from apps.account.models import PurchasedCourse
from apps.course.models import Course, CourseLesson, CourseVideo, Category, CourseCompleted, \
    CourseComment, CourseViewed, Certificate
from helpers.utils import certificaty

from .serializers import CategoryListSerializer, CertificateSerializerGet, VideoSingleSerializer
from .serializers import CourseListSerializer
from .serializers import CourseVideoSerializer
from .serializers import CourseLessonSerializer
from .serializers import CourseCommentSerializer
from .serializers import CompletedCourseSerializer



class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CourseListByCategoryView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs['id']
        if category_id:
            queryset = Course.objects.filter(category__id=category_id)
        else:
            queryset = Course.objects.none()
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CourseListSerializer(queryset, many=True)
        return Response(serializer.data)


class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print(request.user)
        print(**kwargs)
        print(*args)
        queryset = self.get_queryset()
        serializer = CourseListSerializer(queryset, many=True)
        return Response(serializer.data)

class CourseLessonsView(generics.ListAPIView):
    serializer_class = CourseLessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        course_id = self.kwargs['id']
        if course_id:
            queryset = CourseLesson.objects.filter(course__id=course_id)
        else:
            queryset = CourseLesson.objects.none()
        return queryset

    def get(self, request, *args, **kwargs):

        queryset = self.get_queryset()
        serializer = CourseLessonSerializer(queryset, many=True)
        return Response(serializer.data)


class LessonVideoListView(generics.ListAPIView):
    queryset = CourseVideo.objects.all()
    serializer_class = CourseVideoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        lesson_id = self.kwargs['id']

        if lesson_id:
            queryset = CourseVideo.objects.filter(course=lesson_id)
        else:
            queryset = CourseVideo.objects.none()
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CourseVideoSerializer(queryset, many=True)
        return Response(serializer.data)




class VideoSingleView(generics.RetrieveAPIView):
    queryset = CourseVideo.objects.all()

    serializer_class = VideoSingleSerializer
    permission_classes = [IsAuthenticated]

    lookup_field = 'lesson_id'

    def get_queryset(self):

        lesson_id = self.kwargs['lesson_id']

        # print(self.kwargs)
        video_id = self.kwargs['video_id']
        if lesson_id and video_id:

            queryset = CourseVideo.objects.get(course_id=lesson_id, id=video_id)
            # print(queryset.course.course.id)
            # print(Purchased_course.objects.filter(user=self.request.user).values_list('course_id', flat=True))
            if queryset.course.course.id in PurchasedCourse.objects.filter(user=self.request.user).values_list(
                    'course_id', flat=True):
                return queryset
            #     queryset = CourseVideo.objects.filter(course_id=lesson_id, id=video_id)

        return CourseVideo.objects.none()

    def get(self, request, *args, **kwargs):
        if queryset := self.get_queryset():
            serializer = VideoSingleSerializer(queryset)
            return Response(serializer.data)
        return Response("You are not buy this course")


class CompletedCourseCreateAPIView(generics.CreateAPIView):
    serializer_class = CompletedCourseSerializer


class CourseCommentListAPIView(generics.ListAPIView):
    queryset = CourseComment.objects.all()
    serializer_class = CourseCommentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CourseCommentSerializer(queryset, many=True)
        return Response(serializer.data)


class CourseCommentCreateAPIView(generics.CreateAPIView):
    queryset = CourseComment.objects.all()
    serializer_class = CourseCommentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = CourseCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class GenerateCerificateView(generics.CreateAPIView):
    queryset = PurchasedCourse.objects.all()
    serializer_class = CertificateSerializerGet
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = request.user
        course = request.data.get('course')
        # print(request.data)
        qs = self.queryset.get(user=user, course=course)
        if qs.lessons_video_count == qs.viewed_video_count:
            if len(Certificate.objects.filter(user_id=user.id, course_id=course)) == 0:
                obj = Certificate.objects.create(user_id=user.id, course_id=course)
                obj.save()
                # print(user, qs.course)
                certificaty(str(user), str(qs.course))
                serizalizer = self.get_serializer(obj).data
                return Response(serizalizer)
            return Response({"message": "Sertifikat mavjud"})
        return Response({'Error': "Kurslar to'liq ko'rilmagan!"})
