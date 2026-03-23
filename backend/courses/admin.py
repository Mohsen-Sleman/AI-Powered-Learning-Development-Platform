from django.contrib import admin

from .models import Track,Course,Section,CourseContent,Enrollment
# Register your models here.

admin.site.register(Track)
admin.site.register(Course)
admin.site.register(Section)
admin.site.register(CourseContent)
admin.site.register(Enrollment)
