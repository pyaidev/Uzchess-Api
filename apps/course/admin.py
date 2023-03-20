from django.contrib import admin
from .models import Course, CourseLesson, CourseVideo, CourseCategory, PurchaseCourse, CourseCompleted, CourseComment




class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'is_discount', 'discount_price', 'language',)
    list_filter = ('title', 'author', 'price', 'is_discount', 'discount_price',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'author', 'price', 'is_discount', 'discount_price',)


class CourseLessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'lesson_status')
    list_filter = ('title', 'course', 'lesson_status')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'course', 'lesson_status')


class CourseVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'length', 'is_viewed')
    list_filter = ('title', 'course', 'is_viewed')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'course', 'is_viewed')


class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_filter = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


admin.site.register(Course, CourseAdmin)
admin.site.register(CourseLesson, CourseLessonAdmin)
admin.site.register(CourseVideo, CourseVideoAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(PurchaseCourse)
admin.site.register(CourseCompleted)
admin.site.register(CourseComment)
