from django.contrib import admin
import nested_admin
from .models import Track,Course,Section,CourseContent,Enrollment
from .forms import CourseContentForm
# Register your models here.

class CourseContentInline(nested_admin.NestedStackedInline) :
    model = CourseContent
    form = CourseContentForm
    extra = 1
    sortable_field_name= 'order'
    classes = ['collapse']

    class Media:
        js = ('js/hide_fields.js',)


class SectionInline(nested_admin.NestedStackedInline) :
    model = Section
    extra = 1 
    inlines = [CourseContentInline]
    sortable_field_name = 'order'
    classes = ['collapse']


class CourseAdmin(nested_admin.NestedModelAdmin) :
    model = Course
    inlines = [SectionInline]
    list_display = ('name','instructor','status','created_at')
    search_fields = ('name','slug')
    list_filter = ('status','difficulty_level','created_at')


class SectionAdmin(admin.ModelAdmin) :
    list_display = ('title','order')
    search_fields = ('title',)
    list_filter = ('order',)

class CourseContentAdmin(admin.ModelAdmin) :
    list_display = ('title' , 'content_type' , 'order' , 'video_url' , 'file' , 'external_link')
    search_fields = ('title',)
    list_filter = ('content_type',)

admin.site.register(Track)
admin.site.register(Course , CourseAdmin)
admin.site.register(Section,SectionAdmin)
admin.site.register(CourseContent,CourseContentAdmin)
admin.site.register(Enrollment)
