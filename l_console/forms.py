from django import forms
from .models import lms_con,category_course,Sub_Category_Course
class CategoryForm(forms.ModelForm):
    class Meta:
        model = category_course
        fields = '__all__'
        widgets = {
            'course_category': forms.TextInput(attrs={'class':'form-control'})
        }

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = Sub_Category_Course
        fields = '__all__'
        widgets = {
            'category_course': forms.Select(attrs={'class':'form-control'}),
            'course_sub_category': forms.TextInput(attrs={'class':'form-control'})
        }
class LmsForms(forms.ModelForm):
    class Meta:
        model = lms_con
        fields='__all__'
        widgets = { 'model_name': forms.TextInput(attrs={'class':'form-control'}),
                    'course_title': forms.TextInput(attrs={'class': 'form-control'}),
                    'course_short_description': forms.TextInput(attrs={'class':'form-control'}),
                    'course_duration': forms.TextInput(attrs={'class':'form-control'}),
                    'image': forms.FileInput(attrs={'class':'form-control'}),}