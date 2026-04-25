from django.contrib import admin
from .models import lms_con,category_course,Sub_Category_Course
class lms_admin(admin.ModelAdmin):

    list_display = ('model_name', 'course_id', 'course_title', 'course_type')
    list_filter = ('model_name','course_id')
    search_fields = ('model_name', 'course_id')
    list_display_links = ('model_name', 'course_id')
    # list_editable = ('is_active',)
    # ordering = ('full_name',)
    exclude = ('course_sub_category','maximum_enrollments','discount_type_value','certificate_template')

admin.site.register(lms_con,lms_admin)
admin.site.register(category_course)
admin.site.register(Sub_Category_Course)
# Register your models here.
