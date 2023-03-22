from django.urls import path

from .views import CategoryListAPIView, CourseListView, CompletedCourseCreateAPIView, CourseCommentListAPIView, \
    CourseCommentCreateAPIView, GenerateCerificateView, VideoSingleView, CourseListByCategoryView

urlpatterns = [
    path('category/list/', CategoryListAPIView.as_view()),
    path('list/', CourseListView.as_view()),
    path('list/category/<int:id>/', CourseListByCategoryView.as_view(), name='course-list-by-category'),
    path('<int:lesson_id>/<int:video_id>/', VideoSingleView.as_view(), name='video-detail'),
    path('create-completed-course/', CompletedCourseCreateAPIView.as_view()),
    path('create-list-course-completion/', CompletedCourseCreateAPIView.as_view()),
    path('comment/list/', CourseCommentListAPIView.as_view()),
    path('comment/create/', CourseCommentCreateAPIView.as_view()),
    path("GenerateCertificate/", GenerateCerificateView.as_view())

]


