from django.urls import path

from .views import CategoryListAPIView, CourseListView, CourseCommentListAPIView, \
    CourseCommentCreateAPIView, GenerateCerificateView, VideoSingleView, CourseListByCategoryView, CourseLessonsView, \
    LessonVideoListView, PurchaseUpdate, CertificateListView

urlpatterns = [
    path('category/list/', CategoryListAPIView.as_view()),
    path('list/', CourseListView.as_view()),
    path('list/category/<int:id>/', CourseListByCategoryView.as_view(), name='course-list-by-category'),
    path('<int:id>/lessons/', CourseLessonsView.as_view(), name='lesson-list'),
    path('lesson/<int:id>/', LessonVideoListView.as_view(), name='video-list'),
    path('<int:lesson_id>/<int:video_id>/', VideoSingleView.as_view(), name='video-detail'),
    path('purchase/<int:pk>/', PurchaseUpdate.as_view(), name=''),
    path('comment/list/', CourseCommentListAPIView.as_view()),
    path('comment/create/', CourseCommentCreateAPIView.as_view()),
    path("GenerateCertificate/", GenerateCerificateView.as_view()),
    path("certificate/list/", CertificateListView.as_view()),
]


