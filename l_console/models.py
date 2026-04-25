from django.db import models
from datetime import datetime
class category_course(models.Model):
    course_category = models.CharField(max_length=100)

    def __str__(self):
        return self.course_category

class Sub_Category_Course(models.Model):
    category_course = models.ForeignKey(category_course, on_delete=models.CASCADE, related_name='sub_categories_courses')
    course_sub_category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.course_sub_category
class lms_con(models.Model):
      model_name = models.CharField(max_length=100)
      course_id = models.AutoField(primary_key=True)
      course_code = models.CharField(max_length=50, unique=True)
      image = models.ImageField(blank=True, null=True)
      course_title = models.CharField(max_length=255)
      course_short_description = models.CharField(max_length=500)
      course_detailed_description = models.TextField()
      category_course = models.ForeignKey(category_course, on_delete=models.CASCADE, null=True, blank=True)
      sub_category_course = models.ForeignKey(Sub_Category_Course, on_delete=models.CASCADE, null=True, blank=True)
      course_type = models.CharField(max_length=30,choices=[('Academic', 'Academic'),('Professional', 'Professional'),('Certification', 'Certification'),('Skill', 'Skill')])
      course_level = models.CharField(max_length=30,choices=[('Beginner', 'Beginner'),('Intermediate', 'Intermediate'),('Advanced', 'Advanced')])
      course_duration = models.CharField(max_length=50)
      number_of_modules = models.IntegerField(blank=True, null=True)
      number_of_lessons = models.IntegerField(blank=True, null=True)
      module_title = models.CharField(max_length=255)
      lesson_title = models.CharField(max_length=255)
      content_type = models.CharField(max_length=30,choices=[('Video', 'Video'),('PDF', 'PDF'),('PPT', 'PPT'),('Audio', 'Audio'),('SCORM', 'SCORM'),('Live Session', 'Live Session')])
      content_url_upload = models.FileField(upload_to='courses/content/')
      preview_enabled = models.BooleanField(default=False)
      enrollment_type = models.CharField(max_length=30,choices=[('Free', 'Free'),('Paid', 'Paid'),('Restricted', 'Restricted')])
      enrollment_start_date = models.DateField(blank=True, null=True)
      enrollment_end_date = models.DateField(blank=True, null=True)
      # maximum_enrollments = models.IntegerField()
      access_duration = models.CharField(max_length=30,choices=[('Lifetime', 'Lifetime'),('Fixed Period', 'Fixed Period')])
      prerequisite_courses = models.CharField(max_length=255)
      user_roles_allowed = models.CharField(max_length=50,choices=[('Student', 'Student'),('Employee', 'Employee'),('Partner', 'Partner')])
      course_price = models.FloatField(blank=True, null=True)
      discount_type_value = models.CharField(max_length=50,blank=True, null=True)
      tax_applicable = models.BooleanField(default=0)
      certificate_available = models.BooleanField(default=0)
      certificate_template = models.FileField(upload_to='courses/certificates/',null=True,blank=True)
      minimum_completion_percentage = models.FloatField(blank=True, null=True)

      def __str__(self):
              return self.course_title

